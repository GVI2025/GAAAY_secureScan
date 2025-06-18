from fastapi import FastAPI

from app.routers import article, agent, emplacement, commande, implantation, reception, mission, salle, reservation

app = FastAPI(
    title="Système de réservation de salles",
    description="API REST pour la gestion des réservations de salles et équipements",
    version="1.0.0",
)

# WMS routers (legacy)
app.include_router(article.router)
app.include_router(agent.router)
app.include_router(emplacement.router)
app.include_router(commande.router)
app.include_router(implantation.router)
app.include_router(reception.router)
app.include_router(mission.router)

# New reservation system routers
app.include_router(salle.router)
app.include_router(reservation.router)

@app.get("/")
async def root():
    return {"message": "Bienvenue dans le système de réservation de salles!"}