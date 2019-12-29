<template>
  <v-autocomplete
    v-bind="$props"
    :items="results"
    :loading="isLoading"
    :search-input.sync="search"
    no-filter
    hide-no-data
    :value="model"
    @change="onChange"
    :chips="multiple"
    :deletable-chips="multiple"
    return-object>
  </v-autocomplete>
</template>

<script>
import VuetifyAutoComplete from '../../node_modules/vuetify/lib/components/VAutocomplete/VAutocomplete';
const Fuse = require('fuse.js');

const defaultFuseOptions = {
  shouldSort: true,
  threshold: 0.6,
  location: 0,
  distance: 100,
  maxPatternLength: 64,
  minMatchCharLength: 1,
};

export default {
  name: 'FuzzyAutoComplete',
  extends: VuetifyAutoComplete,
  props: {
    fetchData: { type: Function, required: true },
    fuseOptions: { type: Object, default: () => {} },
    extraKeys: { type: Array, default: () => [] }
  },
  computed: {
    mergedFuseOptions() {
      return { ...defaultFuseOptions, ...{ keys: [this.itemText, ...this.extraKeys] }, ...this.fuseOptions };
    }
  },
  data: () => ({
    search: null,
    isLoading: false,
    rawResults: null,
    results: [],
    model: null
  }),
  methods: {
    onChange (val) {
      this.search = '';
      this.$emit('input', val);
      this.$emit('input-selected');
    },
    fetchRawResults(forceInvalidate = false) {
      if ((forceInvalidate || this.rawResults == null) && !this.isLoading) {
        this.isLoading = true;

        const fetchedData = this.fetchData();
        if (fetchedData instanceof Promise) {
          fetchedData
            .then(data => (this.rawResults = data))
            .catch(err => (this.rawResults = null))
            .finally(() => (this.isLoading = false));
        } else {
          this.rawResults = fetchedData;
          this.isLoading = false;
        }
      }
    },
  },
  watch: {
    search (val) {
      if (!val) return;

      if (!this.rawResults) {
        this.fetchRawResults();
        this.results = [];
      } else {
        const selectedItems = this.value instanceof Array ? this.value : [];
        const fuse = new Fuse(this.rawResults, this.mergedFuseOptions);
        this.results = [...fuse.search(val), ...selectedItems];
      }
    }
  }
};
</script>