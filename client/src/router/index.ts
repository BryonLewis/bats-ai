import { createRouter, createWebHistory, RouteLocationNormalized } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import WaveSurfer from '../components/WaveSurfer.vue';
import Files from '../views/FilesView.vue';
import Species from '../views/SpeciesView.vue';
import FileSpectro from '../views/FileSpectro.vue';

// import oauthClient from '../plugins/Oauth';

function beforeEach(
  to: RouteLocationNormalized,
  _: RouteLocationNormalized,
  next: (route?: string) => void,
) {
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
