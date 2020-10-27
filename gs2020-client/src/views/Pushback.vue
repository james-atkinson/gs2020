<template>
  <v-card>  
    <v-card-text>
      <v-tabs
        v-model="tab"
        dark
        icons-and-text
        centered
      >
        <v-tabs-slider></v-tabs-slider>

        <v-tab href="#planned">
          Planned
          <v-icon>mdi-truck-delivery</v-icon>
        </v-tab>

        <v-tab href="#manual">
          Manual
          <v-icon>mdi-truck</v-icon>
        </v-tab>

        <v-tabs-items v-model="tab" dark>
          <v-tab-item
            value="planned"
          >
            <v-container fluid no-gutters>
              <v-row no-gutters centered>
                <v-col cols="3"></v-col>
                <v-col cols="2">
                  <v-text-field
                    v-model="pushbackRequestDistance"
                    hint="Distance (feet)"
                    persistent-hint
                    outlined
                    dense
                  />
                </v-col>
                <v-col cols="2">  
                  <v-select
                    v-model="pushbackRequestDirection"
                    :items="['Left', 'Right', 'Straight']"
                    hint="Face Aircraft"
                    persistent-hint
                    dense
                    outlined
                  />
                </v-col>
                <v-col cols="2">
                  <v-text-field
                    v-model="pushbackRequestAngle"
                    v-show="pushbackRequestDirection !== 'Straight'"
                    hint="Turn Angle"
                    persistent-hint
                    dense
                    outlined
                  /> 
                </v-col>
                <v-col cols="3"></v-col>
              </v-row>
              <v-row no-gutters centered>
                <v-col cols="12">
                  <v-btn color="primary" @click="togglePushback" dark>Start!</v-btn>
                </v-col>
              </v-row>
              <v-row no-gutters align-end>
                <v-col cols="12" centered>
                  <v-switch
                    v-model="autoParkingBrake"
                    label="Automate Parking Brake"
                    dense
                    width="24%"
                  />
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
          <v-tab-item value="manual">
            <BigButton :buttonText="manualButtonText" icon="mdi-airplane" @click="togglePushback" /><br />
            <BigButton buttonText="Turn Left" :is-disabled="!isPushbackStarted" icon="mdi-airplane" @click="setPushbackLeft" />
            <BigButton buttonText="Straight" :is-disabled="!isPushbackStarted" icon="mdi-airplane" @click="setPushbackStraight" />
            <BigButton buttonText="Right Turn" :is-disabled="!isPushbackStarted" icon="mdi-airplane" @click="setPushbackRight" /><br />
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from 'vuex';
import simRequests from '../lib/simRequests';
import calculateHaversine from '../lib/calculateHaversine';
import BigButton from '../components/BigButton';

const PUSHBACK_STOPPED = 3.0;
const PUSHBACK_STARTED = 0.0;

export default {
  name: 'Home',
  components: {
    BigButton,
  },
  data: () => ({
    autoParkingBrake: false,
    pushbackRequestDistance: 10,
    pushbackRequestAngle: 90,
    pushbackRequestDirection: 'Straight',
    pushbackState: PUSHBACK_STOPPED,
    startLocation: {},
    tab: null,
  }),
  computed: {
    ...mapState({
      simData: state => state.simData,
      currentLatitude: state => state.simData.PLANE_LATITUDE,
      currentLongitude: state => state.simData.PLANE_LONGITUDE,
    }),
    isPushbackStarted() {
      return this.simData && this.simData.PUSHBACK_STATE && this.simData.PUSHBACK_STATE !== PUSHBACK_STOPPED;
    },
    manualButtonText() {
      return this.isPushbackStarted ? 'Stop Pushback' : 'Start Pushback';
    },
  },
  methods: {
    async getNewTugHeading(direction = null) {
      const currentState = await simRequests.getDataset('aircraft');
      const currentAngle = parseInt(currentState.WISKEY_COMPASS_INDICATION_DEGREES);
      const variation = parseInt(currentState.MAGVAR);
      let newAngle = currentAngle + variation;

      if (currentAngle !== null && direction !== null)  {
        newAngle = direction === 'left' ? currentAngle + 90 : currentAngle - 90;
        if(newAngle < 0) {
          newAngle =  360 + newAngle;
        } else if(newAngle > 360) {
          newAngle -= 360;
        }
      }
      
      const newTugHeading = (4294967295 / 360) * newAngle;
      return newTugHeading;
    },
    async togglePushback() {
      console.log(calculateHaversine(53.7691644, -112.8070943, 53.7691644, -112.8070943));
      /*try {
        const pushbackStartRequest = await simRequests.sendEvent('TOGGLE_PUSHBACK');
        console.log(pushbackStartRequest)
        this.startLocation = {
          latitude: this.currentLatitude,
          longitude: this.currentLongitude,
        }
      } catch (e) {
        console.error(`Error sending TOGGLE_PUSHBACK event ${e}`);
        this.$store.dispatch('setErrored');
      }*/
    },
    async setPushbackLeft() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', await this.getNewTugHeading('left'));
    },
    async setPushbackStraight() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', await this.getNewTugHeading());
    },
    async setPushbackRight() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', await this.getNewTugHeading('right'));
    },
  },
};
</script>
