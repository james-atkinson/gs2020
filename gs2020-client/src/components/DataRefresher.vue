<template>
  <div class="datarefresher"></div>
</template>

<script>
import simRequests from '../lib/simRequests';

export default {
  name: 'DataRefresher',
  data: () => ({
    refreshHandle: null,
  }),
  created() {
    this.refreshHandle = setInterval(this.refreshData, 1000);
  },
  beforeDestroy() {
    clearInterval(this.refreshHandle);
  },
  methods: {
    async refreshData() {
      const data = await simRequests.getDataset('aircraft');
      // this.$store.dispatch('setData', data)
      console.log('aircraft data: ', data);
    },
  },
}
</script>