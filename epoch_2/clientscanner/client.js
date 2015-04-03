/**
    The Javascript we inject into the browser to intercept events of
    interest.
      - changes in cookies
      - ajax requests
      - attempts to redirect the user
      - messages received from cross domain frames (Facebook)
*/
window.KO = {
   ajaxhistory: [], /** a history of AJAX calls */
   getcookies: function () {
       /** Parse Cookie Data */
       var pairs = document.cookie.split(";");
       var cookies = {};
       for (var i=0; i<pairs.length; i++) {
           var pair = pairs[i].split("=");
           cookies[pair[0]] = unescape(pair[1]);
       }
       return cookies;
   },
   cookies0: {}, /** before sign in */
   cookies1: {}  /** after sign in */
};

(function() {
/**
  Try to position ourselves between the site's AJAX calls and its servers
  http://stackoverflow.com/questions/3596583/javascript-detect-an-ajax-event
*/
var s_ajaxListener = new Object();
s_ajaxListener.tempOpen = XMLHttpRequest.prototype.open;
s_ajaxListener.tempSend = XMLHttpRequest.prototype.send;
s_ajaxListener.callback = function () {
  // this.method :the ajax method used
  // this.url    :the url of the requested script (including query string, if any) (urlencoded) 
  // this.data   :the data sent, if any ex: foo=bar&a=b (urlencoded)
  console.log("AJAX event made!!");
  var rec = {
      method: this.method,
      url: this.url,
      data: this.data,
  };
  window.KO.ajaxhistory.push(rec);
};

XMLHttpRequest.prototype.open = function(a,b) {
  if (!a) var a='';
  if (!b) var b='';
  s_ajaxListener.tempOpen.apply(this, arguments);
  s_ajaxListener.method = a;
  s_ajaxListener.url = b;
  if (a.toLowerCase() == 'get') {
    s_ajaxListener.data = b.split('?');
    s_ajaxListener.data = s_ajaxListener.data[1];
  }
};

XMLHttpRequest.prototype.send = function(a,b) {
  if (!a) var a='';
  if (!b) var b='';
  s_ajaxListener.tempSend.apply(this, arguments);
  if(s_ajaxListener.method.toLowerCase() == 'post') s_ajaxListener.data = a;
  s_ajaxListener.callback();
};

/** Collect Cookie Data */
window.KO.cookies0 = window.KO.getcookies();
})();

/**
    log the data from Facebook
*/
window.addEventListener('message', function (event) {
    window.KO.data = event.data;
}, false);

window.addEventListener('beforeunload', function(e) {
    /**
        Make sure the user doesn't run off anywhere
    */
    e.returnValue = "I'm afraid I can't let you do that Dave.";
    return "I'm afraid I can't let you do that Dave.";
});
