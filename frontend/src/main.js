import Vue from 'vue';
import App from './App.vue';
import router from './router';

// setup vuetify
import Vuetify from 'vuetify/lib';
import 'vuetify/src/styles/main.sass';
import vuetify from './plugins/vuetify';
Vue.use(Vuetify);

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');