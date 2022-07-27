-- Create sansecondo_openspaces_data
-- I.e., the union among all the tables
drop table if exists sansecondo_openspaces_data;
create table sansecondo_openspaces_data as
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_openspaces_1697
union
select id, geometry, "BW_ID", "IslandName", "Date", "Start", "End", "Name", "Function", "Start_Function", "End_Function", "Use", "Start_Use", "End_Use", "Typology", "Start_Typology", "End_Typology", "Owner", "Start_Owner", "End_Owner", "Tenant", "Start_Tenant", "End_Tenant", "SHP_Lenght", "SHP_Area"
from sansecondo_openspaces_1789;

-- Create sansecondo_openspaces
drop table if exists __sansecondo_openspaces;
create table __sansecondo_openspaces as 
select distinct "BW_ID" as identifier, date(null) as "start_bob", date("Start") as "start_eob", 
case when "End" = '' then date(null) else date("End") end as "end_boe", date(null) as "end_eoe", geometry,
'Open Spaces' as t, 2 as z
from sansecondo_openspaces_data;

-- Set the BW_ID as primary key
ALTER TABLE __sansecondo_openspaces
  ADD PRIMARY KEY (identifier);