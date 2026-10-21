import jwt
import time
import requests

APP_ID = "983619"  # <-- pon aquí tu App ID de GitHub

PRIVATE_KEY_PATH = "metadata-updater-for-fairsoft.2024-08-30.private-key.pem"

# Leer la clave privada
with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

# Generar JWT válido por 10 minutos
payload = {
    "iat": int(time.time()),
    "exp": int(time.time()) + (10 * 60),
    "iss": APP_ID,
}

jwt_token = jwt.encode(
    payload,
    PRIVATE_KEY,
    algorithm="RS256"
)

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json"
}

url = "https://api.github.com/app/installations"

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    installations = response.json()
    print("Number of installations:", len(installations))
    print("Installations:")
    for inst in installations:
        print(f"- ID {inst['id']} | account: {inst['account']['login']}")
else:
    print(response.text)
