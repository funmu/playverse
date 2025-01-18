# NewsReader

Let us build APIs and experience for a simple news reader. We will use the daily news summary from [NewsAPI.org](https://newsapi.org) to build APIs that provide info for an experience. Let us use **Verse** to build the API service

## Build a local API server

We use **manifest.yaml** to describe the Verse based project. All News API related contnet is in the [News API](./news_api/) folder.

- *manifest.yaml* file to provide information to the sytem

### Define the component

Create a **component.py** file. This is a new component with a single method called hello_world. In Verse framework, a component just defines the contract. Accordingly, there is no implementation given here.

```py
class CustomComponent(Component):

    @operation()
    def hello(self) -> str: pass

    # get all top headlines
    @operation()
    def headlines( self, country="us") -> str: pass

    # get the latest news for given area of scope
    @operation()
    def latest( self, scope: str="technology") -> str: pass

    # get the headlines by country
    @operation()
    def headlinesByCountry( self, country="us"): pass

    # get the sources for getting news from
    @operation()    
    def sources( self): pass
    
    # get the headlines by source; default is from reuters
    @operation()    
    def headlinesBySource( self, source="reuters"): pass    
```

NOTE: *This component.py in the starting folder is a reseved file that the system uses to launch the app.* There are three methods defined now. The *hello* method is used for simple ping testing. For news we expose a handful of functions including *headlines*, *sources", and *headlinesBySource*

### Define a provider

Implementation for the component resides in provides. Here we have a provider defined inside the folder *news_api/providers*.

```py
class Default(Provider):

    # declare variables

    # declare methods
    def __init__(self, api_key: str):
        self.api_key = api_key

    # our implementation for the component contract
    def hello_world(self) -> str:
        return "Hello world"
```

Notice that the *__init__* method has a special parameter api_key. The api_key is supplied to the provider from the manifest via secrets or .env file. This way the provider is pretty agnostic and secure without having the keys hard coded.

### Define the manifest

In the manifest.yaml, we declare the components and the binding to providers.

```yaml
    - handle: news_secrets
    name: storage.secret_store
    provider:
      name: env_file

  - handle: news_component
    name: custom.news_api
    provider:
      name: default
      parameters:
        api_key: "{{news_secrets.MY_NEWS_API_KEY}}"
```

First, we define a secrets component. We use the standard secrets store component and implemention. *storage.secret_store* componet is used with a pre-built *env_file* provider. This provider will read secrets from the *.env* file. Make sure to store the API key for newsapi server in the .env file for the name MY_NEWS_API_KEY.

Next there is the *news_component* that is bound to the news_api default provider. The API key is fetched from news_secrets and fed as a parameter for this provider.

Next let us add an API component for creating API endpoints for the hello world sample

```yaml
- handle: news_api
    name: interface.api
    parameters:
      component: "{{news_component}}"
      host: 127.0.0.1
      port: 8080
    provider:
      name: default
```

Here we are using a built-in API provider supplied as *interface.api*. This provider expects minimal set of paramters to host the component as a http endpoint. Let us choose to host at the local server and port 8080. NOTE: on some environments, you will need root permissions to run at port 80. Hence we are using port 8080.

### Start the API sever now

Voila! we are ready. Let us run this from the python venv terminal

```sh

verse run --handle news_api

```

### Use the service

Access the service **http://127.0.0.1:8080/docs** and submit the requests to the API interface. For now the submitted requests will return "Hello World ...".

POST to the endpoint using followin input request body

```json
{
  "operation": {
    "name": "hello"
  }
}
```

You should get back a response like following

```json
{
  "result": "Hello world! Time now is: 2024-11-24 08:51:26 UTC",
  "context": null,
  "native": null
}
```

Next, try the headlines operation to find the latest headlines.

```json
{
  "operation": {
    "name": "headlines"
  }
}
```

Next, try the sources operation to find the list of sources.

```json
{
  "operation": {
    "name": "sources"
  }
}
```

The response will consist of JSON formatted list of supported sources.

Finally, let us try to fetch news from a single source

```json
{
  "operation": {
    "name": "headlinesBySources",
    "args": { "source": "bloomberg" }
  }
}
```

The response will consist of JSON formatted list of news from Bloomberg.

### Congrats - you got a local server

You have built a simple **news_api** component with a provider.
Let us look at more things made simpler soon!

NOTE: we can build out the SSL endpoints as well. That comes later.

## Add a Docker Container

Docker makes life simple with a well packaged version of OS, framework, and our new services. Let us use it to host our *Hello World* api service.

### Get Docker Installed

First, install Docker for your operating system. 

Visit [Docker](https://www.docker.com) and get the docker build. It is useful to get the CLI for docker as well.

More details on Docker [here](https://github.com/funmu/tooldocs/docs/docker.md)

### Define the docker container

Verse makes it easy to *docker-ize* the API server and deploy it locally. There is a pre-built **compute.container** with local provider that is part of Verse distribution. We just need to use this and provide the parameters for local deployment.

The two important parameters for the component are:

- *handle* - defines what is dockerized. In our case, we use the *hw_api* handle defined earlier for the API service
- *expose* - what port does the docker container run this API service at. We chose port 8080 to ensure that there are no security blockers.
- *requirements* mappeed to requirements.txt. This allows one to pick up any additional Python modules required for the project. For the news_api, we use the *requests* module which is included in the requirements.txt file.

In addition we need to provide parameters for the local provider too. One parameter is the port mapping. Docker will map the port 8080 from the docker instance to the port 8081 of the host. For the docker run, it is essential that the host is set as 0.0.0.0 in the API service. To make it easy we add a new handle **news_api_for_docker** to news_api component and bind host as 0.0.0.0

```yaml

  - handle: news_api_for_docker
    name: interface.api
    parameters:
      component: "{{news_component}}"
      host: 0.0.0.0
      port: 8080
    provider:
      name: default

  - handle: news_docker_local
    name: compute.container
    parameters:
      handle: news_api_for_docker
      expose: 8081
      requirements: requirements.txt
    provider:
      name: local
      parameters:
        ports:
          "8080": 8081    
```

### Deploy the service in docker

We are almost there. We just have to run the new component. The Verse system will take care of the details of creating docker container, hosting the API service, and running it.

```sh

verse run --handle news_docker_local

```

The docker hosted component starts running now. Much like befoer, access the service at **http://127.0.0.1:8081/docs**. Use the swagger UI to do a POST request to the API. And much like before you will get the response back promptly.

## Using Google Cloud

### Set up Google Project

- Visit the [Google Cloud Console](https://console.cloud.google.com)
- Create a new project. Let us call it "playverse1"
- Install google cloud SDK from [here](https://cloud.google.com/sdk/docs/install-sdk)
- Configure the local connection to the Google Cloud project

### Set up Google Cloud CLI

Login to Google cloud with your credentials and then set up the project. See [Google Cloud Auth Tutorial](https://cloud.google.com/sdk/auth_success)

```sh
gcloud auth login

gcloud config set project playverse1

```

### Let us run Verse

Now let us run the verse. Go to verse project and find the pyproject.toml
Run the poetry configuration and then again set up the Google Cloud connection.
Make sure to start Docker on the desktop before starting to run services.

```sh

poetry shell
```

### Google Cloud setup

As a one time step, login and create a project on Google Cloud

```sh

gcloud auth login
gcloud config set project playverse1

```

### Go run your project on Google Cloud

Visit your project and ensure there is the manifest.yaml.
Include a new entry for the cloud hosted version of news API

```yaml

  - handle: news_docker_gcloud
    name: compute.container
    parameters:
      handle: news_api_for_docker
      expose: 8080
      requirements: requirements.txt
    provider:
      name: google_cloud_run
      parameters:
        project_id: playverse1
        region: us-central1
        service_name: playnews1
```

Now use verse to start the docker image in the Google Cloud

```sh

verse run news_docker_gcloud
```

Get the URL location from the output and open the link within a browser.
Access the /docs location to retrieve the FastAPI endpoint for testing the APIs.

output in the console wil have the URL as shown

```text

result='https://playnews1-<FULL-PATH>' context=None native=None
```

Use the entire path at *https://playnews1-<FULL-PATH>/docs* in the browser

Now you can try out your API operations using the "Try it out!" action.

## Manual mode to run service on Google Cloud

This was done as an experiment to try out steps independent of the vers runner

### Set up Docker on Google Cloud

```sh
gcloud auth configure-docker

# accept the terms of agreement (one time thing) and save configuration
# docker config saved in ~/.docker/config.json

```

In Google console, visit "artifact registry" and enable it for this project

```sh

# also enable google services
gcloud services enable run.googleapis.com

```

### Special: Build image for Google docker

There were issues with docker run from Verse.
So we will attempt to run it on the side.

Find the name of the Docker container on the site. It is likely located at gcr.io/projectname which is *gcr.io/playverse1*. Our project tag then will be

```sh
GCLOUD_PATH=gcr.io/playverse1/news_api_for_docker:v1

# enable docker
 gcloud auth configure-docker

```

### Special for MAC: enable cross platform Docker build

On MAC, by default the images are built as *linux/arm64* which needs to be changed to *linux/amd64* for the Google Cloud and most cloud services. See [multi-platform docker](https://github.com/multiarch/qemu-user-static/blob/master/README.md) for more details

```sh
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx create --use
docker buildx inspect --bootstrap
```

Once that is done we can do the cross platform build as shown here. BTW, push also pushes the image out

```sh
# builds a docker container for amd64 and loads it inside the local Docker Desktop
 docker buildx build --platform linux/amd64 -t $GCLOUD_PATH --load .

# check the architecture type. should show amd64
docker inspect news_api_for_docker | grep Arc

# tag the image for my google cloud deployment
docker tag news_api_for_docker $GCLOUD_PATH 

# push the image to Google Cloud
docker push $GCLOUD_PATH

# inspect the image in google cloud
gcloud artifacts docker images describe $GCLOUD_PATH

```

verse run --handle news_docker_gcloud

### Some useful Google Cloud Run commands

```sh
gcloud run jobs list
gcloud run services list
gcloud run services describe playnews1 --region=us-central1
gcloud run services delete playnews1 --region=us-central1
```