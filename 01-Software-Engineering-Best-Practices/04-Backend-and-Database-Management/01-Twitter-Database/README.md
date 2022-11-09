# Twitter database

🎯 The goal of this exercise is to create
- a Twitter **database** using *alembic*, containing a `tweets` and a `users` table
- and a functioning **front-end** with *fastapi*


# 1️⃣ Setup
<details>
<summary markdown='span'>❓ Instruction (expand me)</summary>

## Creating the database

❓ Lets create a new database in our postgres called `twitter`

<details>
<summary markdown='span'>Quickly make a db</summary>

```bash
createdb twitter
```

</details>

<br>

Now lets set up the `.env` by `cp .env.sample .env` so that you have an url ready to be used

```bash
POSTGRES_DATABASE_URL = postgresql+psycopg2://$USER:$POSTGRES_PASSWORD@localhost:5432/twitter
```

Then connect to our new database through dbeaver like we did yesterday!

❗️ Now we are ready to start creating our python files!

</details>

# 2️⃣ Python connection

<details>
<summary markdown='span'>❓ Instruction (expand me)</summary>

## sqlalchemy connection

We have setup a file for you at `twitter_api/database.py` which has what we need to connect to the database from our api. Try to read it and understand what we have created. Don't forget to setup your VS code interpreter to the poetry env of the day (interpreter path: `which python`)

1️⃣ First import the necessary imports from sqlalchemy.
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
```

2️⃣ Next we get our databse url string from the enviroment variable
```python
DATABASE_URL = os.environ.get("DATABASE_URL")
```

3️⃣ Now we create an [engine](https://docs.sqlalchemy.org/en/20/core/engines.html), which is the point at which we are most abstracted away from the database. For us it is the intial point of connection.

```python
engine = create_engine(DATABASE_URL)
```

4️⃣ To utilise our engine we create a sessionmaker which can create lots of [sessions](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#what-does-the-session-do). Which are what allows us to interact with the database through the api and make changes but this setup means that lots of calls and updates can be made concurrently.

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

5️⃣ Lets test our connection you can run the file `python twitter_api/database.py` and if it runs succesfully your connection string is allowing us to execute queries against the database!

```python
if __name__ == "__main__":
    with SessionLocal() as db:
        print(db.execute("""
            SELECT * FROM information_schema.tables
            WHERE table_schema = 'public'
            """).fetchall())
```

</details>

# 3️⃣ Creating the tables

<details>
<summary markdown='span'>❓ Instruction (expand me)</summary>


❓ Go to `twitter_api/models.py` and for now your goal is to try and fill up the
users class using sqlalchemy [declarative mapping](https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html). The class is there ready to be filled **start with just
the tablename and columns section**.

<details>
<summary markdown='span'>💡 Table naming</summary>

```python
__tablename__ = "tablename"
```

</details>

<details>
<summary markdown='span'>💡 Column creation</summary>

```python
id = Column(Integer, primary_key=True)
```

</details>

❗️ Now we have our table defined we are ready to use [alembic](https://alembic.sqlalchemy.org/en/latest/) to autogenerate migrations!

The intial setup of alembic is a little tricky so we have included it all here

The first step is to run

```bash
alembic init alembic
```

This will create an alembic folder and in there **we want to edit the `env.py` file!**

It will begin looking like this when you open the file

![initial env](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/initial-env.png)

We want to populate these pieces of code in the file into the sections highlight in red below!

1️⃣ imports
```python
import os
import pathlib
from dotenv import load_dotenv
```
2️⃣ connection url
```python
env_path = pathlib.Path(__file__).resolve().parent.parent.joinpath(".env")
load_dotenv(env_path)
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
```

3️⃣ model data
```python
from twitter_api import models

target_metadata = models.Base.metadata
```


![filled env](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/filled-env.png)

Now our alembic should be ready setup should be ready to go, you can now run your first revision!

```bash
alembic revision --autogenerate -m "added users table"
```

This will generate a new file in `alembic/versions` describing the changes to apply to the database. Now we want to apply this to our database so run:

```bash
alembic upgrade head
```

❗️If you now go and check your database you should see a users table created with all the columns you defined in python!

🔎 There are some restrictions to what autogenerate will correct you can read about them [here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html).

</details>

# 4️⃣ Creating the api

<details>
<summary markdown='span'>❓ Instruction (expand me)</summary>

❗️ **We have three steps to creating the api**

1️⃣ Defining the pydantic models in `schemas.py`
2️⃣ Defining the functions to interact with the database in `crud.py`
3️⃣ Defining the endpoints in `main.py`


## 4.1 Pydantic

If you look at the [documentation](https://pydantic-docs.helpmanual.io/usage/models/) you can see that inside fields for pydantic model the types are defined with type hints for example `id: int` compared to how we defined the tables. We want these models to describe how we would like to send and recive data from the api try to fill the user classes in `schemas.py`.

❓ Ask yourself which piece of data should be avaliable at all stages so it belongs in `UserBase`, only when you are creating the class `UserCreate`, and `User` for when we query from the database.

<details>
<summary markdown='span'>💡 When you are stuck or done!</summary>

```python
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
```
</details>

Here the main piece you were probably missing was `orm_mode` to allow us to leverage the models using orm patterns!

## 4.2 Interact with the database

❓ We need to create the four functions in the users section in `crud.py` you can
see that the functions all take a session as an input so we need to interact with that in order to get data from our db. Start with the `read_user` function!

<details>
<summary markdown='span'>💡 User function</summary>

You can see how we can use our models we defined to help us interact with the db without writing a single line of sql!
```python
return db.query(models.User).filter(models.User.id == user_id).first()
```

</details>

❓ Now attempt to create the remaining three functions. The hardest will be the create users one, **take notice of the schema as an input to the function because we can demand it as a input to our input you can access the attributes of it just like a normal python class!**

<details>
<summary markdown='span'>💡 Create user function</summary>

```python
fake_hashed_password = user.password + "notreallyhashed"
db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
db.add(db_user)
db.commit()
db.refresh(db_user)
return db_user
```

</details>

## 4.3 Endpoints

Check out `main.py` the scaffolding is there ready for you to start filling! Lets run the app and check out where we are starting from!

```bash
uvicorn twitter_api.main:app --reload
```

Now make sure port 8000 is forwarded and go to `localhost:8000`, you should get `detail": "Not Found"` as we have not defined anything for this endpoint. Instead lets go to `localhost:8000/docs` and you should see some lovely documentation automatically created. **We can also use this interface to test our endpoints!**

If we go to a specifc endpoint

![intial](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/docs.png)

We can click try it out

![try](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/try.png)

Then we fill the values and execute (for now it should fail we havent written the logic behind the endpoint yet)!

![execute](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D4/execute.png)

❗️ This is all made possible because of the pydantic models we defined.

You are now ready to add code to the endpoints we have coded all the logic in `crud.py` so here we just need to use that in conjunction with the inputs!

❓ Start by trying the `read_users` endpoint

<details>
<summary markdown='span'>💡 If you get stuck</summary>

```python
users = crud.read_users(db, skip=skip, limit=limit)
return users
```

</details>

❓ Now try and build the last two users endpoints! The part that is more diffiucult here is dealing with the scenario where a user is already using that email or no user exists with that id (this [documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/) should help)!

</details>
