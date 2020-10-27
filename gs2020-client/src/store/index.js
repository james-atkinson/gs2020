import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    simOnGround: true,
    pushbackState: 3.0,
    currentHeading: 0,
    groundVelocity: 0,
    tugAngle: 0,
    tugConnected: false,
  },
  mutations: {
    set(state, payload) {
      const { key, value } = payload;
      Vue.set(state, key, value);
    }
  },
  actions: {
    setData({ commit }, payload) {
      Object.keys(payload).forEach((key) => {
        commit('set', { key, value: payload[key] });
      });
    }
  },
  modules: {
  },
});
