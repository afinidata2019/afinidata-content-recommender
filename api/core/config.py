from functools import lru_cache
import os
import random
import string
from typing import Union

from pydantic import BaseSettings, AnyUrl


class BaseConfig(BaseSettings):
    # inspired from https://github.com/tiangolo/fastapi/issues/508#issuecomment-532360198
    PRODUCTION: bool = os.getenv('PRODUCTION', False)

    project_name: str = "API for the recommender system"
    project_description: str = "Set of endpoints that manage several operations for the recommender system"
    project_prefix: str = 'recommender'
    api_v1_route: str = f"/api/v1/{project_prefix}"
    openapi_route: str = f"/api/v1/{project_prefix}/openapi.json"
    docs_url = f'/docs/{project_prefix}'
    redoc_url = f'/redoc/{project_prefix}'


class DevelopmentConfig(BaseConfig):
    DB_URI: AnyUrl = os.getenv('CONTENT_MANAGER_DB_URI',
                               'mysql://user:password@mysql:3306/content_manager')

    SECRET_KEY: str = 'dev'
    DEBUG: bool = True
    TESTING: bool = False


class ProductionConfig(BaseConfig):
    DB_URI: AnyUrl = os.getenv('CONTENT_MANAGER_DB_URI',
                               'mysql://user:password@mysql:3306/content_manager')

    def random_string(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    SECRET_KEY: str = random_string()
    DEBUG: bool = False
    TESTING: bool = False


ConfigClass = Union[DevelopmentConfig, ProductionConfig]


@lru_cache()
def get_settings() -> ConfigClass:
    prod = os.getenv('API_PRODUCTION', None)

    if prod:
        return ProductionConfig()
    else:
        return DevelopmentConfig()
