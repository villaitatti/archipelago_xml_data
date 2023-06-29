-- ####################################################################################################
-- ############################################  Veniss data #########################################
-- ####################################################################################################
-- Table containing all the features.
-- The main query in VeNiss is going to be executed on this table
DROP TABLE IF EXISTS PUBLIC.veniss_data;

CREATE TABLE PUBLIC.veniss_data(
  identifier varchar(100) NOT NULL,
  t varchar(255),
  z integer,
  geometry GEOMETRY
);

-- Create a function called when a new feature is added to a specific table
-- This function creates the same feature in the veniss_data table
CREATE OR REPLACE FUNCTION INSERT_BLDG_feature()
  RETURNS TRIGGER
  AS $INSERT_BLDG_feature$
BEGIN
  INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry)
    VALUES(NEW.identifier, 'Buildings', 1, NEW.geometry);
  RETURN NEW;
END;
$INSERT_BLDG_feature$
LANGUAGE plpgsql;

-- Create a function called when a feature is removed from a specific table
-- This function removes the same feature from the veniss_data table
CREATE OR REPLACE FUNCTION DELETE_BLDG_feature()
  RETURNS TRIGGER
  AS $DELETE_BLDG_feature$
BEGIN
  DELETE FROM PUBLIC.veniss_data
  WHERE identifier = OLD.identifier;
  RETURN OLD;
END;
$DELETE_BLDG_feature$
LANGUAGE plpgsql;

-- Create a function called when a feature is updated in a specific table
-- This function updates the same feature in the veniss_data table
CREATE OR REPLACE FUNCTION UPDATE_BLDG_feature()
  RETURNS TRIGGER
  AS $UPDATE_BLDG_feature$
BEGIN
  UPDATE
    PUBLIC.veniss_data
  SET
    geometry = NEW.geometry
  WHERE
    identifier = NEW.identifier;
  RETURN NEW;
END;
$UPDATE_BLDG_feature$
LANGUAGE plpgsql;

-- Function adding islands
CREATE OR REPLACE FUNCTION INSERT_IS_feature()
  RETURNS TRIGGER
  AS $INSERT_IS_feature$
BEGIN
  INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry)
    VALUES(NEW.identifier, 'Island', 0, NEW.geometry);
  RETURN NEW;
END;
$INSERT_IS_feature$
LANGUAGE plpgsql;

-- Function adding islands
CREATE OR REPLACE FUNCTION INSERT_OS_feature()
  RETURNS TRIGGER
  AS $INSERT_OS_feature$
BEGIN
  INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry)
    VALUES(NEW.identifier, 'Open Space', 1, NEW.geometry);
  RETURN NEW;
END;
$INSERT_OS_feature$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION INSERT_WV_feature()
  RETURNS TRIGGER
  AS $INSERT_WV_feature$
BEGIN
  INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry)
    VALUES(NEW.identifier, 'Water way', -1, NEW.geometry);
  RETURN NEW;
END;
$INSERT_WV_feature$
LANGUAGE plpgsql;

