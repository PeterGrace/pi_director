<%inherit file="pi_director:templates/base.mak"/>
<%block name="BlockContent">

%if pis != None:
          <h2 class="sub-header">Current Fleet</h2>
          <div class="table-responsive" style="overflow-x: visible;">
            <table class="table table-striped" id="PiTable">
              <thead>
                <tr>
                  <th>MAC</th>
                  <th>Screen</th>
				  <th>Description</th>
				  <th>Last Seen</th>
                  <th>URL</th>
				  <th>Landscape Mode</th>
				  <th>Edit</th>
				  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
%for pi in pis:
                <tr>
%if pi.ip == None:				
                  <td>${pi.uuid}</td>
% else:
                  <td>${pi.uuid} (${pi.ip})</td>
%endif
				  
				  <td><span id="screenshotMO" data-toggle="tooltip" data-placement="right" title="<img src='${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}' height=270 width=480>"><img src='${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}' height=67 width=120></span></td>

                  <td>${pi.description}</td>

				




<%
from datetime import datetime, timedelta
if pi.lastseen is None:
	timediff = timedelta(1979,12,31,23,59,59)
else:
	timediff = datetime.now() - pi.lastseen
%>

% if (timediff.total_seconds() > 300):
				  <td><div class="alert alert-danger">${int(timediff.total_seconds())} seconds ago</div></td>
% elif (timediff.total_seconds() > 60):
				  <td><div class="alert alert-warning">${int(timediff.total_seconds())} seconds ago</div></td>
% else:
				  <td><div class="alert alert-info">${int(timediff.total_seconds())} seconds ago</div></td>
% endif
%if len(pi.tags)==0:
                  <td>${pi.url}</td>
%else:
				  <td>${pi.url}<br>
%for tag in pi.tags:
				<button type="button" data-id="${tag.tag}" href="#btnTag${tag.tag}" class="btn btn-xs btn-primary">${tag.tag}</button>
%endfor				
		</td>
%endif
				  %if pi.landscape == True:
				  	<td><span class="glyphicon glyphicon-ok-circle"></span></td>
			      %else:
				  	<td><span class="glyphicon glyphicon-remove-circle"></span></td>
				  %endif
				  <td><button type="button" data-id="${pi.uuid}" data-toggle="modal" href="#editModal" class="btn btn-xs btn-primary macedit">Edit</button></td>
				  <td><button type="button" data-id="${pi.uuid}" data-toggle="modal" href="#deleteModal" class="btn btn-xs btn-danger macdelete">Delete</button></td>
                </tr>
%endfor
%endif
			</tbody>
</table>
</div> <!-- table-responsive -->
<button type="button" data-toggle="modal" href="#editModal" class="btn btn-lg btn-success addpi">Add Pi</button>

<div class="modal fade" id="deleteModal">
	<div class="modal-content">
		<div class="modal-header">
			<a class="close" data-dismiss="modal">x</a>
			<h3> Delete Entry </h3>
		</div>
		<div class="modal-body">
			<p>Do you really want to delete this entry?</p>
		</div>
		<div class="modal-footer">
			<a href="#" class="btn btn-danger" id="modalDelete">Delete</a>
			<a href="#" class="btn btn-warning" data-dismiss="modal">Cancel</a>
		</div>
	</div>
</div>

<div class="modal fade" id="editModal" style="padding-left: 100px; padding-right: 100px;">
	<div class="modal-content">
		<div class="modal-header">
			<a class="close" data-dismiss="modal">x</a>
			<h3> Edit Entry </h3>
		</div>
		<div class="modal-body">
			<form class="form-horizontal">
				<div class="form-group">
					<label for="modalMAC" class="control-label col-xs-2">MAC Address</label>
					<div class="col-xs-10">
						<input type="text" class="form-control" id="modalMAC" placeholder="MAC Address">
					</div>
				</div>
				<div class="form-group">
					<label for="modalDesc" class="control-label col-xs-2">Description</label>
					<div class="col-xs-10">
						<input type="text" class="form-control" id="modalDesc" placeholder="Description">
					</div>
				</div>
				<div class="form-group">
					<label for="modalURL" class="control-label col-xs-2">URL</label>
					<div class="col-xs-10">
						<input type="text" class="form-control" id="modalURL" placeholder="URL">
					</div>
				</div>
				<div class="form-group">
					<label for="modalLandscape" class="control-label col-xs-2">Landscape Mode</label>
					<div class="col-xs-10">
						<input type="checkbox" class="form-control" id="modalLandscape">
					</div>	
				</div>

		</div>
		<div class="modal-footer">
			<a href="#" class="btn btn-primary" id="modalSave">Save</a>
			<a href="#" class="btn btn-warning" data-dismiss="modal">Discard Changes</a>
		</div>
	</div>
</div>
</%block>

<%block name="ScriptContent">
<script>
addLoadEvent(function() {
	$(".macdelete").click(function(e) {
		e.preventDefault();
		window.current_pi = $(this).attr("data-id");
	});
});
addLoadEvent(function() {
	$("#modalDelete").click(function(e) {
		e.preventDefault();
		var id = window.current_pi;
		$.ajax({
			type: "DELETE",
			url: '/ajax/PiUrl/'+id,
			success: function(formdata) {
                $("#deleteModal").modal('hide');
                location.reload(true);
			}
		});
	});
});

addLoadEvent(function() {
	$(".macedit").click(function(e) {
		e.preventDefault();
		var id = $(this).attr("data-id");
		$.ajax({
			type: "GET",
			url: '/ajax/PiUrl/'+id,
			success: function(formdata) {
				$("#modalMAC").val(formdata.uuid);
				$("#modalDesc").val(formdata.description);
				$("#modalURL").val(formdata.url);
				$("#modalLandscape").prop('checked',formdata.landscape);
				$("#modalMAC").prop('disabled',true);
			}
		});
	});
});
addLoadEvent(function() {
	$("#modalSave").click(function(e) {
		e.preventDefault();
		var modalMAC = $("#modalMAC").val();
		var newDesc = $("#modalDesc").val();
		var newURL = $("#modalURL").val();
		var newLandscape = $("#modalLandscape").prop('checked');
		$.ajax({
			type: "POST",
			url: '/ajax/PiUrl/'+modalMAC,
			data: JSON.stringify({'url':newURL,'landscape':newLandscape,'description':newDesc}),
			success: function(result) {
				$("#editModal").modal('hide');
				location.reload(true);
			}
		});
	});
});
$(function () {
  $('[data-toggle="tooltip"]').tooltip({ html: true})
})
</script>
</%block>
