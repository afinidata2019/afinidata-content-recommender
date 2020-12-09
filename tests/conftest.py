from fastapi.testclient import TestClient
import pytest
from sqlalchemy import text

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
def engine():
    engine = override_get_engine()
    return engine


@pytest.fixture(scope='session')
def setup_database(engine):
    drop_articles_table_sql = "DROP TABLE IF EXISTS articles_article;"
    drop_interaction_table_sql = "DROP TABLE IF EXISTS articles_interaction;"
    drop_articlefeedback_table_sql = "DROP TABLE IF EXISTS articles_articlefeedback;"

    create_articles_table_sql = """
        CREATE TABLE articles_article (
            id int(11) PRIMARY KEY,
            min int(11) DEFAULT NULL,
            max int(11) DEFAULT NULL,
            user_id int(11) DEFAULT NULL,
            status varchar(255) NOT NULL
        );
    """
    create_interaction_table_sql = """
        CREATE TABLE articles_interaction (
            id int(11) PRIMARY KEY,
            user_id int(11) NOT NULL,
            type varchar(255) NOT NULL,
            article_id int(11) DEFAULT NULL,
            instance_id int(11) DEFAULT NULL,
            value int(11) DEFAULT NULL
        );
    """
    create_articlefeedback_table_sql = """
        CREATE TABLE articles_articlefeedback (
            id int(11) PRIMARY KEY,
            value int(11) NOT NULL,
            article_id int(11) NOT NULL,
            user_id int(11) DEFAULT NULL
        );
    """

    with engine.connect() as con:
        con.execute(text(drop_articles_table_sql))
        con.execute(text(drop_interaction_table_sql))
        con.execute(text(drop_articlefeedback_table_sql))
        con.execute(text(create_articles_table_sql))
        con.execute(text(create_interaction_table_sql))
        con.execute(text(create_articlefeedback_table_sql))


@pytest.fixture(scope='session')
def populate_db(setup_database, engine):
    populate_article_table_sql = """
        INSERT INTO articles_article (id, min, max, user_id, status)
        VALUES (1, -10,  0, 1, 'published'),
               (2,   1,  2, 1, 'draft'),
               (3, -10, -5, 1, 'draft');
    """
    populate_interaction_table_sql = """
        INSERT INTO articles_interaction (id, user_id, type, article_id, instance_id, value)
        VALUES (1, 1, 'dispatched', 1, 1, 0),
               (2, 1, 'open', 1, 1, 0);
    """
    populate_articlefeedback_table_sql = """
        INSERT INTO articles_articlefeedback (id, value, article_id, user_id)
        VALUES (1, 5, 1, 1);
    """

    with engine.connect() as con:
        con.execute(text(populate_article_table_sql))
        con.execute(text(populate_interaction_table_sql))
        con.execute(text(populate_articlefeedback_table_sql))


@pytest.fixture(scope='module')
def client(app):
    client = TestClient(app=app)
    yield client
