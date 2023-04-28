-- Create san_secondo_islands_data
-- I.e., the union among all the tables
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
DROP TABLE IF EXISTS PUBLIC.__sansecondo_islands_tmp;
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
  geometry,
  'Buildings' AS t, 
  2 AS z
FROM PUBLIC.sansecondo_islands_data;

-- Create table for the years, if not exists

-- ATTENTION: DO NOT UNCOMMENT NEXT LINE UNLESS YOU KNOW WHAT YOU ARE DOING 
-- DROP TABLE IF EXISTS public.feature_years;
CREATE TABLE IF NOT EXISTS public.feature_years(
	identifier VARCHAR(100) NOT NULL,
	y VARCHAR(100) NOT NULL
);

-- 1500
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1500' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1500" = 1;
-- 1697
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1697' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1697" = 1;
-- 1717
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1717' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1717" = 1;
-- 1789
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1789' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1789" = 1;
-- 1839
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1839' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1839" = 1;
-- 1850
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1850' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1850" = 1;
-- 1852
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1852' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1852" = 1;
-- 1945
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1945' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1945" = 1;
-- 1982
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '1982' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "1982" = 1;
-- 2019
INSERT INTO PUBLIC.feature_years(identifier, y)
	SELECT identifier, '2019' AS y FROM PUBLIC.__sansecondo_islands_tmp WHERE "2019" = 1;

-- Create sansecondo_island
DROP TABLE IF EXISTS PUBLIC.sansecondo_islands;
CREATE TABLE PUBLIC.sansecondo_islands AS
  SELECT DISTINCT identifier, 'Islands' AS t, 2 AS z, geometry FROM PUBLIC.__sansecondo_islands_tmp GROUP BY identifier, t, z, geometry;

DROP TABLE IF EXISTS PUBLIC.__sansecondo_islands_tmp;

-- Set the BW_ID as primary key
ALTER TABLE PUBLIC.sansecondo_islands
  ADD PRIMARY KEY (identifier);