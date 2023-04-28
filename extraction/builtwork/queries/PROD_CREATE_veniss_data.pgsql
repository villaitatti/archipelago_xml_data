DROP TABLE IF EXISTS PUBLIC.veniss_data;
CREATE TABLE PUBLIC.veniss_data(
  --id INTEGER DEFAULT(nextval('certosa_buildings_id_seq'::regclass)) NOT NULL,
  identifier VARCHAR(100) NOT NULL,
  t VARCHAR(255),
  z INTEGER,
  geometry GEOMETRY
);

CREATE OR REPLACE FUNCTION update_veniss_data() RETURNS TRIGGER AS $update_veniss_data$
   BEGIN
      INSERT INTO PUBLIC.veniss_data(identifier, t, z, geometry) 
      VALUES (new.identifier, new.t, new.z, new.geometry);
      RETURN NEW;
   END;
$update_veniss_data$ LANGUAGE plpgsql;


