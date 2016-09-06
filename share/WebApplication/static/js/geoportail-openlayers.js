/* Bleau Database - A database of the bouldering area of Fontainebleau
 * Copyright (C) 2015 Fabrice Salvaire
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/**************************************************************************************************
 *
 * Configuration Variables
 *
 */

// var place_name = "...";
// var center = {longitude: ..., latitude: ...}
// var extent_margin = [1000, 1000]; // m
// var extent = null;

// var geoportail_api_key = "...";

// var show_edit_toolbar = false;

/**************************************************************************************************/

// new OpenLayers.Projection('EPSG:4326');
var proj_4326 = ol.proj.get('EPSG:4326');
var proj_3857 = ol.proj.get('EPSG:3857');

/**************************************************************************************************/

if (extent) {
  var center_in_mercator = [.5*(extent[0] + extent[2]),
			    .5*(extent[1] + extent[3])];
} else {
  var center_in_mercator = ol.proj.transform([center.longitude, center.latitude],
					     'EPSG:4326', 'EPSG:3857');

  extent = [
    center_in_mercator[0] - extent_margin[0], center_in_mercator[1] - extent_margin[1],
    center_in_mercator[0] + extent_margin[0], center_in_mercator[1] + extent_margin[1]
  ]
}

var view_setup = {
  zoom: 15,
  center: center_in_mercator
}

/**************************************************************************************************/

var zoom_to_extent = new ol.control.ZoomToExtent({
  extent: extent
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
var precision_input = $('#precision');

function set_precision(value) {
  var format = ol.coordinate.createStringXY(value);
  mouse_position_control.setCoordinateFormat(format);
}

// Fixme: last_precision
var last_precision = precision_input.valueAsNumber;
projection_select.on('change', function() {
  var value = this.value;
  if (value == 'EPSG:3857') {
    last_precision = precision_input.valueAsNumber;
    precision_input.val(0);
    set_precision(0);
  }
  else if (value == 'EPSG:4326') {
    last_precision = 4;
    precision_input.val(last_precision);
    set_precision(last_precision);
  }
  mouse_position_control.setProjection(ol.proj.get(value));
});
projection_select.val(mouse_position_control.getProjection().getCode());

precision_input.on('change', function() {
  var value = this.valueAsNumber;
  last_precision = value;
  set_precision(value);
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
  view: new ol.View(view_setup)
});

if (extent)
  map.getView().fit(extent, map.getSize());

/**************************************************************************************************/

var resolutions = [];
var matrix_ids = [];
var resolution_max = ol.extent.getWidth(proj_3857.getExtent()) / 256;

for (var i = 0; i < 18; i++) {
  matrix_ids[i] = i.toString();
  resolutions[i] = resolution_max / Math.pow(2, i);
}
console.log("Resolutions:", resolutions)

var tile_grid = new ol.tilegrid.WMTS({
  origin: [-20037508, 20037508],
  resolutions: resolutions,
  matrixIds: matrix_ids
});

var ign_attribution = new ol.Attribution({
    html: '<a href="http://www.geoportail.fr/" target="_blank">' +
      '<img src="http://api.ign.fr/geoportail/api/js/latest/' +
      'theme/geoportal/img/logo_gp.gif"></a>'
});

function ign_layer_factory(layer_settings) {
  var source = new ol.source.WMTS({
    url: 'http://wxs.ign.fr/' + geoportail_api_key + '/wmts',
    layer: layer_settings.layer_name,
    matrixSet: 'PM',
    format: layer_settings.image_format,
    projection: 'EPSG:3857',
    tileGrid: tile_grid,
    style: 'normal',
    attributions: [ign_attribution]
  });

  var layer = new ol.layer.Tile({
    source: source,
    visible: false
  });

  return layer;
}

var ign_layer_settings = [
  {layer_name: 'GEOGRAPHICALGRIDSYSTEMS.MAPS', image_format: 'image/jpeg'},
  {layer_name: 'ORTHOIMAGERY.ORTHOPHOTOS', image_format: 'image/jpeg'},
  {layer_name: 'GEOGRAPHICALGRIDSYSTEMS.PLANIGN', image_format: 'image/jpeg'},
  // {layer_name: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD', image_format: 'image/jpeg'},
  // {layer_name: 'TRANSPORTNETWORKS.ROADS', image_format: 'image/png'},
  // {layer_name: 'CADASTRALPARCELS.PARCELS', image_format: 'image/png'}
];

var ign_layers = [];
ign_layer_settings.forEach(function(layer_settings) {
  var layer = ign_layer_factory(layer_settings);
  if (layer_settings.layer_name == 'GEOGRAPHICALGRIDSYSTEMS.PLANIGN')
    layer.setVisible(true);
  map.addLayer(layer);
  ign_layers.push(layer);
});

var map_source_input = $('#map-source');
map_source_input.on('change', function() {
  var layer_name = this.value;
  // var layers = map.getLayers();
  ign_layers.forEach(function(layer) {
    layer.setVisible(layer.getSource().getLayer() == layer_name);
  });
});

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
  // console.log("style_function: resolution =", resolution);
  var object_type = feature.get('object');
  if (object_type == 'Massif') {
    if (feature.get('name') == place_name)
      return styles['Massif/current'];
    else
      return styles['Massif/default'];
  } else {
    if (resolution < resolutions[14])
      return styles[object_type + '/default'];
    else
      return null;
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
// map.addLayer(massif_geojson_layer);

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

var cluster_source = new ol.source.Cluster({
  distance: 20,
  source: massif_geojson_source
});

var style_cache = {};

function has_current_place(features, place_name) {
  for (var i = 0; i < features.length; i++) {
    feature = features[i];
    if (feature.get('name') == place_name)
      return true;
  }
  return false;
}

function make_cluster_style(size, colour) {
  return [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 10,
      stroke: new ol.style.Stroke({
        color: '#fff'
      }),
      fill: new ol.style.Fill({
        color: colour
      })
    }),
    text: new ol.style.Text({
      text: size.toString(),
      fill: new ol.style.Fill({
        color: '#fff'
      })
    })
  })];
}

var cluster_style_function = function(feature, resolution) {
  // console.log("clusters style_function: resolution =", resolution);
  var features = feature.get('features');
  if (resolution > resolutions[14]) {
    var size = features.length;
    if (has_current_place(features, place_name)) {
      return make_cluster_style(size, 'red');
    } else {
      var style = style_cache[size];
      if (!style) {
	style = make_cluster_style(size, '#3399CC');
	style_cache[size] = style;
      }
      return style;
    }
  } else {
    features = feature.get('features');
    feature = features[0];
    return style_function(feature, resolution);
  }
};

var clusters = new ol.layer.Vector({
  source: cluster_source,
  style: cluster_style_function
});
map.addLayer(clusters);

/**************************************************************************************************/

// Define styles

var normal_style = new ol.style.Style({
  image: new ol.style.Circle({
    radius: 4,
    fill: new ol.style.Fill({
      color: 'rgba(20,150,200,0.3)'
    }),
    stroke: new ol.style.Stroke({
      color: 'rgba(20,130,150,0.8)',
      width: 1
    })
  })
});

var selected_style = new ol.style.Style({
  image: new ol.style.Circle({
    radius: 40,
    fill: new ol.style.Fill({
      color: 'rgba(150,150,200,0.6)'
    }),
    stroke: new ol.style.Stroke({
      color: 'rgba(20,30,100,0.8)',
      width: 3
    })
  })
});

var selected_text_style_function = function(name, coordinate) {
  // var box_width = feature_name.length * ...;
  // var margin = box_width * ...;
  // map.getView().getResolution();
  return new ol.style.Style({
    // geometry: new ol.geom.Polygon([[[coordinate[0] -margin, coordinate[1] -margin],
    // 				   [coordinate[0] +margin, coordinate[1] -margin],
    // 				   [coordinate[0] +margin, coordinate[1] +margin],
    // 				   [coordinate[0] -margin, coordinate[1] +margin]
    // 				  ]]),
    // fill: new ol.style.Fill({
    //   color: '#FFF'
    // }),
    text: new ol.style.Text({
      font: '20px helvetica, sans-serif',
      text: name,
      fill: new ol.style.Fill({
        color: '#000'
      }),
      stroke: new ol.style.Stroke({
        color: '#fff', // #fff #DEFFCD #D1FEBB
        width: 20
      })
    })
  });
};

var selected_features = [];

// Unselect previous selected features
function unselect_previous_features() {
  var i;
  for(i=0; i < selected_features.length; i++) {
    selected_features[i].setStyle(null);
  }
  selected_features = [];
}

// Handle pointer
map.on('pointermove', function(event) {
  unselect_previous_features();
  map.forEachFeatureAtPixel(event.pixel, function(feature) {
    features = feature.get('features');
    if (features) {
      feature1 = features[0];
      feature_name = feature1.get('name');
      if (features.length > 1)
	feature_name += ' ...' // fixme: unicode
      coordinate = feature1.getGeometry().getCoordinates();
    } else {
      var object_type = feature.get('object');
      if (object_type == 'Circuit') {
	feature_name = feature.get('massif') + ' n°' + feature.get('number') + ' ' + feature.get('grade');
      } else
	feature_name = feature.get('name');
      coordinate = feature.getGeometry().getCoordinates();
    }

    feature.setStyle([
      // selected_style,
      selected_text_style_function(feature_name, coordinate)
    ]);
    selected_features.push(feature);
  });
});

/**************************************************************************************************/

if (show_edit_toolbar) {

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
    switch(id) {
    case "select":
      interaction = new ol.interaction.Select();
      map.addInteraction(interaction);
      break;

    case "point":
      interaction = new ol.interaction.Draw({
        type: 'Point',
        source: custom_source
      });
      map.addInteraction(interaction);
      interaction.on('drawend', onDrawEnd);
      break;

    case "modify":
      interaction = new ol.interaction.Modify({
        features: new ol.Collection(custom_source.getFeatures())
      });
      map.addInteraction(interaction);
      break;

    default:
      break;
    }
  });

  var current_feature = null;
  var feature_modal = $('#feature-modal');
  var feature_wgs84_position = feature_modal.find('#feature-wsg84-position');
  var feature_mercator_position = feature_modal.find('#feature-mercator-position');
  var feature_name_group = feature_modal.find('#feature-name-group');
  var feature_name_input = feature_modal.find('#feature-name');
  var feature_category_input = feature_modal.find('#feature-category');
  var feature_note_input = feature_modal.find('#feature-note');
  var cancel_feature_button = feature_modal.find('#cancel-feature-button');
  var save_feature_button = feature_modal.find('#save-feature-button');
  var download_feature_button = $("#download-feature-button");
  var number_of_features_label = $("#number-of-features");

  function show_feature_modal(feature) {
    current_feature = feature;
    mercator_coordinate = feature.getGeometry().getCoordinates();
    coordinate = ol.proj.transform(mercator_coordinate, 'EPSG:3857', 'EPSG:4326');
    feature_wgs84_position.text(coordinate[0].toFixed(5) + ', ' + coordinate[1].toFixed(5))
    feature_mercator_position.text(mercator_coordinate[0].toFixed(0) + ', ' + mercator_coordinate[1].toFixed(0))
    feature_modal.modal();
  }

  function hide_feature_modal() {
    feature_modal.modal('hide');
    feature_name_group.removeClass('has-error')
    feature_name_input.removeClass('form-control-error')
    features = custom_source.getFeatures();
    number_of_features_label.text(features.length.toString());
    feature_name_input.val('');
    feature_note_input.val('');
    current_feature = null;
  }

  function onDrawEnd(event) {
    show_feature_modal(event.feature);
  }

  save_feature_button.on('click', function(event) {
    var name = feature_name_input.val();
    if (name) {
      current_feature.set('name', name);
      current_feature.set('category', feature_category_input.val());
      current_feature.set('note', feature_note_input.val());
      hide_feature_modal();
    }
    else {
      feature_name_group.addClass('has-error')
      feature_name_input.addClass('form-control-error')
    }
  });

  cancel_feature_button.on('click', function(event) {
    custom_source.removeFeature(current_feature)
    hide_feature_modal();
  });

  download_feature_button.click(function(event) {
    var obj_geojson = (new ol.format.GeoJSON()).writeFeatures(custom_source.getFeatures(), feature_options);
    var obj_json = JSON.stringify(obj_geojson);
    var blob = new Blob([obj_geojson], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "bleau-geo.json");
  });
}

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
