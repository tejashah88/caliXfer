<template>
  <div>
    <v-autocomplete
      v-model="model"
      :items="items"
      :loading="isLoading"
      :search-input.sync="search"
      color="deep-purple"
      hide-no-data
      hide-selected
      :item-text="description"
      :item-value="itemValue"
      :label="label"
      :placeholder="placeholder"
      :prepend-icon="prefixIcon"
      :append-icon="suffixIcon"
      return-object
    ></v-autocomplete>
    <v-expand-transition>
      <v-list v-if="model" class="red lighten-3">
        <v-list-tile
          v-for="(field, i) in fields"
          :key="i"
        >
          <v-list-tile-content>
            <v-list-tile-title v-text="field.value"></v-list-tile-title>
            <v-list-tile-sub-title v-text="field.key"></v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-expand-transition>
  </div>
</template>

<script>
const Fuse = require('fuse.js');

export default {
  name: 'FuzzyAutoComplete',
  props: {
    label: String,
    description: String,
    itemValue: String,
    placeholder: String,
    isLoading: Boolean,
    prefixIcon: String,
    suffixIcon: String

  },
  data: () => ({
    model: null,
    search: null,
    descriptionLimit: 60,
    entries: [],
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
    items () {
      return this.entries.map(entry => {
        const Description = entry.Description.length > this.descriptionLimit
          ? entry.Description.slice(0, this.descriptionLimit) + '...'
          : entry.Description;

        return Object.assign({}, entry, { Description });
      });
    }
  },
  watch: {
    search (val) {
      // Items have already been loaded
      if (this.items.length > 0) return;

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
          console.log(this.entries);
        })
        .catch(err => {
          console.log(err);
        })
        .finally(() => (this.isLoading = false));
    }
  }
};
</script>