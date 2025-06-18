# Système de réservation de salles

Une API REST pour la gestion des réservations de salles et équipements, construite avec FastAPI et SQLAlchemy.

## 🧱 Fonctionnalités

### MVP v1.0.0
* Gestion des salles (création, consultation, modification, suppression)
* Réservation de créneaux horaires (1h fixe)
* Contrainte métier : pas de double réservation sur un même créneau

### v1.1.0
* Filtrage des salles par disponibilité
* Ajout de commentaires aux réservations
* Suppression de réservations
* Champ disponible pour les salles

## 🚀 Démarrage rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/GVI2025/GAAAY_secureScan
cd GAAAY_secureScan
```

### 2. Installer Poetry (si pas déjà installé)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Installer les dépendances

```bash
poetry install
```

### 4. Activer l'environnement virtuel

```bash
poetry shell
```

### 5. Configurer la base de données

**Option A - Script rapide (recommandé pour développement) :**
```bash
python create_tables.py
```

**Option B - Avec Alembic (pour production) :**
```bash
# Générer une nouvelle migration pour les tables salles et réservations
alembic revision --autogenerate -m "Add salles and reservations tables"

# Appliquer les migrations
alembic upgrade head
```

### 6. Données de test (optionnel)

```bash
python -m app.seed.seed_data
```

### 7. Lancer l'application

```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur : [http://localhost:8000](http://localhost:8000)
Documentation Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Tests

```bash
poetry run test
```

---

## 📁 Structure du projet

```
app/
├── routers/           # API routers
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── services/          # Business logic
├── database/          # DB session and engine
├── seed/              # Data seeding
├── main.py            # FastAPI app
alembic/               # Alembic migrations
tests/                 # Unit tests
```

---

## 📊 Modèles de données

### Salle
- **id**: UUID (PK)
- **nom**: string (unique)
- **capacite**: integer
- **localisation**: string
- **disponible**: boolean (v1.1.0)

### Réservation
- **id**: UUID (PK)
- **salle_id**: UUID (FK vers Salle)
- **date**: date
- **heure**: time
- **utilisateur**: string
- **commentaire**: string optionnel (v1.1.0)

---

## 🔧 Scripts

Ces scripts sont définis dans `pyproject.toml`:
* `poetry run test`: Exécuter les tests
* `poetry run migrate`: Appliquer les migrations Alembic

---

## 🐛 Résolution des problèmes

### Erreur "no such table"

Si vous obtenez l'erreur `no such table: salles` ou `no such table: reservations` :

**Solution rapide :**
```bash
python create_tables.py
```

**Solution avec Alembic :**
```bash
# Générer la migration
alembic revision --autogenerate -m "Add missing tables"

# Appliquer la migration
alembic upgrade head
```
