/**************************************************************************************************/

// new OpenLayers.Projection("EPSG:4326");
var proj_4326 = ol.proj.get('EPSG:4326');
var proj_3857 = ol.proj.get('EPSG:3857');

/**************************************************************************************************/

var map = new ol.Map({
  target: 'map',
  controls: ol.control.defaults({
    attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
      collapsible: false
    })
  }),
  view: new ol.View({
    zoom: 15,
    center: ol.proj.transform([center.longitude, center.latitude], 'EPSG:4326', 'EPSG:3857')
  })
});

/**************************************************************************************************/

var resolutions = [];
var matrix_ids = [];
var resolution_max = ol.extent.getWidth(proj_3857.getExtent()) / 256;

for (var i = 0; i < 18; i++) {
  matrix_ids[i] = i.toString();
  resolutions[i] = resolution_max / Math.pow(2, i);
}

var tile_grid = new ol.tilegrid.WMTS({
  origin: [-20037508, 20037508],
  resolutions: resolutions,
  matrixIds: matrix_ids
});

// Géoportail API Key
var key = 'usho1r0e3pl581viejhrjfsf';

var ign_source = new ol.source.WMTS({
  url: 'http://wxs.ign.fr/' + key + '/wmts',
  layer: 'GEOGRAPHICALGRIDSYSTEMS.MAPS',
  matrixSet: 'PM',
  format: 'image/jpeg',
  projection: 'EPSG:3857',
  tileGrid: tile_grid,
  style: 'normal',
  attributions: [new ol.Attribution({
    html: '<a href="http://www.geoportail.fr/" target="_blank">' +
      '<img src="http://api.ign.fr/geoportail/api/js/latest/' +
      'theme/geoportal/img/logo_gp.gif"></a>'
  })]
});

var ign = new ol.layer.Tile({
  source: ign_source
});

map.addLayer(ign);

/**************************************************************************************************/

var styles = {
  'GeometryCollection': [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
	color: 'rgba(255, 0, 0, .25)'
      }),
      stroke: new ol.style.Stroke({
        color: 'red',
	width: 2
      })
    })
  })]
};

var style_function = function(feature, resolution) {
  return styles[feature.getGeometry().getType()];
};

var geojson_data = {
  'type': 'FeatureCollection',
  'crs': {
    'type': 'name',
    'properties': {
      'name': 'EPSG:4326'
    }
  },
  'features': [
    {
      'type': 'Feature',
      'geometry': {
        'type': 'GeometryCollection',
        'geometries': [
          {
            'type': 'MultiPoint',
	    'coordinates': [[center.longitude, center.latitude],
			    [center.longitude + .01, center.latitude]]
          },
        ]
      }
    }
  ]
};

var vector_source = new ol.source.Vector({
  // readProjection(geojson_object),
  features: (new ol.format.GeoJSON()).readFeatures(geojson_data,
						   {'dataProjection': proj_4326,
						    'featureProjection': proj_3857})
});

var vector_layer = new ol.layer.Vector({
  source: vector_source,
  style: style_function
});

map.addLayer(vector_layer);

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
