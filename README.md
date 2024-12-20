# Playverse

Verse is a new framework for building services. With its component and provider model, one can quickly build and host services across a wide range of backends. In this repository we will have a variety of projects to *play with verse*

## Newsreader

A simple service that wraps the newsapi.org services. This service also illustrates how easy it is to build with Verse. See [newsreader](./newsreader/) for details. 

- See [News API](./newsreader/newsapi/) for the API implemented and hosted using *verse* framework

### Clients

Once we have APIs running, one can use the same with a variety of clients. The clients are built with pointers to API running on localhost:8080. That can be achieved by launching the newsapi using *verse run news_api* which hosts the API at localhost:8080

- See [News Web1](./newsreader/clients/web1) for a simple web client built using python/flask
- See [News CLI](./newsreader/clients/cli1) for a CLI to work with the news api
- See [News CLI](./newsreader/clients/streamlit) for a Streamlit client to work with the news api
