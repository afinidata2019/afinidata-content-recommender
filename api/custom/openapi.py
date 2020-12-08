from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api.core.config import ConfigClass


def custom_openapi(server: FastAPI, settings: ConfigClass):
    if server.openapi_schema:
        return server.openapi_schema

    openapi_schema = get_openapi(
        title=settings.project_name,
        version="0.1.0",
        description=settings.project_description,
        routes=server.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        'url': 'https://afinidata.com/wp-content/uploads/2020/01/LogoAfinidata.png'
    }
    server.openapi_schema = openapi_schema
    return server.openapi_schema
