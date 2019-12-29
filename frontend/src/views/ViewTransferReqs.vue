<template>
  <div>
    <h1>View Transfer Requirements</h1>
    <outdated-agreement-warning/>

    <fuzzy-auto-complete
      v-model="selected.startSchool"
      label="Starting school"
      color="deep-purple"
      placeholder="Where are you transfering from?"
      item-text="names.current"
      :fetch-data="this.AssistAPI.fetchSourceInstitutions"
      @input-selected="filled |= 1">
    </fuzzy-auto-complete>

    <fuzzy-auto-complete
      v-model="selected.endSchool"
      :disabled="!(selected.startSchool)"
      label="Destination school"
      color="deep-purple"
      placeholder="Where do you want to transfer to?"
      item-text="name"
      :fetch-data="() => this.AssistAPI.fetchTargetInstitutions(selected.startSchool.id)"
      @input-selected="filled |= 2">
    </fuzzy-auto-complete>

    <fuzzy-auto-complete
      v-model="selected.major"
      :disabled="!(selected.startSchool && selected.endSchool)"
      label="Major"
      color="deep-purple"
      placeholder="What major are you planning to study?"
      item-text="name"
      :fetch-data="() => this.AssistAPI.fetchMajors(selected.startSchool.id, selected.endSchool.id, 67)"
      @input-selected="filled |= 4">
    </fuzzy-auto-complete>

    <v-btn
      large
      block
      color="deep-purple lighten-1"
      :disabled="dialog || !!(filled ^ 7)"
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

    <div v-for="(item, index) in formFields" :key="index">
      <v-list v-if="item.name in selected" :class="[item.color, 'lighten-3']">
        <v-list-item
          v-for="(keyval, i) in Object.entries(selected[item.name])"
          :key="i*10**index">
          <v-list-item-content>
            <v-list-item-title v-text="keyval[0]"></v-list-item-title>
            <v-list-item-subtitle v-text="keyval[1]"></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>

    {{ selected }}
  </div>
</template>

<script>
import FuzzyAutoComplete from '@/components/FuzzyAutoComplete';
import OutdatedAgreementWarning from '@/components/OutdatedAgreementWarning';
import MemoizedAssistAPI from '@/pseudo-assist-api.js';

export default {
  name: 'ViewTransferReqs',
  components: {
    FuzzyAutoComplete,
    OutdatedAgreementWarning
  },
  data: () => ({
    selected: {},
    AssistAPI: MemoizedAssistAPI,
    formFields: [
      {
        name: 'startSchool',
        color: 'red'
      },
      {
        name: 'endSchool',
        color: 'green'
      },
      {
        name: 'major',
        color: 'blue'
      },
      {
        name: 'year',
        color: 'yellow'
      },
    ],
    filled: 0,
    dialog: false,
  }),
  watch: {
    dialog (val) {
      if (!val) return;

      setTimeout(() => (this.dialog = false), 3000);
    },
  }
};
</script>