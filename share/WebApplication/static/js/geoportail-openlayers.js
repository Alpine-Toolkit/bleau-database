/**************************************************************************************************/

// Fixme: use JQuery
// document.getElementById('mouse-position')

/**************************************************************************************************/

// new OpenLayers.Projection('EPSG:4326');
var proj_4326 = ol.proj.get('EPSG:4326');
var proj_3857 = ol.proj.get('EPSG:3857');

/**************************************************************************************************/

var center_in_mercator = ol.proj.transform([center.longitude, center.latitude],
					   'EPSG:4326', 'EPSG:3857');

/**************************************************************************************************/

var extent_margin = 1000; // m
var zoom_to_extent = new ol.control.ZoomToExtent({
  extent: [
    center_in_mercator[0] - extent_margin, center_in_mercator[1] - extent_margin,
    center_in_mercator[0] + extent_margin, center_in_mercator[1] + extent_margin
  ]
});

var scale_line_control = new ol.control.ScaleLine();

var full_screen_control = new ol.control.FullScreen();

// control is shown in the top right corner of the map
// css selector .ol-mouse-position.
// var mouse_position_control = new ol.control.MousePosition();

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

var map = new ol.Map({
  target: document.getElementById('map'),
  controls: ol.control.defaults({
    attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
      collapsible: false
    })
  }).extend([
    zoom_to_extent,
    scale_line_control,
    mouse_position_control,
    full_screen_control
  ]),
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

var ign_layer = new ol.layer.Tile({
  source: ign_source
});

map.addLayer(ign_layer);

/**************************************************************************************************/

var styles = {
  // GeometryCollection
  'Massif/default': [new ol.style.Style({
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
  'Massif/current': [new ol.style.Style({
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
  })],
  'Circuit/default': [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
	color: 'rgba(0, 255, 255, .5)'
      }),
      stroke: new ol.style.Stroke({
        color: 'blue',
	width: 2
      })
    })
  })],
  'Place/default': [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
	color: 'rgba(255, 0, 255, .5)'
      }),
      stroke: new ol.style.Stroke({
        color: 'blue',
	width: 2
      })
    })
  })]
};

var style_function = function(feature, resolution) {
  // return styles[feature.getGeometry().getType()];
  // console.log(feature, resolution);
  // console.log(feature.getProperties());
  var object_type = feature.get('object');
  if (object_type == 'Massif')
  {
    if (feature.get('massif') == place_name)
      return styles['Massif/current'];
    else
      return styles['Massif/default'];
  }
  else
  {
    return styles[object_type + '/default'];
  }
};

var feature_options = {'dataProjection': proj_4326,
		       'featureProjection': proj_3857};
// feature loader http://openlayersbook.github.io/ch05-using-vector-layers/example-03.html
// readProjection(geojson_object),

var massif_geojson_source = new ol.source.Vector({
  features: (new ol.format.GeoJSON()).readFeatures(massif_geojson, feature_options)
});
var massif_geojson_layer = new ol.layer.Vector({
  source: massif_geojson_source,
  style: style_function
});
map.addLayer(massif_geojson_layer);

var circuit_geojson_source = new ol.source.Vector({
  features: (new ol.format.GeoJSON()).readFeatures(circuit_geojson, feature_options)
});
var circuit_geojson_layer = new ol.layer.Vector({
  source: circuit_geojson_source,
  style: style_function
});
map.addLayer(circuit_geojson_layer);

var place_geojson_source = new ol.source.Vector({
  features: (new ol.format.GeoJSON()).readFeatures(place_geojson, feature_options)
});
var place_geojson_layer = new ol.layer.Vector({
  source: place_geojson_source,
  style: style_function
});
map.addLayer(place_geojson_layer);

/**************************************************************************************************/

//////var popup_element = document.getElementById('popup');
//////
//////// Fixme: popup don't move with the map
//////var popup = new ol.Overlay({
//////  element: popup_element,
//////  positioning: 'bottom-center',
//////  stopEvent: false
//////});
//////map.addOverlay(popup);
//////
//////// display popup on click
//////map.on('click', function(event) {
//////  var feature = map.forEachFeatureAtPixel(event.pixel,
//////      function(feature, layer) {
//////        return feature;
//////      });
//////  if (feature) {
//////    console.log("feature", feature.get('massif'))
//////    $('#massif-name').html('Massif : ' + feature.get('massif'))
//////    var geometry = feature.getGeometry();
//////    var coordinate = geometry.getCoordinates();
//////    popup.setPosition(coordinate);
//////    $(popup_element).popover({
//////      'placement': 'top',
//////      'html': true,
//////      'content': feature.get('massif'), // Fixme: not updated next time
//////      // 'title': feature.get('massif')
//////      // delay: { "show": 200, "hide": 100 } // Fixme: do nothing
//////    });
//////    $(popup_element).popover('show');
//////  } else {
//////    console.log("feature None")
//////    // https://github.com/twbs/bootstrap/issues/17544
//////    $(popup_element).popover('dispose');
//////  }
//////});
//////
//////// change mouse cursor when over marker
//////$(map.getViewport()).on('mousemove', function(e) {
//////  var pixel = map.getEventPixel(e.originalEvent);
//////  var hit = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
//////    return true;
//////  });
//////  if (hit) {
//////    map.getTarget().style.cursor = 'pointer';
//////  } else {
//////    map.getTarget().style.cursor = '';
//////  }
//////});

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

/**************************************************************************************************/

var style_function_custom = function(feature, resolution) {
  return [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
	color: 'rgba(255, 0, 255, .5)'
      }),
      stroke: new ol.style.Stroke({
        color: 'blue',
	width: 2
      })
    })
  })]
}

var custom_source = new ol.source.Vector({
  features: new ol.format.GeoJSON()
});

var custom_layer = new ol.layer.Vector({
  source: custom_source,
  style: style_function_custom
});

map.addLayer(custom_layer);

var interaction;
$('#map-toolbar label').on('click', function(event) {
  map.removeInteraction(interaction);

  var id = event.target.id;
  console.log("click on ", id)
  switch(id) {
  case "select":
    interaction = new ol.interaction.Select();
    map.addInteraction(interaction);
    break;

  case "point":
    interaction = new ol.interaction.Draw({
      type: 'Point',
      source: custom_layer.getSource()
    });
    map.addInteraction(interaction);
    interaction.on('drawend', onDrawEnd);
    break;

  case "modify":
    interaction = new ol.interaction.Modify({
      features: new ol.Collection(custom_layer.getSource().getFeatures())
    });
    map.addInteraction(interaction);
    break;

  default:
    break;
  }
});

function onDrawEnd(event) {
  console.log(event.feature)
}

$("#download-button").click(function(event) {
  console.log("download-button");
  // ???
  var obj_geojson = (new ol.format.GeoJSON()).writeFeatures(custom_source.getFeatures(), feature_options);
  console.log(obj_geojson);
  var obj_json = JSON.stringify(obj_geojson);
  console.log(obj_json);
  var blob = new Blob([obj_geojson], {type: "text/plain;charset=utf-8"});
  saveAs(blob, "bleau-geo.json");
});

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
