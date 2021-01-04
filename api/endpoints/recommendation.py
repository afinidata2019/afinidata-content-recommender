from typing import List

from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.engine import Engine

from api import schemas
from api.core.db import get_engine
from api.custom.exceptions import InvalidInstanceType
from api.schemas.enums import RecommenderType
from src import OpenRateBasedRecommender, RatingBasedRecommender, RandomRecommender


router = APIRouter()


@router.get('/pregnancy/{instance_id}/popularity', response_model=List[schemas.Article])
async def get_popularity_recommendation(
        instance_id: int = Path(..., description='Instance `id`'),
        n: int = Query(1, description='Number of articles'),
        type_: RecommenderType = Query(..., alias='type', description='Recommender type'),
        repeated: bool = Query(False, description='Repeat activities'),
        engine: Engine = Depends(get_engine),
):
    recommender_models = {
        RecommenderType.rating: RatingBasedRecommender,
        RecommenderType.open_rate: OpenRateBasedRecommender,
        RecommenderType.random: RandomRecommender
    }

    model = recommender_models[type_]
    recommender = model(instance_id=instance_id)
    try:
        articles_df = recommender.rated_articles(engine=engine)
    except InvalidInstanceType as e:
        raise HTTPException(status_code=422, detail=e.message)

    return recommender.sample(df=articles_df, n=n, repeated=repeated).to_dict(orient='records')
