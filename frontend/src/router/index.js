import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import DetailPage from '@/components/DetailPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/detail/:id', component: DetailPage}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
