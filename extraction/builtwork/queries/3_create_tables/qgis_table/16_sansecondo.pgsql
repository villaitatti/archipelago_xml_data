-- ########################################################################################
-- ############################## San Secondo  ############################################
-- ########################################################################################
-- Create a function to store the tuple feature year.
-- This is important to remember the specific year where a feature existed
CREATE OR REPLACE FUNCTION SS_ALL_year()
  RETURNS TRIGGER
  AS $ALL_year$
BEGIN
  INSERT INTO PUBLIC.feature_years(identifier, "year")
    VALUES(NEW.identifier, CASE WHEN NEW."Today" IS TRUE THEN
        'Today'
      WHEN NEW. "1982: Ortofoto" IS TRUE THEN
        '1982: Ortofoto'
      WHEN NEW. "1943-45: RAF" IS TRUE THEN
        '1943-45: RAF'
      WHEN NEW. "1850: Direzione genio militare" IS TRUE THEN
        '1850: Direzione genio militare'
      WHEN NEW. "1838-41: Censo Stabile, Mappe Austriache - rettifica" IS TRUE THEN
        '1838-41: Censo Stabile, Mappe Austriache - rettifica'
      WHEN NEW. "1830-31: Censo Stabile, Mappe Austriache" IS TRUE THEN
        '1830-31: Censo Stabile, Mappe Austriache'
      WHEN NEW. "1807-10: Censo Stabile, Mappe Napoleoniche" IS TRUE THEN
        '1807-10: Censo Stabile, Mappe Napoleoniche'
      WHEN NEW."1789" IS TRUE THEN
        '1789'
      WHEN NEW."1697" IS TRUE THEN
        '1697'
      ELSE
        NULL
      END);
  RETURN NEW;
END;
$ALL_year$
LANGUAGE plpgsql;

DROP TABLE IF EXISTS PUBLIC.qgis_sansecondo_buildings;

CREATE TABLE PUBLIC.qgis_sansecondo_buildings(
  identifier varchar(100) NOT NULL PRIMARY KEY,
  "Today" boolean NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" boolean NOT NULL DEFAULT FALSE,
  "1943-45: RAF" boolean NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" boolean NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" boolean NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" boolean NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" boolean NOT NULL DEFAULT FALSE,
  "1789" boolean NOT NULL DEFAULT FALSE,
  "1697" boolean NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);

CREATE TRIGGER INSERT_feature
  AFTER INSERT ON PUBLIC.qgis_sansecondo_buildings
  FOR EACH ROW
  EXECUTE PROCEDURE INSERT_BLDG_feature();

CREATE TRIGGER DELETE_feature
  AFTER INSERT ON PUBLIC.qgis_sansecondo_buildings
  FOR EACH ROW
  EXECUTE PROCEDURE DELETE_BLDG_feature();

CREATE TRIGGER UPDATE_feature
  AFTER INSERT ON PUBLIC.qgis_sansecondo_buildings
  FOR EACH ROW
  EXECUTE PROCEDURE UPDATE_BLDG_feature();

CREATE TRIGGER SS_ALL_year
  AFTER INSERT ON PUBLIC.qgis_sansecondo_buildings
  FOR EACH ROW
  EXECUTE PROCEDURE SS_ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sansecondo_islands;

CREATE TABLE PUBLIC.qgis_sansecondo_islands(
  identifier varchar(100) NOT NULL,
  "Today" boolean NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" boolean NOT NULL DEFAULT FALSE,
  "1943-45: RAF" boolean NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" boolean NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" boolean NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" boolean NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" boolean NOT NULL DEFAULT FALSE,
  "1697" boolean NOT NULL DEFAULT FALSE,
  "1789" boolean NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);

CREATE TRIGGER INSERT_feature
  AFTER INSERT ON PUBLIC.qgis_sansecondo_islands
  FOR EACH ROW
  EXECUTE PROCEDURE INSERT_IS_feature();

CREATE TRIGGER SS_ALL_year
  AFTER INSERT ON PUBLIC.qgis_sansecondo_islands
  FOR EACH ROW
  EXECUTE PROCEDURE SS_ALL_year();

DROP TABLE IF EXISTS PUBLIC.qgis_sansecondo_openspaces;

CREATE TABLE PUBLIC.qgis_sansecondo_openspaces(
  identifier varchar(100) NOT NULL,
  "Today" boolean NOT NULL DEFAULT FALSE,
  "1982: Ortofoto" boolean NOT NULL DEFAULT FALSE,
  "1943-45: RAF" boolean NOT NULL DEFAULT FALSE,
  "1850: Direzione genio militare" boolean NOT NULL DEFAULT FALSE,
  "1838-41: Censo Stabile, Mappe Austriache - rettifica" boolean NOT NULL DEFAULT FALSE,
  "1830-31: Censo Stabile, Mappe Austriache" boolean NOT NULL DEFAULT FALSE,
  "1807-10: Censo Stabile, Mappe Napoleoniche" boolean NOT NULL DEFAULT FALSE,
  "1697" boolean NOT NULL DEFAULT FALSE,
  "1789" boolean NOT NULL DEFAULT FALSE,
  geometry GEOMETRY
);

CREATE TRIGGER INSERT_feature
  AFTER INSERT ON PUBLIC.qgis_sansecondo_openspaces
  FOR EACH ROW
  EXECUTE PROCEDURE INSERT_OS_feature();

CREATE TRIGGER SS_ALL_year
  AFTER INSERT ON PUBLIC.qgis_sansecondo_openspaces
  FOR EACH ROW
  EXECUTE PROCEDURE SS_ALL_year();

INSERT INTO PUBLIC.years_dates
  VALUES ('1789', 1789, 1789),
('1697', 1697, 1697);

-- Populate database
INSERT INTO PUBLIC.qgis_sansecondo_buildings(identifier, "Today", "1982: Ortofoto", "1943-45: RAF", "1850: Direzione genio militare", "1838-41: Censo Stabile, Mappe Austriache - rettifica", "1789", "1697", geometry)
SELECT DISTINCT
  identifier,
  BOOL_OR(
    CASE WHEN "2019" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "Today",
  BOOL_OR(
    CASE WHEN "1982" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "1982: Ortofoto",
  BOOL_OR(
    CASE WHEN "1945" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "1943-45: RAF",
  BOOL_OR(
    CASE WHEN "1852" IS TRUE
      OR "1850" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "1850: Direzione genio militare",
  BOOL_OR(
    CASE WHEN "1839" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "1838-41: Censo Stabile, Mappe Austriache - rettifica",
  BOOL_OR(
    CASE WHEN "1789" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "1789",
  BOOL_OR(
    CASE WHEN "1697" IS TRUE THEN
      TRUE
    ELSE
      FALSE
    END) AS "1697",
  geometry
FROM
  IMPORTED.__sansecondo_buildings
GROUP BY
  identifier,
  geometry;

