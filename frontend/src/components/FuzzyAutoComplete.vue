<template>
  <v-autocomplete
    v-bind="$props"
    :items="results"
    :loading="isLoading"
    :search-input.sync="search"
    :no-filter="true"
    :disabled="notReady"
    color="deep-purple"
    hide-no-data
    hide-selected
    :value="model"
    @input="onInput"
    @update:search-input="onSelect"
    return-object
  ></v-autocomplete>
</template>

<script>
import VuetifyAutoComplete from '../../node_modules/vuetify/lib/components/VAutocomplete/VAutocomplete';
const Fuse = require('fuse.js');

export default {
  name: 'FuzzyAutoComplete',
  extends: VuetifyAutoComplete,
  props: {
    fetchData: { type: Function, default: () => [] },
    fuseOptions: Object,
  },
  data: () => ({
    search: null,
    results: [],
    isLoading: false,
    notReady: false,
    selected: false,
    model: null
  }),
  methods: {
    onInput (val) {
      if (this.selected) {
        this.$emit('input', val);
        this.selected = false;
      }
    },
    onSelect() {
      this.selected = true;
    }
  },
  asyncComputed: {
    rawResults: {
      get() {
        return this.fetchData();
      },
      default: undefined,
    }
  },
  watch: {
    rawResults (val) {
      this.isLoading = !val;
      this.notReady = this.isLoading;
    },
    search (val) {
      if (!val) return;

      if (!this.rawResults) {
        this.results = [];
        return;
      }

      if (this.fuseOptions) {
        const fuse = new Fuse(this.rawResults, this.fuseOptions);
        this.results = fuse.search(val);
      } else
        this.results = this.rawResults;
    }
  }
};
</script>