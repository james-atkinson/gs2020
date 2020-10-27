<template>
  <div class="nav">
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
