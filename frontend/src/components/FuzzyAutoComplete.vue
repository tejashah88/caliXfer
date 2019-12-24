<template>
  <div>
    <v-autocomplete
      v-bind="$props"
      v-model="model"
      :items="entries"
      :loading="isLoading"
      :search-input.sync="search"
      color="deep-purple"
      hide-no-data
      hide-selected
      return-object
    ></v-autocomplete>
    <v-expand-transition>
      <v-list v-if="model" class="red lighten-3">
        <v-list-item
          v-for="(field, i) in fields"
          :key="i"
        >
          <v-list-item-content>
            <v-list-item-title v-text="field.value"></v-list-item-title>
            <v-list-item-subtitle v-text="field.key"></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-expand-transition>
  </div>
</template>

<script>

import VuetifyAutoComplete from '../../node_modules/vuetify/lib/components/VAutocomplete/VAutocomplete';

const Fuse = require('fuse.js');

export default {
  name: 'FuzzyAutoComplete',
  extends: VuetifyAutoComplete,
  data: () => ({
    model: null,
    search: null,
    descriptionLimit: 60,
    entries: [],
    isLoading: false,
  }),
  computed: {
    fields () {
      if (!this.model) return [];

      return Object.keys(this.model).map(key => {
        return {
          key,
          value: this.model[key] || 'n/a'
        };
      });
    },
  },
  watch: {
    search (val) {
      // Items have already been loaded
      if (this.entries.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Lazily load input items
      fetch('https://api.publicapis.org/entries')
        .then(res => res.json())
        .then(data => {
          const { count, entries } = data;
          this.count = count;
          this.entries = entries;
        })
        .catch(err => {
          console.log(err);
        })
        .finally(() => (this.isLoading = false));
    }
  }
};
</script>