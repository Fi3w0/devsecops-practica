# devsecops-practica

Práctica 4 del módulo de DevOps: integración de seguridad en el ciclo de vida
del desarrollo con Gitleaks, Trivy y Azure Key Vault.

## Correr en local

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export KEY_VAULT_URL="https://kv-devsecops.vault.azure.net/"
python app.py
```

La app expone `/health` y `/secret` (este último lee el secreto desde Azure
Key Vault usando `DefaultAzureCredential`, sin credenciales en el código).
