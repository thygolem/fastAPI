from fastapi import FastAPI
from routes.user import user
from docs import tags_metadata

app = FastAPI(
    title='SISTEMAS DE LOCALIZACIÓN EN INTERIORES',
    description='C# debe obtener información de esta API',
    version='1.0.0',
    openapi_tags=tags_metadata
)

app.include_router(user)


