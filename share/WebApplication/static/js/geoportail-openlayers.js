/**************************************************************************************************/

// Fixme: use JQuery
// document.getElementById('mouse-position')

/**************************************************************************************************/

// new OpenLayers.Projection('EPSG:4326');
var proj_4326 = ol.proj.get('EPSG:4326');
var proj_3857 = ol.proj.get('EPSG:3857');

/**************************************************************************************************/

var mouse_position_control = new ol.control.MousePosition({
  coordinateFormat: ol.coordinate.createStringXY(4),
  projection: 'EPSG:4326',
  // comment the following two lines to have the mouse position be placed within the map.
  className: 'custom-mouse-position',
  target: document.getElementById('mouse-position'),
  undefinedHTML: '&nbsp;'
});

var projection_select = $('#projection');
projection_select.on('change', function() {
  mouse_position_control.setProjection(ol.proj.get(this.value));
});
projection_select.val(mouse_position_control.getProjection().getCode());

var precision_input = $('#precision');
precision_input.on('change', function() {
  var format = ol.coordinate.createStringXY(this.valueAsNumber);
  mouse_position_control.setCoordinateFormat(format);
});

/**************************************************************************************************/

var center_in_mercator = ol.proj.transform([center.longitude, center.latitude],
					   'EPSG:4326', 'EPSG:3857');
var extent_margin = 1000; // m

var map = new ol.Map({
  target: document.getElementById('map'),
  controls: ol.control.defaults({
    attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
      collapsible: false
    })
  }).extend([
    new ol.control.ZoomToExtent({
      extent: [
	center_in_mercator[0] - extent_margin, center_in_mercator[1] - extent_margin,
	center_in_mercator[0] + extent_margin, center_in_mercator[1] + extent_margin
      ]
    }),
    mouse_position_control]),
  view: new ol.View({
    zoom: 15,
    center: center_in_mercator
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

var ign_source = new ol.source.WMTS({
  url: 'http://wxs.ign.fr/' + geoportail_api_key + '/wmts',
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
  // GeometryCollection
  'default': [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
	color: 'rgba(0, 0, 255, .5)'
      }),
      stroke: new ol.style.Stroke({
        color: 'blue',
	width: 2
      })
    })
  })],
  'current': [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
	color: 'rgba(255, 0, 0, .5)'
      }),
      stroke: new ol.style.Stroke({
        color: 'red',
	width: 2
      })
    })
  })]
};

var style_function = function(feature, resolution) {
  // return styles[feature.getGeometry().getType()];
  // console.log(feature, resolution);
  // console.log(feature.getProperties());
  if (feature.get('massif') == massif_name)
    return styles['current'];
  else
    return styles['default'];
};

var geojson_source = new ol.source.Vector({
  // feature loader http://openlayersbook.github.io/ch05-using-vector-layers/example-03.html
  // readProjection(geojson_object),
  features: (new ol.format.GeoJSON()).readFeatures(geojson_data,
						   {'dataProjection': proj_4326,
						    'featureProjection': proj_3857})
});

var geojson_layer = new ol.layer.Vector({
  source: geojson_source,
  style: style_function
});

map.addLayer(geojson_layer);

/**************************************************************************************************/

var popup_element = document.getElementById('popup');

// Fixme: popup don't move with the map
var popup = new ol.Overlay({
  element: popup_element,
  positioning: 'bottom-center',
  stopEvent: false
});
map.addOverlay(popup);

// display popup on click
map.on('click', function(event) {
  var feature = map.forEachFeatureAtPixel(event.pixel,
      function(feature, layer) {
        return feature;
      });
  if (feature) {
    console.log("feature", feature.get('massif'))
    $('#massif-name').html('Massif : ' + feature.get('massif'))
    var geometry = feature.getGeometry();
    var coordinate = geometry.getCoordinates();
    popup.setPosition(coordinate);
    $(popup_element).popover({
      'placement': 'top',
      'html': true,
      'content': feature.get('massif'), // Fixme: not updated next time
      // 'title': feature.get('massif')
      // delay: { "show": 200, "hide": 100 } // Fixme: do nothing
    });
    $(popup_element).popover('show');
  } else {
    console.log("feature None")
    // https://github.com/twbs/bootstrap/issues/17544
    $(popup_element).popover('dispose');
  }
});

// change mouse cursor when over marker
$(map.getViewport()).on('mousemove', function(e) {
  var pixel = map.getEventPixel(e.originalEvent);
  var hit = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
    return true;
  });
  if (hit) {
    map.getTarget().style.cursor = 'pointer';
  } else {
    map.getTarget().style.cursor = '';
  }
});

// var select_single_click = new ol.interaction.Select();
// var select_mouse_move = new ol.interaction.Select({
//   condition: ol.events.condition.mouseMove
// });
// var select = select_mouse_move;
// map.addInteraction(select);
// select.on('select', function(e) {
//   features = e.target.getFeatures()
//   console.log(features);
//   // $('#status').html('&nbsp;' + e.target.getFeatures().getLength() +
//   // 		    ' selected features (last operation selected ' + e.selected.length +
//   // 		    ' and deselected ' + e.deselected.length + ' features)');
// });

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
