# Ascend Quickstart

Welcome to the Ascend Quickstart! This guide will help you get started with your Ascend platform.

You can find full [documentation here](https://docs.ascend.io/tutorials/quickstart/).


## 📁 Folders & 📑 Files

In this quickstart project, you'll find the following folders:
- `connections/`: Connection definitions that you will use to connect your to your underlying data plane, as well as read local files.
- `data/`: Where you place an local data that you want to access in your flow.
- `flows/`: Flow definitions, along with their components.
- `profiles/`: Profiles to configure & customize flow behavior across different environments.
- `vaults/`: Configure secrets access for use across your project.


## Configuration

To get this quickstart working, you'll need to modify the following files:
- `connections/my_data_plane.yaml`: Remove either the bigquery or snowflake sections, depending on what data plane you're using.
- `profiles/prod.yaml`: Update the parameters to match the values you used during your quickstart setup, and remove the parameters not relevant to your setup.
- `vaults/my_vault.yaml`: Remove either the azure_key_vault or gcp_secret_manager sections, depending on what vault you're using.