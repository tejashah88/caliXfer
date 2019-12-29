<template>
  <div>
    <h1>View Transfer Requirements</h1>
    <FuzzyAutoComplete
      v-model="selected.startSchool"
      label="Starting school"
      color="deep-purple"
      placeholder="Where are you transfering from?"
      item-text="names.current"
      :fetch-data="this.AssistAPI.fetchSourceInstitutions"
      @input-selected="filled |= 1">
    </FuzzyAutoComplete>

    <FuzzyAutoComplete
      v-model="selected.endSchool"
      :disabled="!(selected.startSchool)"
      label="Destination school"
      color="deep-purple"
      placeholder="Where do you want to transfer to?"
      item-text="name"
      :fetch-data="() => this.AssistAPI.fetchTargetInstitutions(selected.startSchool.id)"
      @input-selected="filled |= 2">
    </FuzzyAutoComplete>

    <FuzzyAutoComplete
      v-model="selected.major"
      :disabled="!(selected.startSchool && selected.endSchool)"
      label="Major"
      color="deep-purple"
      placeholder="What major are you planning to study?"
      item-text="name"
      :fetch-data="() => this.AssistAPI.fetchMajor(selected.startSchool.id, selected.endSchool.id, 67)"
      @input-selected="filled |= 4">
    </FuzzyAutoComplete>

    <FuzzyAutoComplete
      v-model="selected.year"
      label="Year"
      color="deep-purple"
      placeholder="What year agreements do you want to see?"
      item-text="fall-year"
      :fetch-data="() => this.AssistAPI.fetchYears()"
      @input-selected="filled |= 8">
    </FuzzyAutoComplete>

    <v-btn
      large
      block
      color="deep-purple lighten-1"
      :disabled="dialog || !!(filled ^ 15)"
      :loading="dialog"
      @click="dialog = true"
      class="white--text">
      Submit
    </v-btn>

    <v-dialog
      v-model="dialog"
      persistent>
      <v-card
        color="deep-purple darken-2"
        dark>
        <v-card-title class="headline">Loading...</v-card-title>
        <v-card-text>
          Please stand by
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-list v-if="'startSchool' in selected" class="red lighten-3">
      <v-list-item
        v-for="(keyval, i) in Object.entries(selected.startSchool)"
        :key="i*1">
        <v-list-item-content>
          <v-list-item-title v-text="keyval[0]"></v-list-item-title>
          <v-list-item-subtitle v-text="keyval[1]"></v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-list v-if="'endSchool' in selected" class="green lighten-3">
      <v-list-item
        v-for="(keyval, i) in Object.entries(selected.endSchool)"
        :key="i*100">
        <v-list-item-content>
          <v-list-item-title v-text="keyval[0]"></v-list-item-title>
          <v-list-item-subtitle v-text="keyval[1]"></v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-list v-if="'major' in selected" class="blue lighten-3">
      <v-list-item
        v-for="(keyval, i) in Object.entries(selected.major)"
        :key="i*10000">
        <v-list-item-content>
          <v-list-item-title v-text="keyval[0]"></v-list-item-title>
          <v-list-item-subtitle v-text="keyval[1]"></v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    {{ selected }}
  </div>
</template>

<script>
import FuzzyAutoComplete from '@/components/FuzzyAutoComplete';
import MemoizedAssistAPI from '@/pseudo-assist-api.js';

export default {
  name: 'ViewTransferReqs',
  components: {
    FuzzyAutoComplete
  },
  data: () => ({
    selected: {},
    AssistAPI: MemoizedAssistAPI,
    filled: 0,
    dialog: false,
  }),
  watch: {
    dialog (val) {
      if (!val) return;

      setTimeout(() => (this.dialog = false), 4000);
    },
  }
};
</script>