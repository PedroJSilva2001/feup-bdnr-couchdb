build_dev:
		docker compose build server-dev couchserver

build_prod:
		docker compose build server-prod couchserver

run_dev:
		docker compose up server-dev


run_prod:
		docker compose up server-prod

clean:
		docker rm healthtracks-server-dev -f
		docker rm healthtracks-server-prod -f
		docker rmi healthtracks-server-dev
		docker rmi healthtracks-server-prod
