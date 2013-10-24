<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<HTML xmlns="http://www.w3.org/1999/xhtml">
<head>
<META http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Medialink MWN-WAPR300N</title>
<script type="text/javascript" src="lang/b28n.js"></script>
<SCRIPT language=JavaScript src="gozila.js"></SCRIPT>
<SCRIPT language=JavaScript src="menu.js"></SCRIPT>
<SCRIPT language=JavaScript src="table.js"></SCRIPT>
<SCRIPT language=JavaScript>
var error=new Array(_("No Ethernet cable connected to WAN port!"),_("No Internet access, please check your online settings!"));
message="1";
message2="0";
addCfg("Username",39,"");
addCfg("Password",40,"FledNanders");

var username1="";
var password1="FledNanders";

Butterlate.setTextDomain("index_routing_virtual");
function initTranslate(){
	var e=document.getElementById("sure");
	e.value=_("Apply");
	var e1=document.getElementById("cancel");
	e1.value=_("Cancel");
}
function init(){
	initTranslate();
	Login.Username.value="";
	Login.Password.value="";
//	Login.Password.focus();
    Login.Username.focus();
	if(message==0)
	{
	 document.getElementById("message").innerHTML=_("No Ethernet cable connected to WAN port!");
	}
	else if(message==2 || message==3)
	{
	 document.getElementById("message").innerHTML=_("No Internet access, please check your online settings!");
	}
	else
	{
	 document.getElementById("message").innerHTML="&nbsp;";
	}
	if(message2 == 0)
	{
		show_hide("login_tip",0);		
	}
}

function enterDown(f,e)
{
	var char_code = e.charCode ? e.charCode :e.keyCode;
	if(char_code == 13)
	{
		if(!preSubmit(f))
			return;
	}else{
		return;
	}
}

function preSubmit(f)
{	
    if(f.nocheck.checked)
	{
	 	f.checkEn.value=1;
	}
	else
	{
	 	f.checkEn.value=0;
	}
	
	if(f.Username.value!=username1)
	{
	alert(_("Please enter the correct Username."));
	f.Username.value="";
	 f.Username.focus();
	return false;
	}
	if(f.Password.value!=password1)
	{
	alert(_("Please enter the correct Password."));
	f.Password.value="";
	f.Password.focus();
	return false;
	}
	if(f.Password.value.length>12)
	{
	    alert(_("Password must be smaller than 13 characters."));
		f.Password.value=""; 
		f.Password.focus();
		return false;
	}
	f.submit();
}
</script>
<link rel=stylesheet type=text/css href=style.css>
<style type="text/css">
.login{COLOR: #000000; FONT-FAMILY:"Arial"; font-size:12px; border:solid 1px #0B4F72; line-height:30px; margin-top:100px;}
.STYLE1 {
	color:#000000;
}
</style>
</head>
<body onLoad="init()">
<form name="Login" method="post" action="/LoginCheck">
<!--<input type=hidden name=Username value="">-->
<input type="hidden" name="checkEn" value="0">
<table width="420" border="0" align="center" cellpadding="0" cellspacing="0" class="login">
	<tr><td style="background-color:#0B4F72; color:#FFFFFF; height:35px;" colspan="2"><font size="+1" style="font-weight:bold"> &nbsp;&nbsp;<script>document.write(_("Login"));</script></font></td></tr>
  <tr>
    <!--<td width="20" align="right"></td>-->
    <td colspan="2" align="center"><span class="STYLE1">
      <div id="message"></div>
    </span></td>
  </tr>
  
 <tr>
    <td width="120" align="right"><script>document.write(_("Username"));</script>:</td>
    <td align="left">&nbsp;&nbsp;<input type="text" name="Username" maxlength="12" style="width:130px;" onKeyDown="enterDown(document.Login,event);"/>
    <span class="STYLE1">(<script>document.write(_("Default Username"));</script>:&nbsp;admin)</span></td>
  </tr>
  <tr>
    <td width="120" align="right"><script>document.write(_("Password"));</script>:</td>
    <td align="left">&nbsp;&nbsp;<input type="text" name="Password" maxlength="32" style="width:130px;" onKeyDown="enterDown(document.Login,event);"/>
    <span class="STYLE1">(<script>document.write(_("Default Password"));</script>:&nbsp;admin)</span></td>
  </tr>
  <tr id="login_tip" >
    <td >&nbsp;</td>
    <td align="left">&nbsp;&nbsp;<input type="checkbox" name="nocheck"/>
    <script>document.write(_("No longer prompts "));</script></td>
  </tr>
  <tr>
    <td height="35" colspan="2" align="center" valign="bottom"><input type="button" id="sure" value="" class="button1"   onClick="preSubmit(document.Login)">&nbsp;&nbsp;<input type="reset" id="cancel" value="" class="button1" ></td>
  </tr>
  <tr>
    <td colspan="2" align="center">&nbsp;</td>
  </tr>
</table>
</form>
</body>
</html>






