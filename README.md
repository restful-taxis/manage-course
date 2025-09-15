# Configuration

## Exemple de fichier `.env`

```dotenv
DATABASE_URL=postgresql://main:main@coursedb:5432/main
ACCESS_TOKEN_EXPIRE_MINUTES=60
PATH_PUBLIC_KEY=jwt/public.pem
```

Avec : 
- `coursedb` : nom du conteneneur DB
- `public.pem` : clé publique utilisée par les micro-services `driver` et `customer`

# créer les tables : 
```bash
python -m app.scripts.create_tables
```

# Routes disponibles

## Gestion des courses

### `POST /course/create`

**Description**: Crée une nouvelle course

**Permissions**: Utilisateurs avec le rôle customer

**Body**:
```json
{
  "point_depart": "string",
  "point_arrivee": "string"
}
```

**Réponse**: Retourne les détails de la course créée avec statut `demandée`

### `POST /course/{id}/confirm`

**Description**: Confirme une course (chauffeur accepte la course)

**Permissions**: Utilisateurs avec le rôle `driver`

**Path Parameters**:

- `id`: UUID de la course

**Réponse**: Retourne la course mise à jour avec statut validée et chauffeur_id assigné

### `POST /course/{id}/cancel`

**Description**: Annule une course

**Permissions**: Utilisateurs avec le rôle `customer` (uniquement leurs propres courses)

**Path Parameters**:

- `id`: UUID de la course

**Conditions**: La course doit avoir le statut `demandée`

**Réponse**: Retourne la course mise à jour avec statut annulée

### `POST /course/{id}/start`

**Description**: Démarre une course

**Permissions**: Utilisateurs avec le rôle `driver` (uniquement les courses qui leur sont assignées)

**Path Parameters**:

- `id`: UUID de la course

**Conditions**: La course doit avoir le statut `validée`

**Réponse**: Retourne la course mise à jour avec statut `en cours` et `date_heure_depart` remplie

### `POST /course/{id}/end`

**Description**: Termine une course et calcule le tarif

**Permissions**: Utilisateurs avec le rôle `driver` (uniquement les courses qui leur sont assignées)

**Path Parameters**:

- `id`: UUID de la course

**Conditions**: La course doit avoir le statut `en cours`

**Réponse**: Retourne la course mise à jour avec statut terminée, date_heure_arrivee remplie et tarif calculé

## Consultation des courses

### `GET /course/my`

**Description**: Récupère toutes les courses de l'utilisateur connecté

**Permissions**: Utilisateurs avec le rôle `customer` ou `driver`

**Réponse**: Liste des courses où l'utilisateur est client ou chauffeur, triées par date de modification (récentes first)

### `GET /course/pending`

**Description**: Récupère toutes les courses en attente (statut "demandée")

**Permissions**: Utilisateurs avec le rôle `driver`

**Réponse**: Liste des courses disponibles pour acceptation, triées par date de modification (récentes first)
