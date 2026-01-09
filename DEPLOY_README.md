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

## Step 1: Edit Configuration

Open `deploy-azure.ps1` (or `.sh`) and fill in your credentials at the top:

```powershell
# REQUIRED - Fill these in:
$ANTHROPIC_API_KEY = "sk-ant-..."
$AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$AZURE_OPENAI_API_KEY = "your-azure-key-here"
$AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"
```

**Optional - Customize names:**
```powershell
$BACKEND_APP_NAME = "interview-eval-backend"  # Change if name taken
$FRONTEND_APP_NAME = "interview-eval-frontend"  # Change if name taken
$LOCATION = "eastus"  # Or "westus", "centralus", etc.
```

## Step 2: Run the Script

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

- **Free tier**: $0/month (Backend F1 has 60 min/day limit)
- **Production**: Change `$BACKEND_SKU = "B1"` for $13/month (Always On, no limits)

## Manual Cleanup

To delete everything:
```powershell
az group delete --name interview-eval-rg --yes --no-wait
```

---

**For detailed explanation, see:** `AZURE_DEPLOYMENT.md`
