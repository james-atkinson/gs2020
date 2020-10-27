<template>
  <div id="app">
    <v-app id="inspire">
      <v-card
        elevation="5"
        width="850"
        height="500"
        class="background"
        dark
      >
        <v-card-title>
          <div style="width: 100%; margin: auto;">
            Ground Services 2020
          </div>
        </v-card-title>
        <v-card-text>
          <div v-if="!simConnected">
            <span v-if="!simErrored">Sim is not connected.</span>
            <span v-else>GS 2020 Server Error communicating with sim. Restart the server and try again.</span>
          </div>
          <div v-show="simConnected && !simErrored">
            <Nav />
            <div>
              <router-view/>
            </div>
          </div>
        </v-card-text>
      </v-card>
      <DataRefresher />
    </v-app>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import DataRefresher from './components/DataRefresher';
import Nav from './components/Nav';
import simRequests from './lib/simRequests';

export default {
  components: {
    DataRefresher,
    Nav,
  },
  computed: {
    ...mapState({
      simConnected: state => state.simConnected,
      simErrored: state => state.simErrored,
    }),
    refreshData() {
      return false;
    },
  },
  async created() {
    try {
      const result = await simRequests.connectSim();
      this.$store.dispatch('setConnected');
    } catch (e) {
      console.error(`Error connecting to sim: ${e}`);
    }
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: 0.8rem;
  color: white !important;
}

.background {
  background-image: url('assets/background.jpg');
}
</style>
