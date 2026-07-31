import os

from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SECRET_NAME = os.environ.get("SECRET_NAME", "db-connection-string")


def get_secret_client():
    # DefaultAzureCredential prueba, en orden, variables de entorno,
    # Managed Identity y la sesion de az cli. Nunca hay credenciales
    # escritas en el codigo.
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=KEY_VAULT_URL, credential=credential)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/secret")
def secret():
    if not KEY_VAULT_URL:
        return jsonify(error="KEY_VAULT_URL no esta configurada"), 500

    try:
        client = get_secret_client()
        value = client.get_secret(SECRET_NAME).value
    except Exception as exc:
        return jsonify(error=f"no se pudo obtener el secreto: {exc}"), 500

    # Solo devolvemos que la conexion fue posible, nunca el valor real.
    return jsonify(secret_name=SECRET_NAME, retrieved=True, length=len(value))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
