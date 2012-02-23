var w = window;
var s = document.getElementsByTagName('script');
var site = new RegExp("http.*//[^/]+/").exec(s[s.length - 1].src);
w.location = site+"feedback?url="+encodeURIComponent(w.location);
