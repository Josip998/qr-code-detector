<template>
  <div class="upload-container">
    <h1>Upload image with QR Code</h1>

    <!-- File input is hidden while loading -->
    <div v-if="!loading">
      <input type="file" id="file-upload" class="file-input" @change="handleFileUpload" />
      <label for="file-upload" class="custom-file-input">Choose File</label>
    </div>

    <!-- Loading Spinner with Text -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">Loading...</p>
    </div>
    
    <div v-if="qrCodes.length" class="qr-codes">
      <h2>What we found:</h2>
      <ul>
        <li v-for="(qrCode, index) in qrCodes" :key="index" class="qr-code-item">
          <p><strong>URL:</strong> {{ qrCode.data }}</p>
          <button @click="openUrl(qrCode.data)" class="open-url-button">Open URL</button>
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
      qrCodes: [],
      loading: false,
    };
  },
  methods: {
    async handleFileUpload(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);
      
      this.loading = true; // Show spinner

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
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      } finally {
        this.loading = false; // Hide spinner when request is done
      }
    },
    openUrl(url) {
      // Open the URL in a new tab
      window.open(url, '_blank');
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

/* Spinner Container */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

/* Spinner */
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.open-url-button {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #3498db;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.open-url-button:hover {
  background-color: #2980b9;
}

/* Loading Text */
.loading-text {
  margin-top: 10px;
  font-size: 16px;
  color: #333;
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
</style>
