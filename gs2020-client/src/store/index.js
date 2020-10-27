import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    simConnected: false,
    simErrored: false,
    simData: {},
  },
  mutations: {
    set(state, payload) {
      const { key, value } = payload;
      Vue.set(state, key, value);
    }
  },
  actions: {
    setData({ commit }, payload) {
      commit('set', { key: 'simData', value: payload });
    },
    setConnected({ commit }) {
      commit('set', { key: 'simConnected', value: true });
    },
    setErrored({ commit }) {
      commit('set', { key: 'simConnected', value: false });
      commit('set', { key: 'simErrored', value: true });
    }
  },
  modules: {
  },
});
