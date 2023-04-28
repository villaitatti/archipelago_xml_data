DROP TABLE IF EXISTS PUBLIC.sansecondo_buildings;
CREATE TABLE PUBLIC.sansecondo_buildings(
  --id INTEGER DEFAULT(nextval('certosa_buildings_id_seq'::regclass)) NOT NULL,
  identifier VARCHAR(100) NOT NULL,
  t VARCHAR(255),
  z INTEGER,
  geometry GEOMETRY
);

DROP TABLE IF EXISTS PUBLIC.sansecondo_islands;
CREATE TABLE PUBLIC.sansecondo_islands(
  --id INTEGER DEFAULT(nextval('certosa_buildings_id_seq'::regclass)) NOT NULL,
  identifier VARCHAR(100) NOT NULL,
  t VARCHAR(255),
  z INTEGER,
  geometry GEOMETRY
);

DROP TABLE IF EXISTS PUBLIC.feature_years;
CREATE TABLE IF NOT EXISTS PUBLIC.feature_years(
	identifier VARCHAR(100) NOT NULL,
	y VARCHAR(100) NOT NULL
);