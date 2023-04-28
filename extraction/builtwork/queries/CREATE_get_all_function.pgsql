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
      'SELECT distinct t."BW_ID", t.geometry as geo
	   FROM public.' || formal_table || ' t 
	   WHERE t."BW_ID" IS NOT NULL';
   END LOOP;
END;
