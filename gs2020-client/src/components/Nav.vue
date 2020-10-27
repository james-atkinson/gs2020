<template>
  <div class="nav">
    <BigButton :buttonText="jetwayText" icon="mdi-airport" @click="toggleJetway"/>
    <BigButton buttonText="Ground Services" icon="mdi-bag-checked" @click="gotoGroundServices"/>
    <BigButton buttonText="Pushback" @click="gotoPushback"/>
  </div>
</template>

<script>
import simRequests from '../lib/simRequests';
import BigButton from './BigButton';

export default {
  name: 'Home',
  components: {
    BigButton,
  },
  data: () => ({
    jetwayStatus: false,
  }),
  computed: {
    jetwayText() {
      return this.jetwayStatus ? 'Disconnect Jetway' : 'Connect Jetway';
    },
  },
  methods: {
    gotoPushback() {
      this.$route.name !== 'Pushback' && this.$router.push({ name: 'Pushback' });
    },
    gotoGroundServices() {
      this.$route.name !== 'GroundServices' && this.$router.push({ name: 'GroundServices' });
    },
    async toggleJetway() {
      const toggleResult = await simRequests.sendEvent('TOGGLE_JETWAY');
      console.log('toggleResult: ', toggleResult);
      if (toggleResult && toggleResult.data === 'success') {
        this.jetwayStatus = !this.jetwayStatus;
      }
    },
  },
};
</script>
