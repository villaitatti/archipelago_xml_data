DROP TABLE IF EXISTS PUBLIC.sanclemente_buildings_data;
CREATE TABLE PUBLIC.sanclemente_buildings_data AS
SELECT id, geometry, "BW_ID", '2019' as "Date"
FROM PUBLIC.sanclemente_buildings_2019
UNION
SELECT id, geom as geometry, "BW_ID", '1982' as "Date"
FROM PUBLIC.sanclemente_buildings_1982;

DROP TABLE IF EXISTS PUBLIC.__sanclemente_buildings;
CREATE TABLE PUBLIC.__sanclemente_buildings AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  CASE WHEN "Date" = '1982' THEN 1 ELSE 0 END AS "1982",
  geometry
FROM PUBLIC.sanclemente_buildings_data;

DROP TABLE IF EXISTS PUBLIC.sanclemente_islands_data;
CREATE TABLE PUBLIC.sanclemente_islands_data AS
SELECT id, geometry, "BW_ID", '2019' as "Date"
FROM PUBLIC.sanclemente_island_2019;

DROP TABLE IF EXISTS PUBLIC.__sanclemente_islands;
CREATE TABLE PUBLIC.__sanclemente_islands AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '1982' THEN 1 ELSE 0 END AS "1982",
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.sanclemente_islands_data;

DROP TABLE IF EXISTS PUBLIC.sanclemente_openspaces_data;
CREATE TABLE PUBLIC.sanclemente_openspaces_data AS
SELECT id, geometry, "BW_ID", '2019' as "Date"
FROM PUBLIC.sanclemente_openspaces_2019;

DROP TABLE IF EXISTS PUBLIC.__sanclemente_openspaces;
CREATE TABLE PUBLIC.__sanclemente_openspaces AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.sanclemente_openspaces_data;