require('./bootstrap');

import Vue from 'vue';

// import Datetime from 'vue-datetime'

// import 'vue-datetime/dist/vue-datetime.css'

// Vue.use(Datetime);


// Vue.component('example-component', require('./components/ExampleComponent.vue').default);
Vue.component('make', require('./components/make.vue').default);
Vue.component('dashboard', require('./components/dashboard.vue').default);
Vue.component('transactions', require('./components/transactions.vue').default);
Vue.component('make-donation', require('./components/make-donation.vue').default);
Vue.component('match', require('./components/match.vue').default);



const app = new Vue({
    el: '#app'
});
