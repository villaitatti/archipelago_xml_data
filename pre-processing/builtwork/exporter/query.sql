select distinct quote_ident(c.table_name) as tabs from information_schema.columns c join information_schema.tables t on t.table_name=c.table_name and t.table_schema=c.table_schema where t.table_name not like 'spatial_%' and t.table_name like 'sansecondo_buildings%' or t.table_name like 'sansecondo_open_spaces%' and t.table_type='BASE TABLE' and t.table_schema = 'public' ;

