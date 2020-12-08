from pandas import DataFrame
from sqlalchemy import text

from api.schemas.enums import RecommenderType
from src import RatingBasedRecommender, OpenRateBasedRecommender


def test_setting_instance_id_open_rate_recommender():
    recommender = OpenRateBasedRecommender(1)

    assert recommender.instance_id == 1


def test_setting_instance_id_rating_recommender():
    recommender = RatingBasedRecommender(1)

    assert recommender.instance_id == 1


def test_rating_recommender_type():
    recommender = RatingBasedRecommender(1)

    assert recommender.type == RecommenderType.rating


def test_open_rate_recommender_type():
    recommender = OpenRateBasedRecommender(1)

    assert recommender.type == RecommenderType.open_rate


def test_open_rate_model_rated_articles_gets_df(populate_db, engine, monkeypatch):
    def mock_query(*args, **kwargs):
        _sql = """
            SELECT * FROM articles_article;
        """
        return text(_sql)

    recommender = OpenRateBasedRecommender(1)
    monkeypatch.setattr(recommender, '_query', mock_query)
    rated_articles = recommender.rated_articles(engine)

    assert isinstance(rated_articles, DataFrame)


def test_rating_model_rated_articles_gets_df(populate_db, engine, monkeypatch):
    def mock_query(*args, **kwargs):
        _sql = """
            SELECT * FROM articles_article;
        """
        return text(_sql)

    recommender = RatingBasedRecommender(1)
    monkeypatch.setattr(recommender, '_query', mock_query)
    rated_articles = recommender.rated_articles(engine)

    assert isinstance(rated_articles, DataFrame)
