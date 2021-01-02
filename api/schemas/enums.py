from enum import Enum


class RecommenderType(Enum):
    rating = 'rating'
    open_rate = 'open_rate'
    random = 'random'
