# SAProgEx-server

システムアーキテクトプログラミング演習のサーバサイドプログラム

## Develop

### Requirements

- [Python](https://www.python.org/)
  - v3.8.\*
- [Poetry](https://python-poetry.org/)
  - 1.\*

### Preparation

Clone this repository.

Then, install dependencies with Poetry.

```sh
poetry install
```

Initiate database.

```sh
poetry run flask init-db
```

### Run

Run in development mode:

```sh
poetry run flask run --debugger --reload
```
