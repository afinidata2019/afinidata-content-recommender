import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from api.custom.exceptions import InvalidInstanceType
from api.schemas.enums import RecommenderType


class RatingBasedRecommender(object):
    def __init__(self, instance_id: int):
        self.instance_id = instance_id
        self.type = RecommenderType.rating

    _sql = """
        WITH articles AS (
            SELECT aa.*, usst.name AS type
            FROM articles_article aa
            JOIN user_sessions_sessiontype usst ON usst.id=aa.type_id
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
        ), relevant_feedback AS (
            SELECT *
            FROM articles_articlefeedback
            WHERE article_id IN (SELECT id FROM articles)
        ), ratings AS (
            SELECT article_id,
            AVG(value) as metric,
            COUNT(id) as feedback_count
            FROM relevant_feedback
            GROUP BY article_id
        ), rated_unread AS (
        SELECT unread_articles.*,
               IFNULL(ratings.metric, (SELECT AVG(value) FROM relevant_feedback)) AS metric,
               IFNULL(ratings.feedback_count, 0) AS feedback_count,
               CASE WHEN pd.weeks > unread_articles.min AND pd.weeks < unread_articles.max THEN TRUE ELSE FALSE END AS in_weeks
        FROM unread_articles
        LEFT JOIN ratings ON unread_articles.id=ratings.article_id
        LEFT JOIN pregnancy_data pd ON pd.instance_id=:instance_id
        )
        SELECT *
        FROM rated_unread
        ORDER BY metric DESC;
    """

    def _query(self):
        return text(self._sql).bindparams(instance_id=self.instance_id)

    def rated_articles(self, engine: Engine):
        df = pd.read_sql(sql=self._query(), con=engine)
        df['is_opened'] = df['is_opened'].astype('bool')
        df['in_weeks'] = df['in_weeks'].astype('bool')

        df_in_weeks = df[df['in_weeks']]
        if len(df_in_weeks.index) == 0:
            raise InvalidInstanceType('There are no pregnancy articles for this instance')

        return df_in_weeks

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
