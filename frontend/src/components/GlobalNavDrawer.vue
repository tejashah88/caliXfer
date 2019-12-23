<template>
  <v-navigation-drawer
    app
    temporary
    width="320"
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
    drawerOpen: Boolean,
  },
  data: () => ({
    routes: routingInfo
  }),
  computed: {
    isOpen: {
      get() {
        return this.drawerOpen;
      },
      set(value) {
        this.$emit('update:drawerOpen', value);
      },
    },
  },
};
</script>