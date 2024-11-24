# Hello World

Getting started is always about building **Hello World** programs.

Let us build a sequence of **Hello World** programs to meet increasing scope of requirements. Collectively these will give us a good basics for understanding and using the Verse framework.

All the instructions and code are last built and verified on Nov 23, 2024.

## Build a local API server

Let us get oriented with some basics

1. This folder hello_world is the project root folder. Inside this folder, there are several sub-folders. Each sub-folder starting at number hello_world1 illustrate the details. Each folder should have a couple of must have files

- *manifest.yaml* file to provide information to the sytem
- *component.py* file that defines the component

### Create component folder

Create a folder **hello_world** to host our component and providers.

### Define the component

Create a **component.py** file. This is a new component with a single method called hello_world. In Verse framework, a component just defines the contract. Accordingly, there is no implementation given here.

```py
class CustomComponent(Component):

    @operation()
    def hello_world(self) -> str: pass 
```

NOTE: *This component.py in the starting folder is a reseved file that the system uses to launch the app.* You can have any number of components, each with its own folder. Each folder should have a component.py that defines the interface.

### Define a provider

Implementation for the component resides in provides. Here we have a provider defined inside the folder *hello_world.1/providers*.

```py
class Default(Provider):

    # our implementation for the component contract
    def hello_world(self) -> str:
        return "Hello world"
```

### Define the manifest

In the manifest.yaml, we declare the components and the binding to providers.

```yaml
  - handle: hello_world
    name: custom.hello_world
    provider:
      name: default
```

Here, hello_world is defined as a component that has the implementation in *hello_world.1* folder

Next let us add an API component for creating API endpoints for the hello world sample

```yaml
- handle: hw_api
    name: interface.api
    parameters:
      component: "{{hello_world}}"
      host: 127.0.0.1
      port: 8080
    provider:
      name: default
```

Here we are using a built-in API provider supplied as *interface.api*. This provider expects minimal set of paramters to host the component as a http endpoint. Let us choose to host at the local server and port 8080. NOTE: on some environments, you will need root permissions to run at port 80. Hence we are using port 8080.

### Start the API sever now

Voila! we are ready. Let us run this from the python venv terminal

```sh

verse run --handle hw_api

```

### Use the service

Access the service **http://127.0.0.1:8080/docs** and submit the requests to the API interface. For now the submitted requests will return "Hello World".

POST to the endpoint using followin input request body

```json
{
  "operation": {
    "name": "hello_world"
  }
}
```

You should get back a response like following

```json
{
  "result": "Hello world! Today is a great day",
  "context": null,
  "native": null
}
```

### Congrats - you got a local server

You have built a simple **Hello World** component with a provider.
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

In addition we need to provide parameters for the local provider too. The only parameter is the port mapping. Docker will mape the port 8080 from the docker instance to the port 8080 of the host. For the docker run, it is essential that the host is set as 0.0.0.0 in the API service. To make it easy we add a new handle **hw_api_for_docker** to hello_world component and bind host as 0.0.0.0

```yaml

  - handle: hw_api_for_docker
    name: interface.api
    parameters:
      component: "{{hello_world}}"
      host: 0.0.0.0
      port: 8080
    provider:
      name: default

- handle: hw_docker_local
    name: compute.container
    parameters:
      handle: hw_api_for_docker
      expose: 8080
    provider:
      name: local
      parameters:
        ports:
          "8080": 8080       
```

### Deploy the service in docker

We are almost there. We just have to run the new component. The Verse system will take care of the details of creating docker container, hosting the API service, and running it.

```sh

verse run --handle hw_docker_local

```

The docker hosted component starts running now. Much like befoer, access the service at **http://127.0.0.1:8080/docs**. Use the swagger UI to do a POST request to the API. And much like before you will get the response back promptly. 

### Checking for absent or errors

It is a good idea to send random inputs to the API service and see how it responds. Here are a few cases to check out.

1.POST with no body. We get a HTTP 415 error: Unsupported Media Type

```json

# request

{
}

# response
{
  "detail": "None"
}
```

2.POST with an invalid *operation*. We get a HTTP 415 error: Unsupported Media Type

```json

# request

{
"operation": {
  "name": "ask_for_random_stuff"
 }
}

# response	
{
  "detail": "{\"name\":\"ask_for_random_stuff\",\"args\":null}"
}
```

3.POST with empty *argument(s)*. We get a valid response back

```json
# request
{
  "operation": {
    "name": "hello_world",
    "args": {}
  }
}

# response
{
  "result": "Hello world! Today is a great day",
  "context": null,
  "native": null
}

```

4.POST with invalid *argument(s)*. We get an error response with HTTP status 500. 

```json
# request
{
  "operation": {
    "name": "hello_world",
    "args": { "param1": "none"}
  }
}

# response
Internal Server Error
```

And the Verse runner will show error log indicating

- *ERROR:    Exception in ASGI application*
- *TypeError: Default.hello_world() got an unexpected keyword argument 'param1'*
