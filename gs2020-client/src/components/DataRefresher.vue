<template>
  <div class="datarefresher"></div>
</template>

<script>
import { mapState } from 'vuex';
import simRequests from '../lib/simRequests';

export default {
  name: 'DataRefresher',
  data: () => ({
    refreshHandle: null,
  }),
  computed: {
    ...mapState({
      simConnected: state => state.simConnected,
      simErrored: state => state.simErrored,
    }),
  },
  created() {
    this.refreshData();
    this.refreshHandle = setInterval(this.refreshData, 2000);
  },
  beforeDestroy() {
    clearInterval(this.refreshHandle);
  },
  methods: {
    async refreshData() {
      if (this.simConnected && !this.simErrored) {
        try {
          const data = await simRequests.getDataset('uidata');
          if (data.PLANE_LATITUDE !== null && data.PLANE_LONGITUDE !== null && data.WISKEY_COMPASS_INDICATION_DEGREES !== null) {
            this.$store.dispatch('setData', data);
          }
        } catch (e) {
          console.error(`Error fetching data: ${e}`);
          this.$store.dispatch('setErrored');
        }
      }

      if (!this.simConnected || this.simErrored) {
        try {
          await simRequests.connectSim();
          this.$store.dispatch('setConnected');
        } catch(e) {
          console.error(`Error attempting sim reconnection ${e}`);
        }
      }
    },
  },
}
</script>