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
        Planned Things
      </v-tab-item>
      <v-tab-item value="manual">
        <BigButton buttonText="Start Pushback" icon="mdi-airplane" @click="startPushback" /><br />
        <BigButton buttonText="Turn Left" icon="mdi-airplane" @click="setPushbackLeft" />
        <BigButton buttonText="Straight" icon="mdi-airplane" @click="setPushbackStraight" />
        <BigButton buttonText="Right Turn" icon="mdi-airplane" @click="setPushbackRight" /><br />
      </v-tab-item>
    </v-tabs-items>
    </v-tabs>
  </div>
</template>

<script>
import simRequests from '../lib/simRequests';
import BigButton from '../components/BigButton';

const PUSHBACK_STOPPED = 3.0;
const PUSHBACK_STRAIGHT = 0.0;
const PUSHBACK_LEFT = 1.0;
const PUSHBACK_RIGHT = 2.0;

export default {
  name: 'Home',
  components: {
    BigButton,
  },
  data: () => ({
    pushbackState: PUSHBACK_STOPPED,
    tab: null,
  }),
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
    async startPushback() {
      const pushbackStartRequest = await simRequests.sendEvent('TOGGLE_PUSHBACK');
    },
    async setPushbackLeft() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', await this.getNewTugHeading('left'));
      console.log('response: ', eventResponse);
    },
    async setPushbackStraight() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', await this.getNewTugHeading());
      console.log('response: ', eventResponse);
    },
    async setPushbackRight() {
      const eventResponse = await simRequests.sendEvent('KEY_TUG_HEADING', await this.getNewTugHeading('right'));
      console.log('response: ', eventResponse);
    },
  },
};
</script>
