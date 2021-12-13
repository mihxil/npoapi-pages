docker:
	docker build -t mihxil/npoapi-pages .

docker-run:
	docker run --env secret=${secret} -p 5000:5000  mihxil/npoapi-pages

run:
	FLASK_ENV=development configdir=$(pwd) flask run
