#create storage in azure
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
    
  name: 'mystorageaccount${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}