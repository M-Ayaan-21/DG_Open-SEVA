# FarmStack React App

![Image Alt Text](https://farmstack.co/wp-content/uploads/2021/07/FarmStack-logo.png)

Welcome to FarmStack React App! This open-source project allows you to build a powerful web application for managing farm/farmer data. This readme file will guide you through the process of setting up the app and configuring the necessary environment variables. Let's get started!

> **Quick Start**: For a streamlined setup process, check out the [Quick Start Guide](./QUICKSTART.md)

## Prerequisites

Before you begin, ensure that you have the following dependencies installed:

- **Node.js** (version 14 or higher, recommended: v16.x or v18.x)
  - Check your version: `node --version`
  - Download from: https://nodejs.org/
  
- **npm** (Node Package Manager)
  - Usually comes with Node.js
  - Check your version: `npm --version`

**Note**: This project uses React 17 and some dependencies may have peer dependency warnings with newer npm versions. The provided `.npmrc` configuration handles these automatically.

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/digitalgreenorg/datahub-frontend
   ```

2. Navigate to the project directory:
   ```bash
   cd farmstack-frontend
   ```

3. Install the required dependencies using npm:
   ```bash
   npm install
   ```
   
   **Note**: The project includes an `.npmrc` file that automatically handles peer dependency conflicts. If you encounter any issues during installation, you can manually run:
   ```bash
   npm install --legacy-peer-deps
   ```

## Configuration

The FarmStack React App requires some environment variables to be set in order to function properly. These variables are used to configure the app's behavior and access external services. Follow the steps below to set up the environment variables:

1. Create a `.env` file in the root directory of the project.

2. Open the `.env` file and add the following variables:

   ```bash
   REACT_APP_BASEURL="https://datahubethdev.farmstack.co/be/"
   REACT_APP_BASEURL_without_slash="https://datahubethdev.farmstack.co/be"
   REACT_APP_BASEURL_without_slash_view_data="http://datahubethdev.farmstack.co:"
   REACT_APP_DEV_MODE="true"
   ```

Make sure to replace the values with the appropriate URLs and settings for your environment.

## Usage

To start the FarmStack React App, run the following command:

```bash
npm start
```

This command will build the app and start a local development server. Open your browser and visit http://localhost:3000 to access the application.

## Deployment

To deploy the FarmStack React App to a production environment, follow these steps:

1. Build the app using the following command:
   ```bash
   npm run build
   ```

2. This command will create a `build` directory containing optimized and minified production-ready files.

3. Serve the app using a static server of your choice. You can use tools like `serve`, `nginx`, or `Apache` to serve the static files located in the `build` directory.

   For example, using `serve`:
   ```bash
   npx serve -s build
   ```

The app will be available at the specified server URL.

## Troubleshooting

### Installation Issues

If you encounter errors during `npm install`, try the following solutions:

1. **Peer Dependency Conflicts**:
   ```bash
   npm install --legacy-peer-deps
   ```
   This is automatically configured in the `.npmrc` file, but you can run it manually if needed.

2. **Clear npm cache** (if you have persistent issues):
   ```bash
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Node.js Version Issues**: 
   - Ensure you're using Node.js v14 or higher (v16.x or v18.x recommended)
   - Use a version manager like [nvm](https://github.com/nvm-sh/nvm) to switch between Node.js versions

4. **Memory Issues**: 
   The build scripts are configured with increased memory allocation (`--max-old-space-size=6144`). If you still face memory issues, you can increase this value in `package.json`.

### Build or Start Issues

- Make sure all environment variables are properly set in the `.env` file
- Check that port 3000 is not already in use
- Review the console output for specific error messages

For more help, please open an issue on the GitHub repository.

## Contributing

We welcome contributions to the FarmStack React App! If you'd like to contribute, please follow these steps:

1. Fork the repository on GitHub.

2. Create a new branch with a descriptive name for your feature or bug fix:
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. Make your changes and commit them with clear and concise messages:
   ```bash
   git commit -m "Add feature XYZ"
   ```

4. Push your changes to your forked repository:
   ```bash
   git push origin feature/my-new-feature
   ```

5. Open a pull request on GitHub and provide a detailed description of your changes.

## Backend Setup

For backend setup, visit: https://github.com/digitalgreenorg/datahub-api

## License
The FarmStack React App is released under the MIT License.
