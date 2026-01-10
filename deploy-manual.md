# Manual Deployment (Without GitHub Access)

If you prefer not to give Azure access to your GitHub repository, you can deploy manually.

## Option 1: Deploy from Local Machine

### Backend (Using Azure CLI):
```powershell
# Build and deploy backend directly from your machine
cd "C:\Users\shirawat1\Downloads\Interview Agent"

# Create a zip of the backend
Compress-Archive -Path .\* -DestinationPath deploy.zip -Force

# Deploy to Azure Web App
az webapp deployment source config-zip `
  --resource-group interview-eval-rg `
  --name interview-eval-backend `
  --src deploy.zip
```

### Frontend (Build locally and deploy):
```powershell
# Build Next.js app locally
cd frontend
npm install
npm run build

# Deploy using Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli
swa deploy --app-location . --output-location .next
```

## Option 2: Deploy from Private Repository

If your concern is that the repo is public:

1. **Make your repository private:**
   - Go to GitHub repo Settings → General → Danger Zone
   - Click "Change visibility" → Make Private

2. **Then grant Azure access** - it can only access this one private repo

## Option 3: Fork and Deploy from Your Fork

1. Fork the repository to your personal account
2. Make it private
3. Deploy from your private fork

## Revoking Access Later

If you want to revoke Azure's access to GitHub:

1. Go to GitHub → Settings → Applications → Authorized OAuth Apps
2. Find "Azure Static Web Apps"
3. Click "Revoke"

This will stop automatic deployments but won't affect already-deployed resources.

---

**Recommendation:** For production use, the GitHub integration is convenient and secure. Your API keys are never exposed to GitHub, only stored encrypted in Azure.
