# CLI for News API

This folder has code for creating and running a CLI to call the NEWS APIs hosted in Verse

## Calling the methods

Once this code is ready, we can call the APIs using following approach

```sh

# do a gentle hello call
python newscli.py hello

# let us get the headlines
#   NOTE: it will spew out the headlines as JSON text on console
python newscli.py headlines

# let us get latest news about india
python newscli.py latest --scope india

# let us get latest news about waymo
python newscli.py latest --scope waymo | tee latest.waymo.news.txt
```

for now the *newsapi.definitions.json* is implicit; so it is not provided everytime