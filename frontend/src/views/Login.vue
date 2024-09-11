<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
        <p v-if="error">{{ error }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { auth, signInWithEmailAndPassword } from '../firebase';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const email = ref('');
      const password = ref('');
      const error = ref('');
      const router = useRouter();
  
      const login = async () => {
        try {
          // Ensure you pass the auth instance along with email and password
          await signInWithEmailAndPassword(auth, email.value, password.value);
          router.push('/profile'); // Redirect to profile or another page upon successful login
        } catch (e) {
          error.value = e.message;
        }
      };
  
      return { email, password, error, login };
    }
  };
  </script>
  
  
  
  