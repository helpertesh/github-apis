from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gigs",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to GigHub API",
        "documentation": "/docs"
    }


# ==========================
# In-memory Database
# ==========================

gigs_db = [
    {
        "id": 1,
        "title": "Build React Dashboard",
        "description": "Develop a responsive React dashboard for a fintech startup.",
        "category": "Development",
        "budget": 1200.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Design Company Logo",
        "description": "Create a modern logo for a software company.",
        "category": "Design",
        "budget": 400.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Peter Kamau"
    },
    {
        "id": 3,
        "title": "Write Tech Articles",
        "description": "Write five SEO-friendly cloud computing articles.",
        "category": "Writing",
        "budget": 550.0,
        "currency": "USD",
        "status": "In Progress",
        "client_name": "Grace Wanjiku"
    },
    {
        "id": 4,
        "title": "FastAPI Backend",
        "description": "Develop a REST API using FastAPI.",
        "category": "Development",
        "budget": 1800.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Brian Otieno"
    },
    {
        "id": 5,
        "title": "Mobile App UI",
        "description": "Design mobile screens for an e-learning platform.",
        "category": "Design",
        "budget": 900.0,
        "currency": "USD",
        "status": "Closed",
        "client_name": "Faith Achieng"
    },
    {
        "id": 6,
        "title": "Technical Documentation",
        "description": "Prepare documentation for an inventory system.",
        "category": "Writing",
        "budget": 650.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "David Mwangi"
    },
    {
        "id": 7,
        "title": "Portfolio Website",
        "description": "Develop a portfolio website for a photographer.",
        "category": "Development",
        "budget": 1000.0,
        "currency": "USD",
        "status": "In Progress",
        "client_name": "Mercy Njeri"
    }
]


# ==========================
# Models
# ==========================

class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=500)
    category: Literal["Development", "Design", "Writing"]
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None


# ==========================
# GET ALL GIGS
# ==========================

@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):

    results = gigs_db

    if category:
        results = [
            gig for gig in results
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] <= max_budget
        ]

    return results


# ==========================
# SEARCH GIGS
# ==========================

@app.get("/gigs/search")
def search_gigs(q: str):

    results = []

    for gig in gigs_db:
        if (
            q.lower() in gig["title"].lower()
            or q.lower() in gig["description"].lower()
        ):
            results.append(gig)

    return results


# ==========================
# GET GIG BY ID
# ==========================

@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):

    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


# ==========================
# CREATE GIG
# ==========================

@app.post("/gigs")
def create_gig(gig: GigCreate):

    new_id = max(g["id"] for g in gigs_db) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "USD",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }


# ==========================
# UPDATE GIG
# ==========================

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):

    for gig in gigs_db:

        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gig["budget"] = gig_update.budget

            if gig_update.status is not None:
                gig["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")


# ==========================
# DELETE GIG
# ==========================

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")