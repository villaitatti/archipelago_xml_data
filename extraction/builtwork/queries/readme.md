# Database migration

First of all the database postgres *must not be touched!* It is better to clone the database:

from the psql cli, log in the server and then copy the database:

```
create database veniss_test with template postgres owner postgres;
```

If there are other sessions using the database:

```
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'database_name'
  AND pid <> pg_backend_pid();
```

## San Secondo

### Wed 20 Jul 2022

Execute the query in sansecondo_buildings.sql

It creates a table called `sansecondo_buildings_data` that will be used to download the metadata to parse. Then, the query creates the table `sansecondo_buildings` that will be used by QGIS.

Moreover, the query fixes two errors: 

* removes the feature with id `SS_BLDG_052` with the wrong `end_boe` (the one in 1838 is right)
* removes the feature with id `SS_BLDG_001` with the wrong `end_boe` (the one without any is right)