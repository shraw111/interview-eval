# ============================================================================
# DEPLOYMENT CONFIGURATION
# ============================================================================
#
# IMPORTANT: This file contains sensitive credentials!
#
# HOW TO USE:
# 1. Copy this file to: deploy-config.ps1
# 2. Fill in your actual values in deploy-config.ps1
# 3. Run the deployment script: .\deploy-azure.ps1
#
# The deploy-config.ps1 file is gitignored and will NOT be committed to Git.
# ============================================================================

# Resource configuration
$RESOURCE_GROUP = "interview-eval-rg"
$LOCATION = "eastus"  # Change to your preferred region
$BACKEND_APP_NAME = "interview-eval-backend"  # Must be globally unique - change this!
$FRONTEND_APP_NAME = "interview-eval-frontend"  # Must be globally unique - change this!

# Your Azure OpenAI credentials (REQUIRED - fill these in)
# Find these in Azure Portal -> Your OpenAI resource -> Keys and Endpoint
$AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$AZURE_OPENAI_API_KEY = "paste-your-key-here"
$AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"  # Your deployment name (e.g., gpt-4o, gpt-4, gpt-35-turbo)
$AZURE_OPENAI_API_VERSION = "2024-08-01-preview"

# GitHub repository
$GITHUB_REPO = "shraw111/interview-eval"
$GITHUB_BRANCH = "main"

# Pricing tiers
$BACKEND_SKU = "B1"  # B1=Basic ($13/mo) with Always On + unlimited storage. Use "F1" for free tier (60 min/day limit)
$FRONTEND_SKU = "Free"
