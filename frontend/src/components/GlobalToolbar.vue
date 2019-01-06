<template>
  <v-toolbar app dark color="deep-purple accent-2">
    <v-toolbar-side-icon @click="$emit('side-button-click')"></v-toolbar-side-icon>

    <v-toolbar-title class="headline">
      <span class="font-weight-bold">CaliXfer</span>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items>
      <v-btn
        v-for="route in routes"
        :key="route.id"
        flat
        @click="$router.push(route.link)">
        {{ route.title }}
      </v-btn>
    </v-toolbar-items>

    <v-toolbar-items>
      <v-btn large icon @click="$emit('toggle-dark-mode')">
        <lightbulb-icon class="icon-2x"/>
      </v-btn>

      <v-btn large icon href="https://github.com/tejashah88/caliXfer" target="_blank">
        <github-circle-icon class="icon-2x"/>
      </v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<style>
.material-design-icon.icon-2x {
  height: 2em;
  width: 2em;
}

.material-design-icon.icon-2x > .material-design-icon__svg {
  height: 2em;
  width: 2em;
}
</style>

<script>
const routingInfo = require('@/routing-info.json');

import LightbulbIcon from 'vue-material-design-icons/Lightbulb';
import GithubCircleIcon from 'vue-material-design-icons/GithubCircle';

export default {
  name: 'GlobalToolbar',
  components: {
    LightbulbIcon,
    GithubCircleIcon
  },
  data: () => ({
    routes: routingInfo
  })
};
</script>