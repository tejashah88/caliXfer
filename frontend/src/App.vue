<template>
  <v-app>
    <global-toolbar @toggle-drawer="isDrawerOpen = !isDrawerOpen"></global-toolbar>
    <global-nav-drawer @close-drawer="isDrawerOpen = false" :isOpen="isDrawerOpen"></global-nav-drawer>

    <v-content>
      <v-container fluid>
      <fade-transition :duration="200" mode="out-in">
        <v-container pa-4>
          <router-view></router-view>
        </v-container>
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
    isDrawerOpen: false
  }),
  watch: {
    '$route':{
      handler: (to, from) => {
        document.title = to.meta.title || 'CaliXfer';
      },
      immediate: true
    }
  },
};
</script>