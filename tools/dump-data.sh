
for i in massif circuit place ; do
  echo $i.json
  ./bin/importer --write-geojson=data/bleau-${i}s-geo.json --${i}s data/bleau.json
  echo $i.js
  ./bin/importer --write-geojson=share/WebApplication/static/data/bleau-${i}s-geoson.js --js-var=${i}_geojson --${i}s data/bleau.json
done

echo GPX
./bin/importer --write-gpx=data/bleau.gpx --massifs --circuits --places data/bleau.json

####################################################################################################
#
# End
#
####################################################################################################
