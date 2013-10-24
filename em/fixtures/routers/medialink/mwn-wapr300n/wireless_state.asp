<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<META http-equiv="Pragma" content="no-cache">
<META http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<TITLE>Wireless State</TITLE>
<script type="text/javascript" src="lang/b28n.js"></script>
<SCRIPT language=JavaScript src="gozila.js"></SCRIPT>
<SCRIPT language=JavaScript src="menu.js"></SCRIPT>
<SCRIPT language=JavaScript src="table.js"></SCRIPT>
<script language="javascript">
var enablewireless="1";
var ssidlist = "piesafe";
var Cur_ssid_index = "0";

var SSID = new Array();
Butterlate.setTextDomain("wireless_set");
function initTranslate(){
	var e=document.getElementById("refresh_btn");
	e.value=_("Refresh");
}
function init(){
	initTranslate();
	if(enablewireless==1){
		SSID = ssidlist.split(";");
		UpdateMBSSIDList();
	}else{
		alert(_("This function can only be used after the wireless function is enabled"));
		top.mainFrame.location.href="wireless_basic.asp";
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
	
	var loc = "/goform/onSSIDChange?GO=wireless_state.asp";

	loc += "&ssid_index=" + ssid_index; 
	var code = 'location="' + loc + '"';
   	eval(code);
}
</script>
<link rel=stylesheet type=text/css href=style.css>
</HEAD>
<BODY leftMargin=0 topMargin=0 MARGINHEIGHT="0" MARGINWIDTH="0" onLoad="init();" class="bg">
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
				<FORM name=frmSetup action="" method=post >
					<table cellpadding="0" cellspacing="0" class="content1" id="table1">
					<tbody>
					<tr>
					<td width="100" align="right" class="head"><script>document.write(_("Select SSID"));</script></td>
					<td align="left">
					  &nbsp;&nbsp;&nbsp;&nbsp;<select name="ssidIndex" size="1" onChange="selectMBSSIDChanged()">
							<!-- ....Javascript will update options.... -->
					  </select>
					</td>
					</tr>
					</tbody>
					</table>
					<table  class="content3" id="table2">
					   <TR> <TD valign="top" align="left"><script>document.write(_("This page displays the connection information of the wireless router"));</script>
					   </TR>
						<TR> <TD align="center">
							  <input id="refresh_btn" type=button class=button2 value="" onclick=refresh("wireless_state.asp")></TD>
						</TR>
							<tr><td>	
							 <TABLE align=center cellPadding=0 cellSpacing=0 width=450>
									<TBODY>
									  <TR>
										<TD width=450><TABLE align=center border=1 cellPadding=0 cellSpacing=0 class=content1 style="margin-top:0px;" id="table1">
											<TBODY>
											  <TR>
												<TD align=middle width=20%><script>document.write(_("NO."));</script></TD>
												<TD align=middle width=50%><script>document.write(_("MAC address"));</script></TD>
												<TD align=middle width=30%><script>document.write(_("Bandwidth"));</script></TD>
											  </TR> 
                              <tr><td width=20% align=middle>0</td><td width=50% align=middle>1C:E6:2B:A7:8F:14</td><td width=30% align=middle>20M</td></tr><tr><td width=20% align=middle>1</td><td width=50% align=middle>00:23:31:6B:A9:89</td><td width=30% align=middle>20M</td></tr><tr><td width=20% align=middle>2</td><td width=50% align=middle>10:40:F3:90:E5:E8</td><td width=30% align=middle>20M</td></tr><tr><td width=20% align=middle>3</td><td width=50% align=middle>28:EF:01:2B:89:A4</td><td width=30% align=middle>20M</td></tr><tr><td width=20% align=middle>4</td><td width=50% align=middle>CC:6D:A0:0A:D3:75</td><td width=30% align=middle>20M</td></tr>
											</TBODY>
										</TABLE></TD>
									  </TR>
								  </TABLE>
								  <br>
								  </td>
								<td class=vline rowspan=15 width="27"><br></td>
							  </tr>			
							 <TR><TD class=hline></TD></TR>   
						   </tbody>
						</table>
				</FORM>
				</td>
              </tr>
            </table></td>
          </tr>
        </table></td>
        <td align="center" valign="top" height="100%">
		<script>helpInfo(_("Wireless_state_helpinfo1")+"<br>&nbsp;&nbsp;&nbsp;&nbsp;"+_("Wireless_state_helpinfo2"));</script>
		</td>
      </tr>
    </table>
	<script type="text/javascript">
	  table_onload('table1');
    </script>
</BODY>
</HTML>






