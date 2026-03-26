from functools import lru_cache

import requests
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from app.core.config import settings

bearer_scheme = HTTPBearer()


@lru_cache
def get_jwks() -> dict:
    jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
    response = requests.get(jwks_url, timeout=10)
    response.raise_for_status()
    return response.json()


def verify_token(token: str) -> dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
        jwks = get_jwks()

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Unable to find appropriate key")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.auth0_audience,
            issuer=settings.auth0_issuer,
        )
        return payload

    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> dict:
    return verify_token(credentials.credentials)