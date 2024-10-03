import requests
import msal
from ascend.resources import custom_python
from ascend.application.context import ComponentExecutionContext


@custom_python()
# Function to refresh dataset
def refresh_powerbi_dataset(context: ComponentExecutionContext):
    # Configuration - replace with your values from you vault
    client_id = context.vaults["my_vault"].get("powerbi","CLIENT_ID")
    client_secret = context.vaults["my_vault"].get("powerbi","CLIENT_SECRET")
    tenant_id = context.vaults["my_vault"].get("powerbi","TENANT_ID")
    workspace_id = 'powerbi_workspace_id'  # Power BI workspace ID
    dataset_id = 'powerbi_dataset_id'  # Dataset ID for customer_cohort_analysis

    # Authority URL and scope
    authority_url = f'https://login.microsoftonline.com/{tenant_id}'
    scope = ["https://analysis.windows.net/powerbi/api/.default"]

    app = msal.ConfidentialClientApplication(client_id, authority=authority_url, client_credential=client_secret)
    result = app.acquire_token_for_client(scopes=scope)

    if "access_token" in result:
        access_token = result["access_token"]
    else:
        raise Exception(f"Failed to obtain access token: {result.get('error_description', 'Unknown error')}")

    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        print(f"Dataset '{dataset_id}' refresh initiated successfully.")
    else:
        raise Exception(f"Failed to refresh dataset: {response.status_code}, {response.text}")

