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
drop table if exists sansecondo_buildings;
create table sansecondo_buildings as 
select distinct "BW_ID" as identifier, date(null) as "start_bob", date("Start") as "start_eob", 
case when "End" = '' then date(null) else date("End") end as "end_boe", date(null) as "end_eoe", geometry
from sansecondo_buildings_data;

-- Fix errors: see readme.md
delete from sansecondo_buildings
where identifier = 'SS_BLDG_052' and end_boe = '1788-12-31';

delete from sansecondo_buildings
where identifier = 'SS_BLDG_001' and end_boe = '2019-12-31';

-- Set the BW_ID as primary key
ALTER TABLE sansecondo_buildings
  ADD PRIMARY KEY (identifier);