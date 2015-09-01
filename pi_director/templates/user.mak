<%inherit file="pi_director:templates/base.mak"/>
<%block name="BlockContent">

%if pis != None:
          <h2 class="sub-header">Users</h2>
          <div class="table-responsive" style="overflow-x: visible;">
            <table class="table table-striped" id="PiTable">
              <thead>
                <tr>
                  <th>E-Mail</th>
				  <th>Authorized?</th>
				  <th>Authorize</th>
				  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
%for user in users:
                <tr>
				  <td>${user.email}</td>
				  %if user.AccessLevel == 2:
				  	<td><span class="glyphicon glyphicon-ok-circle"></span></td>
			      %else:
				  	<td><span class="glyphicon glyphicon-remove-circle"></span></td>
				  %endif
				  <td><button type="button" data-id="${user.email}" href="#toggleAdmin" class="btn btn-xs btn-primary userauthorize">Authorize</button></td>
				  <td><button type="button" data-id="${user.email}" href="#deleteAdmin" class="btn btn-xs btn-danger userdelete">Delete</button></td>
                </tr>
%endfor
%endif
			</tbody>
</table>
</div> <!-- table-responsive -->

</%block>

<%block name="ScriptContent">
<script>
addLoadEvent(function() {
	$(".userdelete").click(function(e) {
		e.preventDefault();
		var id = $(this).attr("data-id");
		$.ajax({
			type: "DELETE",
			url: '/ajax/User/'+id,
			success: function(formdata) {
                location.reload(true);
			}
		});
	});
});
addLoadEvent(function() {
	$(".userauthorize").click(function(e) {
		e.preventDefault();
		var id = $(this).attr("data-id");
		$.ajax({
			type: "POST",
			url: '/ajax/User/'+id,
            data: JSON.stringify({'AccessLevel': 2}),
			success: function(formdata) {
                location.reload(true);
			}
		});
	});
});

</script>
</%block>
