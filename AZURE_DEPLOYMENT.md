# Azure Deployment Guide

## Architecture

We'll deploy this as **TWO separate Azure resources**:
1. **Azure Web App** (Linux) - Python backend (FastAPI)
2. **Azure Static Web App** - Next.js frontend (FREE tier)

This is the recommended Azure approach for full-stack apps.

---

## Step 1: Deploy Backend to Azure Web App

### 1.1 Create Azure Web App via Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"** → Search **"Web App"**
3. Click **Create**

**Settings:**
- **Resource Group**: Create new or select existing
- **Name**: `interview-eval-backend` (or your choice)
- **Publish**: `Code`
- **Runtime stack**: `Python 3.11`
- **Operating System**: `Linux`
- **Region**: Choose nearest region
- **Pricing**: Select your plan (F1 Free tier works for testing)

4. Click **Review + Create** → **Create**

### 1.2 Configure Application Settings

Once created, go to your Web App:

1. **Configuration** → **Application settings** → Click **New application setting**

Add these environment variables:
```
ANTHROPIC_API_KEY=<your-anthropic-key>
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment>
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

2. **Configuration** → **General settings**
- **Startup Command**:
```bash
cd /home/site/wwwroot/backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 300
```

3. Save changes

### 1.3 Enable WebSocket Support

1. **Configuration** → **General settings**
2. **Web sockets**: `On`
3. **Always On**: `On` (if not on Free tier)
4. Save

### 1.4 Deploy Backend Code

**Option A: Via GitHub Actions (Recommended)**

1. In Azure Portal, go to your Web App
2. **Deployment Center** → **Source**: `GitHub`
3. Authorize and select:
   - **Organization**: Your GitHub account
   - **Repository**: `interview-eval`
   - **Branch**: `main`
4. It will auto-create a GitHub Actions workflow

**Option B: Via Azure CLI**

```bash
# Login to Azure
az login

# Deploy
az webapp up --name interview-eval-backend --resource-group <your-rg> --runtime "PYTHON:3.11" --location eastus
```

### 1.5 Verify Backend

Visit: `https://interview-eval-backend.azurewebsites.net/docs`

You should see the FastAPI Swagger UI.

---

## Step 2: Deploy Frontend to Azure Static Web Apps

### 2.1 Create Static Web App

1. Go to [Azure Portal](https://portal.azure.com)
2. **Create a resource** → Search **"Static Web App"**
3. Click **Create**

**Settings:**
- **Resource Group**: Same as backend or new
- **Name**: `interview-eval-frontend`
- **Plan type**: `Free`
- **Region**: Auto-selected
- **Deployment details**:
  - **Source**: `GitHub`
  - **Organization**: Your account
  - **Repository**: `interview-eval`
  - **Branch**: `main`
  - **Build Presets**: `Next.js`
  - **App location**: `/frontend`
  - **Api location**: (leave empty)
  - **Output location**: (leave empty - Next.js default)

4. Click **Review + Create** → **Create**

### 2.2 Configure Frontend Environment Variables

1. Go to your Static Web App resource
2. **Configuration** → **Environment variables**
3. Add:
```
NEXT_PUBLIC_API_URL=https://interview-eval-backend.azurewebsites.net
NEXT_PUBLIC_WS_URL=wss://interview-eval-backend.azurewebsites.net
```

4. Save

### 2.3 Update Frontend Code for Azure

Update `frontend/src/lib/websocket/useEvaluationStream.ts`:

```typescript
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
```

Update `frontend/src/app/page.tsx`:

```typescript
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/evaluations`, {
  method: "POST",
  // ...
});
```

### 2.4 Push Changes and Deploy

```bash
git add .
git commit -m "feat: Add Azure deployment configuration"
git push origin main
```

GitHub Actions will automatically:
1. Build your Next.js app
2. Deploy to Azure Static Web Apps

### 2.5 Verify Frontend

Visit: `https://<generated-url>.azurestaticapps.net`

You should see your app running!

---

## Step 3: Configure CORS

Your backend needs to allow frontend domain:

1. Go to **Backend Web App** → **API** → **CORS**
2. Add allowed origins:
```
https://<your-static-web-app>.azurestaticapps.net
http://localhost:3000
```
3. Enable **"Enable Access-Control-Allow-Credentials"**
4. Save

---

## Alternative: Single Docker Container Deployment

If you prefer deploying both as a single container:

### Create Dockerfile

See `Dockerfile` in project root.

### Deploy to Azure Container Apps

```bash
# Build and push to Azure Container Registry
az acr build --registry <your-acr> --image interview-eval:latest .

# Deploy to Container App
az containerapp create \
  --name interview-eval \
  --resource-group <your-rg> \
  --image <your-acr>.azurecr.io/interview-eval:latest \
  --target-port 3000 \
  --ingress external \
  --environment <your-env>
```

---

## Troubleshooting

### Backend not starting
- Check **Log Stream** in Azure Portal
- Verify Python version is 3.11
- Check if all environment variables are set

### Frontend build fails
- Check **GitHub Actions** logs
- Verify `app location` is set to `/frontend`
- Check if `node_modules` is gitignored

### WebSocket connection fails
- Ensure **Web sockets** is enabled on backend
- Check CORS settings
- Verify `NEXT_PUBLIC_WS_URL` uses `wss://` (not `ws://`)

### Long evaluations timeout
- Increase timeout in startup command: `--timeout 600` (10 minutes)
- Ensure **Always On** is enabled (not available on Free tier)

---

## Cost Estimate

**Recommended production setup:**
- **Backend Web App**: B1 Basic (~$13/month) - Always On + unlimited compute + 10 GB storage
- **Static Web App**: Free tier (100 GB bandwidth/month)
- **Total**: ~$13/month

**Free tier alternative (for testing only):**
- **Backend**: F1 Free tier (1 GB RAM, 60 min/day compute limit, no Always On)
- **Frontend**: Free tier
- **Total**: $0/month (with usage limits)

---

## Security Checklist

- ✅ `.env` file is gitignored
- ✅ Environment variables set in Azure Portal (not in code)
- ✅ CORS properly configured
- ✅ HTTPS enabled by default on Azure
- ✅ WebSockets use WSS (secure)

---

## Next Steps

1. Deploy backend first
2. Get backend URL
3. Update frontend environment variables
4. Deploy frontend
5. Test end-to-end

Need help? Check Azure documentation or reach out!
