\copy (select "BW_ID","IslandName","Date","Start","End","Name","Function","Start_Function","End_Function","Use","Start_Use","End_Use","Typology","Start_Typology","End_Typology","Height","Material","Architect","Patron","Owner","Start_Owner","End_Owner","Tenant","Start_Tenant","End_Tenant","SHP_Lenght","SHP_Area"
 from "public"."sansecondo_buildings_1697") TO 'DATA.tsv' CSV HEADER DELIMITER E'\t'
