-- Create san_secondo_buildings_data
-- I.e., the union among all the tables
drop table if exists sansecondo_buildings_data;
create table sansecondo_buildings_data as
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_buildings_1500
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_buildings_1697
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_buildings_1717
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_buildings_1789
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_buildings_1839
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_buildings_1850
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" as double precision), cast("SHP_Area" as double precision)
from sansecondo_buildings_1852
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" as double precision), cast("SHP_Area" as double precision)
from sansecondo_buildings_1945
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Height", "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" as double precision), cast("SHP_Area" as double precision)
from sansecondo_buildings_1982
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", cast("Height" as double precision), "Material", "Architect", "Patron", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", cast("SHP_Lenght" as double precision), cast("SHP_Area" as double precision)
from sansecondo_buildings_2019;

-- Create sansecondo_buildings
drop table if exists __sansecondo_buildings_tmp;
create table __sansecondo_buildings_tmp as 
select distinct 
  "BW_ID" as identifier, 
  case when "Date" = '1500' then 1 else 0 end as "1500",
  case when "Date" = '1697' then 1 else 0 end as "1697",
  case when "Date" = '1717' then 1 else 0 end as "1717",
  case when "Date" = '1789' then 1 else 0 end as "1789",
  case when "Date" = '1839' then 1 else 0 end as "1839",
  case when "Date" = '1850' then 1 else 0 end as "1850",
  case when "Date" = '1852' then 1 else 0 end as "1852",
  case when "Date" = '1945' then 1 else 0 end as "1945",
  case when "Date" = '1982' then 1 else 0 end as "1982",
  case when "Date" = '2019' then 1 else 0 end as "2019",
  geometry,
  'Buildings' as t, 
  2 as z
from sansecondo_buildings_data;

drop table if exists __sansecondo_buildings;
create table __sansecondo_buildings as
select distinct 
  identifier,
  CAST(CASE WHEN SUM(CAST("1500" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1500",
  CAST(CASE WHEN SUM(CAST("1697" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1697",
  CAST(CASE WHEN SUM(CAST("1717" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1717",
  CAST(CASE WHEN SUM(CAST("1789" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1789",
  CAST(CASE WHEN SUM(CAST("1839" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1839",
  CAST(CASE WHEN SUM(CAST("1850" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1850",
  CAST(CASE WHEN SUM(CAST("1852" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1852",
  CAST(CASE WHEN SUM(CAST("1945" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1945",
  CAST(CASE WHEN SUM(CAST("1982" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "1982",
  CAST(CASE WHEN SUM(CAST("2019" AS INT)) > 0 THEN 1 ELSE 0 END AS bool) AS "2019",
  'Buildings' as t, 2 as z, geometry
from __sansecondo_buildings_tmp
group by identifier, t, z, geometry;

drop table if exists __sansecondo_buildings_tmp;

-- Fix errors: see readme.md

-- Set the BW_ID as primary key
ALTER TABLE __sansecondo_buildings
  ADD PRIMARY KEY (identifier);