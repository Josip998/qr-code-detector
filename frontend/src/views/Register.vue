<template>
    <div>
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit">Register</button>
        <p v-if="error">{{ error }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { auth, createUserWithEmailAndPassword } from '../firebase';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const email = ref('');
      const password = ref('');
      const error = ref('');
      const router = useRouter();
  
      const register = async () => {
        try {
          await createUserWithEmailAndPassword(auth, email.value, password.value);
          router.push('/profile'); // Redirect to profile or another page upon successful registration
        } catch (e) {
          error.value = e.message;
        }
      };
  
      return { email, password, error, register };
    }
  };
  </script>
  
  
  