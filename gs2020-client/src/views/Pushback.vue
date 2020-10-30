<template>
  <v-card>  
    <v-card-text v-show="showPushbackForm">
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
            <v-container fluid no-gutters v-show="!isPushbackStarted" class="mt-2">
              <v-row no-gutters centered>
                <v-col cols="3"></v-col>
                <v-col cols="2">
                  <v-text-field
                    v-model="pushbackRequestDistance"
                    hint="Distance (feet)"
                    persistent-hint
                    outlined
                    dense
                    class="ml-1 mr-1"
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
                    class="ml-1 mr-1"
                  />
                </v-col>
                <v-col cols="2">
                  <v-text-field
                    v-model="pushbackRequestAngle"
                    :disabled="pushbackRequestDirection === 'Straight'"
                    hint="Turn Angle"
                    persistent-hint
                    dense
                    outlined
                    class="ml-1 mr-1"
                  /> 
                </v-col>
                <v-col cols="3"></v-col>
              </v-row>
              <v-row no-gutters align-end>
                <v-col cols="4"></v-col>
                <v-col cols="4" centered>
                  <v-switch
                    v-model="autoParkingBrake"
                    label="Automate Parking Brake"
                    color="primary"
                  />
                </v-col>
                <v-col cols="4"></v-col>
              </v-row>
              <v-row no-gutters centered v-if="canStartPlannedPushback && !isPushbackStarted">
                <v-col cols="12">
                  <v-btn color="primary" @click="startPlannedPushback" dark>Start!</v-btn>
                </v-col>
              </v-row>
            </v-container>

            <v-container v-show="isPushbackStarted ">
              <v-row no-gutters centered>
                <v-col cols="12">
                  <span>Pushback In Progress!</span><br />
                  <v-progress-linear
                    color="deep-purple"
                    rounded
                    indeterminate 
                  ></v-progress-linear>
                </v-col>
              </v-row>
              <v-row no-gutters class="mt-1">
                <v-col cols="12" centered>
                  Requested Distance: {{ pushbackRequestDistance }} | Distance Pushed: {{ pushbackDistanceTravelled }}
                </v-col>
              </v-row>
              <v-row no-gutters class="mt-1">
                <v-col cols="12" centered>
                  Requested Angle: {{ pushbackRequestAngle }} | Current Angle: {{ parseInt(simData.WISKEY_COMPASS_INDICATION_DEGREES) }}
                </v-col>
              </v-row>
              <v-row no-gutters class="mt-1">
                <v-col cols="12" centered>
                  <v-btn
                    color="primary"
                    @click="togglePushback"
                  >
                    Stop Now!
                  </v-btn>
                </v-col>
              </v-row>
              <v-row no-gutters class="mt-1">
                <v-col cols="12" centered>
                  <span>You may close this window now, your pushback will continue to be managed.</span>
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
    <v-card-text v-show="!showPushbackForm">
      Pushback only available when engines are off.
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from 'vuex';
import simRequests from '../lib/simRequests';
import calculateHaversine from '../lib/calculateHaversine';
import BigButton from '../components/BigButton';

const PUSHBACK_STOPPED = 3;
const PUSHBACK_STARTED = 0;

export default {
  name: 'Home',
  components: {
    BigButton,
  },
  data: () => ({
    autoParkingBrake: true,
    pushbackRequestDistance: 200,
    pushbackRequestAngle: 90,
    pushbackRequestDirection: 'Straight',
    pushbackDistanceTravelled: 0,
    pushbackWatcherHandle: null,
    startLocation: {},
    tab: null,
  }),
  computed: {
    ...mapState({
      simData: state => state.simData,
    }),
    canStartPlannedPushback() {
      return this.simData && this.simData.PLANE_LONGITUDE
    },
    isPushbackStarted() {
      return this.simData && this.simData.PUSHBACK_STATE !== 3;
    },
    isEngineRunning() {
      return this.simData['GENERAL_ENG_COMBUSTION:1'] || this.simData['GENERAL_ENG_COMBUSTION:2'] || this.simData['GENERAL_ENG_COMBUSTION:3'] || this.simData['GENERAL_ENG_COMBUSTION:4'];
    },
    manualButtonText() {
      return this.isPushbackStarted ? 'Stop Pushback' : 'Start Pushback';
    },
    showPushbackForm() {
      return this.isPushbackStarted
        ? true
        : !this.isEngineRunning;
    },
  },
  methods: {
    calculateHeading(direction, changeValue, includeVariation = true) {
      const currentState = this.simData;
      const currentAngle = parseInt(currentState.WISKEY_COMPASS_INDICATION_DEGREES);
      const variation = parseInt(currentState.MAGVAR);
      let newAngle = includeVariation ? currentAngle + variation : currentAngle;

      if (currentAngle !== null && direction !== null && direction !== 'straight')  {
        newAngle = direction === 'left' ? currentAngle - changeValue : currentAngle + changeValue;
        if(newAngle < 0) {
          newAngle =  360 + newAngle;
        } else if(newAngle > 360) {
          newAngle = newAngle - 360;
        }
      }

      return newAngle;
    },
    getNewTugHeading(direction = null, targetAngle = 90) {
      const newAngle = this.calculateHeading(direction, targetAngle);
      const newTugHeading = (4294967295 / 360) * newAngle;
      return newTugHeading;
    },
    async togglePushback() {
      try {
        this.pushbackType = this.isPushbackStarted ? null : 'manual';
        const pushbackStartRequest = await simRequests.sendEvent('TOGGLE_PUSHBACK');
        clearInterval(this.pushbackWatcherHandle);
        
      } catch (e) {
        console.error(`Error sending TOGGLE_PUSHBACK event ${e}`);
        this.$store.dispatch('setErrored');
      }
    },
    async setPushbackLeft() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', this.getNewTugHeading('left'));
    },
    async setPushbackStraight() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', this.getNewTugHeading());
    },
    async setPushbackRight() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', this.getNewTugHeading('right'));
    },
    async startPlannedPushback() {
      try {
        const pushbackStartRequest = await simRequests.sendEvent('TOGGLE_PUSHBACK');
        
        this.autoParkingBrake && await simRequests.sendEvent('PARKING_BRAKES');
        
        if (pushbackStartRequest && pushbackStartRequest.data === 'success') {
          this.pushbackActive = true;
          this.startLocation = {
            latitude: this.simData.PLANE_LATITUDE,
            longitude: this.simData.PLANE_LONGITUDE,
            targetHeading: this.calculateHeading(this.pushbackRequestDirection.toLowerCase(), this.pushbackRequestAngle, false),
          }

          this.pushbackWatcherHandle = setInterval(() => { this.pushbackWatcher.call(this) }, 2200);
        }
      } catch (e) {
        console.error(`Error starting planned pushback ${e}`);
        this.pushbackActive = false;
      }
    },
    pushbackWatcher() {
      const currentHeading = parseInt(this.simData.WISKEY_COMPASS_INDICATION_DEGREES);

      if (this.startLocation && this.startLocation.latitude && this.startLocation.longitude) {
        this.pushbackDistanceTravelled = Math.floor(calculateHaversine(this.startLocation.latitude, this.startLocation.longitude, this.simData.PLANE_LATITUDE, this.simData.PLANE_LONGITUDE));
      }

      if (this.pushbackDistanceTravelled >= this.pushbackRequestDistance) {
        if (this.pushbackRequestDirection) {
          const headingDiff = Math.abs(currentHeading - this.startLocation.targetHeading);
          if (headingDiff < 3) {
            this.togglePushback();
            clearInterval(this.pushbackWatcherHandle);
            this.pushbackWatcherHandle = null;
            this.autoParkingBrake && simRequests.sendEvent('PARKING_BRAKES');
            return;
          }

          if(this.pushbackRequestDirection === 'Left') {
            this.setPushbackLeft();
          } else {
            this.setPushbackRight();
          }
        } else {
          this.togglePushback();
          clearInterval(this.pushbackWatcherHandle);
          this.pushbackWatcherHandle = null;
          this.autoParkingBrake && simRequests.sendEvent('PARKING_BRAKES');
          return;
        }
      }
    },
  },
};
</script>
