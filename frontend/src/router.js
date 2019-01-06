import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const routingInfo = require('@/routing-info.json');

const routes = routingInfo.map(route => ({
  path: route.link,
  name: route.id,
  component: () => import(/* webpackChunkName: "[request]-[index]" */ `@/views/${route.filename}`)
}));

export default new Router({ routes });