#!/bin/bash

# Azure Deployment Script for Interview Evaluation System
# This script creates and configures all Azure resources needed

set -e  # Exit on error

# ============================================================================
# LOAD CONFIGURATION
# ============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/deploy-config.sh"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Configuration file not found!"
    echo ""
    echo "Please create your configuration file:"
    echo "1. Copy: deploy-config.example.sh"
    echo "2. To:   deploy-config.sh"
    echo "3. Edit deploy-config.sh and fill in your Azure OpenAI credentials"
    echo ""
    echo "The deploy-config.sh file is gitignored and safe from being committed."
    exit 1
fi

echo "Loading configuration from: $CONFIG_FILE"
source "$CONFIG_FILE"

# Validate required variables
required_vars=(
    "RESOURCE_GROUP"
    "LOCATION"
    "BACKEND_APP_NAME"
    "FRONTEND_APP_NAME"
    "AZURE_OPENAI_ENDPOINT"
    "AZURE_OPENAI_API_KEY"
    "AZURE_OPENAI_DEPLOYMENT_NAME"
    "GITHUB_REPO"
    "GITHUB_BRANCH"
    "BACKEND_SKU"
)

missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "❌ ERROR: Missing required configuration variables:"
    for var in "${missing_vars[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "Please edit deploy-config.sh and fill in all required values."
    exit 1
fi

# ============================================================================
# DEPLOYMENT SCRIPT - DO NOT EDIT BELOW THIS LINE
# ============================================================================

echo "=========================================="
echo "Azure Deployment - Interview Eval System"
echo "=========================================="
echo ""

# Check if logged in to Azure
echo "Checking Azure login status..."
if az account show > /dev/null 2>&1; then
    echo "✅ Already logged in to Azure"
else
    echo "❌ Not logged in to Azure. Opening browser for login..."
    az login
fi

# List subscriptions and let user choose
echo ""
echo "Available Azure Subscriptions:"
echo "=============================="
az account list --query "[].{Index:name, ID:id}" -o table

echo ""
read -p "Enter subscription ID (press Enter for default): " SUB_ID

if [ ! -z "$SUB_ID" ]; then
    echo "Setting subscription to: $SUB_ID"
    az account set --subscription "$SUB_ID"
fi

CURRENT_SUB=$(az account show --query name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "✅ Using subscription: $CURRENT_SUB"
echo "   Subscription ID: $SUBSCRIPTION_ID"
echo ""

# Create resource group
echo "Creating resource group: $RESOURCE_GROUP..."
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --output table
echo ""

# ============================================================================
# BACKEND - Azure Web App (Python FastAPI)
# ============================================================================

echo "=========================================="
echo "Creating Backend Web App..."
echo "=========================================="

# Create App Service Plan
echo "Creating App Service Plan..."
az appservice plan create \
  --name "${BACKEND_APP_NAME}-plan" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --is-linux \
  --sku "$BACKEND_SKU" \
  --output table
echo ""

# Create Web App
echo "Creating Web App: $BACKEND_APP_NAME..."
az webapp create \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --plan "${BACKEND_APP_NAME}-plan" \
  --runtime "PYTHON:3.11" \
  --output table
echo ""

# Configure Web App settings
echo "Configuring Web App settings..."

# Set startup command
az webapp config set \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --startup-file "cd /home/site/wwwroot/backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 300" \
  --output table
echo ""

# Enable WebSockets
az webapp config set \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --web-sockets-enabled true \
  --output table
echo ""

# Enable Always On (only works on B1 and above, not F1 Free)
if [ "$BACKEND_SKU" != "F1" ]; then
  echo "Enabling Always On..."
  az webapp config set \
    --name "$BACKEND_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --always-on true \
    --output table
  echo ""
fi

# Set environment variables
echo "Setting environment variables..."
az webapp config appsettings set \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --settings \
    AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
    AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
    AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" \
    AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
  --output table
echo ""

# Configure deployment from GitHub
echo "Configuring GitHub deployment..."
echo "⚠️  You'll need to authorize GitHub access in your browser..."
az webapp deployment source config \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --repo-url "https://github.com/$GITHUB_REPO" \
  --branch "$GITHUB_BRANCH" \
  --manual-integration \
  --output table
echo ""

BACKEND_URL="https://${BACKEND_APP_NAME}.azurewebsites.net"
echo "✅ Backend deployed at: $BACKEND_URL"
echo ""

# ============================================================================
# FRONTEND - Azure Static Web App (Next.js)
# ============================================================================

echo "=========================================="
echo "Creating Frontend Static Web App..."
echo "=========================================="

# Note: Static Web Apps with GitHub integration requires GitHub token
# The CLI will open a browser for OAuth authorization

echo "Creating Static Web App: $FRONTEND_APP_NAME..."
echo "⚠️  You'll need to authorize GitHub access in your browser..."

az staticwebapp create \
  --name "$FRONTEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --source "https://github.com/$GITHUB_REPO" \
  --branch "$GITHUB_BRANCH" \
  --app-location "/frontend" \
  --output-location "" \
  --login-with-github \
  --output table
echo ""

# Get Static Web App URL
FRONTEND_URL=$(az staticwebapp show \
  --name "$FRONTEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "defaultHostname" -o tsv)
FRONTEND_URL="https://$FRONTEND_URL"

echo "✅ Frontend deployed at: $FRONTEND_URL"
echo ""

# Set frontend environment variables
echo "Setting frontend environment variables..."
az staticwebapp appsettings set \
  --name "$FRONTEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --setting-names \
    NEXT_PUBLIC_API_URL="$BACKEND_URL" \
    NEXT_PUBLIC_WS_URL="wss://${BACKEND_APP_NAME}.azurewebsites.net" \
  --output table
echo ""

# ============================================================================
# CONFIGURE CORS
# ============================================================================

echo "=========================================="
echo "Configuring CORS..."
echo "=========================================="

# Add frontend URL to backend CORS
az webapp cors add \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --allowed-origins "$FRONTEND_URL" "http://localhost:3000" \
  --output table
echo ""

# Enable credentials
az webapp cors set \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --allowed-origins "$FRONTEND_URL" "http://localhost:3000" \
  --output table
echo ""

# ============================================================================
# DEPLOYMENT COMPLETE
# ============================================================================

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🔗 Backend API:  $BACKEND_URL"
echo "🔗 Backend Docs: $BACKEND_URL/docs"
echo "🔗 Frontend App: $FRONTEND_URL"
echo ""
echo "📋 Next steps:"
echo "1. Wait 2-3 minutes for GitHub Actions to build and deploy"
echo "2. Visit $BACKEND_URL/docs to verify backend"
echo "3. Visit $FRONTEND_URL to use the app"
echo ""
echo "🔍 Monitor deployments:"
echo "   Backend:  az webapp log tail --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP"
echo "   Frontend: Check GitHub Actions at https://github.com/$GITHUB_REPO/actions"
echo ""
echo "💰 Cost estimate:"
echo "   - Backend (B1):  \$13/month (Always On, unlimited)"
echo "   - Frontend:      \$0/month (Free tier)"
echo "   - Total:         ~\$13/month"
echo ""
echo "📚 For troubleshooting, see: AZURE_DEPLOYMENT.md"
