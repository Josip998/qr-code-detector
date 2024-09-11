<template>
    <div class="home-container">
      <h1>Home</h1>
      <h2>Welcome to our QR Code Detector app</h2>
      <router-link to="/upload" class="upload-link">Upload Image</router-link>

    </div>
  </template>
  
  <script>
  export default {
    name: 'Home'
  }
  </script>
  
  <style scoped>
  .home-container {
    max-width: 600px;
    margin: auto;
    padding: 2em;
    text-align: center;
    background: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    color: #333;
    margin-bottom: 1.5em;
  }
  
  .upload-link {
    display: inline-block;
    padding: 0.75em 1.5em;
    margin-top: 1em;
    color: #fff;
    background-color: #42b983;
    border-radius: 4px;
    text-decoration: none;
    font-size: 1.1em;
    transition: background-color 0.3s;
  }
  
  .upload-link:hover {
    background-color: #369f6c;
  }
  </style>
  
  