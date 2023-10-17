<script lang="ts">
import { defineComponent, inject, computed, PropType, ref, onMounted } from 'vue';
import OAuthClient from '@girder/oauth-client';

export default defineComponent({
  props: {
    wrapper: {
        type: Object as PropType<HTMLDivElement>,
        required: true,
    },
    canvas: {
        type: Object as PropType<HTMLCanvasElement>,
        required: true,
    },
    xScale: {
        type: Number,
        required: true,
    },
    yScale: {
        type: Number, //duration in ms
        required: true,
    },
  },
  setup(props) {
    const frequency = ref(-1);
    const time = ref(-1);
    const tooltipLocation = ref([0, 0]);
    const tooltipOffset = [20,20];
    // We need a mousemovement event listener
    const eventListener = (e: MouseEvent) => {

        const {offsetX, offsetY} = e;
        // scale the X value
        time.value = offsetX * props.xScale;
        frequency.value = ((props.wrapper.clientHeight - offsetY) * props.yScale ) / 1000.0;
        tooltipLocation.value = [props.wrapper.offsetLeft + offsetX,  props.wrapper.offsetTop + offsetY];
    };
    onMounted(()=> {
    props.wrapper.addEventListener('mousemove', (e: MouseEvent)=> eventListener(e));
    });
    return {
        tooltipLocation,
        frequency,
        time,
    };
  },
});
</script>

<template>
  <v-card
    style="position:absolute; z-index: 9999;"
    :style="`left: ${tooltipLocation[0]}px; top: ${tooltipLocation[1]}px`"
  >
    <v-card-text>
      <v-row dense>
        <span>{{ frequency.toFixed(1) }}KHz</span>
      </v-row>
      <v-row dense>
        <span>{{ time.toFixed(0) }}ms</span>
      </v-row>
    </v-card-text>
  </v-card>
</template>
