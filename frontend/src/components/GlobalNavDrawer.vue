<template>
  <v-navigation-drawer
    app
    stateless
    temporary
    v-model="isOpen">
    <v-list>
      <v-list-item
        v-for="route in routes"
        :key="route.id"
        @click.stop="$router.push(route.link).catch(err => {}); $emit('close-drawer');">
        <v-list-item-action>
          <v-icon>{{ route.icon }}</v-icon>
        </v-list-item-action>

        <v-list-item-content>
          <v-list-item-title>{{ route.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
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