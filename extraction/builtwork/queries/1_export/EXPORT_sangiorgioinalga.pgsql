DROP TABLE IF EXISTS PUBLIC.sangiorgioinalga_buildings_data;
CREATE TABLE PUBLIC.sangiorgioinalga_buildings_data AS
SELECT id, geometry, bw_id as "BW_ID", '2023' as "Date"
FROM PUBLIC.sangiorgioinalga_buildings;

DROP TABLE IF EXISTS PUBLIC.__sangiorgioinalga_buildings;
CREATE TABLE PUBLIC.__sangiorgioinalga_buildings AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2023' THEN 1 ELSE 0 END AS "2023",
  geometry
FROM PUBLIC.sangiorgioinalga_buildings_data;

DROP TABLE IF EXISTS PUBLIC.sangiorgioinalga_islands_data;
CREATE TABLE PUBLIC.sangiorgioinalga_islands_data AS
SELECT id, geometry, "BW_ID", bob as "Date"
FROM PUBLIC.sangiorgioinalga_islands;

DROP TABLE IF EXISTS PUBLIC.__sangiorgioinalga_islands;
CREATE TABLE PUBLIC.__sangiorgioinalga_islands AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2010-01-01' THEN 1 ELSE 0 END AS "2023",
  CASE WHEN "Date" = '1982-01-01' THEN 1 ELSE 0 END AS "1982",
  CASE WHEN "Date" = '1931-01-01' THEN 1 ELSE 0 END AS "1931",
  CASE WHEN "Date" = '1944-11-09' THEN 1 ELSE 0 END AS "1944",
  geometry
FROM PUBLIC.sangiorgioinalga_islands_data;