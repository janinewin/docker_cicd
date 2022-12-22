## 2️⃣ MongoDB Basics
1 ❓ Switch the database
```bash
$ use food
```

2 ❓ Create a collection 📁
```bash
db.createCollection("fruits")
```
✅ Verify in `Mongo-express` that the database has been created.

3 ❓ Insert multiple documents 📄
```bash
db.fruits.insertMany([ {name: "apple", origin: "usa", price: 5}, {name: "orange", origin: "italy", price: 3}, {name: "mango", origin: "malaysia", price: 3} ])
```

4 ❓ Query the documents using the find command
```bash
db.fruits.find().pretty()
```

5 ❓ Insert another record, but now also containing the color, 💡 this is no problem for Mongodb due to it being **schemaless**
```bash
db.fruits.insertOne( { name: "apple", origin: "usa", price: 3, color: "red" } )
```

6 ❓ Update the record you just inserted in the previous step ☝️. For example, you can change the price to 4 and the color to green
```bash
db.fruits.updateOne( { name: "orange", origin: "italy" }, { $set: { price: 4, color: "green" } } )
```

7 ❓ Use the `countDocuments` command to count the number of documents in the collection
```bash
db.fruits.countDocuments()
```

8 ❓ Use the `find` command with a query to search for only the fruits that are from the USA
```bash
db.fruits.find( { origin: "usa" } ).pretty()
```

💡 What happens when you try to query a country that does not exist in the db, e.g. `FRA`?

9 ❓ Use the `deleteMany` command to delete all the fruits that are from Italy:
```bash
db.fruits.deleteMany( { origin: "italy" } )
```

10 ❓ Use the `drop` command to drop the entire collection 💥
```bash
db.fruits.drop()
```
