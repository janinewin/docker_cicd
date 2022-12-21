.PHONY: install

download-sql-file:
	echo "Downloading datasets"
	curl --output ./01-Streamlit/database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz

	echo "Unzipping the .gz file"
	gzip -d ./01-Streamlit/database/init/f1db.sql.gz
