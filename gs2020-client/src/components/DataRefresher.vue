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
    this.refreshHandle = setInterval(this.refreshData, 500);
  },
  beforeDestroy() {
    clearInterval(this.refreshHandle);
  },
  methods: {
    async refreshData() {
      if (this.simConnected && !this.simErrored) {
        try {
          const data = await simRequests.getDataset('uidata');
          Object.keys(data).forEach((key) => {
            const dataPoint = data[key];
            dataPoint !== null && this.$store.dispatch('setSimDataVar', { key, value: data[key] });
          })
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