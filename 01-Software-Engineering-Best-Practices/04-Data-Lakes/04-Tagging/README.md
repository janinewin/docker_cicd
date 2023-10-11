
## Google Cloud's Data Catalog Setup

Lets setup our Data Catalog to really make our data lake more comprehensive!  You should be able to use lots of the code from the lecture as boilerplate!

### 0. Setup

❓ Copy the `.env` from the previous exercise and add the `PROJECT_ID` variable with the id of your project! You will also need to copy across the GreatExpectations folder `gx` from the previous challenge as well!

### 1. Setting up the Entry Group:

Create an entry group called `hn_day` in the same location as your bucket!

<details>
<summary markdown='span'>💡 Command if you get stuck</summary>

```bash
gcloud beta data-catalog entry-groups create hn_day --location=eu --description="Entry group for daily Hacker News data"
```

</details>


### 2. Creating the Tag Template:

Design a tag template to label your data assets. For this challenge, you should have two fields: `source_system` and `source_date`. Representing where the data came from and when it was collected, respectively.

<details>
<summary markdown='span'>💡 Hint</summary>

```bash
gcloud beta data-catalog tag-templates create data_source_info_template --location=eu --display-name="Data Source Info" \
    --field=id=source_system,type=string,display-name="Source System" \
    --field=id=source_date,type=timestamp,display-name="Source Date"
```

</details>


### 3. Build the function:

Now you need to implement the `catalog_entry` function in `tag.py`

a. Initializing the Data Catalog Client:

   i. Import the necessary modules to work with Google Cloud's Data Catalog.
   ii. Initialize a connection to the Data Catalog by creating a client instance.

b. Setting up the Entry Details:

   i. Retrieve the project ID from the environment variables.
   ii. Specify the location where you're storing the data.
   iii. Define an entry group for categorizing the data.
   iv. Generate a unique entry ID, preferably based on the current date.

c. Configuring the Entry:

   i. Initialize a new entry object.
   ii. Set the display name for the entry, which could be based on the current   date.
   iii. Provide a description that informs about the data the entry represents.
   iv. Specify the type of entry you're creating.
   v. Configure where the data is located, especially if it's in Google Cloud Storage.

d. Creating or Retrieving the Entry:

   i. Use the client to attempt to create the entry in the Data Catalog.
   ii. If an entry with the same ID already exists, handle the situation by retrieving the existing entry instead of creating a new one.

e. Tagging the Entry:

   i. Initialize a new tag object.
   ii. Set the tag template to the one you created earlier.
   iii. Fill in the tag's fields with appropriate metadata.
   iv. Attach the tag to the entry using the Data Catalog client.

### 4. Testing 🧪:

You can run `python/main.py` and check that your entry gets tagged properly feel free to change it to a loop and collect the previous few days of articles to checkout how the catalog would grow!

### 🏁 Finish and Conclusion

Now we have a pipeline: scraping -> checking quality -> uploading to our lake -> tagging the data to make to easily accessible!
