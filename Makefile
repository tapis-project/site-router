# build the images
build:
	docker build -f Dockerfile-api -t tapis/site-router-api .

# start up the local development stack
up: build
	docker-compose up -d

# remove all running containers
clean:
	docker-compose down

# remove all existing containers and rebuild and restart the development stack
all: clean up

# run the tests -- this requires that the stack is up because the db is required
test: up
	docker-compose run tests

# tag and push the dev image to docker hub; does NOT first build the image in case there are pending 
# changes that should not be pushed.
push-dev:
	docker tag tapis/site-router-api tapis/site-router-api:dev; docker push tapis/site-router-api:dev