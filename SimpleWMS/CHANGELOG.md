# [1.1.0] (2025-01-01)

### Added

- **Filtrage des salles**: Filtre par disponibilité avec `GET /salles?disponible=true/false`.
- **Suppression de réservations**: Endpoint `DELETE /reservations/{id}`.
- **Commentaires**: Ajout d'un champ commentaire optionnel aux réservations.
- **Disponibilité des salles**: Champ booléen `disponible` pour marquer les salles hors service.

### Fixed

- Validation renforcée des créneaux de réservation.

---

# [1.0.0] (2025-01-01)

### Added

- **Gestion des salles**: Création, consultation, modification et suppression des salles.
- **Système de réservations**: Réservation de créneaux d'1h avec validation des conflits.
- **Contraintes métier**: Prévention des doubles réservations sur un même créneau.
- **API REST complète**: Endpoints CRUD pour salles et réservations.
- **Base de données**: Schéma SQLite avec migrations Alembic.
- **Documentation**: Interface Swagger automatique.

### Initial Release

Premier MVP du système de réservation de salles avec fonctionnalités de base.