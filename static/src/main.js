// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import Header from 'components/common/header'
import VueResource from 'vue-resource'

Vue.use(VueResource);
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    'header-template':Header,
  }
})
