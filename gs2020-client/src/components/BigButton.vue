<template>
  <v-btn
    x-large
    color="primary"
    dark
    width="220"
    height="85"
    style="margin: 10px;"
    :disabled="isDisabled"
    @click="(v) => $emit('click', v)"
  >
    <div style="width: 100%; height: 100%;">
      <v-icon style="display: block; margin: 10px;">{{ icon }}</v-icon>
      {{ buttonText }}
    </div>
  </v-btn>
</template>

<script>
export default {
  name: 'BigButton',
  props: {
    buttonText: {
      type: String,
      default: 'BigButton',
    },
    icon: {
      type: String,
      default: 'mdi-airplane',
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
