import jwt
import time
import requests

APP_ID = "983619"  # <-- pon aquí tu App ID
PRIVATE_KEY_PATH = "metadata-updater-for-fairsoft.2024-08-30.private-key.pem"

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

def make_app_jwt():
    """Create a JWT to authenticate as the GitHub App."""
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),  # 10 minutes
        "iss": APP_ID,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def get_installations(jwt_token):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = "https://api.github.com/app/installations"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def create_installation_token(jwt_token, installation_id):
    """Create an installation access token for a given installation."""
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["token"]

def get_repos_for_installation(installation_token):
    """Return (total_count, repositories_list) for one installation."""
    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json"
    }
    url = "https://api.github.com/installation/repositories"
    params = {"per_page": 100}
    
    total_count = 0
    repos = []

    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        # data["total_count"] is total for the installation
        # data["repositories"] is the current page
        if total_count == 0:
            total_count = data.get("total_count", len(data.get("repositories", [])))

        repos.extend(data.get("repositories", []))

        # Pagination: check if there is a "next" link
        link = resp.headers.get("Link", "")
        if 'rel="next"' not in link:
            break

        # GitHub uses pagination via "page" parameter, so increment it
        if "page=" in url:
            # crude way: not strictly needed if we parse Link, but fine for small scripts
            pass

        # Simpler: parse "next" from Link header (small helper)
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                next_url = part.split(";")[0].strip().strip("<>")
                break
        if not next_url:
            break
        url = next_url  # use the full next URL

    return total_count, repos

def main():
    jwt_token = make_app_jwt()
    installations = get_installations(jwt_token)

    print(f"Number of installations: {len(installations)}")

    grand_total_repos = 0

    for inst in installations:
        inst_id = inst["id"]
        account = inst["account"]["login"]
        print(f"\nInstallation {inst_id} on account '{account}'")

        installation_token = create_installation_token(jwt_token, inst_id)
        total_count, repos = get_repos_for_installation(installation_token)

        print(f"  Repositories in this installation: {total_count}")
        grand_total_repos += total_count

    print("\n============================")
    print(f"Total repositories across all installations: {grand_total_repos}")
    print("============================")

if __name__ == "__main__":
    main()
