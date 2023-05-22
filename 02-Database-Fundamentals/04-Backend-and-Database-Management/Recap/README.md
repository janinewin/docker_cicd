# Twitter Recap

## MVC + Routeur

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/mvc-twitter.png" width=600>

## Order to add a feature

1. Model + migration ⇒ alchemy + Alembic
2. Routeur ⇒ *operation paths* in `[main.py](http://main.py)` (`@app.get(url)`)
3. Controller ⇒ *decorated_functions* from [`main.py`](http://main.py) + `[crud.py](http://crud.py)` = actions, manipulate data using models
4. View ⇒ not very relevant for APIs, could have a templates to build complex responses

## Create Likes

Following previous recipe (Order)

## Alembic upgrade

- alembic checks the revision_id of the latest revision that was run in the `alembic_version` table
- `alembic upgrade head` will only run the migrations that haven’t been played (check if a revision has the revision_id of the one stored in `alembic_version` as `down_revision`)
- This allows to run safely `alembic upgrade head` as many time as you want (do it systematically after pulling `master` )
