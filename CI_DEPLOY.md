# CI/CD and GitHub Actions — Azure Static Web Apps + App Service

This document describes the minimal steps to enable the workflows added to `.github/workflows/`:

Required GitHub secrets (Repository settings -> Secrets -> Actions):

- `AZURE_CREDENTIALS` : JSON output from `az ad sp create-for-rbac --name "github-actions-svc" --role contributor --scopes /subscriptions/<sub-id>/resourceGroups/<rg> --sdk-auth`.
- `AZURE_RESOURCE_GROUP` : the resource group name where the App Service exists (or will be created).
- `AZURE_BACKEND_APP` : the App Service name for the backend web app.
- `AZURE_STATIC_WEB_APPS_API_TOKEN` : token created when you provision an Azure Static Web App and connect it to GitHub. See note below.

Create Azure service principal (example):

```bash
az login
az account set --subscription <SUBSCRIPTION_ID>
az ad sp create-for-rbac --name "github-actions-svc" --role contributor --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP> --sdk-auth
```

Copy the JSON output and add it to the repository secret `AZURE_CREDENTIALS`.

Static Web App token note:
- The `Azure/static-web-apps-deploy` action expects an `azure_static_web_apps_api_token` which is normally created when you provision a Static Web App via the Azure Portal and connect your GitHub repository. When you create the Static Web App from the portal, GitHub integration will add the required secret automatically; otherwise obtain the token from the portal or create the SWA via the CLI and follow Azure docs.

Using the workflows:
- Frontend: pushes to `main` will build the Next.js app in `frontend` and run the Static Web Apps deploy action. Ensure `AZURE_STATIC_WEB_APPS_API_TOKEN` is present.
- Backend: pushes to `main` will install backend dependencies, run tests, and then use `az webapp deploy` (zip deploy) to push `backend` to App Service. Ensure `AZURE_CREDENTIALS`, `AZURE_RESOURCE_GROUP`, and `AZURE_BACKEND_APP` secrets are present.

If you don't yet have the App Service or Static Web App created, you can either:

1) Run the repo's existing `deploy-azure.ps1` script locally (on Windows PowerShell) or `deploy-azure.sh` (on Bash) after copying `deploy-config.example.ps1` and setting values; those scripts will create the resources and set app settings. They will also output the SWA connection/token when they configure the GitHub deployment.

2) Manually create resources via Azure Portal and add the required secrets to GitHub.

Post-deploy checks:

- Backend logs: `az webapp log tail --name <APP_NAME> --resource-group <RG>`
- Frontend: monitor GitHub Actions run and visit the Static Web App URL shown in the action or portal.
