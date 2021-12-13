docker:
	docker build -t mihxil/npoapi-pages .

docker-run:
	docker run --env secret=${secret} --env profile=vpro -p 5000:5000  mihxil/npoapi-pages

run:
	FLASK_ENV=development configdir=$(pwd) profile=vpro flask run
