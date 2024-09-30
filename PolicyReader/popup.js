document.getElementById('getTextButton').addEventListener('click', async () => {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        chrome.scripting.executeScript(
            {
                target: { tabId: tab.id },
                function: getSelectedText,
            },
            async (results) => {
                if (results && results[0]) {
                    const selectedText = results[0].result || "No text selected.";
                    document.getElementById('output').textContent = "FinMeds is Thinking...";
                    const llmOutput = await getLLMOutput(selectedText);
                    document.getElementById('output').textContent = llmOutput;
                }
            }
        );
    } catch (error) {
        console.error(error);
        document.getElementById('output').textContent = "An error occurred: " + error.message;
    }
});

function getSelectedText() {
    return window.getSelection().toString();
}

async function getLLMOutput(prompt) {
    const input = {
        messages: [
            {
                role: 'system',
                content: 'You are an expert medical policy reader who has to answer/explain the given question/keyword in less than 60 words strictly'
            },
            {
                role: 'user',
                content: prompt
            }
        ],
        model: 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    };

    try {
        const response = await fetch('https://api.together.xyz/v1/chat/completions', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'content-type': 'application/json',
                'authorization': 'Bearer d64fa560a12a4ad9cfa423a368cda858d86c403c6ffc6a4cff31457bbc225fe9'
            },
            body: JSON.stringify(input),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(`HTTP error! status: ${response.status}, message: ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        return data.choices[0].message.content; // Adjust this to get the correct output format
    } catch (error) {
        console.error('Error:', error);
        return `An error occurred while processing the request: ${error.message}`;
    }
}
