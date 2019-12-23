<template>
  <v-card
    class="mx-auto"
    :max-width="maxWidth"
    link
    :to="route">
    <v-img
      class="white--text align-end"
      height="200px"
      :src="img">
      <v-card-title>{{ title }}</v-card-title>
    </v-img>

    <v-card-text class="text--primary">
      <div>{{ description }}</div>
    </v-card-text>

    <v-card-actions>
      <v-btn text>Go</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>

export default {
  name: 'HomeTile',
  props: {
    maxWidth: String,
    title: String,
    img: String,
    description: String,
    route: String,
  },
};
</script>