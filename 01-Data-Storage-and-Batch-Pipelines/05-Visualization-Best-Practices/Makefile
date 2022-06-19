.PHONY: install

install:
	echo "Downloading datasets"
	curl --output ./00-Setup-Exercise/database/init/f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz
	cp ./00-Setup-Exercise/database/init/f1db.sql.gz ./01-streamlit/database/init/f1db.sql.gz

	#Track long dataset
	curl --output ./02-Track-long/database/init/postgres-movies-no-owner-w01d04.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/w1d3/postgres-movies-no-owner-w01d04.sql.gz
	
	echo "Setup done"
	
