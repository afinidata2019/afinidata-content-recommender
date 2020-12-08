from fastapi import FastAPI

from api.custom.openapi import custom_openapi
from api.endpoints import router
from api.core.config import get_settings


def get_app() -> FastAPI:

    # inspired from https://github.com/tiangolo/fastapi/issues/508#issuecomment-532368194
    settings = get_settings()  # see example above

    server = FastAPI(title=settings.project_name,
                     openapi_url=settings.openapi_route,
                     debug=settings.DEBUG,
                     docs_url=settings.docs_url,
                     redoc_url=settings.redoc_url)

    server.include_router(router, prefix=f'{settings.api_v1_route}')

    server.openapi_schema = custom_openapi(server, settings)

    return server
