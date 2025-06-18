"""
Script pour créer toutes les tables de la base de données
"""
from app.database.database import engine, Base

# Import tous les modèles pour qu'ils soient enregistrés
from app.models.article import Article
from app.models.agent import Agent
from app.models.commande import Commande, LigneCommande
from app.models.emplacement import Emplacement
from app.models.implantation import Implantation
from app.models.mission import Mission
from app.models.reception import Reception
from app.models.salle import Salle
from app.models.reservation import Reservation

if __name__ == "__main__":
    print("Création de toutes les tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès!")
