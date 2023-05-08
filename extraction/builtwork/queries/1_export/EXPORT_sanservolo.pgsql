DROP TABLE IF EXISTS PUBLIC.sanservolo_buildings_data;
CREATE TABLE PUBLIC.sanservolo_buildings_data AS
SELECT id, geometry, "BW_ID", '2019' as "Date"
FROM PUBLIC.sanservolo_buildings_2019;

DROP TABLE IF EXISTS PUBLIC.__sanservolo_buildings;
CREATE TABLE PUBLIC.__sanservolo_buildings AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.sanservolo_buildings_data;
