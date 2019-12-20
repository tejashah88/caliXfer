<template>
  <v-footer app height="auto" dark color="deep-purple darken-1">
    <v-layout justify-center row wrap>
      Made with <vuejs-icon class="icon-breath-room"/> and <language-python-icon class="icon-breath-room"/> by Tejas Shah (<a href="https://github.com/tejashah88" class="white--text" target="_blank">tejashah88</a>)
    </v-layout>
  </v-footer>
</template>

<style>
.icon-breath-room {
  padding: 0px 2px;
}
</style>

<script>
import VuejsIcon from 'vue-material-design-icons/Vuejs';
import LanguagePythonIcon from 'vue-material-design-icons/LanguagePython';

export default {
  name: 'GlobalFooter',
  components: {
    VuejsIcon,
    LanguagePythonIcon
  }
};
</script>