build:
	docker-compose --file docker-compose.yml build --no-cache

status:
	## Show status of containers
	@docker-compose ps

stop:
	## Stop containers
	@docker-compose --file docker-compose.yml stop

clean:
	## Clean all data
	@docker-compose --file docker-compose.yml down

up:
	## Start all or c=<name> containers in foreground
	@docker-compose --file docker-compose.yml up $(c)

start:
	## Start all or c=<name> containers in background
	@docker-compose --file docker-compose.yml up -d $(c)

test:
	## Run tests
	@docker-compose --file docker-compose.yml run --rm recommender-service bash -c "pytest --cov=./ --cov-report=xml"


lint:
	## Lint code
	@docker-compose --file docker-compose.yml run --rm recommender-service bash -c "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics"