import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from api.schemas.enums import RecommenderType


class OpenRateBasedRecommender(object):
    def __init__(self, instance_id: int):
        self.instance_id = instance_id
        self.type = RecommenderType.open_rate

    _sql = """
        WITH articles AS (
            SELECT * 
            FROM articles_article 
            WHERE min < 0 AND status='published'
        ), unread_articles AS (
            SELECT *, 
                CASE
                    WHEN id IN (SELECT article_id FROM articles_interaction WHERE instance_id=:instance_id AND type='open') THEN TRUE
                    ELSE FALSE
                END AS is_opened
            FROM articles
        ), relevant_interactions AS (
            SELECT * 
            FROM articles_interaction WHERE type IN ('dispatched', 'open') AND article_id IN (SELECT id FROM articles)
        ), ratios AS (
            SELECT article_id, 
                   SUM(CASE WHEN type='open' THEN 1 ELSE 0 END) / SUM(CASE WHEN type='dispatched' THEN 1 ELSE 0 END) as metric
            FROM relevant_interactions
            GROUP BY article_id
        ), rated_unread AS (
        SELECT unread_articles.*, 
               IFNULL(ratios.metric, 0) AS metric
        FROM unread_articles
        LEFT JOIN ratios ON unread_articles.id=ratios.article_id
        )
        SELECT * 
        FROM rated_unread
        ORDER BY metric DESC;
    """

    def _query(self):
        return text(self._sql).bindparams(user_id=self.instance_id)

    def rated_articles(self, engine: Engine):
        df = pd.read_sql(sql=self._query(), con=engine)
        return df

    def sample(self, df: pd.DataFrame, n: int = 1, repeated: bool = False):
        weights = None

        if len(df.index) > 0:
            max_metric = df['metric'].min()
            min_metric = df['metric'].max()
            mean_metric = df['metric'].mean()
            df['prob'] = df['metric'].apply(lambda x: np.exp(-(x - mean_metric) / (max_metric - min_metric)))
            weights = 'prob'

        if not repeated:
            df = df[df['is_opened']]

        return df.sample(n=n, weights=weights)
