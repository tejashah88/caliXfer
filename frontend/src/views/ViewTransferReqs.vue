<template>
  <div>
    <h1>View Transfer Requirements</h1>
    <FuzzyAutoComplete
      v-model="selected.startSchool"
      label="Starting school"
      placeholder="Where are you transfering from?"
      item-text="names.current"
      item-value="id"
      :fetch-data="this.AssistAPI.fetchSourceInstitutions">
    </FuzzyAutoComplete>

    <FuzzyAutoComplete
      v-model="selected.endSchool"
      :disabled="!(selected.startSchool)"
      label="Destination school"
      placeholder="Where do you want to transfer to?"
      item-text="name"
      item-value="id"
      :fetch-data="() => this.AssistAPI.fetchTargetInstitutions(selected.startSchool.id)">
    </FuzzyAutoComplete>

    <FuzzyAutoComplete
      v-model="selected.major"
      :disabled="!(selected.startSchool && selected.endSchool)"
      label="Major"
      placeholder="What major are you planning to study?"
      item-text="name"
      item-value="id"
      :fetch-data="() => this.AssistAPI.fetchMajor(selected.startSchool.id, selected.endSchool.id, 67)">
    </FuzzyAutoComplete>

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
  })
};
</script>