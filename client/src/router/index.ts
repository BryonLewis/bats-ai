import { createWebHistory, RouterOptions } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import WaveSurfer from '../components/WaveSurfer.vue';
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
        path: '/wavesurfer',
        // component: HomePage,
        component: WaveSurfer,
      },
    ],
  };
}

export default makeOptions;
