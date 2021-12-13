FROM mihxil/npo-pyapi:latest

RUN apk add --no-cache curl
RUN  pip3 install flask waitress
ADD . /flask
WORKDIR /flask
ENV FLASK_ENV=production
ENV configdir=/flask

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["app.py"]

