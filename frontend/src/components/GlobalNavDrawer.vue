<template>
  <v-navigation-drawer
    app
    stateless
    fixed
    v-model="isOpen">
    <v-list>
      <v-list-tile
        v-for="route in routes"
        :key="route.id"
        @click.stop="$router.push(route.link)">
        <v-list-tile-action>
          <v-icon>{{ route.icon }}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{ route.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
const routingInfo = require('@/routing-info.json');

export default {
  name: 'GlobalNavDrawer',
  props: {
    isOpen: Boolean,
  },
  data: () => ({
    routes: routingInfo
  })
};
</script>