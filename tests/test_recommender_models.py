from pandas import DataFrame

from api.schemas.enums import RecommenderType
from src import RatingBasedRecommender, OpenRateBasedRecommender, BaseRecommender


def test_setting_instance_id_open_rate_recommender():
    recommender = OpenRateBasedRecommender(1)

    assert recommender.instance_id == 1


def test_setting_instance_id_rating_recommender():
    recommender = RatingBasedRecommender(1)

    assert recommender.instance_id == 1


def test_setting_instance_id_random_recommender():
    recommender = BaseRecommender(1)

    assert recommender.instance_id == 1


def test_rating_recommender_type():
    recommender = RatingBasedRecommender(1)

    assert recommender.type == RecommenderType.rating


def test_open_rate_recommender_type():
    recommender = OpenRateBasedRecommender(1)

    assert recommender.type == RecommenderType.open_rate


def test_random_recommender_type():
    recommender = BaseRecommender(1)

    assert recommender.type == RecommenderType.random


def test_feedback_sample(articles_df):
    recommender = RatingBasedRecommender(1)

    sample_df = recommender.sample(df=articles_df, n=1, repeated=False)
    assert isinstance(sample_df, DataFrame)


def test_random_sample(articles_df):
    recommender = BaseRecommender(1)

    sample_df = recommender.sample(df=articles_df, n=1, repeated=False)
    assert isinstance(sample_df, DataFrame)


def test_open_rate_sample(articles_df):
    recommender = OpenRateBasedRecommender(1)

    sample_df = recommender.sample(df=articles_df, n=1, repeated=False)
    assert isinstance(sample_df, DataFrame)



"""
def test_open_rate_model_rated_articles_gets_df(populate_db, engine):
    recommender = OpenRateBasedRecommender(1)
    rated_articles = recommender.rated_articles(engine)

    assert isinstance(rated_articles, DataFrame)


def test_rating_model_rated_articles_gets_df(populate_db, engine):
    recommender = RatingBasedRecommender(1)
    rated_articles = recommender.rated_articles(engine)

    assert isinstance(rated_articles, DataFrame)


def test_rating_model_get_sample(populate_db, engine):
    recommender = RatingBasedRecommender(1)
    rated_articles = recommender.rated_articles(engine)

    sample = recommender.sample(rated_articles, 2)
    assert isinstance(sample, DataFrame)


def test_open_rate_model_get_sample(populate_db, engine):
    recommender = OpenRateBasedRecommender(1)
    rated_articles = recommender.rated_articles(engine)

    sample = recommender.sample(rated_articles, 2)
    assert isinstance(sample, DataFrame)
"""