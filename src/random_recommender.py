import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from api.schemas.enums import RecommenderType


class RandomRecommender(object):
    def __init__(self, instance_id: int):
        self.instance_id = instance_id
        self.type = RecommenderType.random

    _sql = """
        WITH articles AS (
            SELECT *
            FROM articles_article
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
        )
        SELECT unread_articles.*, 1 as metric
        FROM unread_articles
        ORDER BY metric DESC;
    """

    def _query(self):
        return text(self._sql).bindparams(instance_id=self.instance_id)

    def rated_articles(self, engine: Engine):
        df = pd.read_sql(sql=self._query(), con=engine)
        df['is_opened'] = df['is_opened'].astype('bool')
        return df

    def sample(self, df: pd.DataFrame, n: int = 1, repeated: bool = False):
        if not repeated:
            df = df[~df['is_opened']]

        size = min(n, len(df.index))

        return df.sample(n=size)
