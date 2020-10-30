<template>
  <div class="nav">
    <BigButton buttonText="Ground Services" icon="mdi-bag-checked" :is-disabled="pushbackActive || !isOnGround" @click="gotoGroundServices"/>
    <BigButton buttonText="Pushback" :is-disabled="!isPushbackAvilable" @click="gotoPushback"/>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import simRequests from '../lib/simRequests';
import BigButton from './BigButton';

export default {
  name: 'Home',
  components: {
    BigButton,
  },
  computed: {
    ...mapState({
      simData: state => state.simData,
    }),
    pushbackActive() {
      return this.simData.PUSHBACK_STATE === 0 || this.simData.PUSHBACK_STATE === 1 || this.simData.PUSHBACK_STATE === 2
    },
    isOnGround() {
      return this.simData.SIM_ON_GROUND;
    },
    isEngineRunning() {
      return this.simData['GENERAL_ENG_COMBUSTION:1'] || this.simData['GENERAL_ENG_COMBUSTION:2'] || this.simData['GENERAL_ENG_COMBUSTION:3'] || this.simData['GENERAL_ENG_COMBUSTION:4'];
    },
    isPushbackAvilable() {
      return this.simData.PUSHBACK_STATE === 3 && !this.isEngineRunning;
    },
  },
  methods: {
    gotoPushback() {
      this.$route.name !== 'Pushback' && this.$router.push({ name: 'Pushback' });
    },
    gotoGroundServices() {
      this.$route.name !== 'GroundServices' && this.$router.push({ name: 'GroundServices' });
    },
  },
};
</script>

<style lang="scss" scoped>
.nav {
  border-bottom: 1px dashed white;
}
</style>
