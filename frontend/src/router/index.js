import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import DetailPage from '@/components/DetailPage.vue';
import PredictPage from '@/components/PredictPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/detail/:id', component: DetailPage},
  { path: '/predict', component: PredictPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
