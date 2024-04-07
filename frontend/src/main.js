import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

Vue.config.productionTip = false;

Vue.prototype.$http = axios;


import './style.css';

new Vue({
  router, 
  render: h => h(App), 
}).$mount('#app'); 