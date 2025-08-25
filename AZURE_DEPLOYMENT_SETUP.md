# Azure Container Apps Deployment Setup

This guide will help you set up GitHub Actions to automatically deploy your FastAPI application to Azure Container Apps.

## Prerequisites

1. **Azure Resources** (create these first):
   - Azure Container Registry (ACR)
   - Azure Container App Environment
   - Azure Container App

2. **GitHub Repository Secrets** (configure these in your repo):
   - `AZURE_CREDENTIALS`
   - `REGISTRY_USERNAME` 
   - `REGISTRY_PASSWORD`
   - `AZURE_KEY`
   - `AZURE_ENDPOINT_NAME`

## Step 1: Create Azure Resources

using Azure CLI, create the necessary resources:

```bash
# Create Resource Group
az group create --name myResourceGroup --location "West US 2"

# Create Azure Container Registry
az acr create --name myacrname --resource-group myResourceGroup --sku Basic --admin-enabled true

# Create Container App Environment
az containerapp env create \
  --name mycontainerappenv \
  --resource-group myResourceGroup \
  --location "West US 2"

# Create Container App
az containerapp create \
  --name multiagents-web-api \
  --resource-group myResourceGroup \
  --environment mycontainerappenv \
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
  --target-port 8282 \
  --ingress external \
  --query properties.configuration.ingress.fqdn
```

## Step 2: Get Azure Credentials

### 2.1 Create Service Principal
```bash
az ad sp create-for-rbac --name "myApp" --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

### 2.2 Get ACR Credentials
```bash
az acr credential show --name myacrname
```

## Step 3: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

1. **AZURE_CREDENTIALS**: The entire JSON output from the service principal creation
2. **REGISTRY_USERNAME**: ACR username from `az acr credential show`
3. **REGISTRY_PASSWORD**: ACR password from `az acr credential show`
4. **AZURE_KEY**: Your Azure OpenAI API key
5. **AZURE_ENDPOINT_NAME**: Your Azure OpenAI endpoint name

## Step 4: Update Workflow Variables

Edit `.github/workflows/build-and-deploy-simple.yml` and update these variables:

```yaml
env:
  REGISTRY_NAME: "your-acr-name"                    # Your ACR name
  RESOURCE_GROUP: "your-resource-group"            # Your resource group
  CONTAINER_APP_NAME: "multiagents-web-api"        # Your container app name
  CONTAINER_APP_ENVIRONMENT: "your-aca-environment" # Your container app environment
```

## Step 5: Deploy

Push your code to the `main` branch, and the GitHub Action will automatically:

1. Build your Docker image
2. Push it to Azure Container Registry
3. Deploy it to Azure Container Apps

Your app will be available at the FQDN returned by the container app creation command.

## Troubleshooting

- **Authentication errors**: Verify your service principal has the correct permissions
- **Registry access**: Ensure ACR admin is enabled and credentials are correct
- **Port issues**: Make sure your app listens on 0.0.0.0:8282 and the container app target port is 8282
- **Environment variables**: Check that all required secrets are set in GitHub

## Monitoring

Monitor your deployment in the Azure Portal:
- Container Apps → Your app → Revision management
- Container Registry → Repositories → Check for new images
- Log Analytics → Query container app logs
