<template>
  <v-container fluid no-gutters>
    <v-row no-gutters>
      <v-col cols="12">
        <BigButton :buttonText="jetwayText" :icon="jetwayIcon" @click="toggleJetway"/>
        <BigButton :buttonText="fuelTruckText" :icon="fuelTruckIcon" :is-disabled="fuelTruckCalled || fuelTruckHoseDeployed" @click="toggleFuelTruck"/>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <span style="padding: 20px; font-size: 1.2rem; font-weight: 600;">
          <br />
          Want to control more ground items?<br />
          <br />
          Bug Asobo about it, there are currently limited events or SimVars that allow us to call ground services outside of the ATC.
        </span>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';
import BigButton from '../components/BigButton';
import simRequests from '../lib/simRequests';

export default {
  name: 'GroundServices',
  components: {
    BigButton,
  },
  data: () => ({
    jetwayStatus: false,
    fuelTruckCalled: false,
  }),
  computed: {
    ...mapState({
      fuelTruckHoseDeployed: state => state.simData.FUELTRUCK_HOSE_DEPLOYED,
    }),
    jetwayText() {
      return this.jetwayStatus ? 'Disconnect Jetway' : 'Connect Jetway';
    },
    jetwayIcon() {
      return this.jetwayStatus ? 'mdi-walk' : 'mdi-transit-transfer';
    },
    fuelTruckText() {
      if (this.fuelTruckHoseDeployed) {
        return 'Fueling In Progress';
      }

      return this.fuelTruckCalled ? 'Fuel Truck Called' : 'Call Fuel Truck';
    },
    fuelTruckIcon() {
      if (this.fuelTruckHoseDeployed) {
        return 'mdi-gas-station';
      }

      return this.fuelTruckCalled ? 'mdi-timer-sand' : 'mdi-tanker-truck';
    },
  },
  methods: {
    async toggleJetway() {
      const toggleResult = await simRequests.sendEvent('TOGGLE_JETWAY');
      if (toggleResult && toggleResult.data === 'success') {
        this.jetwayStatus = !this.jetwayStatus;
      }
    },
    async toggleFuelTruck() {
      try {
        const toggleResult = await simRequests.sendEvent('REQUEST_FUEL_KEY');
        if(toggleResult && toggleResult.data === 'success') {
          this.fuelTruckCalled = true;
          setTimeout(() => { this.fuelTruckCalled = false }, 30000);
        }
      } catch (e) {
        console.error(`Error calling fuel truck ${e}`);
      }
    }
  },
};
</script>
