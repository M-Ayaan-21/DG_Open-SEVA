"""
Servvia - AI-Powered Symptom Analyzer
Uses OpenAI API for intelligent symptom analysis and remedies
"""

import os
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Structured result from AI symptom analysis."""
    condition: str
    severity: str
    confidence: str
    analysis: str
    remedies: List[str]
    when_to_see_doctor: List[str]
    precautions: List[str]
    disclaimer: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API responses."""
        return asdict(self)


class ServviaSymptomAnalyzer:
    """
    AI-powered symptom analyzer using OpenAI API.
    No hardcoded rules - uses AI for intelligent analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the analyzer with OpenAI API.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: OpenAI model to use (default: gpt-4o)
                   Options: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment "
                "variable or pass api_key parameter"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        self.system_prompt = """You are Servvia's medical AI assistant, specialized in analyzing symptoms and providing helpful remedies. 

Your role is to:
1. Analyze the user's symptoms intelligently
2. Identify the most likely condition(s)
3. Provide practical, safe home remedies
4. Give clear guidance on when professional medical help is needed
5. Always prioritize patient safety

IMPORTANT GUIDELINES:
- Never diagnose definitively - use terms like "may indicate", "could be", "commonly associated with"
- Always include when to seek professional medical help
- Focus on evidence-based remedies and self-care
- Flag emergency symptoms immediately
- Be empathetic and reassuring while being informative

OUTPUT FORMAT (respond ONLY with valid JSON):
{
  "condition": "Most likely condition name",
  "severity": "mild/moderate/severe/emergency",
  "confidence": "low/medium/high",
  "analysis": "Brief analysis of the symptoms and what they may indicate",
  "remedies": ["List of practical remedies and self-care steps"],
  "when_to_see_doctor": ["Specific signs that indicate need for professional care"],
  "precautions": ["Important precautions and things to avoid"],
  "disclaimer": "Standard medical disclaimer"
}"""
    
    def analyze_symptoms(
        self, 
        symptoms: str,
        additional_info: Optional[Dict] = None
    ) -> AnalysisResult:
        """
        Analyze symptoms using AI and return remedies.
        
        Args:
            symptoms: User's symptom description
            additional_info: Optional dict with age, gender, duration, etc.
            
        Returns:
            AnalysisResult with AI-generated analysis and remedies
            
        Raises:
            ValueError: If input is invalid
            Exception: If API call fails
        """
        # Validate input
        if not symptoms or not isinstance(symptoms, str):
            raise ValueError("Symptoms must be a non-empty string")
        
        if len(symptoms.strip()) < 5:
            raise ValueError("Please provide more detailed symptom description")
        
        # Build the prompt
        user_message = self._build_prompt(symptoms, additional_info)
        
        logger.info(f"Analyzing symptoms via AI: {symptoms[:50]}...")
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            result_data = json.loads(response_text)
            
            # Create structured result
            result = AnalysisResult(
                condition=result_data.get("condition", "Unknown"),
                severity=result_data.get("severity", "moderate"),
                confidence=result_data.get("confidence", "medium"),
                analysis=result_data.get("analysis", ""),
                remedies=result_data.get("remedies", []),
                when_to_see_doctor=result_data.get("when_to_see_doctor", []),
                precautions=result_data.get("precautions", []),
                disclaimer=result_data.get(
                    "disclaimer",
                    "This is not a medical diagnosis. Consult a healthcare professional."
                )
            )
            
            logger.info(f"Analysis complete: {result.condition}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            raise Exception("AI returned invalid response format")
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            raise Exception(f"Failed to analyze symptoms: {str(e)}")
    
    def _build_prompt(
        self, 
        symptoms: str, 
        additional_info: Optional[Dict]
    ) -> str:
        """Build the prompt for OpenAI API."""
        prompt = f"Please analyze these symptoms:\n\n{symptoms}"
        
        if additional_info:
            prompt += "\n\nAdditional Information:"
            for key, value in additional_info.items():
                prompt += f"\n- {key.replace('_', ' ').title()}: {value}"
        
        prompt += "\n\nProvide your analysis in the specified JSON format."
        return prompt
    
    def analyze_with_streaming(
        self,
        symptoms: str,
        additional_info: Optional[Dict] = None
    ):
        """
        Analyze symptoms with streaming response.
        Useful for real-time UI updates.
        """
        user_message = self._build_prompt(symptoms, additional_info)
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=2000,
                stream=True,
                response_format={"type": "json_object"}
            )
            
            collected_content = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    collected_content += content
                    yield content
            
            # Parse final result
            result_data = json.loads(collected_content)
            return AnalysisResult(
                condition=result_data.get("condition", "Unknown"),
                severity=result_data.get("severity", "moderate"),
                confidence=result_data.get("confidence", "medium"),
                analysis=result_data.get("analysis", ""),
                remedies=result_data.get("remedies", []),
                when_to_see_doctor=result_data.get("when_to_see_doctor", []),
                precautions=result_data.get("precautions", []),
                disclaimer=result_data.get(
                    "disclaimer",
                    "This is not a medical diagnosis. Consult a healthcare professional."
                )
            )
            
        except Exception as e:
            logger.error(f"Streaming analysis failed: {e}")
            raise Exception(f"Failed to analyze symptoms: {str(e)}")


class ServviaAPI:
    """
    API wrapper for Servvia symptom analyzer.
    Ready for Flask/FastAPI integration.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.analyzer = ServviaSymptomAnalyzer(api_key, model)
    
    def analyze(
        self,
        symptoms: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        duration: Optional[str] = None,
        severity_level: Optional[str] = None,
        medical_history: Optional[str] = None
    ) -> Dict:
        """
        API endpoint for symptom analysis.
        
        Args:
            symptoms: User's symptom description
            age: Patient age (optional)
            gender: Patient gender (optional)
            duration: How long symptoms have lasted (optional)
            severity_level: User's perceived severity (optional)
            medical_history: Relevant medical history (optional)
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Build additional info
            additional_info = {}
            if age:
                additional_info["age"] = age
            if gender:
                additional_info["gender"] = gender
            if duration:
                additional_info["duration"] = duration
            if severity_level:
                additional_info["severity_level"] = severity_level
            if medical_history:
                additional_info["medical_history"] = medical_history
            
            # Analyze
            result = self.analyzer.analyze_symptoms(
                symptoms,
                additional_info if additional_info else None
            )
            
            return {
                "status": "success",
                "data": result.to_dict()
            }
            
        except ValueError as e:
            return {
                "status": "error",
                "error": str(e),
                "code": "INVALID_INPUT"
            }
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "status": "error",
                "error": "Failed to analyze symptoms. Please try again.",
                "code": "ANALYSIS_FAILED"
            }


# Flask Integration Example
def create_flask_app():
    """
    Example Flask application setup.
    """
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    servvia_api = ServviaAPI()
    
    @app.route('/api/analyze', methods=['POST'])
    def analyze_symptoms():
        """Endpoint to analyze symptoms."""
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({
                "status": "error",
                "error": "Symptoms field is required"
            }), 400
        
        result = servvia_api.analyze(
            symptoms=data.get('symptoms'),
            age=data.get('age'),
            gender=data.get('gender'),
            duration=data.get('duration'),
            severity_level=data.get('severity_level'),
            medical_history=data.get('medical_history')
        )
        
        return jsonify(result)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "service": "Servvia"})
    
    return app


# FastAPI Integration Example
def create_fastapi_app():
    """
    Example FastAPI application setup.
    """
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    
    app = FastAPI(title="Servvia API", version="1.0.0")
    servvia_api = ServviaAPI()
    
    class SymptomRequest(BaseModel):
        symptoms: str
        age: Optional[int] = None
        gender: Optional[str] = None
        duration: Optional[str] = None
        severity_level: Optional[str] = None
        medical_history: Optional[str] = None
    
    @app.post("/api/analyze")
    async def analyze_symptoms(request: SymptomRequest):
        """Endpoint to analyze symptoms."""
        result = servvia_api.analyze(
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender,
            duration=request.duration,
            severity_level=request.severity_level,
            medical_history=request.medical_history
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Servvia"}
    
    return app


# Example usage
def main():
    """Demonstrate Servvia analyzer with OpenAI."""
    
    # Note: Set your API key as environment variable or pass directly
    # export OPENAI_API_KEY="your-api-key-here"
    
    try:
        # Initialize with GPT-4o (recommended) or gpt-3.5-turbo (cheaper)
        analyzer = ServviaSymptomAnalyzer(model="gpt-4o")
        
        # Example symptom analysis
        symptoms = """
        I've been having a persistent headache for 2 days, 
        feeling nauseous, and sensitive to light. 
        The pain is throbbing on one side of my head.
        """
        
        print("🏥 Servvia - AI Symptom Analyzer (Powered by OpenAI)\n")
        print(f"Analyzing: {symptoms.strip()}\n")
        print("=" * 60)
        
        result = analyzer.analyze_symptoms(
            symptoms,
            additional_info={
                "age": 30,
                "gender": "female",
                "duration": "2 days"
            }
        )
        
        # Display results
        print(f"\n🔍 CONDITION: {result.condition}")
        print(f"⚠️  SEVERITY: {result.severity.upper()}")
        print(f"📊 CONFIDENCE: {result.confidence.upper()}\n")
        
        print(f"📝 ANALYSIS:\n{result.analysis}\n")
        
        print("💊 RECOMMENDED REMEDIES:")
        for i, remedy in enumerate(result.remedies, 1):
            print(f"{i}. {remedy}")
        
        print("\n🏥 WHEN TO SEE A DOCTOR:")
        for i, sign in enumerate(result.when_to_see_doctor, 1):
            print(f"{i}. {sign}")
        
        print("\n⚠️  PRECAUTIONS:")
        for i, precaution in enumerate(result.precautions, 1):
            print(f"{i}. {precaution}")
        
        print(f"\n📋 {result.disclaimer}")
        print("=" * 60)
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        print("\nMake sure to set OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")


if __name__ == "__main__":
    main()
