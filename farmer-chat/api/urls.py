from django.urls import path
from api.servvia_endpoint import get_answer_for_text_query
from api.language_endpoint import get_supported_languages

urlpatterns = [
    # ServVIA Healthcare endpoints - handle both single and double /api/ paths
    path("chat/get_answer_for_text_query/", get_answer_for_text_query, name="servvia-healthcare"),
    path("api/chat/get_answer_for_text_query/", get_answer_for_text_query, name="servvia-healthcare-double-api"),
    
    # Language endpoints - handle both single and double /api/ paths  
    path("languages/", get_supported_languages, name="get-languages"),
    path("language/languages/", get_supported_languages, name="get-languages-alt"),
    path("api/language/languages/", get_supported_languages, name="get-languages-double-api"),
]
