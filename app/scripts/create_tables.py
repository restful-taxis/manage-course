"""
Script de création automatique des tables.

Exécution:
    python -m app.scripts.create_tables
ou:
    python app/scripts/create_tables.py  (si PYTHONPATH inclut la racine)

Le script:
- charge les variables d'environnement (via app.service.database),
- importe dynamiquement tous les modèles sous app.models,
- appelle Base.metadata.create_all(bind=engine).
"""
import importlib
import pkgutil

import app.models as models_pkg
from app.service.Database import Base, engine


def import_all_models() -> None:
    """
    Importe récursivement tous les modules du package app.models
    afin d'enregistrer toutes les classes déclaratives auprès du metadata.
    """
    prefix = models_pkg.__name__ + "."
    for _finder, name, _ispkg in pkgutil.walk_packages(models_pkg.__path__, prefix):
        importlib.import_module(name)


def main() -> None:
    # S'assurer que toutes les tables des modèles sont enregistrées
    import_all_models()
    # Création idempotente des tables
    Base.metadata.create_all(bind=engine)
    print("Tables créées (si absentes).")


if __name__ == "__main__":
    main()
