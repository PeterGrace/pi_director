<%inherit file="pi_director:templates/base.mak"/>
<%block name="BlockContent">

%if pis != None:
<h2 class="sub-header">Current Fleet</h2>
<div class="table-responsive" style="overflow-x: visible;">
	<table class="table table-striped" id="PiTable">
		<thead>
			<tr>
				<th>Pi</th>
				<th>Screen</th>
				<th>Description</th>
				<th>URL</th>
				<th class="text-center">Orientation</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
	% for pi in pis:
			<tr>
<%
		from datetime import datetime, timedelta
		if pi.lastseen is None:
			timediff = timedelta(1979,12,31,23,59,59)
		else:
			timediff = datetime.now() - pi.lastseen
	
		current_url = request.url	
			
%>
		% if pi.ip == None:
				<td>${pi.uuid}<br>
		% else:
				<td>${pi.uuid}<br>(${pi.ip})<br>
		%endif
		% if (timediff.total_seconds() > 300):
				<a href='logs/${pi.uuid}'><button class="pull-right btn btn-xs btn-danger" title="Last seen ${int(timediff.total_seconds())} seconds ago">OFFLINE</button></td></a>
		% elif (timediff.total_seconds() > 70):
				<a href='logs/${pi.uuid}'><button class="pull-right btn btn-xs btn-warning" title="Last seen ${int(timediff.total_seconds())} seconds ago">LAGGED</button></td></a>
		% else:
				<a href='logs/${pi.uuid}'><button class="pull-right btn btn-xs btn-info" title="Last seen ${int(timediff.total_seconds())} seconds ago">OK</button></td></a>
		% endif
				<td><span class="screenshotMO" data-toggle="tooltip" data-placement="right" title="<img src='${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}' height=270 width=480>"><img src='${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}' height=67 width=120></span></td>
				<td>${pi.description}</td>

	
		% if len(pi.tags)==0:
				<td>${pi.url}</td>
		% else:
				<td>${pi.url}<br/>
		% for tag in pi.tags:
			% if "tagged" in current_url:
					<a href="${current_url};${tag.tag}" class="btn btn-xs btn-primary">${tag.tag}</a>
			% else:		
					<a href="${current_url}tagged/${tag.tag}" class="btn btn-xs btn-primary">${tag.tag}</a>
			% endif		

		% endfor
				</td>
		% endif

		%if pi.orientation == 0:
				<td class="text-center"><span style="font-size:4em;" class="glyphicon glyphicon-triangle-top" 
				title=${pi.orientation}°></span></td>
		% elif pi.orientation == 90:
				<td class="text-center"><span style="font-size:4em;" class="glyphicon glyphicon-triangle-left"
				title=${pi.orientation}°></span></td>
		% elif pi.orientation == 180:		
				<td class="text-center"><span style="font-size:4em;" class="glyphicon glyphicon-triangle-bottom"
				title=${pi.orientation}°></span></td>
		% elif pi.orientation == 270:		
				<td class="text-center"><span style="font-size:4em;" class="glyphicon glyphicon-triangle-right"
				title=${pi.orientation}°></span></td>
		%endif
				<td>
					<div class="dropdown">
						<button class="btn btn-default dropdown-toggle" type="button" id="dropdown-${pi.uuid}" data-toggle="dropdown">Actions<span class="caret"></span></button>
						<ul class="dropdown-menu" aria-labelledby="dropdown-${pi.uuid}">
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#editModal" href="#editModal" class="macedit">Edit</a></li>
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#deleteModal" href="#deleteModal" class="macdelete">Delete</a></li>
							<li role="separator" class="divider"</li>
							<li><a href="#" data-id="${pi.uuid}" class="refreshPi">Refresh</a></li>
							<li role="separator" class="divider"</li>
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#tagModal" href="#tagModal" class="tagedit">Tag Management</a></li>
		%if pi.requested_commands:
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#commandResultModal" href="#commandResultModal" class="commandsresults">Command Results</a></li>
		%else:
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#commandModal" href="#commandModal" class="sendcommands">Send Commands</a></li>
		%endif
						</ul>
					</div>
				</td>
			</tr>
	%endfor
%endif
		</tbody>
	</table>
</div> <!-- table-responsive -->
<button type="button" data-toggle="modal" href="#editModal" class="btn btn-lg btn-success addpi">Add Pi</button>

<div class="modal fade" id="tagModal" style="margin: 10% 10% 0 10%;">
	<div class="modal-content">
		<div class="modal-header">
			<a class="close" data-dismiss="modal">x</a>
			<h3> Tag Management </h3>
		</div>
		<div class="modal-body">
			<form class="form-horizontal">
				<div class="form-group">
					<label for="divTagList" class="control-label col-xs-2">Current tags</label>
					<div class="col-xs-10" id="divTagList"></div>
				</div>
				<br>
				<div class="form-group">
					<label for="iptAddTag" class="control-label col-xs-2">Add New Tag</label>
					<div class="col-xs-2">
					<input type="text" class="form-control" id="iptAddTag" placeholder="tag" />
					</div>
					<button class="btn btn-sm btn-normal" id="btnAddTag">Add Tag</button>
				</div>
			</form>
		</div>
		<div class="modal-footer">
			<button type="button" href="#" class="btn btn-lg btn-normal" data-dismiss="modal" id="btnDoneTag">Done</a>
		</div>
		<div class="clearfix"></div>
	</div>
</div>

<div class="modal fade" id="deleteModal" style="margin: 10% 25% 0 25%;">
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
		<div class="clearfix"></div>
	</div>
</div>

<div class="modal fade" id="editModal" style="margin: 10% 10% 0 10%;">
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
						<input type="text" class="form-control" id="modalMAC" placeholder="MAC Address" />
					</div>
				</div>
				<div class="form-group">
					<label for="modalDesc" class="control-label col-xs-2">Description</label>
					<div class="col-xs-10">
						<input type="text" class="form-control" id="modalDesc" placeholder="Description" />
					</div>
				</div>
				<div class="form-group">
					<label for="modalURL" class="control-label col-xs-2">URL/Command</label>
					<div class="col-xs-10">
						<input type="radio" name="rdioCommand" value="1"/>URL
						<input type="radio" name="rdioCommand" value="0"/>Custom Command
						<input type="text" class="form-control" id="modalURL" placeholder="" />
					</div>
				</div>
				<div class="form-group">
					<label for="modalOrient" class="control-label col-xs-2">Orientation:</label>
					<div class="col-xs-10">
    					<select id="modalOrient" class="form-control">
  						<option value="orientation"><span class="caret"></option>
  						<option value=0>0</option>
  						<option value=90>90</option>
  						<option value=180>180</option>
  						<option value=270>270</option>
						</select>
    					<ul class="dropdown-menu" role="menu">
        				<li><a href="#" data-value="0">0</a></li>
        				<li><a href="#" data-value="90">90</a></li>
        				<li><a href="#" data-value="180">180</a></li>
        				<li><a href="#" data-value="270">270</a></li>
    					</ul>
					</div>
				</div>
			</form>
			<div class="clearfix"></div>
		</div>
		<div class="modal-footer">
			<a href="#" class="btn btn-primary" id="modalSave">Save</a>
			<a href="#" class="btn btn-warning" data-dismiss="modal">Discard Changes</a>
		</div>
	</div>
</div>

<div class="modal fade" id="commandResultModal" style="margin: 10% 10% 0 10%;">
	<div class="modal-content">
		<div class="modal-header">
			<a href="#" class="close" data-dismiss="modal">x</a>
			<h3> Command(s) Results </h3>
		</div>
		<div class="modal-body">
			<p>If the pi has executed commands, their results (if any) will turn up here.
			Deleting results/pending commands after the pi has checked in but before it has
			returned results could be problematic and is not recommended (but supported).</p>
			<table class="table table-striped" id="commandResults">
				<thead>
					<tr>
						<th class="col-xs-2">Command</th>
						<th>Result</th>
					</tr>
				</thead>
				<tbody>
				</tbody>
			</table>
		</div>

		<div class="modal-footer">
			<a href="#" class="btn btn-danger pull-left" id="commandResultDelete">Delete Results/Pending Commands</a>
			<a href="#" class="btn btn-info" data-dismiss="modal">Close</a>
		</div>
		<div class="clearfix"></div>
	</div>
</div>

<div class="modal fade" id="commandModal" style="margin: 10% 10% 0 10%;">
	<div class="modal-content">
		<div class="modal-header">
			<a href="#" class="close" data-dismiss="modal">x</a>
			<h3> Send Command(s) </h3>
		</div>
		<div class="modal-body">
			<p>Note that commands will be run as root via sudo next time the pi checks in.
			Execution working directory begins in /home/pi, arguments are for each specific command.</p>

			<form class="form-horizontal table-responsive" id="commandModalCommands">
			</form>
			
			<table class="hidden table table-striped" id="commandModalTemplate">
				<thead>
					<tr>
						<th class="col-xs-2">Command</th>
						<th>Arguments</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><input type="text" class="form-control" placeholder="cmd" /></td>
						<td><input type="text" class="form-control" placeholder="argument" /></td>
					</tr>
				</tbody>
			</table>
		</div>

		<div class="modal-footer">
			<a href="#" class="btn btn-info pull-left" id="commandModalClear">Reset Form</a>
			<a href="#" class="btn btn-danger" id="commandModalQueue">Queue Execution</a>
			<a href="#" class="btn btn-warning" data-dismiss="modal">Cancel</a>
		</div>
		<div class="clearfix"></div>
	</div>
</div>

</%block>

<%block name="ScriptContent">
<script type="text/javascript">

////////////////////////////////////////
// EDIT PI MODAL
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
				if (formdata.browser == true) {
					$('input:radio[name=rdioCommand]')[0].checked = true;
				}
				else {
					$('input:radio[name=rdioCommand]')[1].checked = true;
				};
				$("#modalOrient").val(formdata.orientation);
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
		var newOrient = $("#modalOrient").val();
		var newCommandType = $("input:radio[name=rdioCommand]:checked").val();
		$.ajax({
			type: "POST",
			cache: false,
			url: '/ajax/PiUrl/'+modalMAC,
			data: JSON.stringify({'url':newURL,'orientation':newOrient,'description':newDesc,'browser':newCommandType}),
			success: function(result) {
				$("#editModal").modal('hide');
				location.reload(true);
			}
		});
	});
});

addLoadEvent(function() {
	$(".refreshPi").click(function(e) {
		e.preventDefault();
		var id = $(this).attr("data-id");
		$.ajax({
			type: "GET",
			url: '/api/v1/refresh/'+id,
			success: function(formdata) {
				showAndDismissAlert('success', 'Command Queued!');
			}
		});
	});
});

addLoadEvent(function() {
	$("#btnDoneTag").click(function(e) {
		e.preventDefault();
		location.reload(true);
	});
});

addLoadEvent(function() {

});


function reloadTagList(id) {
	$.ajax({
		type: "GET",
		cache: false,
		url: '/api/v1/cache/'+id,
		success: function(result) {
			var $divTagList = $('#divTagList').empty();
			for(i=0;i<result['tags'].length;i++)
			{
				$divTagList.append($(
					"<button data-id=\"" + id + "\" class=\"btn btn-primary btn-sm\">" + result['tags'][i] + "</button>&nbsp;"
				).click(function(e) {
					e.preventDefault();
					var id = $('#tagModal').data('uid');
					var tag = $(this).text();
					
					console.log('/api/v1/tags/' + id + '/' + tag);
					console.log(id);
					console.log(tag);
					$.ajax({
						type: "DELETE",
						cache: false,
						url: '/api/v1/tags/' + id + '/' + tag,
						success: function(result) {
							reloadTagList(id);
						}
					});
				}));
			}
		}
	});
}

$(document).ready(function() {

	$('#tagModal').one('show.bs.modal', function(e) {
		$("#btnAddTag").click(function(e) {
			e.preventDefault();
			var id = $('#tagModal').data('uid');
			var tag = $("#iptAddTag").val();
			$.ajax({
				type: "POST",
				cache: false,
				url: '/api/v1/tags/'+id+ '/' + tag,
				data: JSON.stringify({'uid':id,'tag':tag}),
				success: function(result) {
					reloadTagList(id);
				},
				failure: function(result) {
					alert(result);
				}
			});
		});
	}).on('show.bs.modal', function(e) {
		var myid = $(e.relatedTarget).data('id');

		if (typeof(myid) == 'undefined') {
			return;
		}

		$('#tagModal').attr('data-uid', myid);
		reloadTagList(myid);
	});
});

////////////////////////////////////////
// TOOLTIP RELOADING
$(document).ready(function() {
	function fixup_cburl(url) {
		var d = new Date().getTime();
		
		if (url.lastIndexOf('?') > -1) {
			//already have a cache buster on it
			return url.replace(/\?_=[0-9]+/, '?_=' + d);
		} else {
			//need to append a cache buster
			return url + '?_=' + d;
		}
	}

	function reload_tooltip() {
		$('.screenshotMO').each(function(i) {
			$(this).find('img').each(function(i) {
				$(this).attr('src', fixup_cburl($(this).attr('src')));
			});

			var $tmp = $($(this).attr('data-original-title'));
			$tmp.attr('src', fixup_cburl($tmp.attr('src')));

			$(this).attr('data-original-title', $tmp.wrap('<div/>').parent().html());
		});
	}

	$('[data-toggle="tooltip"]').tooltip({ html: true});
	setInterval(reload_tooltip, 30000);
});

</script>

<!-- SEND COMMAND(S) MODAL -->
<script type="text/javascript" src="${request.static_url('pi_director:static/js/commands_modal.js')}"></script>

<!-- COMMANDS(S) RESULTS MODAL -->
<script type="text/javascript" src="${request.static_url('pi_director:static/js/commands_results_modal.js')}"></script>

</%block>
