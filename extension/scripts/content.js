function extractTransactionId(url) {
    const regex = /(?:tx\/)([a-zA-Z0-9]+)/;
    const match = url.match(regex);
    if (match && match[1]) {
      return match[1];
    }
    return null;
}

function typewriterEffect(text) {
    let i = 0;
    const delay = 20; // delay in milliseconds
    
    function typeNextChar() {
        if (i < text.length) {
            document.getElementById('explanation').innerHTML += text.charAt(i);
            i++;
            setTimeout(typeNextChar, delay);
        }
    }
    
    typeNextChar();
}

const url = location.href;
const txId = extractTransactionId(url);

(async () => {
    if (txId) {
        const response = await fetch('https://solsage-api.getnimbus.io/ask', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({question: `What happened in transaction ${txId} ?`})
        });

        const explanation = await response.json()
            .then((res) => res.result)
            .catch((err) => console.log(err));

        // const explanation = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        
        if (explanation) {
            console.log(explanation);
            const explanationDiv = document.createElement('div');
            explanationDiv.id = 'explanation';
            explanationDiv.classList.add('color-secondary-text', 'type--caption', 'typewriter');

            if (url.includes('https://solscan.io')) {
                document.getElementsByClassName('adsHeaderTextWrapper')[0].insertAdjacentElement('afterend', explanationDiv);
            } else if (url.includes('https://explorer.solana.com')) {
                document.getElementsByClassName('header-body')[0].insertAdjacentElement('afterend', explanationDiv);
            } else if (url.includes('https://solana.fm')) {
                document.getElementsByTagName('div')[0].insertAdjacentElement('afterbegin', explanationDiv);
            }

            typewriterEffect(explanation);
        }
    }
})();