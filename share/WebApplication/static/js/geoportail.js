window.onload = function() {
  Geoportal.load(
    'geoportail_map', // div's ID
    ['usho1r0e3pl581viejhrjfsf'], // API's keys
    { // map's center :
      lon: 2.640046,
      lat: 48.447261,
    },
    15, //zoom
    //options
    {
      layers: [
	'ORTHOIMAGERY.ORTHOPHOTOS',
	'GEOGRAPHICALGRIDSYSTEMS.MAPS'
      ],
      layersOptions: {
	'ORTHOIMAGERY.ORTHOPHOTOS': {visibility: false},
	'GEOGRAPHICALGRIDSYSTEMS.MAPS': {opacity: 1.}
      },
      viewerClass: Geoportal.Viewer.Default
    }
  );
};
