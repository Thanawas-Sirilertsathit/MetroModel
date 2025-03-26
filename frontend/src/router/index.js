import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import SamplePage from '../components/SamplePage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/sample', component: SamplePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
