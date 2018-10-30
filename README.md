# salary

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

### Database Migration

``` bash
flask db init
flask db migrate
flask db upgrade
```

### Run

Note: Environment variables are already set in the `.env` file for local development.

``` bash
flask run
```
