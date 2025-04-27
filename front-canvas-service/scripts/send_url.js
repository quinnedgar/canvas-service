
function exportUrl(url){
    fetch('http://localhost:5000/import_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({url: url})
    })

    .then(response => response.json())
    .then(data => console.log('Response from backend:', data))
    .catch(error => console.error('Error:', error));
}


chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    let Url = tabs[0].url;
    exportUrl(Url);
});