function showTab(tabId) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.content');

    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    contents.forEach(content => {
        content.classList.remove('active');
    });

    document.querySelector(`.tab[onclick="showTab('${tabId}')"]`).classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

// Fetch and display recordings
async function fetchRecordings() {
    const response = await fetch('recordings/');
    const text = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, 'text/html');
    const links = Array.from(doc.querySelectorAll('a'));
    const recordingsContainer = document.getElementById('recordings-container');

    // Filter and sort links by date (assuming filenames include timestamps)
    const videoLinks = links.filter(link => link.href.match(/\.(avi|mp4|mov|mkv)$/))
                            .sort((a, b) => b.href.localeCompare(a.href));

    videoLinks.forEach(link => {
        const relativeHref = 'recordings/' + link.getAttribute('href').split('/').pop();
        const videoItem = document.createElement('div');
        videoItem.classList.add('video-item');
        const videoDateTime = link.getAttribute('href').match(/(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})/);
        const displayDateTime = videoDateTime ? videoDateTime[0].replace('_', ' ') : '';
        videoItem.innerHTML = `
            <video width="320" height="240" controls>
                <source src="${relativeHref}" type="video/${relativeHref.split('.').pop()}">
                Your browser does not support the video tag.
            </video>
            <p>${displayDateTime}</p>
        `;
        recordingsContainer.appendChild(videoItem);
    });
}

fetchRecordings();
