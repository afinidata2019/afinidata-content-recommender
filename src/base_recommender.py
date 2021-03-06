from typing import List

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from api.custom.exceptions import InvalidInstanceType
from api.schemas.enums import RecommenderType


class BaseRecommender(object):
    type = RecommenderType.random

    def __init__(self, instance_id: int):
        self.instance_id = instance_id

    _sql = """
        WITH articles AS (
            SELECT aa.*, usst.name AS type
            FROM articles_article aa
            LEFT JOIN user_sessions_sessiontype usst ON usst.id=aa.type_id
            WHERE min < 0 AND status='published'
        ), unread_articles AS (
            SELECT *,
                CASE
                    WHEN id IN (
                        SELECT article_id FROM articles_interaction WHERE instance_id=:instance_id AND type='open'
                    ) THEN TRUE
                    ELSE FALSE
                END AS is_opened
            FROM articles
        ), pregnancy_data AS (
            SELECT iav.instance_id, iav.value - FLOOR(DATEDIFF(CURDATE(), iav.created_at)/7) AS weeks
            FROM instances_attributevalue iav
            JOIN attributes_attribute aa ON aa.id=iav.attribute_id
            WHERE aa.name='pregnant_weeks' AND iav.instance_id=:instance_id
        )
        SELECT unread_articles.*, 
               1 as metric,
               CASE WHEN pd.weeks > unread_articles.min AND pd.weeks < unread_articles.max THEN TRUE ELSE FALSE END AS in_weeks
        FROM unread_articles
        LEFT JOIN pregnancy_data pd ON pd.instance_id=:instance_id

        ORDER BY metric DESC;
    """

    def _query(self):
        return text(self._sql).bindparams(instance_id=self.instance_id)

    def rated_articles(
            self,
            engine: Engine,
            include_only_type: List[str] = None,
            exclude_type: List[str] = None,
    ):
        df = pd.read_sql(sql=self._query(), con=engine)
        df['is_opened'] = df['is_opened'].astype('bool')
        df['in_weeks'] = df['in_weeks'].astype('bool')

        df = df[df['in_weeks']]
        if len(df.index) == 0:
            raise InvalidInstanceType('There are no pregnancy articles for this instance')

        if include_only_type is not None:
            df = df[df['type'].isin(include_only_type)]

        if exclude_type is not None:
            df = df[~df['type'].isin(exclude_type)]

        return df

    def sample(self, df: pd.DataFrame, n: int = 1, repeated: bool = False):
        if not repeated:
            df = df[~df['is_opened']]

        size = min(n, len(df.index))

        return df.sample(n=size)
