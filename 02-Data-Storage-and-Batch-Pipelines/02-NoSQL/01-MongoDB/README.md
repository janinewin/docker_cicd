## 1️⃣ Set up

🎯 The goal of this session is to get familiar with MongoDB, a document database. We will start with setting up the MongoDB services using `docker-compose`, and will then go through the basics of inserting and querying the data. The advanced exercise is more open, and focuses on interacting with MongoDB using the Python package `pymongo`.

We will use 2 different images, one from `Mongo` and one from `Mongo Express`, which is an interactive lightweight Web-Based Administrative Tool 💻  to interact with the MongoDB Databases through the UI.

### MongoDB service
1️⃣ ❓ Add the following line: `version: '3.1'` to the top of the `docker-compose` file.

2️⃣ ❓ Add a new service named `mongo` with the following properties (use Google for examples):
- `image`: specify the name of the Docker image to use for the MongoDB instance and use version `6.0`
- `restart`: `always`
- `environment`:
  - specify the desired username and password for the MongoDB root user
- `volumes`:
  - specify the host directory `data/db` where you want to store the MongoDB data files and the corresponding directory `data/db` in the Docker container
- `ports`:
  - specify the host port and the container port that you want to use for accessing the MongoDB instance - use `27017`


☝️ This will create a Docker container for the MongoDB instance using the specified Docker image. 💡 The `restart` property specifies that the container should always be restarted if it stops. The `environment` section specifies the username and password for the MongoDB root user. The `volumes` section mounts the local directory where you want to store the MongoDB data files to the corresponding directory in the container. The `ports` section forwards the local port and the container port that you specified, allowing you to locally connect to the MongoDB instance.

### MongoDB Express service

3️⃣ ❓ In the `docker-compose.yml` file, add a new service named `mongo-express` with the following properties (use the [mongo-express-docker documentation](https://github.com/mongo-express/mongo-express-docker#configuration))
- `image`: specify the name of the Docker image to use for the MongoDB Express web interface and use version `1.0.0-alpha`
- `restart`: `always`
- `ports`:
  - specify the host port and the container port that you want to use for accessing the `mongo-express` web interface - use `8081`
- `environment`:
  - specify the username and password for the MongoDB root user
  - specify the URL of the MongoDB instance

### Get it up and running
4️⃣ ❓ Run
```bash
`docker-compose up`
```
and visit http://localhost:8081 after initialization

5️⃣ 💡 The `docker exec` command allows you to run commands inside a Docker container. This allows us to interact with MongoDB inside the container. ❓ Run the following command, which will give you a bash shell inside your mongo container:

```bash
$ docker exec -it [CONTAINER NAME] bash
```

6️⃣ ❓ Run `mongosh` inside the container to interact with Mongo using your username and password (replace the values with the credentials that you specified in the environment variables)
```bash
$ mongosh admin -u username -p password
```

🚀 You are now ready to interact with the database

---

## 2️⃣ MongoDB Basics

1️⃣ ❓ Switch the database
```bash
$ use food
```

2️⃣ ❓ Create a collection 📁
```bash
db.createCollection("fruits")
```
✅ Verify in `Mongo-express` that the database has been created.

3️⃣ ❓ Insert documents 📄
```bash
db.fruits.insertMany([ {name: "apple", origin: "usa", price: 5}, {name: "orange", origin: "italy", price: 3}, {name: "mango", origin: "malaysia", price: 3} ])
```

4️⃣ ❓ Search for the documents using the find command
```bash
db.fruits.find().pretty()
```

5️⃣ ❓ Insert another record, but now also containing the color, 💡 this is no problem for Mongodb due to it being **schemaless**
```bash
db.fruits.insertOne( { name: "apple", origin: "usa", price: 3, color: "red" } )
```

6️⃣ ❓ Use the `updateOne` command to update the record you just inserted in the previous step ☝️. For example, you can change the price to 4 and the color to green
```bash
db.fruits.updateOne( { name: "orange", origin: "italy" }, { $set: { price: 4, color: "green" } } )
```
7️⃣ ❓ Use the `countDocuments` command to count the number of documents in the collection
```bash
db.fruits.countDocuments()
```

8️⃣ ❓ Use the `find` command with a query to search for only the fruits that are from the USA
```bash
db.fruits.find( { origin: "usa" } ).pretty()
```

💡 What happens when you try to query a country that does not exist in the db, e.g. `FRA`?

9️⃣ ❓ Use the `deleteMany` command to delete all the fruits that are from Italy:
```bash
db.fruits.deleteMany( { origin: "italy" } )
```

🔟 ❓ Use the `drop` command to drop the entire collection 💥
```bash
db.fruits.drop()
```

👊 These exercises should have given you a good idea of some of the common operations that you can perform with MongoDB. It is now time for some more open questions!

---

## 3️⃣ Pymango
### Setting up the db connection in Python
We will use the `pymongo` library to interact with the MongoDB database from Python 🐍.  The commands will be very similar, but by including in Python scripts we can structure our code better. There is already an outline of the functions that will need to be written, it is your job to create the logic for these functions 💪

Lets start by setting up the database connection in `app/pymongo_get_database.py`.

1️⃣ ❓ The connection string consists of the following format: `mongodb://username:password@localhost:27017/`. Load your username and password from the `.env` file and use them in the connection string (instead of hardcoding) them. This is used to create a connection to the MongoDB server using the MongoClient object. By loading them from a `.env` file and including that file in `.gitignore`, you are making sure to not store any credentials in `Git` 💀.

2️⃣ ❓ Use the client object to access the restaurant database and create a new database called `restaurant`. A database is used to create and manipulate collections of documents. We will use this client object in other parts of our code to interact with this specific database. ❗ Note: the database will only be visible in Mongo Express after you have inserted some documents in step 4️⃣

🚀 Nice, you have set up the database connection using python and created a database called `restaurant`! We are now going to ingest documents into this database. Switch to `ingest.py`.

### Inserting the documents
3️⃣ ❓ Create a collection named `customers` and insert the following documents 📄 into it from the `ingest_data` function:
```bash
{ "name": "John Doe", "age": 35, "gender": "male", "address": "123 Main St" },
{ "name": "Jane Smith", "age": 28, "gender": "female", "address": "456 Park Ave" },
{ "name": "Michael Johnson", "age": 41, "gender": "male", "address": "789 Oak St" }
```

4️⃣ ❓ Count the number of documents in the "customers" collection in the `ingest` file. You can also check in mongo express whether the documents have been successfully inserted.

### Reading data
👉 We are now ready to read the data from the database. Continue working in the `app/query.py` file.  💡 The type hints and docstrings give a good indication about the values that you are expected to return from the functions. One function has already been filled, ❓ run `python query.py` to run the full script. 💡 Pymongo returns a cursor when running a MongoDB command, extract the values using the `list()` function.

<details>
  <summary markdown='span'>💡 What is a cursor?</summary>

💡 By default the pymongo functinalities return a `pymongo.cursor.Cursor`, because it allows for the efficient iteration over a large number of results. To see the values that are in the cursor, you can simply use the `list()` function
</details>

5️⃣ ❓ Use the `find` command to search for customers who are 35 years old or older

6️⃣ ❓ Use the `aggregate` command to calculate the average age of the customers in the collection

7️⃣ ❓ Use the `updateMany` command to update all customers with a new field called "membership" that has a value of "gold":

8️⃣ ❓ Use the `find` command with the sort modifier to search for customers and sort the results by their age in descending order:

9️⃣ ❓ Use the `deleteOne` command to delete the customer with the name "Jane Smith"

🏁🚀 Congratulation on finishing these MongoDB exercises!
