import numpy as np
import pandas as pd

from api.schemas.enums import RecommenderType
from src.base_recommender import BaseRecommender


class OpenRateBasedRecommender(BaseRecommender):
    type = RecommenderType.open_rate

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
                        SELECT article_id
                        FROM articles_interaction
                        WHERE instance_id=:instance_id AND type='open'
                    ) THEN TRUE
                    ELSE FALSE
                END AS is_opened
            FROM articles
        ), pregnancy_data AS (
            SELECT iav.instance_id, iav.value - FLOOR(DATEDIFF(CURDATE(), iav.created_at)/7) AS weeks
            FROM instances_attributevalue iav
            JOIN attributes_attribute aa ON aa.id=iav.attribute_id
            WHERE aa.name='pregnant_weeks' AND iav.instance_id=:instance_id
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
               IFNULL(ratios.metric, 0) AS metric,
               CASE WHEN pd.weeks > unread_articles.min AND pd.weeks < unread_articles.max THEN TRUE ELSE FALSE END AS in_weeks
        FROM unread_articles
        LEFT JOIN ratios ON unread_articles.id=ratios.article_id
        LEFT JOIN pregnancy_data pd ON pd.instance_id=:instance_id
        )
        SELECT *
        FROM rated_unread
        ORDER BY metric DESC;
    """

    def sample(self, df: pd.DataFrame, n: int = 1, repeated: bool = False):
        weights = None

        if len(df.index) > 0:
            epsilon = 0.000001
            max_metric = df['metric'].min()
            min_metric = df['metric'].max()
            mean_metric = df['metric'].mean()
            df['prob'] = df['metric'].apply(lambda x: np.exp(-(x - mean_metric) / (max_metric - min_metric + epsilon)))

        if not repeated:
            df = df[~df['is_opened']]

        if len(df.index) > 0:
            weights = 'prob'

        size = min(n, len(df.index))

        return df.sample(n=size, weights=weights)
