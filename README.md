# Afinidata recommender service

![Tests](https://github.com/afinidata2019/afinidata-content-recommender/workflows/Recommender%20service%20CI/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/afinidata2019/afinidata-content-recommender/branch/master/graph/badge.svg?token=SBRPQ8OMJE)](https://codecov.io/gh/afinidata2019/afinidata-content-recommender)

## Overview

Afinidata recommender engine for articles for pregnant women. The logic for the recommendations is straightforward:
1. an API call is made requesting a number of articles for a pregnant woman,
2. the pool of articles suitable for her pregnancy weeks is selected,
3. a probability distribution is determined over the articles in the resulting pool,
4. articles are sampled according to this probability distribution,
5. articles are delivered according to some schema.

The logic in the recommendation lies primarily in the probability distribution mentioned above. Currently, we support:
1. totally random recommendation,
2. popularity based on historical open-rate (ratio of times an article was opened with respect the article was delivered),
3. popularity based on mean feedback.

The API documentation (URL, parameters and response schemas) is found in [here](https://analytics.afinidata.com/redoc/recommender).

## Running
To run the recommender, you must have `Docker` and `docker-compose` installed. Then, you can run the project with:
```shell
git clone https://github.com/afinidata2019/afinidata-content-recommender.git
cd afinidata-content-recommender
docker-compose up -d
```


## Contributing

The Afinidata Content Manager is a Free Software Product created by Afinidata and available under the AGPL Licence. 

To contribute, read our [Code of Conduct](CODE_OF_CONDUCT.md), our [documentation](https://analytics.afinidata.com/redoc/recommender) and code away.
Create a pull request and contact us in order to merge your suggested changes. We suggest the use of git flow in order to provide a better contributing experience.


