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
CREATE OR REPLACE FUNCTION INSERT_BLDG_feature() RETURNS TRIGGER AS $INSERT_BLDG_feature$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, 'Buildings', 1, new.geometry);
      RETURN NEW;
   END;
$INSERT_BLDG_feature$ LANGUAGE plpgsql;

-- Function adding islands
CREATE OR REPLACE FUNCTION INSERT_IS_feature() RETURNS TRIGGER AS $INSERT_IS_feature$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, 'Island', 0, new.geometry);
      RETURN NEW;
   END;
$INSERT_IS_feature$ LANGUAGE plpgsql;

-- Function adding islands
CREATE OR REPLACE FUNCTION INSERT_OS_feature() RETURNS TRIGGER AS $INSERT_OS_feature$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, 'Open Space', 1, new.geometry);
      RETURN NEW;
   END;
$INSERT_OS_feature$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION INSERT_WV_feature() RETURNS TRIGGER AS $INSERT_WV_feature$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, 'Water way', -1, new.geometry);
      RETURN NEW;
   END;
$INSERT_WV_feature$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION REMOVE_feature() RETURNS TRIGGER AS $REMOVE_feature$
   BEGIN
      DELETE FROM PUBLIC.veniss_data
      WHERE identifier = OLD.identifier
      RETURN OLD;
   END;
$REMOVE_feature$ LANGUAGE plpgsql;