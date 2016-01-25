// Fixme: prefix jquery selector with $

// Table must have id editable-table
var table = $('#editable-table');

$('.editable-table-add').click(function () {
  var hidden_line = table.find('tr.invisible');
  var clone = hidden_line.clone(true);
  clone.removeClass('invisible');
  $(this).parents('tr').after(clone);
});

$('.editable-table-add-bottom').click(function () {
  var hidden_line = table.find('tr.invisible');
  var clone = hidden_line.clone(true);
  hidden_line.removeClass('invisible');
  table.append(clone);
});

$('.editable-table-remove').click(function () {
  $(this).parents('tr').detach();
});

$('.editable-table-up').click(function () {
  var row = $(this).parents('tr');
  if (row.index() === 1) return; // Don't go above the header
  row.prev().before(row.get(0));
});

$('.editable-table-down').click(function () {
  var row = $(this).parents('tr');
  row.next().after(row.get(0));
});

// Add to jQuery shift/pop functions
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

function export_data() {
  var rows = table.find('tr:not(tr.invisible)');
  console.log(rows);
  var headers = [];
  var data = [];
  
  // Get the headers (add special header logic here)
  $(rows.shift()).find('th:not(:empty)').each(function () {
    headers.push($(this).text().toLowerCase());
  });
  
  // Turn all existing rows into a loopable array
  rows.each(function () {
    var td = $(this).find('td');
    var h = {};
    
    // Use the headers from earlier to name our hash keys
    headers.forEach(function (header, i) {
      h[header] = td.eq(i).text();
    });
    
    data.push(h);
  });

  return data;
}

function rest_patch(server, endpoint, data) {
  json_data = JSON.stringify(data);
  console.log(json_data)
  
  url = server + endpoint;
  console.log(url)
  
  var csrf_token = Cookies.get('csrftoken');
  console.log(csrf_token)
  
  var xhr_request = $.ajax({
    url : url,
    type : 'PATCH',
    headers: {"X-CSRFToken": csrf_token},
    contentType : 'application/json',
    // data : data,
    data : json_data,
    processData: false,
    dataType: 'json'
  });
  
  return xhr_request;
}
