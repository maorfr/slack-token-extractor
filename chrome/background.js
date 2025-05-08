chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'SLACK_TOKENS') {
    // Get the 'd' cookie (XOXD token)
    chrome.cookies.get({
      url: sender.tab.url,
      name: 'd'
    }, (cookie) => {
      // Save or display tokens as needed
      chrome.storage.local.set({
        xoxcToken: message.xoxcToken,
        xoxdToken: cookie ? cookie.value : null,
        teamId: message.teamId
      });
    });
  }
}); 