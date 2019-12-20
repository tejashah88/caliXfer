<template>
  <v-app-bar app dark color="deep-purple accent-2">
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')"></v-app-bar-nav-icon>

    <v-toolbar-title class="headline">
      <span class="font-weight-bold">CaliXfer</span>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items class="hidden-xs-only">
      <v-btn
        v-for="route in routes"
        :key="route.id"
        text
        @click="$router.push(route.link).catch(err => {})">
        {{ route['abbr-title'] }}
      </v-btn>
    </v-toolbar-items>

    <v-toolbar-items>
      <v-btn large icon href="https://github.com/tejashah88/caliXfer" target="_blank">
        <github-circle-icon class="icon-2x"/>
      </v-btn>
    </v-toolbar-items>
  </v-app-bar>
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

import GithubCircleIcon from 'vue-material-design-icons/GithubCircle';

export default {
  name: 'GlobalToolbar',
  components: {
    GithubCircleIcon
  },
  data: () => ({
    routes: routingInfo
  })
};
</script>