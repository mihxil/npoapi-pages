#URL:=openshift-image-registry.apps.cluster.chp4.io/poms-plus/npoapi-pages:latest
URL:=mihxil/npoapi-pages:latest
#URL:=docker.vpro.nl/mihxil/npoapi-pages:latest
PROFILE:=vpro

docker:
	docker build -t $(URL) .

docker-run:
	docker run --env secret=${secret} --env profile=$(PROFILE) -p 8080:8080  $(URL)


docker-push: docker
	docker 	push $(URL)

run:
	FLASK_ENV=development configdir=$(pwd) profile=$(PROFILE) flask run

waitress:
	configdir=$(pwd) profile=$(PROFILE) waitress-serve app:app

