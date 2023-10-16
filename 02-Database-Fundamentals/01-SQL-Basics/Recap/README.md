### Schema spy

Download schema spy

```bash
https://github.com/schemaspy/schemaspy/releases/download/v6.2.4/schemaspy-6.2.4.jar
```

Make sure your environment variables to connect to the container are available

Download the driver for postgres

```bash
wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
```

Install graph viz

```bash
sudo apt install graphviz
```

Run the schema spy and launch the index.html. Take some time to explore the docs!

```bash
java -jar schemaspy-6.2.4.jar -t pgsql -dp postgresql-42.6.0.jar -db pagila -host 0.0.0.0:5410 -u $POSTGRES_USER -p $POSTGRES_PASSWORD -o output
```
