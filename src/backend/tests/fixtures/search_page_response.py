class SearchPageResponse:
    RESPONSE = """
<html>
<head>
  <link rel="stylesheet" type="text/css" href="#>
</head>


<body onload="return ReloadPage()" style="overflow: auto">

  <form name="SearchParameters" method="post" action="Search.aspx?ID=100" onkeypress="javascript:return WebForm_FireDefaultButton(event, 'SearchSubmit')" id="SearchParameters" onsubmit="return ValidateSearchParameters()">
<div>
<input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="bleh" />
<input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="boo" />
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="billy bob" />
</div>
<div>

  <input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="thornton" />
  <input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="validate" />
</div>
    <input type="hidden" name="NodeID" value="a lot of nodes" />
    <input type='checkbox' id='chkExactName'  name='ExactName' checked='checked' LabelName='Exact Name:'/>
</html>
  """
