
fetch('http://localhost:5000/video_feed')
  .then(response => {
    // handle video stream in extension
  })
  .catch(error => console.log('Error fetching video feed:', error));
