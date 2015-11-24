
for i in massif circuit place ; do
  ./bin/importer --write-geojson=data/bleau-${i}s-geo.json --${i}s data/bleau.json
  ./bin/importer --write-geojson=share/WebApplication/static/data/bleau-${i}s-geoson.js --js-var=${i}_geojson --${i}s data/bleau.json
done

./bin/importer --write-gpx=data/bleau.gpx --massifs --circuits --places data/bleau.json

####################################################################################################
#
# End
#
####################################################################################################
