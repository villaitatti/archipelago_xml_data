DROP TABLE IF EXISTS PUBLIC.santospirito_buildings_data;
CREATE TABLE PUBLIC.santospirito_buildings_data AS
SELECT id, geometry, "BW_ID", "Date"
FROM PUBLIC.santospirito_buildings_2019;

DROP TABLE IF EXISTS PUBLIC.__santospirito_buildings;
CREATE TABLE PUBLIC.__santospirito_buildings AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.santospirito_buildings_data;

DROP TABLE IF EXISTS PUBLIC.santospirito_islands_data;
CREATE TABLE PUBLIC.santospirito_islands_data AS
SELECT id, geometry, "BW_ID", "Date"
FROM santospirito_island_1841
UNION
SELECT id, geometry, "BW_ID", "Date"
FROM santospirito_island_1982
UNION
SELECT id, geometry, "BW_ID", "Date"
FROM santospirito_island_2019;

DROP TABLE IF EXISTS PUBLIC.__santospirito_islands;
CREATE TABLE PUBLIC.__santospirito_islands AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '1982' THEN 1 ELSE 0 END AS "1982",
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  CASE WHEN "Date" = '1841' THEN 1 ELSE 0 END AS "1841",
  geometry
FROM PUBLIC.santospirito_islands_data;