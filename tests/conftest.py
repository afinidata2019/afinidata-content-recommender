import pandas as pd
import pytest

from api import get_app
from api.core.db import get_engine
from tests.db import override_db_dependencies, override_get_engine


@pytest.fixture(scope='session')
def app():
    app = get_app()
    yield app


@pytest.fixture(scope='session', autouse=True)
def overrride_database(app):
    override_db_dependencies(app, get_engine)


@pytest.fixture(scope='session')
def articles_df():
    columns = [
        'id',
        'name',
        'content',
        'text_content',
        'min',
        'max',
        'preview',
        'thumbnail',
        'created_at',
        'updated_at',
        'status',
        'is_opened',
        'metric',
        'in_weeks'
    ]

    row = [
        [1, 'article', 'content', 'text_content', '-10', '-40', 'preview', 'thumbnail', '2020-01-01', '2020-01-01',
         'published', False, 1., True],
        [2, 'article', 'content', 'text_content', '-10', '-40', 'preview', 'thumbnail', '2020-01-01', '2020-01-01',
         'published', True, 1., True]
    ]

    return pd.DataFrame(columns=columns, data=row)
