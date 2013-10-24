<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<META http-equiv="Pragma" content="no-cache">
<META http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<TITLE>Firewall | MAC Control</TITLE>
<script type="text/javascript" src="lang/b28n.js"></script>
<SCRIPT language=JavaScript src="gozila.js"></SCRIPT>
<SCRIPT language=JavaScript src="menu.js"></SCRIPT>
<SCRIPT language=JavaScript src="table.js"></SCRIPT>
<SCRIPT language=JavaScript>
var filter_mode = "deny";	
var res = "00:15:af:e6:6b:da";
var enablewireless="1";
var ssidlist = "piesafe";
var Cur_ssid_index = "0";
var wl0_mode = "ap";
var flist = new Array();
var SSID = new Array();
if(res != "")
	flist = res.split(" ");
Butterlate.setTextDomain("wireless_set");
function initTranslate(){
	var e=document.getElementById("add");
	e.value=_("Add");
}
function init(f){
    initTranslate();
	if(enablewireless==1){	
		SSID = ssidlist.split(";");
		
		UpdateMBSSIDList();
		
		if(filter_mode == "disabled")
			f.FilterMode.selectedIndex = 0;
		else if(filter_mode == "allow")
			f.FilterMode.selectedIndex = 1;
		else if(filter_mode == "deny")
			f.FilterMode.selectedIndex = 2;
		var cur=document.frmSetup;
		cur.mac[0].value = "";
		cur.mac[1].value = "";
		cur.mac[2].value = "";
		cur.mac[3].value = "";
		cur.mac[4].value = "";
		cur.mac[5].value = "";
		onChangeRule();
		showList();
		if(wl0_mode=="sta"){
			f.FilterMode.disabled = true;
		}
	}else{
		alert(_("This function can only be used after the wireless function is enabled"));
		top.mainFrame.location.href="wireless_basic.asp";
	}
}
function showList()
{
	var s = '<table align=center border=1 cellspacing=0 class="content1"  style="margin-top:5px; line-height:18px; width:55%;" id="listTab">';
	for(var i=0;i<flist.length;i++)
	{
		s += '<tr><td align="center">' + flist[i] + '</td><td align="center"><input type="button" class="button" value='+_("Delete")+' onClick="onDel(this,'+i+')"></td></tr>';
	}
	s += '</table>';
	document.getElementById("list").innerHTML = s;
}
function preSubmit(f) {
	var macL = '';
	for(var i=0; i<flist.length; i++)
	{
		macL += flist[i] + " ";
	}
	if(flist.length == 0 && f.FilterMode.selectedIndex == 1)
	{
	 alert(_("rule"));
	 return false;
	}
	document.getElementById("maclist").value = macL.replace(/\W$/,"");
	//alert("Successful");
	f.submit();
	
}
function onDel(obj,dex)
{
	if(confirm(_("Are you sure to delete")))
	{
		document.getElementById("listTab").deleteRow(dex);
		var i=0;
		for(i=dex;i<flist.length;i++)
		{
			flist[i] = flist[eval(i+1)];
		}
		flist.length--;
		showList();	
    }	
}
function addMac()
{
    var cur=document.frmSetup;
    var mac1=cur.mac[0].value;
    var mac2=cur.mac[1].value;
    var mac3=cur.mac[2].value;
    var mac4=cur.mac[3].value;
    var mac5=cur.mac[4].value;
    var mac6=cur.mac[5].value;
    var add_mac;
    var tmp_mac;
    var m = /^[0-9a-fA-F]{1,2}$/;
	for(i=0;i<6;i++)
	{
	     if(!m.test(cur.mac[i].value)){
			//alert(_("Invalid MAC address"));
			alert("Please enter a valid MAC Address.");
			return;
         }
	}
    if(!(mac1!="" && mac2!="" && mac3!="" &&
    	mac4!="" && mac5!="" && mac6!=""))
    {
        //window.alert(_("Invalid MAC address"));
		window.alert("Please enter a valid MAC Address.");
        return;
    }
    if((mac1.toLowerCase()=="ff")&&(mac2.toLowerCase()=="ff")&&
       (mac3.toLowerCase()=="ff")&&(mac4.toLowerCase()=="ff")&&
       (mac5.toLowerCase()=="ff")&&(mac6.toLowerCase()=="ff"))
    {
        window.alert(_("Please enter a unicast MAC address"));
        return;
    }
     if( (mac1.charAt(1) == "1") || (mac1.charAt(1) == "3") ||
		 (mac1.charAt(1) == "5") || (mac1.charAt(1) == "7") ||
		 (mac1.charAt(1) == "9") || (mac1.charAt(1).toLowerCase() == "b")|| 
		 (mac1.charAt(1).toLowerCase() == "d") || (mac1.charAt(1).toLowerCase() == "f") )
    {
        window.alert(_("Please enter a unicast MAC address"));
        return;
    }
    cur.mac[0].value=(mac1.length==2)?mac1:("0"+mac1);
    cur.mac[1].value=(mac2.length==2)?mac2:("0"+mac2);
    cur.mac[2].value=(mac3.length==2)?mac3:("0"+mac3);
    cur.mac[3].value=(mac4.length==2)?mac4:("0"+mac4);
    cur.mac[4].value=(mac5.length==2)?mac5:("0"+mac5);
    cur.mac[5].value=(mac6.length==2)?mac6:("0"+mac6);
    if(cur.mac[0].value=="00" && cur.mac[1].value=="00" && 
       cur.mac[2].value=="00" && cur.mac[3].value=="00" && 
       cur.mac[4].value=="00" && cur.mac[5].value=="00")
    {
        //window.alert(_("Invalid MAC address"));
		window.alert("Please enter a valid MAC Address.");
        return;
    }
    if(cur.mac[0].value=="01" && cur.mac[1].value=="00" && 
       (cur.mac[2].value=="5e"|cur.mac[2].value=="5E"))
    {
        window.alert(_("Please enter a unicast MAC address"));
        return;
    }
    add_mac=cur.mac[0].value+":"+cur.mac[1].value+":"+cur.mac[2].value+":"+
		       cur.mac[3].value+":"+cur.mac[4].value+":"+cur.mac[5].value;
    if(flist.length > 15)
    {
        window.alert(_("Max.16 MAC addresses"));
	 	return;
    }
    for(var i=0; i<flist.length; i++)
    {
		if(flist[i].toLowerCase() == add_mac.toLowerCase())
		{
			window.alert(_("The MAC address already exists"));
			return;
		}
    }
   	flist[flist.length] = add_mac;
	showList();
}
function onChangeRule()
{
	if(document.getElementById("FilterMode").value == "disabled")
	{
		document.getElementById("filterTab").style.display = "none";
		document.getElementById("list").style.display = "none";
	}
	else
	{
		document.getElementById("filterTab").style.display = "";
		document.getElementById("list").style.display = "";
	}
}
function UpdateMBSSIDList() {
    	document.frmSetup.ssidIndex.length = 0;
	var defaultSelected = false;
	var selected = false;
	
	for(var i=0; i<SSID.length; i++){
		var j = document.frmSetup.ssidIndex.options.length;
		if(SSID[i] != "")
			document.frmSetup.ssidIndex.options[j] = new Option(SSID[i], i, defaultSelected, (Cur_ssid_index == i)?"selected":selected);
	}
	
}
/*
 * When user select the different SSID, this function would be called.
 */ 
function selectMBSSIDChanged()
{
	var ssid_index;
	
	ssid_index = document.frmSetup.ssidIndex.options.selectedIndex;
	
	var loc = "/goform/onSSIDChange?GO=wireless_filter.asp";

	loc += "&ssid_index=" + ssid_index; 
	var code = 'location="' + loc + '"';
   	eval(code);
}
</SCRIPT>
<link rel=stylesheet type=text/css href=style.css>
</HEAD>
<BODY leftMargin=0 topMargin=0 MARGINHEIGHT="0" MARGINWIDTH="0" onLoad="init(document.frmSetup);" class="bg">
	<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
        <td width="33">&nbsp;</td>
        <td width="679" valign="top">
		<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" height="100%">
          <tr>
            <td align="center" valign="top">
			<table width="98%" border="0" align="center" cellpadding="0" cellspacing="0" height="100%">
              <tr>
                <td align="center" valign="top">
				<form name=frmSetup method=POST action="/goform/WlanMacFilter">
				<input type=hidden name=GO value="wireless_filter.asp">
				<input type=hidden id="maclist" name="maclist">
				<table cellpadding="0" cellspacing="0" class="content1" id="table1">
					<tbody>
					<tr>
					<td width="150" align="right" class="head"><script>document.write(_("Select SSID"));</script></td>
					<td align="left">
					  &nbsp;&nbsp;&nbsp;&nbsp;<select name="ssidIndex" size="1" onChange="selectMBSSIDChanged()">
							<!-- ....Javascript will update options.... -->
					  </select>
					</td>
					</tr>
					</tbody>
				</table>
				<table cellpadding="0" cellspacing="0"  class="content3">
						<TR> <TD valign="top" align="left">&nbsp;&nbsp;&nbsp;&nbsp;<script>document.write(_(" "));</script>
					   </TR>
				</table>
				<table cellpadding="0" cellspacing="0"  class="content3" id="table2">
						<tr >
						  <td width="150" align="right" valign="top"><script>document.write(_("MAC Address Filter"));</script></td>	
						  <td valign="top" bordercolor="#FFFFFF" align="left">        
						  &nbsp;&nbsp;&nbsp;&nbsp;
						  <select size="1" name="FilterMode" id="FilterMode" onChange="onChangeRule()">
						  <option value="disabled"><script>document.write(_("Disable"));</script></option>
						  <option value="allow"><script>document.write(_("Permit"));</script></option>
						  <option value="deny"><script>document.write(_("Forbid"));</script></option>
						</select></td>
						</tr>
				</table>
				  <table border ="0" cellpadding="0" cellspacing="0" class="content1" id="filterTab"  style="margin-top:0px;">
					<tr>
					  <td width="75%" align="center"><script>document.write(_("MAC Address"));</script></td>
					  <td width="25%" align="left"><script>document.write(_(" "));</script></td>
					</tr>
					<tr align=center>
					<td height="30" >
					  <input class=text id=mac size=2 maxlength=2 onKeyUp="value=value.replace(/[^0-9a-fA-F]/g,'')" onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^0-9a-fA-F]/g,''))">:
					<input class=text id=mac size=2 maxlength=2 onKeyUp="value=value.replace(/[^0-9a-fA-F]/g,'')" onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^0-9a-fA-F]/g,''))">:
					<input class=text id=mac size=2 maxlength=2 onKeyUp="value=value.replace(/[^0-9a-fA-F]/g,'')" onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^0-9a-fA-F]/g,''))">:
					<input class=text id=mac size=2 maxlength=2 onKeyUp="value=value.replace(/[^0-9a-fA-F]/g,'')" onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^0-9a-fA-F]/g,''))">:
					<input class=text id=mac size=2 maxlength=2 onKeyUp="value=value.replace(/[^0-9a-fA-F]/g,'')" onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^0-9a-fA-F]/g,''))">:
					<input class=text id=mac size=2 maxlength=2 onKeyUp="value=value.replace(/[^0-9a-fA-F]/g,'')" onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^0-9a-fA-F]/g,''))">    </td>
					<td align=left><input name="button"  type=button class=button2 id=add onClick="addMac()"  value=""></td>
					</tr>
				  </table>  
					<div id="list" style="position:relative;visibility:visible;"></div>
				  <SCRIPT>
				   tbl_tail_save("document.frmSetup");
				  </SCRIPT>       
				</FORM>
				</td>
              </tr>
            </table></td>
          </tr>
        </table></td>
        <td align="center" valign="top" height="100%">
		<!--<script>helpInfo(_("Wireless_filter_helpinfo"));</script>-->
		<script>helpInfo(_("Wireless_filter_helpinfo1")+"<br>&nbsp;&nbsp;&nbsp;&nbsp;"+_("Wireless_filter_helpinfo2"));</script>
		</td>
      </tr>
    </table>
	<script type="text/javascript">
	  table_onload('table1');
	  table_onload('table2');
	  table_onload1('filterTab');
    </script>
</BODY>
</HTML>






