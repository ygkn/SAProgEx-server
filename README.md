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

### Run

Run in development mode:

```sh
FLASK_APP=librarian poetry run flask run --debugger --reload
```
