import Vue from 'vue';
import Router from 'vue-router';
import Books from '../components/Books.vue';
import HelloWorld from '../components/HelloWorld.vue';
/* eslint-disable */

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [{
            path: '/',
            name: 'Books',
            component: Books,
        },
        {
            path: '/ping',
            name: 'Ping',
            component: HelloWorld,
        },
    ],
});