import { createRouter, createWebHistory } from 'vue-router';
import { auth } from '../firebase'; // Adjust the path if needed
import Home from '../views/Home.vue';
import Upload from '../views/Upload.vue';
import UserProfile from '../views/UserProfile.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';


const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/upload', name: 'Upload', component: Upload, meta: { requiresAuth: true } },
    { path: '/profile', name: 'UserProfile', component: UserProfile, meta: { requiresAuth: true } },
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register }
  ];
  

  const router = createRouter({
    history: createWebHistory(),
    routes
  });
  
  router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const user = auth.currentUser; // Check if user is authenticated
  
    if (requiresAuth && !user) {
      // If route requires auth and user is not authenticated, redirect to login
      next('/login');
    } else if (to.path === '/login' && user) {
      // If user is already authenticated and tries to access login page, redirect to profile
      next('/profile');
    } else {
      next();
    }
  });
  
  export default router;
  

