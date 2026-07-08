chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'SLACK_TOKENS') {
    // Get the 'd' cookie (XOXD token)
    chrome.cookies.get({
      url: sender.url || (sender.tab && sender.tab.url),
      name: 'd',
      // Firefox scopes cookies per contextual-identity container; without
      // storeId this only searches the default store and misses the cookie
      // when the tab is in a non-default container.
      storeId: sender.tab && sender.tab.cookieStoreId
    }, (cookie) => {
      chrome.storage.local.set({
        xoxcToken: message.xoxcToken,
        xoxdToken: cookie ? cookie.value : null,
        teamId: message.teamId
      });
    });
  }
});