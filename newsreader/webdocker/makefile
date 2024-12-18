
# makefile for the docker creation and run

build:
   @echo create the docker image
   docker  build  -t newsweb1 --load .

run:
   @echo run the created docker image
   docker run -d -p 5000:5000 newsweb1

