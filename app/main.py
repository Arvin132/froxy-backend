from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import analysis_router, auth_router
from lifespan import lifespan, documents_uploaded
from dotenv import load_dotenv
import database

import os

load_dotenv()

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Froxy Backend",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix="/api/analysis", tags=["analysis"])
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Hello World", "document_uplosded": documents_uploaded}

