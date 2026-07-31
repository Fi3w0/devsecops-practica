import os

from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SECRET_NAME = os.environ.get("SECRET_NAME", "db-connection-string")
# Simulacion local: mi suscripcion de azure free caduco y no pude crear el
# key vault real para esta entrega. Si esta variable esta puesta, la app
# responde como si el secreto viniera de key vault pero en realidad es un
# valor local, solo para poder probar el endpoint /secret.
LOCAL_MOCK_SECRET = os.environ.get("LOCAL_MOCK_SECRET")


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
    if LOCAL_MOCK_SECRET:
        return jsonify(
            secret_name=SECRET_NAME,
            retrieved=True,
            length=len(LOCAL_MOCK_SECRET),
            source="local-mock (sin azure, suscripcion caducada)",
        )

    if not KEY_VAULT_URL:
        return jsonify(error="KEY_VAULT_URL no esta configurada"), 500

    try:
        client = get_secret_client()
        value = client.get_secret(SECRET_NAME).value
    except Exception as exc:
        return jsonify(error=f"no se pudo obtener el secreto: {exc}"), 500

    # Solo devolvemos que la conexion fue posible, nunca el valor real.
    return jsonify(secret_name=SECRET_NAME, retrieved=True, length=len(value), source="azure-key-vault")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
