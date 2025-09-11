import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from dotenv import load_dotenv

load_dotenv()


class Auth:
    """
    Service d'authentification:
    - hachage / vérification de mot de passe (bcrypt)
    - création / décodage de JWT RS256
    - dépendance FastAPI pour récupérer l'utilisateur courant
    """

    def __init__(self) -> None:
        with open(os.getenv("PATH_PUBLIC_KEY"), "r") as f:
            self.PUBLIC_KEY = f.read()

        self.ALGORITHM = "RS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))

    def decodeToken(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.PUBLIC_KEY, algorithms=[self.ALGORITHM])
            id = payload.get("id")
            if id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def getCurrentUser(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/customer/login"))) -> dict:
        """
        Dépendance FastAPI : extrait et valide le token,
        retourne le payload (ou une erreur 401 si invalide).
        """
        return self.decodeToken(token)