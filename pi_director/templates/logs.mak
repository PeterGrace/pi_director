<%inherit file="pi_director:templates/base.mak"/>
<%block name="BlockContent">

System Logs for : ${uuid}
<br>
% for log in logs:
                    <br><a href=/api/v1/pi_log/${uuid}?filename=${log.filename}>${log.filename}</a><br>
% endfor
</%block>
