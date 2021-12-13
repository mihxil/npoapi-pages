#URL:=openshift-image-registry.apps.cluster.chp4.io/poms-plus/npoapi-pages:latest
#URL:=mihxil/npoapi-pages:latest
URL:=docker.vpro.nl/mihxil/npoapi-pages:latest

docker:
	docker build -t $(URL) .

docker-run:
	docker run --env secret=${secret} --env profile=vpro -p 8080:8080  $(URL)


docker-push: docker
	docker 	push $(URL)

run:
	FLASK_ENV=development configdir=$(pwd) profile=vpro flask run
