build_dev:
		docker compose build server-dev couchserver
		docker compose build app

build_prod:
		docker compose build server-prod couchserver

run_dev:
		docker compose up server-dev app


run_prod:
		docker compose up server-prod

clean:
		docker rm healthtracks-server-dev -f
		docker rm healthtracks-server-prod -f
		docker rmi healthtracks-server-dev
		docker rmi healthtracks-server-prod
		docker rm healthtracks-app -f
		docker rmi healthtracks-app
