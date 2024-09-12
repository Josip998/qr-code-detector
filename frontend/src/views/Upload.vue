<template>
    <div class="upload-container">
      <h1>Upload QR Code Image</h1>
      <div>
        <input type="file" id="file-upload" class="file-input" @change="handleFileUpload" />
        <label for="file-upload" class="custom-file-input">Choose File</label>
      </div>
      <div v-if="qrCodes.length" class="qr-codes">
        <h2>Detected QR Codes:</h2>
        <ul>
          <li v-for="(qrCode, index) in qrCodes" :key="index" class="qr-code-item">
            <p><strong>Data:</strong> {{ qrCode.data }}</p>
            <p><strong>Rectangle:</strong> x: {{ qrCode.rect.x }}, y: {{ qrCode.rect.y }}, width: {{ qrCode.rect.width }}, height: {{ qrCode.rect.height }}</p>
            <img :src="qrCode.imagePath" alt="QR Code Image" class="qr-code-image" />
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { getAuth } from 'firebase/auth';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        qrCodes: []
      };
    },
    methods: {
      async handleFileUpload(event) {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
  
        try {
          const auth = getAuth();
          const user = auth.currentUser;
          if (user) {
            const token = await user.getIdToken();
            const response = await axios.post('http://localhost:8000/detect-qr/', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${token}`
              }
            });
            this.qrCodes = response.data.qr_codes;
          } else {
            console.error('User is not authenticated');
            // Handle the case where the user is not authenticated
          }
        } catch (error) {
          console.error('Error uploading file:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .upload-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 800px;
    margin: auto;
    margin-top: 50px;
    padding: 2em;
    background: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  ul {
      list-style-type: none; 
      padding: 0; 
      margin: 0; 
    }
  
  h1 {
    text-align: center;
    color: #333;
  }
  
  .file-input {
    /* display: block;
    margin: 1em auto; */
    display: none;
  }

  .custom-file-input {
      display: inline-block;
      padding: 10px 20px;
      font-size: 16px;
      color: #fff;
      background-color: #369f6c;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
    }

    .custom-file-input:hover {
      background-color: #16662a;
    }

    .custom-file-input:active {
      background-color: #16662a;
    }

    /* This makes sure the label is styled */
    .file-container {
      position: relative;
      display: inline-block;
    }

    .file-container label {
      cursor: pointer;
    }

    .qr-codes {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin-top: 50px;
      border: 1px solid #ddd; 
      border-radius: 8px; 
      padding: 16px; 
      margin-bottom: 16px; 
      background-color: #f9f9f9; 
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
    }
  
  /* .qr-codes {
    margin-top: 2em;
  }
  
  .qr-codes h2 {
    color: #333;
  }
  
  .qr-code-item {
    margin-bottom: 1.5em;
    padding: 1em;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #fff;
  }
  
  .qr-code-item p {
    margin: 0.5em 0;
  }
  
  .qr-code-image {
    max-width: 100%;
    height: auto;
    display: block;
    margin-top: 0.5em;
  } */
  </style>
  
  
  