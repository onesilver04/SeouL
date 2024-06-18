// Get references to all buttons
const aboutButton = document.getElementById('about-button');
const startButton = document.getElementById('start-button');
const gostartButton = document.getElementById('gostart-button');
const endButton = document.getElementById('end-button');
const goHomeButton = document.getElementById('go-home-button');

// Get references to all pages
const page1 = document.getElementById('page1'); // Home page
const page2 = document.getElementById('page2'); // About page
const page3 = document.getElementById('page3'); // Sign language page
const page4 = document.getElementById('page4'); // End page

// Button event listeners
aboutButton.addEventListener('click', function() {
    page1.classList.remove('active');
    page2.classList.add('active');
});

startButton.addEventListener('click', function() {
    page1.classList.remove('active');
    page3.classList.add('active');
    startVideo(); // Start video when moving to page3
});

gostartButton.addEventListener('click', function() {
    page2.classList.remove('active');
    page1.classList.add('active');
});

endButton.addEventListener('click', function() {
    page3.classList.remove('active');
    page4.classList.add('active');
    stopVideo(); // Stop video when moving to page4
});

goHomeButton.addEventListener('click', function() {
    page4.classList.remove('active');
    page1.classList.add('active');
});

// Custom functions (replace with actual video handling functions)
function startVideo() {
    const videoElement = document.getElementById('video');
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoElement.srcObject = stream;
            videoElement.play();
        })
        .catch(error => {
            console.error('Error accessing webcam:', error);
        });
}

function stopVideo() {
    const videoElement = document.getElementById('video');
    const stream = videoElement.srcObject;
    const tracks = stream.getTracks();

    tracks.forEach(track => track.stop());
    videoElement.srcObject = null;
}
