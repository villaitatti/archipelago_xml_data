-- ########################################################################################
-- ############################# 01 Burano ################################################
-- ########################################################################################
DROP TABLE IF EXISTS PUBLIC.qgis_burano_buildings;
CREATE TABLE PUBLIC.qgis_burano_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
DROP TABLE IF EXISTS PUBLIC.qgis_burano_islands;
CREATE TABLE PUBLIC.qgis_burano_islands(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
DROP TABLE IF EXISTS PUBLIC.qgis_burano_openspaces;
CREATE TABLE PUBLIC.qgis_burano_openspaces(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
-- ########################################################################################
-- ############################# 02 Chioggia ##############################################
-- ########################################################################################
DROP TABLE IF EXISTS PUBLIC.qgis_chioggia_buildings;
CREATE TABLE PUBLIC.qgis_chioggia_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
DROP TABLE IF EXISTS PUBLIC.qgis_chioggia_islands;
CREATE TABLE PUBLIC.qgis_chioggia_islands(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
DROP TABLE IF EXISTS PUBLIC.qgis_chioggia_openspaces;
CREATE TABLE PUBLIC.qgis_chioggia_openspaces(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 

-- ########################################################################################
-- ############################# 03 Giudecca ##############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 04 Lido ##################################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 05 Murano ################################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 06 Mazzorbo ##############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 07 Pellestrina ###########################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 08 Sant'Erasmo ###########################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 09 Torcello ##############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 10 Vignole ###############################################
-- ########################################################################################


-- ########################################################################################
-- ############################# 01 Campalto ##############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 02 Certosa ###############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 03 Le Grazie #############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 04 Lazzaretto Nuovo ######################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 05 Lazzaretto Vecchio ####################################
-- ########################################################################################

DROP TABLE IF EXISTS PUBLIC.qgis_lazzarettovecchio_buildings;
CREATE TABLE PUBLIC.qgis_lazzarettovecchio_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_lazzarettovecchio_buildings
FOR EACH ROW EXECUTE PROCEDURE INSERT_BLDG_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_lazzarettovecchio_buildings
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

-- ########################################################################################
-- ############################# 06 Madonna del Monte #####################################
-- ########################################################################################
DROP TABLE IF EXISTS PUBLIC.qgis_madonnadelmonte_buildings;
CREATE TABLE PUBLIC.qgis_madonnadelmonte_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_madonnadelmonte_buildings
FOR EACH ROW EXECUTE PROCEDURE INSERT_BLDG_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_madonnadelmonte_buildings
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_madonnadelmonte_islands;
CREATE TABLE PUBLIC.qgis_madonnadelmonte_islands(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_madonnadelmonte_islands
FOR EACH ROW EXECUTE PROCEDURE INSERT_IS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_madonnadelmonte_islands
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_madonnadelmonte_openspaces;
CREATE TABLE PUBLIC.qgis_madonnadelmonte_openspaces(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_madonnadelmonte_openspaces
FOR EACH ROW EXECUTE PROCEDURE INSERT_OS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_madonnadelmonte_openspaces
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

-- ########################################################################################
-- ############################# 07 Monte dell'Oro ########################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 08 Poveglia ##############################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 08 San Clemente ##########################################
-- ########################################################################################
DROP TABLE IF EXISTS PUBLIC.qgis_sanclemente_buildings;
CREATE TABLE PUBLIC.qgis_sanclemente_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sanclemente_buildings
FOR EACH ROW EXECUTE PROCEDURE INSERT_BLDG_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sanclemente_buildings
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sanclemente_islands;
CREATE TABLE PUBLIC.qgis_sanclemente_islands(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sanclemente_islands
FOR EACH ROW EXECUTE PROCEDURE INSERT_IS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sanclemente_islands
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sanclemente_openspaces;
CREATE TABLE PUBLIC.qgis_sanclemente_openspaces(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sanclemente_openspaces
FOR EACH ROW EXECUTE PROCEDURE INSERT_OS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sanclemente_openspaces
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

-- ########################################################################################
-- ############################# 09 San Francesco del Deserto #############################
-- ########################################################################################

-- ########################################################################################
-- ############################# 10 San Giacomo in Paludo #################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 11 San Giorgio in Alga ###################################
-- ########################################################################################
CREATE OR REPLACE FUNCTION SGA_ALL_year() RETURNS TRIGGER AS $ALL_year$
   BEGIN
      INSERT INTO PUBLIC.feature_years(identifier, "year") 
      VALUES (new.identifier, 
        CASE
          WHEN new."Today" IS TRUE THEN 'Today'
          WHEN new."1982: Ortofoto" IS TRUE THEN '1982: Ortofoto'
          WHEN new."1943-45: RAF" IS TRUE THEN '1943-45: RAF'
          WHEN new."1931" IS TRUE THEN '1931'
          WHEN new."1850: Direzione genio militare" IS TRUE THEN '1850: Direzione genio militare'
          WHEN new."1838-41: Censo Stabile, Mappe Austriache - rettifica" IS TRUE THEN '1838-41: Censo Stabile, Mappe Austriache - rettifica'
          WHEN new."1830-31: Censo Stabile, Mappe Austriache" IS TRUE THEN '1830-31: Censo Stabile, Mappe Austriache'
          WHEN new."1807-10: Censo Stabile, Mappe Napoleoniche" IS TRUE THEN '1807-10: Censo Stabile, Mappe Napoleoniche'
          ELSE NULL
        END 
      );
      RETURN NEW;
   END;
$ALL_year$ LANGUAGE plpgsql;

DROP TABLE IF EXISTS PUBLIC.qgis_sangiorgioinalga_buildings;
CREATE TABLE PUBLIC.qgis_sangiorgioinalga_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1931" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sangiorgioinalga_buildings
FOR EACH ROW EXECUTE PROCEDURE INSERT_BLDG_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sangiorgioinalga_buildings
FOR EACH ROW EXECUTE PROCEDURE SGA_ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sangiorgioinalga_islands;
CREATE TABLE PUBLIC.qgis_sangiorgioinalga_islands(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1931" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sangiorgioinalga_islands
FOR EACH ROW EXECUTE PROCEDURE INSERT_IS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sangiorgioinalga_islands
FOR EACH ROW EXECUTE PROCEDURE SGA_ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sangiorgioinalga_openspaces;
CREATE TABLE PUBLIC.qgis_sangiorgioinalga_openspaces(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1931" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sangiorgioinalga_openspaces
FOR EACH ROW EXECUTE PROCEDURE INSERT_OS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sangiorgioinalga_openspaces
FOR EACH ROW EXECUTE PROCEDURE SGA_ALL_year();

-- ########################################################################################
-- ############################# 12 San Giorgio Maggiore ##################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 13 San Giuliano ##########################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 14 San Lazzaro degli Armeni ##############################
-- ########################################################################################

-- ########################################################################################
-- ############################# 15 San Michele ###########################################
-- ########################################################################################


-- ########################################################################################
-- ############################# 17 San Servolo ###########################################
-- ########################################################################################
DROP TABLE IF EXISTS PUBLIC.qgis_sanservolo_buildings;
CREATE TABLE PUBLIC.qgis_sanservolo_buildings(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sanservolo_buildings
FOR EACH ROW EXECUTE PROCEDURE INSERT_BLDG_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sanservolo_buildings
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sanservolo_islands;
CREATE TABLE PUBLIC.qgis_sanservolo_islands(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sanservolo_islands
FOR EACH ROW EXECUTE PROCEDURE INSERT_IS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sanservolo_islands
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sanservolo_openspaces;
CREATE TABLE PUBLIC.qgis_sanservolo_openspaces(
  identifier VARCHAR(100) NOT NULL,
  "Today" BOOLEAN NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" BOOLEAN NOT NULL DEFAULT FALSE,
  "1943-45: RAF" BOOLEAN NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" BOOLEAN NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" BOOLEAN NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" BOOLEAN NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" BOOLEAN NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
); 
CREATE TRIGGER INSERT_feature AFTER INSERT ON PUBLIC.qgis_sanservolo_openspaces
FOR EACH ROW EXECUTE PROCEDURE INSERT_OS_feature();
CREATE TRIGGER INSERT_year AFTER INSERT ON PUBLIC.qgis_sanservolo_openspaces
FOR EACH ROW EXECUTE PROCEDURE ALL_year();


-- ########################################################################################
-- ############################# 18 Sant'Andrea ###########################################
-- ########################################################################################

-- ########################################################################################
-- ############################# 19 Sant'Angelo della Polvere #############################
-- ########################################################################################

-- ########################################################################################
-- ############################# 20 Santo Spirito #########################################
-- ########################################################################################