# Streamlit for News API

This folder has code for a Streamlit based app to call the NEWS APIs hosted in Verse

## Setup the environment

```sh

# set up required items 
pip install streamlit
pip install watchdog

```

or you can install with the requirements file

```sh

pip install -r requirements.txt
```

## Start the server UI

```sh
streamlit run stnews.py

# it automatically opens browser to http://localhost:8501 for the simple UI
```

for now the *newsapi.definitions.json* is implicitly in the folder