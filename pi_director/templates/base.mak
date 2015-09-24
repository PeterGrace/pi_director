<html>
<head>
	<title>Pi Fleet Management</title>
	<link rel="shortcut icon" type="image/png" href="${request.static_url('pi_director:static/peng-32.png')}" />
	<link rel="stylesheet" href="${request.static_url('pi_director:static/css/bootstrap.css')}" type="text/css" media="screen" charset="utf-8" />
	<link rel="stylesheet" href="${request.static_url('pi_director:static/css/bootstrap-theme.css')}" type="text/css" media="screen" charset="utf-8" />
	<link rel="stylesheet" href="${request.static_url('pi_director:static/css/hover-screenshot.css')}" type="text/css" media="screen" charset="utf-8" />
	<link rel="stylesheet" href="${request.static_url('pi_director:static/css/footer.css')}" type="text/css" media="screen" charset="utf-8" />
	<!-- <meta http-equiv="refresh" content="60"> -->
</head>
<body>

<script type="text/javascript">
	function addLoadEvent(func) {
		var oldonload = window.onload;
		if (typeof window.onload != 'function') {
			window.onload = func;
		} else {
			window.onload = function() {
				if (oldonload) {
					oldonload();
				}
				func();
			}
		}
	}

	//http://stackoverflow.com/a/13371349/274549
	var escapeHtml = (function () {
		'use strict';
		var chr = { '"': '&quot;', '&': '&amp;', '<': '&lt;', '>': '&gt;' };
		return function (text) {
			return text.replace(/[\"&<>]/g, function (a) { return chr[a]; });
		};
	}());
</script>

<nav class="navbar navbar-inverse navbar-static-top">
	<div class="container">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</button>
			<span class="navbar-brand">Pi Fleet Management</a>
		</div>
		<div id="navbar" class="collapse navbar-collapse">
			<ul class="nav navbar-nav">
				<li><a href="/">Home</a></li>
				<li><a href="/users">Users</a></li>
			</ul>
		</div><!--/.nav-collapse -->
	</div>
</nav>
<div class="alert-messages text-center">
</div>


<div class="container">
<%block name="BlockContent"/>
</div> <!-- container -->

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="${request.static_url('pi_director:static/js/bootstrap.min.js')}"></script>
<script src="${request.static_url('pi_director:static/js/bootstrap-modal.js')}"></script>

<script>
function showAndDismissAlert(type, message) {
    var htmlAlert = '<div class="alert alert-' + type + '">' + message + '</div>';

    // Prepend so that alert is on top, could also append if we want new alerts to show below instead of on top.
    $(".alert-messages").prepend(htmlAlert);

    // Since we are prepending, take the first alert and tell it to fade in and then fade out.
    // Note: if we were appending, then should use last() instead of first()
    $(".alert-messages .alert").first().hide().fadeIn(200).delay(2000).fadeOut(1000, function () { $(this).remove(); });
}
</script>

<%block name="ScriptContent"/>

<%
	from datetime import datetime
	time_now=datetime.now()
%>

<footer class="footer">
	<div class="container">
		<p class="text-muted">Server time: ${time_now}</p>
	</div>
</footer>

</body>
</html>

