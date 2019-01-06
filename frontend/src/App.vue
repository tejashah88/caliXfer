<template>
  <v-app :dark="darkMode">
    <global-toolbar @toggle-dark-mode="darkMode = !darkMode" @side-button-click="isDrawerOpen = !isDrawerOpen"></global-toolbar>
    <global-nav-drawer :isOpen="isDrawerOpen"></global-nav-drawer>

    <v-content>
      <v-container fluid>
      <fade-transition :duration="200" mode="out-in">
        <router-view></router-view>
      </fade-transition>
      </v-container>
    </v-content>

    <global-footer></global-footer>
  </v-app>
</template>

<script>
import { FadeTransition } from 'vue2-transitions';

import GlobalToolbar from '@/components/GlobalToolbar';
import GlobalNavDrawer from '@/components/GlobalNavDrawer';
import GlobalFooter from '@/components/GlobalFooter';

export default {
  name: 'App',
  components: {
    FadeTransition,
    GlobalNavDrawer,
    GlobalToolbar,
    GlobalFooter
  },
  data: () => ({
    darkMode: false,
    isDrawerOpen: true
  })
};
</script>