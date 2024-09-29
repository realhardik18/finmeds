

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
                    document.getElementById('output').textContent = "Processing...";
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
        "top_k": 0,
        "top_p": 0.9,
        "prompt": prompt,
        "max_tokens": 512,
        "min_tokens": 0,
        "temperature": 0.6,
        "system_prompt": "You are a medical policy reader expert. Your friend has a doubt from the following string. Help them out in 60 words. The string could be a keyword or an extract from the policy.",
        "length_penalty": 1,
        "stop_sequences": "<|end_of_text|>,<|eot_id|>",
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a medical policy reader expert. Your friend has a doubt from the following string. Help them out in 60 words. The string could be a keyword or an extract from the policy<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "presence_penalty": 1.15,
        "log_performance_metrics": false
    };

    try {
        const response = await fetch('https://api.replicate.com/v1/predictions', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${REPLICATE_API_TOKEN}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                version: "meta/meta-llama-3-70b-instruct",
                input: input,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(`HTTP error! status: ${response.status}, message: ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        return data.output || "No output generated.";
    } catch (error) {
        console.error('Error:', error);
        return `An error occurred while processing the request: ${error.message}`;
    }
}