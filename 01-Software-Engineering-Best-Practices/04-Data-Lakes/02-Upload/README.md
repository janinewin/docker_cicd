# Uploading Scraped Data to a Data Lake

🏁 The goal for this exercise is to integrate the scraping process you've previously set up with a data upload mechanism. After scraping stories from [Hacker News](https://news.ycombinator.com/news), you will upload them to a Google Cloud Platform (GCP) bucket, organizing the data within a data lake's raw zone.

## Uploading to a Data Lake step by step

### Tasks

#### 1. Setup environment variable:

   a. Create a `.env` by renaming the `.env.sample` file
   b. Populate the `.env` with a bucket name. You might need to get creative because the bucket will need to be globally unique!

#### 2. Setting Up a GCP Bucket:

   a. Create a bucket in GCP with the name $LAKE_BUCKET. Ensure you choose the region closest to you for optimal performance.
   b. Once the bucket is set up, verify its creation by running the test: `pytest tests/test_upload.py::test_bucket_exists`.

   <details>
   <summary markdown='span'>💡 Hint</summary>

   To create a bucket in GCP, navigate to the GCS section in the GCP console. Click on "Create Bucket", choose a unique name, and select the region closest to you. Or with gcloud:

   ```bash
   gsutil mb -l eu gs://$LAKE_BUCKET
   ```

   </details>

#### 2. Uploading to GCP:

   a. Familiarize yourself with the `upload_to_lake` function in the `upload.py` file - try to understand what is happening at each line!
   b. Modify the function (if necessary) to upload the CSV file to your GCP bucket. We're organizing data in the data lake's raw zone using a date-based structure (as seen in the lecture).
   c. Ensure you set up authentication with GCP to allow file uploads.

   <details>
   <summary markdown='span'>💡 Hint</summary>

   If the permissions are not working, run the following:

   ```bash
   gcloud auth application-default login
   ```

   </details>

#### 3. Testing 🧪:

   a. After running your integrated script `main.py`, ensure that the data is both scraped and uploaded to the GCP bucket manually by viewing the bucket.
   b. Use the command `make test` to run the tests and verify the proper functioning of your code and the correct organization of the data within the data lake.

## 🏁 Finish

Congratulations on completing the exercise! You've successfully integrated your scraping process with a data upload mechanism, uploading the scraped data to a data lake's raw zone. Now we are ready to integrate data quality checking 🚀
