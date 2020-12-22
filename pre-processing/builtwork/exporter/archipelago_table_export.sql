
create or replace function archipelago_table_export()
    returns table("BW_ID" CHARACTER VARYING, "IslandName" CHARACTER VARYING, 
    "Date" bigint, "Start" CHARACTER VARYING, "End" CHARACTER VARYING, "Name" CHARACTER VARYING, 
    "Function" CHARACTER VARYING, "Start_Function" CHARACTER VARYING, "End_Function" CHARACTER VARYING, 
    "Use" CHARACTER VARYING, "Start_Use" CHARACTER VARYING, "End_Use" CHARACTER VARYING, 
    "Typology" CHARACTER VARYING, "Start_Typology" CHARACTER VARYING, "End_Typology" CHARACTER VARYING, 
    "Height" CHARACTER VARYING, "Material" CHARACTER VARYING, "Architect" CHARACTER VARYING, "Patron" CHARACTER VARYING,
    "Owner" CHARACTER VARYING, "Start_Owner" CHARACTER VARYING, "End_Owner" CHARACTER VARYING,
    "Tenant" CHARACTER VARYING, "Start_Tenant" CHARACTER VARYING, "End_Tenant" CHARACTER VARYING,
    "SHP_Length" CHARACTER VARYING, "SHP_Area" CHARACTER VARYING)
    language plpgsql
    as
$$
DECLARE
   formal_table text;
BEGIN
   FOR formal_table IN
      	select distinct quote_ident(c.table_name)
		from information_schema.columns c
		join information_schema.tables t on t.table_name=c.table_name and t.table_schema=c.table_schema
		where t.table_name not like 'spatial_%'
		and t.table_type='BASE TABLE'
		and t.table_schema = 'public'
   LOOP
      RETURN QUERY EXECUTE
      'SELECT distinct t."BW_ID",t."IslandName",t."Date",t."Start",t."End",t."Name",t."Function",t."Start_Function",t."End_Function",t."Use",t."Start_Use",t."End_Use",t."Typology",t."Start_Typology",t."End_Typology",t."Height",t."Material",t."Architect",t."Patron",t."Owner",t."Start_Owner",t."End_Owner",t."Tenant",t."Start_Tenant",t."End_Tenant",t."SHP_Lenght",t."SHP_Area"
	   FROM public.' || formal_table || ' t 
	   WHERE t."BW_ID" IS NOT NULL';
   END LOOP;
END;
$$