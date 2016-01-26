var $input = $('.typeahead');
$input.typeahead({
  source: person_data,
  autoSelect: true
});

var name_to_pk = person_data.reduce(function(obj, x) {
    obj[x.name] = x.pk;
    return obj;
}, {});

$('#add-person').click(function () {
  var current = $input.val();
  if (current) {
    var duplicate = false;
    var data = export_data();
    for (var i = 0; i < data.length; i++) {
      var row = data[i];
      if (row.name == current) {
	duplicate = true;
	break;
      }
    }
    if (duplicate) {
      alert("Duplicated entry");
    } else {
      var hidden_line = table.find('tr.invisible');
      var clone = hidden_line.clone(true);
      hidden_line.find('td:first').html(current);
      hidden_line.removeClass('invisible');
      table.append(clone);
    }
  }
});

var save_button = $('#save-button');
save_button.click(function () {
  var data = export_data();
  var pks = [];
  data.forEach(function (row) {
    pks.push('/api/person/' + name_to_pk[row.name].toString() + '/');
  });

  var data = {};
  data[pk_key] = pks;

  // server = ''http://127.0.0.1:8000';
  server = '';

  rest_patch(server, endpoint, data).done(function() {
    var modal = $('#rest-patch-modal')
    modal.find('#rest-patch-modal-title').text('Update success');
    modal.find('#rest-patch-modal-body').text('');
    modal.find('.modal-body').hide();
    modal.modal('show');
  }).fail(function(jq_xhr, text_status) {
    $('#rest-patch-modal').modal('show');
    modal.find('#rest-patch-modal-title').text('Update failure');
    modal.find('#rest-patch-modal-body').text('Retry later or contact the webmaster if the problem persists.');
    modal.find('.modal-body').show();
    modal.modal('show');
  })
});
