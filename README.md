# goit-pythonweb-hw-06

SQLAlchemy ORM usage for flexible and high-performed work with Postgres database. Alembic package usage for database migration processes automatisation and simplification.

1. To initialize virtual environment

```
poetry shell
```

2. To run the database in the docker container

```
docker run --name postgres-hw-06 -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

We will work with default database named 'postgres' that is served at the localhost:5432 and can be connected to through DBeaver, for example.

2.1. Skip this step by default

In the case you would like to create a new database, "pythonweb-hw-06" for example. This could be done manualy through DBeaver. Or you can enter into the running container and create the database using the next commands:

```
docker exec -it postgres-hw-06 psql -U postgres
psql -h localhost -U postgres
CREATE DATABASE pythonweb-hw-06
\l
\q
```

After all you should change the url_to_db in connect.py to use the correct database name.

3. To run the initial migration

```
alembic revision --autogenerate -m 'Init'
```

4. To apply initial migration to database and create tables from appointed models

```
alembic upgrade head
```

5. To fill the database with fake data run the seed.py script

```
python seed.py
```

6. To execute sql-queries run the my_select.py file

```
python my_select.py
```
