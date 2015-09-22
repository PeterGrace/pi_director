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
	});

});

