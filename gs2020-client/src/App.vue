<template>
  <div id="app">
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
        <Nav />
        <div>
          <router-view/>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import Nav from './components/Nav';

export default {
  components: {
    Nav,
  },
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
