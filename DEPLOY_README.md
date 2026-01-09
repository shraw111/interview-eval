# Quick Deploy to Azure

Two deployment scripts are provided - use whichever you prefer:
- **`deploy-azure.ps1`** - PowerShell (recommended for Windows)
- **`deploy-azure.sh`** - Bash (Linux/Mac/WSL)

## Prerequisites

1. **Azure CLI** installed
   - Windows: `winget install Microsoft.AzureCLI`
   - Or download from: https://aka.ms/installazurecliwindows

2. **GitHub account** with access to your repository

3. **Azure subscription** (free tier works!)

## Step 1: Get Your Azure OpenAI Details

Go to **Azure Portal** → Your **OpenAI resource** → **Keys and Endpoint**:
- Copy the **Endpoint** (e.g., `https://your-resource.openai.azure.com/`)
- Copy **Key 1** or **Key 2**
- Note your **Deployment name** (e.g., `gpt-4o`, `gpt-4`, `gpt-35-turbo`)

## Step 2: Edit Configuration

Open `deploy-azure.ps1` (or `.sh`) and fill in these values at the top:

```powershell
# REQUIRED - Fill these in:
$AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$AZURE_OPENAI_API_KEY = "your-azure-key-here"
$AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"
```

**Note:** You do NOT need an Anthropic API key - the system uses Azure OpenAI only.

**Optional - Customize names:**
```powershell
$BACKEND_APP_NAME = "interview-eval-backend"  # Change if name taken
$FRONTEND_APP_NAME = "interview-eval-frontend"  # Change if name taken
$LOCATION = "eastus"  # Or "westus", "centralus", etc.
```

## Step 3: Run the Script

The script will:
1. Log you into Azure (opens browser)
2. Show all your subscriptions - choose one or press Enter for default
3. Create all resources automatically

### PowerShell (Windows):
```powershell
cd "C:\Users\shirawat1\Downloads\Interview Agent"
.\deploy-azure.ps1
```

### Bash (Linux/Mac/WSL):
```bash
cd "/c/Users/shirawat1/Downloads/Interview Agent"
chmod +x deploy-azure.sh
./deploy-azure.sh
```

## What the Script Does

1. ✅ Creates resource group
2. ✅ Creates backend Web App (Python 3.11)
3. ✅ Configures WebSocket support
4. ✅ Sets all environment variables
5. ✅ Connects to GitHub for auto-deployment
6. ✅ Creates frontend Static Web App
7. ✅ Configures CORS between frontend/backend
8. ✅ Returns URLs for both services

**Total time: ~5 minutes**

## After Deployment

The script will output:
```
✅ DEPLOYMENT COMPLETE!

🔗 Backend API:  https://interview-eval-backend.azurewebsites.net
🔗 Backend Docs: https://interview-eval-backend.azurewebsites.net/docs
🔗 Frontend App: https://interview-eval-frontend.azurestaticapps.net
```

**Wait 2-3 minutes** for GitHub Actions to build and deploy, then visit the Frontend URL!

## Troubleshooting

### "The name is already in use"
Change `$BACKEND_APP_NAME` or `$FRONTEND_APP_NAME` in the script to something unique.

### GitHub authorization fails
The script will open your browser for GitHub OAuth. Make sure you approve the Azure Static Web Apps application.

### Backend not starting
Check logs:
```powershell
az webapp log tail --name interview-eval-backend --resource-group interview-eval-rg
```

### Frontend build fails
Check GitHub Actions: https://github.com/shraw111/interview-eval/actions

## Cost

- **Default (B1)**: $13/month - Always On, unlimited compute, no daily limits
- **Free tier option**: Change `$BACKEND_SKU = "F1"` for $0/month (60 min/day limit, no Always On)
- **Frontend**: Always free ($0/month)

## Manual Cleanup

To delete everything:
```powershell
az group delete --name interview-eval-rg --yes --no-wait
```

---

**For detailed explanation, see:** `AZURE_DEPLOYMENT.md`
