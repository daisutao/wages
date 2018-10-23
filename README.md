# wages

A pythonic flask app.

## Quick Start

### Build

You can build with [pipenv](https://github.com/pypa/pipenv)

``` bash
git clone https://github.com/daisutao/wages
cd wages
pipenv install --dev
pipenv shell
```

Or build with docker

``` bash
docker build -t wages:latest .
docker run --name wages -d -p 8000:5000 wages:latest
```

### Run

``` bash
export FLASK_APP=wages.py
export FLASK_DEBUG=1
flask run
```

### Database Migration

``` bash
flask db init
flask db migrate
flask db upgrade
```