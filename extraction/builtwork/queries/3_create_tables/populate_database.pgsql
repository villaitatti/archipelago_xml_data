INSERT INTO PUBLIC.qgis_madonnadelmonte_buildings(identifier, "Today", geometry)
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
	geometry
FROM IMPORTED.__madonnadelmonte_buildings;

INSERT INTO PUBLIC.qgis_madonnadelmonte_islands(identifier, "Today", "1982: Ortofoto", geometry)
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
  CASE WHEN "1982" IS TRUE THEN TRUE ELSE FALSE END as "1982: Ortofoto",
	geometry
FROM IMPORTED.__madonnadelmonte_islands

-------------------------------------------------------------------------------------

INSERT INTO PUBLIC.qgis_sanclemente_buildings(identifier, "Today", "1982: Ortofoto", geometry)
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
  CASE WHEN "1982" IS TRUE THEN TRUE ELSE FALSE END as "1982: Ortofoto",
	geometry
FROM IMPORTED.__sanclemente_buildings;

INSERT INTO PUBLIC.qgis_sanclemente_islands(identifier, "Today", "1982: Ortofoto", geometry)
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
  CASE WHEN "1982" IS TRUE THEN TRUE ELSE FALSE END as "1982: Ortofoto",
	geometry
FROM IMPORTED.__sanclemente_islands;

INSERT INTO PUBLIC.qgis_sanclemente_openspaces(identifier, "Today", geometry)
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
	geometry
FROM IMPORTED.__sanclemente_openspaces;

-------------------------------------------------------------------------------------

INSERT INTO PUBLIC.qgis_sangiorgioinalga_buildings(identifier, "Today", geometry)
SELECT 
	identifier,
	CASE WHEN "2023" IS TRUE THEN TRUE ELSE FALSE END as "Today",
	geometry
FROM IMPORTED.__sangiorgioinalga_buildings;

INSERT INTO PUBLIC.qgis_sangiorgioinalga_islands(identifier, "Today", "1982: Ortofoto", "1943-45: RAF", "1931", geometry)
SELECT 
	identifier,
	CASE WHEN "2023" IS TRUE THEN TRUE ELSE FALSE END as "Today",
  CASE WHEN "1982" IS TRUE THEN TRUE ELSE FALSE END as "1982: Ortofoto",
  CASE WHEN "1944" IS TRUE THEN TRUE ELSE FALSE END as "1943-45: RAF",
  CASE WHEN "1931" IS TRUE THEN TRUE ELSE FALSE END as "1931",
	geometry
FROM IMPORTED.__sangiorgioinalga_islands;

-------------------------------------------------------------------------------------

INSERT INTO PUBLIC.qgis_sanservolo_buildings(identifier, "Today", geometry)
SELECT 
	identifier,
	CASE WHEN "2019" IS TRUE THEN TRUE ELSE FALSE END as "Today",
	geometry
FROM IMPORTED.__sanservolo_buildings;