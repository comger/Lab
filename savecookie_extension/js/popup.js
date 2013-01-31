var CURHOSTNAME = '';
function hostname(url){
    var a = document.createElement('a');
    a.href = url;
    return '.'+a.hostname;
}
function need(ahost,bhost){
	if (ahost.indexOf(bhost) >=0) return true;
	if (bhost.indexOf(ahost) >=0) return true;
	return false;
}
function getdata(tab){
	function getstore(cstores){
		var tid = tab.id;
		for(var i=0; i < cstores.length;i ++){
			var c = cstores[i].tabIds;
			for(var j=0; j < c.length; j++){
				if (tid == c[j]) return cstores[i].id;
			}
		}
		return '';
	}
	function getcookie(cookies){
		var t = hostname(tab.url);
		CURHOSTNAME = t;
		var d = {}
		for(var j=0; j < cookies.length; j++){
			//相同的domain的就需要保留了
			var i = cookies[j];	
			if (need(t,i.domain)){
				var c = i.name+'='+i.value+';';
				if (i.expirationDate){
					var e = new Date();
					e.setTime(i.expirationDate*1000);
					c += ' Expires='+e.toGMTString()+';';
				}
				c += ' Path='+i.path+';';
				c += ' Domain='+i.domain+';';
				if (i.httpOnly)
					c += ' HttpOnly;';
				if (i.secure)
					c += ' Secure;';
				//将C进行base64
				d[i.name] = btoa(c);
			}
		}
		if (d){
			var cc = [];
			for(var k in d){
				cc.push(d[k]);
			}
			$("#content").html(cc.join('\n'));
		}
		else
			$("#content").html('NOFOUND');
	}
	//tab.url
	chrome.cookies.getAllCookieStores(function(cstores){
		var csid = getstore(cstores);
		if (csid.length > 0){
			chrome.cookies.getAll({storeId:csid},function(cookies){
				getcookie(cookies);
			});
		}
	});
}
function showpopup(){
	chrome.tabs.query({active:true,currentWindow:true},function(tabs){
		if (tabs.length > 0) getdata(tabs[0]);
	});
}
//========================Loading.=================
document.addEventListener('DOMContentLoaded',function(){
	$("#save").click(function(){
	    var text = document.getElementById("content").value;
//	    var data = "data:x-application/text,"+encodeURIComponent(text);
	    var data = "data:x-application/text,"+escape(text);
		var a = document.createElement('a');
		a.setAttribute('href',data);
		a.setAttribute('target',"_blank");
		a.download = CURHOSTNAME+'-cookie.txt';
		var evt = document.createEvent("MouseEvents");
		evt.initEvent("click", true, true);
		a.dispatchEvent(evt);
	});
	showpopup();
});
