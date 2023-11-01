<script lang="ts">
import { defineComponent, inject, computed, ref, watch } from 'vue';
import OAuthClient from '@girder/oauth-client';
import { useRoute } from 'vue-router';

export default defineComponent({
  setup() {
    const route = useRoute();
    const oauthClient = inject<OAuthClient>('oauthClient');
    if (oauthClient === undefined) {
      throw new Error('Must provide "oauthClient" into component.');
    }

    const loginText = computed(() => (oauthClient.isLoggedIn ? 'Logout' : 'Login'));
    const logInOrOut = () => {
      if (oauthClient.isLoggedIn) {
        oauthClient.logout();
      } else {
        oauthClient.redirectToLogin();
      }
    };

    const currentRoute = computed(() => {
      if (route.path.includes('spectrogram')) {
        return 'spectrogram';
      }
      if (route.path.includes('species')) {
        return 'species';
      }
      if (route.path.includes('files')) {
        return 'files';
      }
      if (route.path === '') {
        return 'home';
      }
      return '';
    });

    const activeTab = ref('files');
    watch(currentRoute, () => activeTab.value = currentRoute.value);

    return { oauthClient, loginText, logInOrOut, activeTab };
  },
});
</script>

<template>
  <v-app id="app">
    <v-app-bar app>
      <v-tabs
        fixed-tabs
        :model-value="activeTab"
      >
        <v-tab
          to="/"
          value="home"
        >
          Home
        </v-tab>

        <v-tab
          to="/files"
          value="files"
        >
          Files
        </v-tab>
        <v-tab
          to="/species"
          value="species"
        >
          Species
        </v-tab>
        <v-tab
          v-if="activeTab === 'spectrogram'"
          value="spectrogram"
        >
          Spectrogram
        </v-tab>
      </v-tabs>
      <v-spacer />
      <v-btn
        @click="logInOrOut"
      >
        {{ loginText }}
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
