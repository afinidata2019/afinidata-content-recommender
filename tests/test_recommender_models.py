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

