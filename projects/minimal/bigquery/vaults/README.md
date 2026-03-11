# Vaults

External credential stores for secure secret management.

## Usage

Reference secrets in YAML configurations:

```yaml
api_key: ${vaults.environment.MY_API_KEY}
```

## Built-in Vault

Ascend provides a built-in `environment` vault for runtime-specific secrets. Use it for secrets that don't need external management:

```yaml
api_key: ${vaults.environment.MY_API_KEY}
```

