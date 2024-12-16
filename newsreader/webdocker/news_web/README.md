# NewsReader Web Client

Our desire is to autogenerate a set of simple UI for the news service. However, we will first start with simpler ways to see news.

## Static version

Let us build render the NEWS using a simple web page. Here we use the *Python Flask* framework to render news.

First get Flask installed locally

```sh
pip install flask
```

Next let us build the *app.py* for hosting the news.
See [Sample Data](./data) folder for data files.
See [News Templates](./templates/) for seeing the news.

## Dynamic Version

To dynamically fetch news, make sure to call the news_api dynamically. This requires  the SERVER location for the news_api in the .env file before running this web app.

Then start the python app using 

```sh
python app.py
```

And you can access the web news at the specified location from the python command
