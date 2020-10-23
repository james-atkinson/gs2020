<template>
  <div class="pushback">
     <v-tabs
      v-model="tab"
      centered
      dark
      icons-and-text
    >
    <v-tabs-slider></v-tabs-slider>

    <v-tab href="#planned">
      Planned
      <v-icon>mdi-phone</v-icon>
    </v-tab>

    <v-tab href="#manual">
      Manual
      <v-icon>mdi-heart</v-icon>
    </v-tab>

    <v-tabs-items v-model="tab">
      <v-tab-item
        value="planned"
      >
        Planned Things
      </v-tab-item>
      <v-tab-item value="manual">
        Manual Things
      </v-tab-item>
    </v-tabs-items>
    </v-tabs>
  </div>
</template>

<script>
import BigButton from '../components/BigButton';

export default {
  name: 'Home',
  components: {
    BigButton,
  },
  data: () => ({
    tab: null,
  }),
};
</script>
