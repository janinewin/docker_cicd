.PHONY: install

install:
	echo "Downloading datasets"
	curl --output ./01-Streamlit/database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz

	echo "Unzipping the .gz file"
	gzip -d ./01-Streamlit/database/init/f1db.sql.gz

	echo "Downloading tests fixtures"
	curl --output ./01-Streamlit/app/tests/fixtures/best_lap_times_989.csv https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/best_lap_times_989.csv
	curl --output ./01-Streamlit/app/tests/fixtures/fastest_lap_989.csv https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/fastest_lap_989.csv
	curl --output ./01-Streamlit/app/tests/fixtures/lap_times_989.csv https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/lap_times_989.csv
	curl --output ./01-Streamlit/app/tests/fixtures/races_2018.csv https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/races_2018.csv

	echo "Setup done"
