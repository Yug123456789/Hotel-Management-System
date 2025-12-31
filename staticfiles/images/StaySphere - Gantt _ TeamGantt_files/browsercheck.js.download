/* eslint-disable */
if (isUnsupportedBrowser()) {
  window.location = '/unsupported-browser.html';
}

function isUnsupportedBrowser() {
  var userAgent = navigator.userAgent;
  var isIE =
    userAgent.indexOf('MSIE ') > -1 || userAgent.indexOf('Trident/') > -1;

  return isIE;
}
