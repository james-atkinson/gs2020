import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home';
import Pushback from '../views/Pushback';
import GroundServices from '../views/GroundServices';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/pushback',
    name: 'Pushback',
    component: Pushback,
  },
  {
    path: '/ground',
    name: 'GroundServices',
    component: GroundServices,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
