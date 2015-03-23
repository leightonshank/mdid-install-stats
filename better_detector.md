These sites need better MDID detection

- https://ccdid.coloradocollege.edu/
  This site is MDID3, but has been customized and the help link has
  been removed.
- https://rdidweb.risd.edu/
  This is an MDID2 install, but it has been customized and the help
  link id is _ctl1_HelpLink instaed of _ctl0_HelpLink
- https://vasari.mcah.columbia.edu/
  A heavily customized version of MDID3

Some ideas for additional MDID3 detectors:
- `<span id="javascriptwarning">You have JavaScript disabled. MDID works better with JavaScript enabled.</span>`
- `<div id="basket-content"><div id="basket-scroll-right"></div><div id="basket-scroll-left"></div><div id="basket-thumbs"><br />No image selected.
</div></div>`
- [server_url]/api/presentations/currentuser/ should always return json that begins `{"result": "ok", "presentations":` if it's an MDID3 server, and it's a pretty idiosyncratic url
    - https://vasari.mcah.columbia.edu/api/presentations/currentuser/
    - https://ccdid.coloradocollege.edu/api/presentations/currentuser/  _versus_
    - https://rdidweb.risd.edu/api/presentations/currentuser/
    
