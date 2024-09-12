<template>
  <div class="container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="input-fields">
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div class="input-fields">
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
      <p v-if="error">{{ error }}</p>
    </form>

    <!-- "No account? Register here" link -->
    <p class="register-link">
      No account? <router-link to="/register">Register here</router-link>.
    </p>
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

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
h2 {
  font-size: 2rem;
}

form {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.input-fields {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  margin-bottom: 15px;
  transition: border-color 0.3s;
}

input {
  border: none;
  outline: none;
}
input:focus {
  border:none;
  outline:none;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #369f6c;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #2b7d55;
}

.register-link {
  margin-top: 15px;
  text-align: center;
}

.register-link a {
  color: #369f6c;
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>


  
  
  
  