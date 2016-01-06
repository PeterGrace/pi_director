<%inherit file="pi_director:templates/base.mak"/>
<%block name="BlockContent">

%if pis != None:
	<div class="container">
		<div class="row">

			%for pi in pis:
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
			%endfor

			<span class="btn btn-xs btn-danger">The following pis are offline:
			%for pi in offline:
				${pi.description}&nbsp;
			%endfor
			</span>

		</div>
	</div>
%endif	

</%block>
