function commandModal_cmd_onkeyup(e) {
	if ($(this).val().length > 0) {
		var mycmdid = parseInt($(this).attr('data-cmdid'));
		var $next = $(this).parents('tbody:first')
							.find('[placeholder=cmd][data-cmdid=' + (mycmdid + 1) + ']');

		//only make a new one if there isn't a new one already
		if ($next.length == 0) {
			commandModal_addCommand(this);
		}
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
				.keyup(commandModal_arg_onkeyup)
				.end()
	);
}

function commandModal_addCommand(el) {
	var $tbody = $(el).parents('tbody:first');
	var cnum = parseInt($(el).attr('data-cmdid')) + 1;

	$tbody.append(
		$('#commandModalTemplate tbody:first tr:first').clone()
			.find('[placeholder=cmd]')
				.attr('data-cmdid', cnum)
				.keyup(commandModal_cmd_onkeyup)
				.end()
			.find('[placeholder=argument]')
				.attr('data-cmdid', cnum)
				.attr('data-argid', 0)
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
				.keyup(commandModal_cmd_onkeyup)
				.end()
			.find('[placeholder=argument]')
				.attr('data-cmdid', 0)
				.attr('data-argid', 0)
				.keyup(commandModal_arg_onkeyup)
				.end()
	);
}

$(document).ready(function() {
	$("#commandModal").one('show.bs.modal', function(e) {
		clearCommandModal();
	}).on('show.bs.modal', function(e) {
		var myid = $(e.relatedTarget).data('id');

		if (typeof myid == "undefined") {
			return;
		}

		$('#commandModalCommands').attr('data-uid', myid);
	});

	$("#commandModalClear").click(function(e) {
		e.preventDefault();
		clearCommandModal();
	});

	$("#commandModalQueue").click(function(e) {
		e.preventDefault();

		//serialize our command form
		var data = {};
		$('#commandModalCommands input').each(function(idx, el) {
			var cmdid = $(el).data('cmdid');
			var argid = $(el).data('argid');

			if ($(el).val() == "") {
				//skip blanks
				return;
			}

			if (typeof(argid) == 'undefined') {
				//we got a command input

				if (typeof(data[cmdid]) == 'undefined') {
					data[cmdid] = {'cmd':$(el).val()}
				} else {
					// we got an argument input first (shouldn't happen)
					if (typeof(data[cmdid]['cmd']) == 'undefined') {
						data[cmdid]['cmd'] = $(el).val();
					}
				}
			} else {
				//we got an argument input
				if (typeof(data[cmdid]) == 'undefined') {
					// we got an argument input first (shouldn't happen)
					data[cmdid] = {}
					data[cmdid][argid] = $(el).val();
				} else {
					data[cmdid][argid] = $(el).val();
				}
			}
		});

		$.ajax({
			type: "POST",
			cache: false,
			url: '/ajax/SendCommands/' + $('#commandModalCommands').data('uid'),
			data: JSON.stringify(data),
			success: function(result, textStatus, jqXHR) {location.reload(true);},
			error: function(jqXHR, textStatus, errorThrown) {}
		});
	});
});