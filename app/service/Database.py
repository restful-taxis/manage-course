import os
from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine unique au module avec pool (les connexions sont réutilisées)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

# Fabrique de sessions et registre "scopé" (une session par thread worker)
_SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
SessionRegistry = scoped_session(_SessionFactory)

Base = declarative_base()


class Database:
    """
    Fournit des utilitaires d'accès à la base.

    Bonnes pratiques:
    - Engine: singleton module + pool (déjà réutilisé).
    - Session: une par unité de travail / requête. On utilise scoped_session
      pour éviter un singleton global dangereux; on obtient une "session par thread".
    """

    @staticmethod
    def get_session() -> Session:
        """
        Retourne la session courante (scopée au thread).
        Si elle n'existe pas encore, elle est créée par le registre.
        """
        return SessionRegistry()

    @staticmethod
    def remove_session() -> None:
        """
        Détache/ferme la session 'courante' du registre (à appeler en fin de requête).
        """
        SessionRegistry.remove()

    @staticmethod
    def getInstance() -> Generator[Session, None, None]:
        """
        Générateur de session (compatible FastAPI Depends).
        Utilise le registre pour avoir une session par requête/thread.
        """
        db = Database.get_session()
        try:
            yield db
        finally:
            Database.remove_session()

    @staticmethod
    @contextmanager
    def session() -> Generator[Session, None, None]:
        """
        Context manager pratique s'appuyant sur le registre:
            with Database.session() as db: ...
        """
        db = Database.get_session()
        try:
            yield db
        finally:
            Database.remove_session()

    @staticmethod
    def with_session(func):
        """
        Décorateur qui injecte la Session 'db' et gère son cycle de vie
        uniquement si aucune session n'a été fournie par l'appelant.

        Usage:
            @Database.with_session
            def my_method(self, db, arg1, ...): ...
        """
        def _wrapper(*args, **kwargs):
            if "db" in kwargs and kwargs["db"] is not None:
                # Une session est déjà fournie (ex: appel imbriqué): ne pas gérer le cycle de vie ici
                return func(*args, **kwargs)
            db = Database.get_session()
            try:
                kwargs["db"] = db
                return func(*args, **kwargs)
            finally:
                Database.remove_session()
        return _wrapper

    @staticmethod
    def get_engine():
        """Accès à l'engine unique du module."""
        return engine
