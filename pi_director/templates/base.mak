<HTML>
<HEAD>
  <title>Pi Fleet Management</title>
  <link rel="shortcut icon" type="image/png" href="${request.static_url('pi_director:static/peng-32.png')}" />
  <link rel="stylesheet" href="${request.static_url('pi_director:static/css/bootstrap.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pi_director:static/css/bootstrap-theme.css')}" type="text/css" media="screen" charset="utf-8" />
  <link rel="stylesheet" href="${request.static_url('pi_director:static/css/hover-screenshot.css')}" type="text/css" media="screen" charset="utf-8" />
</HEAD>
<BODY>
<script>
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
          <a class="navbar-brand" href="#">Pi Fleet Management</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="/users">Users</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

<div class="container">
<%block name="BlockContent"/>
</div> <!-- container -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="${request.static_url('pi_director:static/js/bootstrap.min.js')}"</script>
<script src="${request.static_url('pi_director:static/js/bootstrap-modal.js')}"</script>
<%block name="ScriptContent"/>
</BODY>
</HTML>

