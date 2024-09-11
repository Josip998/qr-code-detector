<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/profile">Profile</router-link>
      <template v-if="!isLoggedIn">
        <router-link to="/register">Register</router-link>
        <router-link to="/login">Login</router-link>
      </template>
      <button v-if="isLoggedIn" @click="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { getAuth, signOut } from 'firebase/auth';
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const isLoggedIn = ref(false);

    const checkAuthStatus = () => {
      const auth = getAuth();
      auth.onAuthStateChanged(user => {
        isLoggedIn.value = !!user;
      });
    };

    const logout = async () => {
      try {
        const auth = getAuth();
        await signOut(auth);
        // Optionally clear any additional state here
        window.location.reload();  // Refresh page to update navigation
      } catch (error) {
        console.error('Error during logout:', error);
      }
    };

    onMounted(() => {
      checkAuthStatus();
    });

    return { isLoggedIn, logout };
  },
};
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-around;
  padding: 1em;
  background-color: #f3f4f6;
}

nav a {
  text-decoration: none;
  color: #42b883;
  font-weight: bold;
}

nav a.router-link-active {
  color: #333;
}

button {
  background: none;
  border: none;
  color: #42b883;
  font-weight: bold;
  cursor: pointer;
}
</style>


