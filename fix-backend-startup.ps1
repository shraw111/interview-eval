# Fix Backend Startup Command
# This configures Azure Web App to use the startup.sh script
param(
    [string]$AppName = "interview-eval-backend-shrawat",
    [string]$ResourceGroup = "interview-eval-rg",
    [int]$WaitSeconds = 15
)

Write-Host "Configuring Azure Web App startup..." -ForegroundColor Cyan

# Configure startup to use startup.sh (created by Oryx during deploy)
& az webapp config set --name $AppName --resource-group $ResourceGroup --startup-file "startup.sh"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to configure startup file (az returned exit code $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}

Write-Host "Startup file configured successfully." -ForegroundColor Green
Write-Host "Restarting web app..." -ForegroundColor Cyan

& az webapp restart --name $AppName --resource-group $ResourceGroup
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to restart web app (az returned exit code $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}

Write-Host "Web app restarted. Waiting $WaitSeconds seconds for startup..." -ForegroundColor Green
Start-Sleep -Seconds $WaitSeconds

# Health check
$healthUrl = "https://$AppName.azurewebsites.net/api/v1/health"
Write-Host "Testing health endpoint: $healthUrl" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -ErrorAction Stop
    Write-Host "Backend is healthy." -ForegroundColor Green
    Write-Host "Response: $($response.Content)"
} catch {
    Write-Host "Health check failed: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "Tail logs with:" -ForegroundColor Cyan
    Write-Host "az webapp log tail --name $AppName --resource-group $ResourceGroup"
    exit 2
}

Write-Host "Done." -ForegroundColor Green
