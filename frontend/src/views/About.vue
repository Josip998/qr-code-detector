<template>
    <div class="about-container">
      <h1>About This App</h1>
      <p>
        Welcome to our QR Code Detection App! This application allows you to upload images
        containing QR codes, which are then detected and processed to extract the information encoded in them.
        Here's a step-by-step guide on how it works:
      </p>
      
      <h2>How It Works</h2>
      <ol>
        <li>
          <strong>Upload Image:</strong> Click on the "Choose File" button to upload an image that contains a QR code.
        </li>
        <li>
          <strong>Processing:</strong> Our app will process the uploaded image, detect the QR Code and then scan it for URLs.
        </li>
        <li>
          <strong>Detection Results:</strong> The detected QR codes and their details will be displayed on the screen.
        </li>
        <p>Technologies used: Python Image Recognition, Firebase (Authentication and Cloud Firestore) and Vue.js.</p>
        <p>
  This application was developed as an IT project for the Computer Vision course, under the guidance of dr. sc. Željko Marušić. It is part of the Data Science and Engineering program at the University of Mostar. The project was created by students Josip Bošnjak, Tomislav Marušić and Ivan Brkan.
</p>
      </ol>
  
      <h2>Before and After</h2>
      <div class="images">
        <div class="image-container">
          <h3>Before</h3>
          <img src="../assets/before.jpg" alt="Before QR Code Detection" />
          <p class="example">Example of an image that contains a QR Code before processing.</p>
        </div>
        <div class="image-container">
          <h3>After</h3>
          <img src="../assets/after.jpg" alt="After QR Code Detection" />
          <p class="example">After processing, the app finds the QR Code and makes a red rectangle box around it.</p>
        </div>
        <div class="image-container">
          <h3>Scanned QR Code</h3>
          <img src="../assets/scanned.jpg" alt="Scanned QR Code" />
          <p class="example">That box is then cut out from the image and the QR Code is scanned for URLs</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'About'
  };
  </script>
  
  <style scoped>
  .about-container {
    padding: 20px;
    max-width: 800px;
    margin: auto;
  }

  .example {
    font-style: italic;
    font-weight: bold;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  h2 {
    margin-top: 20px;
    color: #369f6c;
  }
  
  ol {
    margin: 20px 0;
  }
  
  ol li {
    margin-bottom: 10px;
  }
  
  .images {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
  }
  
  .image-container {
    text-align: center;
    margin: 10px;
  }
  
  .image-container img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  
  .image-container p {
    margin-top: 10px;
    font-size: 0.9rem;
    color: #555;
  }
  </style>
  
  