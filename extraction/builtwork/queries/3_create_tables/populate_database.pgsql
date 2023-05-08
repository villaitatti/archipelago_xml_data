INSERT INTO PUBLIC.qgis_sansecondo_buildings
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
	CASE WHEN "1982" IS TRUE THEN TRUE ELSE FALSE END as "1982: Ortofoto",
	CASE WHEN "1945" IS TRUE THEN TRUE ELSE FALSE END as "1943-45: RAF",
	CASE WHEN "1852" IS TRUE OR "1850" IS TRUE THEN TRUE ELSE FALSE END as "1850: Direzione genio militare",
	CASE WHEN "1839" IS TRUE THEN TRUE ELSE FALSE END as "1838-41: Censo Stabile, Mappe Austriache - rettifica",
	FALSE as "1830-31: Censo Stabile, Mappe Austriache",
	FALSE as "1807-10: Censo Stabile, Mappe Napoleoniche",
	geometry
FROM PUBLIC.sansecondo_buildings_data