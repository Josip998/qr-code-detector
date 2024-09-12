<template>
    <div class="container">
      <h1>User Profile</h1>
      <button @click="logout">Logout</button>
      <div v-if="scans.length" class="container-for-items">
        <h2>Your Scans:</h2>
        <ul>
          <li v-for="(scan, index) in scans" :key="index" class="items-container">
            <p><strong>QR Code URL:</strong> {{ scan.data }}</p>
            <p><strong>Date:</strong> {{ formatDate(scan.timestamp) }}</p>
            <!-- Display the image -->
            <!-- <img v-if="scan.image_path" :src="`C:\Users\Josip\Desktop\qr code detector\processed_images/${scan.image_path}`" alt="Scan Image" class="scan-image" /> -->
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { getAuth, signOut } from 'firebase/auth';
  import axios from 'axios';
  import { format, parseISO } from 'date-fns';
  
  export default {
    data() {
      return {
        scans: [],
      };
    },
    async created() {
      try {
        const auth = getAuth();
        const user = auth.currentUser;
        if (user) {
          const token = await user.getIdToken();
          const response = await axios.get('http://localhost:8000/user-scans/', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          // Flatten the array of qr_codes from each scan
          this.scans = response.data.flatMap(scan => scan.qr_codes);
        } else {
          this.$router.push('/login');
        }
      } catch (error) {
        console.error('Error fetching user scans:', error);
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    methods: {
      async logout() {
        try {
          const auth = getAuth();
          await signOut(auth);
          this.$router.push('/login');
        } catch (error) {
          console.error('Error during logout:', error);
        }
      },
      formatDate(timestamp) {
        // Parse the ISO timestamp and format it nicely
        const date = parseISO(timestamp);
        return format(date, 'MMMM dd, yyyy HH:mm:ss');
      },
    },
  };
  </script>
  
  <style scoped>

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

ul {
      list-style-type: none; 
      padding: 0; 
      margin: 0; 
    }

button {
  padding: 10px;
  background-color: #369f6c;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.container-for-items{
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

.items-container {
  border: 1px solid #ddd; 
  border-radius: 8px; 
  padding: 16px; 
  margin-bottom: 16px; 
  background-color: #f9f9f9; 
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
}

  .user-profile-container {
    max-width: 800px;
    margin: auto;
    padding: 2em;
    background: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    color: #333;
    margin-bottom: 1.5em;
  }
  
  .scan-item {
    margin-bottom: 1.5em;
    padding: 1em;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #fff;
  }
  
  .scan-item p {
    margin: 0.5em 0;
  }
  
  .scan-image {
    max-width: 100%;
    height: auto;
  }
  </style>
  
  
  
  
  