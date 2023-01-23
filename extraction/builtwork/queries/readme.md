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

## Wed 20 Jul 2022

### San Secondo

Execute the query in sansecondo_buildings.sql

It creates a table called `sansecondo_buildings_data` that will be used to download the metadata to parse. Then, the query creates the table `sansecondo_buildings` that will be used by QGIS.

Moreover, the query fixes two errors: 

* removes the feature with id `SS_BLDG_052` with the wrong `end_boe` (the one in 1838 is right)
* removes the feature with id `SS_BLDG_001` with the wrong `end_boe` (the one without any is right)

## Wed 27 Jul 2022

### San Secondo

The table `sansecondo_buildings` has been renamed `__sansecondo_buildings` (also the others now follow the same behavior). In this way it's easier to find them among the others (such as the old ones etc).

The process have been extended to `__sansecondo_island` and `__sansecondo_openspaces`.

Also, two other columns have been added. **t** is the type such as `Buildings`, `Island`, `Open Spaces`. While **z** is the order to follow in order to draw features. The idea is to keep 0 as the water level and have **1 for islands**, **2 for open spaces and buildings** and so on. According to this, **waterways and canals should be -1**.

### documentation

```
delete from __sansecondo_buildings
where identifier = 'SS_BLDG_052' and end_boe = '1788-12-31';

delete from __sansecondo_buildings
where identifier = 'SS_BLDG_001' and end_boe = '2019-12-31';
```