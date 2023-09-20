import { createWebHistory, RouterOptions } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import Spectrogram from '../components/Spectrogram.vue';

function makeOptions(): RouterOptions {
  return {
    history: createWebHistory(),
    routes: [
      {
        path: '/',
        // component: HomePage,
        component: HomePage,
      },
      {
        path: '/spectrogram',
        // component: HomePage,
        component: Spectrogram,
      },
    ],
  };
}

export default makeOptions;
