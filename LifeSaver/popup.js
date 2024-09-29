document.getElementById('getTextButton').addEventListener('click', async () => {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        chrome.scripting.executeScript(
            {
                target: { tabId: tab.id },
                function: getSelectedText,
            },
            (results) => {
                if (results && results[0]) {
                    document.getElementById('output').textContent = results[0].result || "No text selected.";
                }
            }
        );
    } catch (error) {
        console.error(error);
    }
});

function getSelectedText() {
    return window.getSelection().toString();
}
