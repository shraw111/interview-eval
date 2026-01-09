# Azure Deployment Script for Interview Evaluation System (PowerShell)
# This script creates and configures all Azure resources needed

$ErrorActionPreference = "Stop"

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Resource configuration
$RESOURCE_GROUP = "interview-eval-rg"
$LOCATION = "eastus"  # Change to your preferred region
$BACKEND_APP_NAME = "interview-eval-backend"  # Must be globally unique
$FRONTEND_APP_NAME = "interview-eval-frontend"  # Must be globally unique

# Your credentials (REQUIRED - fill these in)
$ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
$AZURE_OPENAI_ENDPOINT = "your-azure-openai-endpoint-here"
$AZURE_OPENAI_API_KEY = "your-azure-openai-key-here"
$AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name-here"
$AZURE_OPENAI_API_VERSION = "2024-08-01-preview"

# GitHub repository
$GITHUB_REPO = "shraw111/interview-eval"
$GITHUB_BRANCH = "main"

# Pricing tiers
$BACKEND_SKU = "F1"  # F1=Free, B1=Basic ($13/mo with Always On)
$FRONTEND_SKU = "Free"

# ============================================================================
# DEPLOYMENT SCRIPT - DO NOT EDIT BELOW THIS LINE
# ============================================================================

Write-Host "=========================================="
Write-Host "Azure Deployment - Interview Eval System"
Write-Host "=========================================="
Write-Host ""

# Check if logged in to Azure
Write-Host "Checking Azure login status..."
try {
    $account = az account show 2>$null | ConvertFrom-Json
    $subscriptionId = $account.id
    Write-Host "✅ Using subscription: $subscriptionId" -ForegroundColor Green
} catch {
    Write-Host "❌ Not logged in to Azure. Running 'az login'..." -ForegroundColor Red
    az login
    $account = az account show | ConvertFrom-Json
    $subscriptionId = $account.id
}
Write-Host ""

# Create resource group
Write-Host "Creating resource group: $RESOURCE_GROUP..."
az group create `
  --name $RESOURCE_GROUP `
  --location $LOCATION `
  --output table
Write-Host ""

# ============================================================================
# BACKEND - Azure Web App (Python FastAPI)
# ============================================================================

Write-Host "=========================================="
Write-Host "Creating Backend Web App..."
Write-Host "=========================================="

# Create App Service Plan
Write-Host "Creating App Service Plan..."
az appservice plan create `
  --name "$BACKEND_APP_NAME-plan" `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --is-linux `
  --sku $BACKEND_SKU `
  --output table
Write-Host ""

# Create Web App
Write-Host "Creating Web App: $BACKEND_APP_NAME..."
az webapp create `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --plan "$BACKEND_APP_NAME-plan" `
  --runtime "PYTHON:3.11" `
  --output table
Write-Host ""

# Configure Web App settings
Write-Host "Configuring Web App settings..."

# Set startup command
az webapp config set `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --startup-file "cd /home/site/wwwroot/backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 300" `
  --output table
Write-Host ""

# Enable WebSockets
az webapp config set `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --web-sockets-enabled true `
  --output table
Write-Host ""

# Enable Always On (only works on B1 and above, not F1 Free)
if ($BACKEND_SKU -ne "F1") {
    Write-Host "Enabling Always On..."
    az webapp config set `
      --name $BACKEND_APP_NAME `
      --resource-group $RESOURCE_GROUP `
      --always-on true `
      --output table
    Write-Host ""
}

# Set environment variables
Write-Host "Setting environment variables..."
az webapp config appsettings set `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --settings `
    ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" `
    AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" `
    AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" `
    AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" `
    AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" `
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
  --output table
Write-Host ""

# Configure deployment from GitHub
Write-Host "Configuring GitHub deployment..."
Write-Host "⚠️  You'll need to authorize GitHub access in your browser..." -ForegroundColor Yellow
az webapp deployment source config `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --repo-url "https://github.com/$GITHUB_REPO" `
  --branch $GITHUB_BRANCH `
  --manual-integration `
  --output table
Write-Host ""

$BACKEND_URL = "https://$BACKEND_APP_NAME.azurewebsites.net"
Write-Host "✅ Backend deployed at: $BACKEND_URL" -ForegroundColor Green
Write-Host ""

# ============================================================================
# FRONTEND - Azure Static Web App (Next.js)
# ============================================================================

Write-Host "=========================================="
Write-Host "Creating Frontend Static Web App..."
Write-Host "=========================================="

Write-Host "Creating Static Web App: $FRONTEND_APP_NAME..."
Write-Host "⚠️  You'll need to authorize GitHub access in your browser..." -ForegroundColor Yellow

az staticwebapp create `
  --name $FRONTEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --source "https://github.com/$GITHUB_REPO" `
  --branch $GITHUB_BRANCH `
  --app-location "/frontend" `
  --output-location "" `
  --login-with-github `
  --output table
Write-Host ""

# Get Static Web App URL
$FRONTEND_HOSTNAME = az staticwebapp show `
  --name $FRONTEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --query "defaultHostname" -o tsv
$FRONTEND_URL = "https://$FRONTEND_HOSTNAME"

Write-Host "✅ Frontend deployed at: $FRONTEND_URL" -ForegroundColor Green
Write-Host ""

# Set frontend environment variables
Write-Host "Setting frontend environment variables..."
az staticwebapp appsettings set `
  --name $FRONTEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --setting-names `
    NEXT_PUBLIC_API_URL="$BACKEND_URL" `
    NEXT_PUBLIC_WS_URL="wss://$BACKEND_APP_NAME.azurewebsites.net" `
  --output table
Write-Host ""

# ============================================================================
# CONFIGURE CORS
# ============================================================================

Write-Host "=========================================="
Write-Host "Configuring CORS..."
Write-Host "=========================================="

# Add frontend URL to backend CORS
az webapp cors add `
  --name $BACKEND_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --allowed-origins $FRONTEND_URL "http://localhost:3000" `
  --output table
Write-Host ""

# ============================================================================
# DEPLOYMENT COMPLETE
# ============================================================================

Write-Host "=========================================="
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=========================================="
Write-Host ""
Write-Host "🔗 Backend API:  $BACKEND_URL"
Write-Host "🔗 Backend Docs: $BACKEND_URL/docs"
Write-Host "🔗 Frontend App: $FRONTEND_URL"
Write-Host ""
Write-Host "📋 Next steps:"
Write-Host "1. Wait 2-3 minutes for GitHub Actions to build and deploy"
Write-Host "2. Visit $BACKEND_URL/docs to verify backend"
Write-Host "3. Visit $FRONTEND_URL to use the app"
Write-Host ""
Write-Host "🔍 Monitor deployments:"
Write-Host "   Backend:  az webapp log tail --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP"
Write-Host "   Frontend: Check GitHub Actions at https://github.com/$GITHUB_REPO/actions"
Write-Host ""
Write-Host "💰 Cost estimate:"
Write-Host "   - Backend (F1):  `$0/month (60 min/day limit)"
Write-Host "   - Frontend:      `$0/month (Free tier)"
Write-Host "   - Total:         `$0/month"
Write-Host ""
Write-Host "📚 For troubleshooting, see: AZURE_DEPLOYMENT.md"
