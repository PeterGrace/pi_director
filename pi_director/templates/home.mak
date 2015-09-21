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
				<th>Orientation</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
	% for pi in pis:
			<tr>
		% if pi.ip == None:
				<td>${pi.uuid}</td>
		% else:
				<td>${pi.uuid} (${pi.ip})</td>
		%endif
				<td><span class="screenshotMO" data-toggle="tooltip" data-placement="right" title="<img src='${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}' height=270 width=480>"><img src='${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}' height=67 width=120></span></td>
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
	
		% if len(pi.tags)==0:
				<td>${pi.url}</td>
		% else:
				<td>${pi.url}<br/>
		% for tag in pi.tags:
					<a href="/tagged/${tag.tag}" class="btn btn-xs btn-primary">${tag.tag}</a>
		% endfor
				</td>
		% endif
		
		%if pi.landscape == True:
				<td class="text-center"><span class="glyphicon glyphicon-option-horizontal"></span></td>
		%else:
				<td class="text-center"><span class="glyphicon glyphicon-option-vertical"></span></td>
		%endif
				<td>
					<div class="dropdown">
						<button class="btn btn-default dropdown-toggle" type="button" id="dropdown-${pi.uuid}" data-toggle="dropdown">Actions<span class="caret"></span></button>
						<ul class="dropdown-menu" aria-labelledby="dropdown-${pi.uuid}">
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#editModal" href="#editModal" class="macedit">Edit</a>
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#deleteModal" href="#deleteModal" class="macdelete">Delete</a>
							<li role="separator" class="divider"</li>
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#tagModal" href="#tagModal" class="tagedit">Tag Management</a>
							<li><a href="#" data-id="${pi.uuid}" data-toggle="modal" data-target="#commandModal" href="#commandModal" class="sendcommands">Send Commands</a>	
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
					<label for="modalMAC" class="control-label col-xs-2">Current tags</label>
					<div class="col-xs-10">
					</div>
				</div>
		</div>
		<div class="modal-footer">
			<button type="button" href="#" class="btn btn-lg btn-normal" data-dismiss="modal">Done</a>
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
					<label for="modalURL" class="control-label col-xs-2">URL</label>
					<div class="col-xs-10">
						<input type="text" class="form-control" id="modalURL" placeholder="URL" />
					</div>
				</div>
				<div class="form-group">
					<div class="col-xs-offset-2 col-xs-10">
						<label>
							<input type="checkbox" id="modalLandscape" /> Landscape Mode
						</label>
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
				<tr>
					<td><input type="text" class="form-control" placeholder="cmd" /></td>
					<td><input type="text" class="form-control" placeholder="argument" /></td>
				</tr>
			</table>
		</div>

		<div class="modal-footer">
			<a href="#" class="btn btn-danger" id="commandModalQueue">Queue Execution</a>
			<a href="#" class="btn btn-warning" data-dismiss="modal">Cancel</a>
		</div>
		<div class="clearfix"></div>
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

addLoadEvent(function() {	
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

////////////////////////////////////////
// SEND COMMAND(S) MODAL

function commandModal_cmd_onkeyup(e) {
	if ($(this).val().length > 0) {
		var mycmdid = parseInt($(this).attr('data-cmdid'));
		var $next = $(this).parents('tbody:first')
							.find('[placeholder=cmd][data-cmdid=' + (mycmdid + 1) + ']');

		//only make a new one if there isn't a new one already
		if ($next.length == 0) {
			commandModal_addCommand(this);
		}
	} else {
		console.log('---asdf 1---');
	}
}

function commandModal_arg_onkeyup(e) {
	if ($(this).val().length > 0) {
		var myargid = parseInt($(this).attr('data-argid'));
		var mycmdid = parseInt($(this).attr('data-cmdid'));
		var $next = $(this).parents('tbody:first')
			.find('[placeholder=argument][data-cmdid=' + mycmdid + '][data-argid=' + (myargid + 1) + ']');

		//only make a new one if there isn't a new one already
		if ($next.length == 0) {
			commandModal_addArgument(this);
		}
	} else {
		console.log('---asdf 2---');
	}
}

function commandModal_addArgument(el) {
	var $tr = $(el).parents('tr:first');
	var mycmdid = parseInt($(el).attr('data-cmdid'));
	var myargid = parseInt($(el).attr('data-argid'));

	$tr.after(
		$('#commandModalTemplate tbody:first tr:first').clone()
			.find('[placeholder=cmd]')
				.replaceWith('<br/>')
				.end()
			.find('[placeholder=argument]')
				.attr('data-cmdid', mycmdid)
				.attr('data-argid', myargid + 1)
				.attr('name', 'arguments-' + mycmdid + '[]')
				.keyup(commandModal_arg_onkeyup)
				.end()
	);
	
	console.log('addarg called');
}

function commandModal_addCommand(el) {
	var $tbody = $(el).parents('tbody:first');
	var cnum = parseInt($(el).attr('data-cmdid')) + 1;

	$tbody.append(
		$('#commandModalTemplate tbody:first tr:first').clone()
			.find('[placeholder=cmd]')
				.attr('data-cmdid', cnum)
				.attr('name', 'command-' + cnum)
				.keyup(commandModal_cmd_onkeyup)
				.end()
			.find('[placeholder=argument]')
				.attr('data-cmdid', cnum)
				.attr('data-argid', 0)
				.attr('name', 'arguments-' + cnum + '[]')
				.keyup(commandModal_arg_onkeyup)
				.end()
	);
}

function clearCommandModal() {
	$('#commandModalCommands').empty().append(
		$('#commandModalTemplate').clone()
				.removeClass('hidden')
				.attr('id', '')
			.find('[placeholder=cmd]')
				.attr('data-cmdid', 0)
				.attr('name', 'command-0')
				.keyup(commandModal_cmd_onkeyup)
				.end()
			.find('[placeholder=argument]')
				.attr('data-cmdid', 0)
				.attr('data-argid', 0)
				.attr('name', 'arguments-0[]')
				.keyup(commandModal_arg_onkeyup)
				.end()
	);
}

$(document).ready(function() {
	$("#commandModal").one('show.bs.modal', function() {
		clearCommandModal();
	});

	$(".sendcommands").click(function(e) {
		e.preventDefault();
		var id = $(this).attr("data-id");
	});

	$("#commandModalQueue").click(function(e) {
		e.preventDefault();

		console.log($('#commandModalCommands').serialize());
	});
});


</script>
</%block>
