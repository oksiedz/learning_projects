DECLARE @Nigeria_geom Geometry = (SELECT ogr_geometry from countries where sovereignt ='Nigeria');
DECLARE @Nigeria geography = geography::STGeomFromText(@Nigeria_geom.ToString(),4326);

DECLARE @Poland_geom Geometry = (SELECT ogr_geometry from countries where sovereignt ='Poland');
DECLARE @Poland geography = geography::STGeomFromText(@Poland_geom.ToString(),4326);
SELECT @Nigeria.STDistance(@Poland);