from typing import List

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.engine import Engine

from api import schemas
from api.core.db import get_engine
from api.schemas.enums import RecommenderType
from src import OpenRateBasedRecommender, RatingBasedRecommender


router = APIRouter()


@router.get('/pregnancy/{instance_id}/popularity', response_model=List[schemas.Article])
async def get_popularity_recommendation(
        instance_id: int = Path(..., description='Instance `id`'),
        n: int = Query(1, description='Number of articles'),
        type_: RecommenderType = Query(..., alias='type', description='Recommender type'),
        engine: Engine = Depends(get_engine),
):
    recommender_models = {
        RecommenderType.rating: RatingBasedRecommender,
        RecommenderType.open_rate: OpenRateBasedRecommender
    }

    model = recommender_models[type_]
    recommender = model(instance_id=instance_id)
    articles_df = recommender.rated_articles(engine=engine)

    return recommender.sample(df=articles_df, n=n).to_dict(orient='records')
