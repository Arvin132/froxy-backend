from contextlib import asynccontextmanager
from moorcheh_sdk import MoorchehClient
from fastapi import FastAPI
import os

documents_uploaded = False

async def upload_document(app):
    client: MoorchehClient = app.state.m_client
    namespaces: list = client.list_namespaces()['namespaces']
    found = None
    for name in namespaces:
        if name['namespace_name'] == "scam_detection":
            found = name
    
    if found is None:
        client.create_namespace('scam_detection', type='text')
    
    if os.environ.get("UPLOAD") == "T":
        # upload document
        pass
    
        
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler - runs on startup and shutdown
    """
    print("Application starting up...")
    app.state.m_client = MoorchehClient(os.environ.get("MOORCHEH_KEY"))
    await upload_document(app)
    yield
    print("Application shutting down...")