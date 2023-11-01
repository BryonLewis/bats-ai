import { createRouter, createWebHistory, RouterOptions, RouteLocationNormalized } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import WaveSurfer from '../components/WaveSurfer.vue';
import Files from '../views/Files.vue';
import Species from '../views/Species.vue';
import FileSpectro from '../views/FileSpectro.vue';

import oauthClient from '../plugins/Oauth';

function beforeEach(
  to: RouteLocationNormalized,
  _: RouteLocationNormalized,
  next: (route?: string) => void,
) {
  console.log(oauthClient.isLoggedIn);
  // if (!oauthClient.isLoggedIn && to.name !== '/') {
  //   next('/');
  // }
  // if (oauthClient.isLoggedIn && to.name === '/') {
  //   next('/');
  // }
  next();
}


function routerInit(){
  const router  = createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/',
        component: HomePage,
      },
      {
        path: '/wavesurfer',
        component: WaveSurfer,
      },
      {
        path: '/files',
        component: Files,
      },
      {
        path: '/species',
        component: Species,
      },
      {
        path: '/spectrogram/:id',
        component: FileSpectro,
        props: true,
      },

    ],
  });
  router.beforeEach(beforeEach);
  return router;
}

export default routerInit;
