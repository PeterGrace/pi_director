$(document).ready(function() {
	$('#commandResultDelete').click(function(e) {
		e.preventDefault();
		$.ajax({
			type: 'POST',
			cache: false,
			url: '/ajax/CommandResults/' + $('#commandResultModal').data('uid'),
			data: {},
			success: function(result, textStatus, jqXHR) {
				location.reload(true);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				//TODO: handle errors.
			}
		});
	});
	
	$('#commandResultModal').on('show.bs.modal', function(e) {
		var myid = $(e.relatedTarget).data('id');

		if (typeof(myid) == 'undefined') {
			return;
		}

		$('#commandResultModal').attr('data-uid', myid);
		var $resultTBody = $('#commandResults tbody:first').empty();

		$.ajax({
			type: 'GET',
			cache: false,
			url: '/ajax/CommandResults/' + myid,
			data: {},
			success: function(result, textStatus, jqXHR) {
				if (result.status == 'OK') {
					for (cmdid in result.data) {
						var cmd = result.data[cmdid];
						cmdtext = '<pre>' + escapeHtml(cmd.cmd + ' ' + cmd.args.join(' ')) + '</pre>';
						restext = '<pre>' + (cmd.result ? escapeHtml(cmd.result) : '&nbsp') + '</pre>';
						$resultTBody.append(
							'<tr><td>' + cmdtext + '</td><td>' + restext + '</td></tr>'
						);
					}
				}
			},
			error: function(jqXHR, textStatus, errorThrown) {
				//TODO: handle errors
			}
		});
	});
});

