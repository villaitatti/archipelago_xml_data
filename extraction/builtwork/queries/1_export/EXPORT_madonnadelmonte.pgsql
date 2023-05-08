DROP TABLE IF EXISTS PUBLIC.madonnadelmonte_buildings_data;
CREATE TABLE PUBLIC.madonnadelmonte_buildings_data AS
SELECT id, geometry, "BW_ID", "IslandName", '2019' as "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM PUBLIC.madonnadelmonte_buildings_2019;

DROP TABLE IF EXISTS PUBLIC.__madonnadelmonte_buildings;
CREATE TABLE PUBLIC.__madonnadelmonte_buildings AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.madonnadelmonte_buildings_data;

DROP TABLE IF EXISTS PUBLIC.madonnadelmonte_islands_data;
CREATE TABLE PUBLIC.madonnadelmonte_islands_data AS
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM PUBLIC.madonnadelmonte_island_1982
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM PUBLIC.madonnadelmonte_island_2019;

DROP TABLE IF EXISTS PUBLIC.__madonnadelmonte_islands;
CREATE TABLE PUBLIC.__madonnadelmonte_islands AS 
  SELECT DISTINCT 
  CASE WHEN "BW_ID" IS NULL THEN CAST(uuid_generate_v4() AS VARCHAR) ELSE "BW_ID" END AS identifier,
  CASE WHEN "Date" = '1982' THEN 1 ELSE 0 END AS "1982",
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.madonnadelmonte_islands_data;