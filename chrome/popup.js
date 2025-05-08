document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get(['xoxcToken', 'xoxdToken', 'teamId'], (data) => {
    document.getElementById('tokens').innerText =
      `Team ID: ${data.teamId || ''}\n` +
      `XOXC: ${data.xoxcToken || ''}\n` +
      `XOXD: ${data.xoxdToken || ''}`;
  });
}); 