<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<HTML xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<META http-equiv="Pragma" content="no-cache">
<META http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Medialink MWN-WAPR300N</title>
<script type="text/javascript" src="lang/b28n.js"></script>
<SCRIPT language=JavaScript src="gozila.js"></SCRIPT>
<SCRIPT language=JavaScript src="table.js"></SCRIPT>
<SCRIPT language=JavaScript src="menu.js"></SCRIPT>
<SCRIPT language=JavaScript>
def_PUN = "";
def_PPW = "";
def_WANT = "2";
def_SSID = "piesafe";
wireless_mode = "ap";
def_wirelesspassword = "wqkdx8cvmlrmr0v7";
Butterlate.setTextDomain("index_routing_virtual");
addCfg("PUN", 50, def_PUN);
addCfg("PPW", 54, def_PPW );
addCfg("wirelesspassword",59, def_wirelesspassword);
addCfg("SSID", 65, def_SSID );

var illegal_user_pass = new Array("\\r","\\n","\\","'","\"");
var illegal_user_pass1 = new Array("\\r", "\\n", "\\", ",", ";", "'", "\"", " ") ;
function initTranslate(){
	var e=document.getElementById("sure");
	e.value=_("Apply");
	var e1=document.getElementById("cancel");
	e1.value=_("Cancel");
}
function chkPOE(f) {
	var pun = document.basicset.PUN.value;
	var ppw = document.basicset.PPW.value;
	if(pun == "" || ppw == "")
	{
		alert(_("Account and password can not be empty"));
		return false;
	}
	else
	{
		if(!ill_check(pun,illegal_user_pass,_("Account"))) return false;
		if(!ill_check(ppw,illegal_user_pass,_("Password"))) return false;
		form2Cfg(f);
		return true;
	}
} 
function doFinish(f) {
	form2Cfg(f);
	var aa;
	if(document.basicset.isp[0].checked == true)
	{
	 aa=2;
	}
	else if(document.basicset.isp[1].checked == true)
	{
	 aa=3;
	}
	f.WANT1.value = aa;
	if(aa == 3)
	{
		if(!chkPOE(f))
		{
		 return;
		}
	}
	var password=document.basicset.wirelesspassword.value;
	if(password=="")
	{
	 alert(_("Wireless password can not be empty"));
	 return false;
	}
	if(password.length<8)
	{
	 alert(_("Password must be at least 8 characters"));
	 return false;
	}
	if(!ill_check(password,illegal_user_pass1,_("Wireless password"))) return false;
	for(i=0;i<password.length;i++){
	    var c = password.substr(i,1);
	    var ts = escape(c);
	    if(ts.substring(0,2) == "%u"){
		alert("Wireless password contains Chinese character.");
		return false;
		}
		}
	var da = new Date();
	document.getElementById("v12_time").value = da.getTime()/1000;
	if (true==CheckValue())
	{
	 f.submit();
	}   
}
function init() {
	initTranslate();
	cfg2Form(document.basicset);
	document.getElementById("td_PPW").innerHTML='&nbsp;&nbsp;<input name=PPW id=PPW maxLength=50 type=password class=text1 size=25 onFocus="chgPPW(this.value)" value='+def_PPW+'>';
	//weige add
	if(wireless_mode =="ap")
		document.getElementById("SSID").disabled=false;
	else
		document.getElementById("SSID").disabled=true;
	//end
	if(def_WANT==3)
	{
	 onIspchange(0);
	}
	else
	{
	 onIspchange(1);
	}
}

/*huang add*/
function chgPPW(val)
{
	if(document.getElementById("PPW").type == "password"){
		document.getElementById("td_PPW").innerHTML='&nbsp;&nbsp;<input name=PPW id=PPW maxLength=50 type=text class=text1 size=25 onBlur="chgPPW(this.value)" value='+val+'>';
		document.getElementById("PPW").focus();
		//document.getElementById("PPW").focus();
		document.getElementById("PPW").value=val;
		}
	else if(document.getElementById("PPW").type == "text"){
		document.getElementById("td_PPW").innerHTML='&nbsp;&nbsp;<input name=PPW id=PPW maxLength=50 type=password class=text1 size=25 onFocus="chgPPW(this.value)"  value='+val+'>';
		}
}
/*end add*/


function onIspchange(x)
{
 if(x==0)
 {
  document.basicset.isp[1].checked = true;
  document.getElementById("PUN").disabled=false;
  document.getElementById("PPW").disabled=false;
  document.getElementById("pppoeset").style.display="";
 }
 if(x==1)
 {
  document.basicset.isp[0].checked = true;
  document.getElementById("PUN").disabled=true;
  document.getElementById("PPW").disabled=true;
  document.getElementById("pppoeset").style.display="none";
 }
}
//weige add
function CheckValue()
{
	//var re =/^[\w\s`~!@#$^*()\-+={}\[\]\|:'<>.?/ ]+$/;
	var re = /^[0-9a-zA-Z_:]+$/;
	var sid = document.basicset.SSID.value;

	if(!re.test(sid) || sid == "")
	{
		alert(_("SSID can not contain comma, semicolon, double quotation marks, ampersand, percent, backslash."));
		document.basicset.SSID.focus();
		document.basicset.SSID.select();
		return false;
	}
	return true;
}
//end
</script>
<link rel=stylesheet type=text/css href=style.css>
<style type="text/css">
<!--
.STYLE1 {
	color: #5aa1cb;
	font-size: 30px;
	font-weight: bold;
}
.STYLE2 {
	color: #5aa1cb
}
-->
</style>
</head>
<body onLoad="init()">
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" height="100%">  
  <tr>
    <td valign="top">
  <table width="100%" align="center" cellpadding="0" cellspacing="0" class="top">
  <tr>
    <td height="25" align="right" valign="bottom"><a href="advance.asp"><script>document.write(_("Advanced Settings"));</script></a></td>
    <td width="10" align="right" valign="bottom">&nbsp;</td>
  </tr>
  </table>
<div style="width:100%; height:1px; background-color:#c0c7cd; overflow:hidden; padding:0px; margin:0px;"></div>
<table width="897" border="0" align="center" cellpadding="0" cellspacing="0">
  <tr>
    <td height="118" colspan="2" valign="top">
	<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
        <td height="110" align="center" valign="bottom"><img src="logo_420x30.jpg" width="420" height="30" /></td>
      </tr>
    </table>
	<form name="basicset" action="/goform/WizardHandle" method="post">
	<input type="hidden" name="GO" value="index.asp">
	<input type="hidden" id="v12_time" name="v12_time">
	<input type="hidden" name="WANT1" id="WANT1">
	<br>
	
	<center>
	<table width="49%" border="0" align="center" cellpadding="0" cellspacing="0" class="basicset">
		<TR>
		  <TD width="142" align="left"><strong style="font-size:16px; color:#0B4F72;">Connection Type:</strong></TD>
		  <TD width="313" align="left">&nbsp;&nbsp;&nbsp;
		    <input name="isp" value=2 type="radio" onClick="onIspchange(1)">
		    <strong><script>document.write(_("DHCP"));</script></strong>&nbsp;&nbsp;
		  <input name="isp" value=3 type="radio" onClick="onIspchange(0)">
		  <strong><script>document.write(_("ADSL Dial-up"));</script></strong>		  </TD>
		  </TR>
	</table>
	<div id="pppoeset">
	<table width="49%" border="0" align="center" cellpadding="0" cellspacing="0" class="basicset">
		<TR>
		  <TD width="142" align="right"><script>document.write(_("DSL User Name"));</script>:</TD>
		  <TD width="313" align="left" id=td_PUM>&nbsp;
		    <INPUT class=text1 maxLength=50 name=PUN id="PUN" size=25></TD>
		</TR>
		<TR>
		  <TD width="142" align="right"><script>document.write(_("DSL Password"));</script>:</TD>
		  <TD align="left" id=td_PPW>&nbsp;
		    <input class=text1 maxlength=50 name=PPW id="PPW" size=25 type=text></TD>
		</TR>
	</table>
	</div>
	<table width="49%" border="0" align="center" cellpadding="0" cellspacing="0" class="basicset">
		<TR>
          <!--<TD align="center"><span class="STYLE2">For other access methods ,click -->
		  <!--<TD align="center">For more options click"<a href='advance.asp' style="font-size:12px; color:'#0000FF'" onMouseOver="style.color='#FF9933'" onMouseOut="style.color='#0000FF'">Advanced Settings</a>"<!--<script>document.write(_("other access methods"));</script>-->
		  <TD align="center">For more options click "<a href='advance.asp' style="font-size:12px; color:#0000EE">
		  <script>document.write(_("Advanced Settings"))</script></a>"<!--<script>document.write(_("other access methods"));</script>--></TD>
		</TR>
	</table>
<hr width="50%" color="#dedfe1">
<br>
<table width="49%" border="0" align="center" cellpadding="0" cellspacing="0" class="basicset">
  <tr>
    <td width="142" align="left" valign="middle"><strong style="font-size:16px; color:#0B4F72;">Wireless SSID:</strong></td>
    <td width="215" align="left">&nbsp;
      <input name="SSID" id="SSID" type="text" class="text1" maxlength="32">&nbsp;</td>
    <td width="98" align="left">  </tr>
  <tr>
    <td width="142" align="left" valign="middle"><strong style="font-size:16px; color:#0B4F72;">Password:</strong></td>
    <td width="215" align="left">&nbsp;
      <input name="wirelesspassword" type="text" class="text1" maxlength="32">      &nbsp;</td>
    <td width="98" align="left">&nbsp;     </td>
  </tr>
  <tr>
    <td width="142" height="30" align="right" valign="middle"></td>
    <td colspan="2" align="left">&nbsp;
	<span style="font-size:12px; color:#0B4F72">(Password must be at least 8 characters)</span> </td>
  </tr>
</table> 
<center><span style="color:#0B4F72; font-size:12px;">Default Wireless WPA Key is WPA-PSK/AES</span>
<br>
<br>
<table width="49%" border="0" align="center" cellpadding="0" cellspacing="0" class="basicset">
		<TR>
          <!--<TD align="center"><span class="STYLE2">For other access methods ,click -->
		   <TD align="center">For more options click "<a href='advance.asp' style="font-size:12px; color:#0000EE">
		     <script>document.write(_("Advanced Settings"))</script></a>"<!--<script>document.write(_("other access methods"));</script>--></TD>
		</TR>
	</table>
</center>
</center>
<br>
<hr width="60%" color="#dedfe1">
<br>
<table width="50%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tr>
    <td height="45" align="center" valign="top"><input name="button" type="button" class="button1" id="sure" onClick="doFinish(document.basicset)" value="">      &nbsp;&nbsp;
      <input id="cancel" type="reset" value="" class="button1"></td></tr>
</table>
</form>
	</td>
  </tr>
</table>
</td>
</tr>
</table>
</body>
</html>







