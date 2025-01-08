# NewsReader Web Client

Our desire is to autogenerate a set of simple UI for the news service. However, we will first start with simpler ways to see news.

## Static version

Let us build render the NEWS using a simple web page. Here we use the *Python Flask* framework to render news.

First get the requirements installed locally

```sh
pip install -r requirements.txt

# this will install flask, requests, dotenv 
# and also bring in related related modules
```

Next let us build the *app.py* for hosting the news.
See [Sample Data](./data) folder for data files.
See [News Templates](./templates/) for seeing the news.

## Dynamic Version

To dynamically fetch news, make sure to call the news_api dynamically. This requires the SERVER location for the news_api in the .env file before running this web app.

Copy over the *.env.template* file and modify the MY_NEWS_SERVER location as appropriate.
The default is set to *http://localhost:8080*


Then start the python app using

```sh
python app.py
```

And you can access the web news at the specified location from the python command.
Usually the flask based websites run at http://localhost:5000

There are  few paths enabled here for now. Assuming that the MY_NEWS_SERVER=http://localhost:8080

1. http://localhost:5000/ - at the top root, the server queries the news server and shows results
2. http://localhost:5000/sample - shows the results for a sample data set (3 items( that is hard wired in
3. http://localhost:5000/file1 - shows the results for a full news from sample data file (10+ items) that is hard wired in
