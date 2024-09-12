<template>
  <div>
    <nav>
      <nav class="subnav">
      <!-- Home and Profile as links -->
      <router-link to="/">QR Code Detector</router-link>
      <router-link to="/about">About</router-link>

      <router-link to="/profile" v-if="isLoggedIn">Profile</router-link>
      
      <!-- Use buttons for Login, Register, and Logout -->
      <template v-if="!isLoggedIn">
        <button @click="navigateTo('login')" class="nav-button">Login</button>
      </template>
      
      <button v-if="isLoggedIn" @click="logout" class="nav-button-logout">Logout</button>
    </nav>
    </nav>
    <router-view />
  </div>
</template>



<script>
import { getAuth, signOut } from 'firebase/auth';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const isLoggedIn = ref(false);
    const router = useRouter(); // Get the router instance

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
        // After logging out, navigate to the home page
        router.push('/');
      } catch (error) {
        console.error('Error during logout:', error);
      }
    };

    const navigateTo = (route) => {
      router.push({ path: `/${route}` });
    };

    onMounted(() => {
      checkAuthStatus();
    });

    return { isLoggedIn, logout, navigateTo };
  },
};
</script>


<style scoped>
nav {
  display: flex;
  justify-content: space-around;
  padding: 0.5em;
  background-color: #f3f4f6;
}

nav a {
  text-decoration: none;
  color: #42b883;
  font-weight: bold;
  font-size: 18px;
}

nav a.router-link-active {
  color: #333;
}

button.nav-button {
  background-color: #42b883;
  border: none;
  color: white;
  font-weight: bold;
  padding: 0.5em 1em;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 5px;
}

button.nav-button:hover {
  background-color: #36966f;
}

button.nav-button:focus {
  outline: none;
}

button.nav-button-logout {
  background-color: #b84242;
  margin-left: 10px;
  border: none;
  color: white;
  font-weight: bold;
  padding: 0.5em 1em;
  cursor: pointer;
  border-radius: 5px;
}

.subnav {
  width: 50%;
}

button.nav-button-logout:hover {
  background-color: #963636;
}

button.nav-button-logout:focus {
  outline: none;
}
</style>




