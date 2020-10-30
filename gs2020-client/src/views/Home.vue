<template>
  <div class="home">
    <span v-if="simData.SIM_ON_GROUND === 0">You're in the air.<br />Open Ground Services 2020 again when you get back to a gate!<br />Have a great flight!</span>
    <div v-else>
        Welcome to Ground Services 2020<br />
        <br />
        You'll find tools for managing ground service items under the 'Ground Services' section above, and a system for automating pushback under 'Pushback'.<br />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  name: 'Home',
  computed: {
    ...mapState({
      simData: state => state.simData,
    })
  }
};
</script>

<style lang="scss" scoped>
.home {
  padding: 10px;
  font-size: 1.2rem;
  color: white;
}
</style>
