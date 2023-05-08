-- Create san_secondo_buildings_data
-- I.e., the UNION among all the tables
DROP TABLE IF EXISTS PUBLIC.sansecondo_buildings_data;
CREATE TABLE PUBLIC.sansecondo_buildings_data AS
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_buildings_1500
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_buildings_1697
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_buildings_1717
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_buildings_1789
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_buildings_1839
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_buildings_1850
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" AS double precision), cast("SHP_Area" AS double precision)
FROM sansecondo_buildings_1852
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" AS double precision), cast("SHP_Area" AS double precision)
FROM sansecondo_buildings_1945
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" AS double precision), cast("SHP_Area" AS double precision)
FROM sansecondo_buildings_1982
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", cast("Height" AS double precision), "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" AS double precision), cast("SHP_Area" AS double precision)
FROM sansecondo_buildings_2019;

-- Create sansecondo_buildings
DROP TABLE IF EXISTS PUBLIC.__sansecondo_buildings;
CREATE TABLE PUBLIC.__sansecondo_buildings_tmp AS 
  SELECT DISTINCT 
  "BW_ID" AS identifier, 
  CASE WHEN "Date" = '1500' THEN 1 ELSE 0 END AS "1500",
  CASE WHEN "Date" = '1697' THEN 1 ELSE 0 END AS "1697",
  CASE WHEN "Date" = '1717' THEN 1 ELSE 0 END AS "1717",
  CASE WHEN "Date" = '1789' THEN 1 ELSE 0 END AS "1789",
  CASE WHEN "Date" = '1839' THEN 1 ELSE 0 END AS "1839",
  CASE WHEN "Date" = '1850' THEN 1 ELSE 0 END AS "1850",
  CASE WHEN "Date" = '1852' THEN 1 ELSE 0 END AS "1852",
  CASE WHEN "Date" = '1945' THEN 1 ELSE 0 END AS "1945",
  CASE WHEN "Date" = '1982' THEN 1 ELSE 0 END AS "1982",
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM sansecondo_buildings_data;

-- Create san_secondo_islands_data
-- I.e., the UNION among all the tables
DROP TABLE IF EXISTS PUBLIC.sansecondo_islands_data;
CREATE TABLE PUBLIC.sansecondo_islands_data AS
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1500
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1697
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1717
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1789
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1839
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1850
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1852
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1945
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_1982
UNION
SELECT id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_tenant" as "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
FROM sansecondo_island_2019;

-- Create sansecondo_islands
DROP TABLE IF EXISTS PUBLIC.__sansecondo_islands;
CREATE TABLE PUBLIC.__sansecondo_islands_tmp AS
SELECT DISTINCT 
  "BW_ID" AS identifier, 
  CASE WHEN "Date" = '1500' THEN 1 ELSE 0 END AS "1500",
  CASE WHEN "Date" = '1697' THEN 1 ELSE 0 END AS "1697",
  CASE WHEN "Date" = '1717' THEN 1 ELSE 0 END AS "1717",
  CASE WHEN "Date" = '1789' THEN 1 ELSE 0 END AS "1789",
  CASE WHEN "Date" = '1839' THEN 1 ELSE 0 END AS "1839",
  CASE WHEN "Date" = '1850' THEN 1 ELSE 0 END AS "1850",
  CASE WHEN "Date" = '1852' THEN 1 ELSE 0 END AS "1852",
  CASE WHEN "Date" = '1945' THEN 1 ELSE 0 END AS "1945",
  CASE WHEN "Date" = '1982' THEN 1 ELSE 0 END AS "1982",
  CASE WHEN "Date" = '2019' THEN 1 ELSE 0 END AS "2019",
  geometry
FROM PUBLIC.sansecondo_islands_data;
