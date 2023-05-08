
-- Table containing the combination (feature_id, year)
DROP TABLE IF EXISTS PUBLIC.feature_years;
CREATE TABLE PUBLIC.feature_years(
  identifier VARCHAR(100) NOT NULL,
  "year" VARCHAR(255)
);

-- Function updating the year for a feature
CREATE OR REPLACE FUNCTION ALL_year() RETURNS TRIGGER AS $ALL_year$
   BEGIN
      INSERT INTO PUBLIC.feature_years(identifier, "year") 
      VALUES (new.identifier, 
        CASE
          WHEN new."Today" IS TRUE THEN 'Today'
		  WHEN new."1982: Ortofoto" IS TRUE THEN '1982: Ortofoto'
		  WHEN new."1943-45: RAF" IS TRUE THEN '1943-45: RAF'
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

-- Table containing all the features. The query is going to be executed on this
DROP TABLE IF EXISTS PUBLIC.veniss_data;
CREATE TABLE PUBLIC.veniss_data(
  identifier VARCHAR(100) NOT NULL,
  t VARCHAR(255),
  z INTEGER,
  geometry GEOMETRY
);

-- Function adding buildings 
CREATE OR REPLACE FUNCTION ALL_BLDG_feature() RETURNS TRIGGER AS $ALL_BLDG_feature$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, 'Buildings', 1, new.geometry);
      RETURN NEW;
   END;
$ALL_BLDG_feature$ LANGUAGE plpgsql;

-- Function adding islands
CREATE OR REPLACE FUNCTION ALL_IS_feature() RETURNS TRIGGER AS $ALL_IS_feature$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, 'Island', 0, new.geometry);
      RETURN NEW;
   END;
$ALL_IS_feature$ LANGUAGE plpgsql;

-- San Secondo buildings
DROP TABLE IF EXISTS PUBLIC.qgis_sansecondo_buildings;
CREATE TABLE PUBLIC.qgis_sansecondo_buildings(
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
CREATE TRIGGER SS_BLDG_INSERT_feature AFTER INSERT ON PUBLIC.qgis_sansecondo_buildings
FOR EACH ROW EXECUTE PROCEDURE ALL_BLDG_feature();
CREATE TRIGGER SS_BLDG_INSERT_year AFTER INSERT ON PUBLIC.qgis_sansecondo_buildings
FOR EACH ROW EXECUTE PROCEDURE ALL_year();

-- San Secondo islands
DROP TABLE IF EXISTS PUBLIC.qgis_sansecondo_islands;
CREATE TABLE PUBLIC.qgis_sansecondo_islands(
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
CREATE TRIGGER SS_BLDG_INSERT_feature AFTER INSERT ON PUBLIC.qgis_sansecondo_islands
FOR EACH ROW EXECUTE PROCEDURE ALL_IS_feature();
CREATE TRIGGER SS_BLDG_INSERT_year AFTER INSERT ON PUBLIC.qgis_sansecondo_islands
FOR EACH ROW EXECUTE PROCEDURE ALL_year();


-- Madonna del 

