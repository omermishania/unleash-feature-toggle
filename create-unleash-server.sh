# Create a network
docker network create unleash

# Start a postgres database
docker run -d -e POSTGRES_PASSWORD=some_password -e POSTGRES_USER=unleash_user -e POSTGRES_DB=unleash --network unleash --name postgres postgres

# Start Unleash via docker
docker run -d -p 4242:4242 -e DATABASE_HOST=postgres -e DATABASE_NAME=unleash -e DATABASE_USERNAME=unleash_user -e DATABASE_PASSWORD=some_password -e DATABASE_SSL=false --network unleash --name unleash unleashorg/unleash-server
