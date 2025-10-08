# Quick Start Guide

This guide will help you get the FarmStack Frontend up and running in minutes.

## Step 1: Prerequisites Check

Ensure you have Node.js and npm installed:

```bash
node --version   # Should be v14 or higher (v16.x or v18.x recommended)
npm --version    # Should be v6 or higher
```

If not installed, download from: https://nodejs.org/

## Step 2: Navigate to Frontend Directory

```bash
cd farmstack-frontend
```

## Step 3: Install Dependencies

Simply run:

```bash
npm install
```

That's it! The `.npmrc` file automatically handles dependency conflicts.

## Step 4: Configure Environment

Create a `.env` file in the `farmstack-frontend` directory:

```bash
# Create .env file
cat > .env << 'EOF'
REACT_APP_BASEURL="https://datahubethdev.farmstack.co/be/"
REACT_APP_BASEURL_without_slash="https://datahubethdev.farmstack.co/be"
REACT_APP_BASEURL_without_slash_view_data="http://datahubethdev.farmstack.co:"
REACT_APP_DEV_MODE="true"
EOF
```

**Important**: Update these URLs to match your backend setup.

## Step 5: Start Development Server

```bash
npm start
```

The app will automatically open in your browser at http://localhost:3000

## Common Issues

### Installation fails?
Try clearing cache:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Port 3000 already in use?
Kill the process or use a different port:
```bash
PORT=3001 npm start
```

### Build fails?
Check that your `.env` file is properly configured with all required variables.

## Next Steps

- Review the full [README.md](./README.md) for detailed documentation
- Check the [Backend Repository](https://github.com/digitalgreenorg/datahub-api) for backend setup
- Join our community for support and contributions

## Build for Production

When ready to deploy:

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

---

For more detailed information, see [README.md](./README.md)
