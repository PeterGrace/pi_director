<%inherit file="pi_director:templates/base.mak"/>
<%block name="BlockContent">

%if pis != None:
		<div class="row">

			<% counter = 0 %>
			%for pi in pis:
			<% counter += 1 %>
			<div class="col-lg-3 col-md-4 col-xs-6 thumb">
				<div class="icon">
					<div class="thumbnail">
						<a class="thumbnail" href="#">
							<img class="img-responsive" src="${request.resource_url(request.context,'api/v1/screen/'+pi.uuid)}" alt="${pi.uuid}">
						</a>
					<div class="caption">
						<h3>${pi.uuid}</h3>
						<p>${pi.description}</p>
						%for tag in pi.tags:
                    		<span class="btn btn-xs btn-primary">${tag.tag}</span>
						%endfor

					</div>
					</div>
				</div>	
			</div>	
			%if (counter % 4) == 0:
				<div class="clearfix visible-lg-block"></div>
			%endif

			%if (counter % 3) == 0:
				<div class="clearfix visible-md-block"></div>
			%endif

			%if (counter % 2) == 0:
				<div class="clearfix visible-xs-block"></div>	
			%endif

			%endfor

		</div>

	<span class="alert alert-warning">The following pis are offline:
	%for pi in offline:
		%if pi.description == "":
			${pi.uuid},&nbsp;
		%else:	
			${pi.description},&nbsp;
		%endif	
	%endfor
	</span>

%endif	

</%block>

<%block name="ScriptContent">
<script type="text/javascript">
setInterval(function() {location.reload()},30000);
</script>
</%block>
