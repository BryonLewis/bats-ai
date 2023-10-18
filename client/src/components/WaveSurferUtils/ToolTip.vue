<script lang="ts">
import { defineComponent, PropType, ref, onMounted } from 'vue';

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
    delay: {
      type: Number,
      default: 250, //ms to delay showing the tooltip
    }
  },
  setup(props) {
    const frequency = ref(-1);
    const time = ref(-1);
    const tooltipLocation = ref([0, 0]);
    const tooltipOffset = { x:10, y:10 };
    let timeout: Node.timeout = 0;
    const showTooltip = ref(false);
    // We need a mousemovement event listener

    
    const moveListener = (e: MouseEvent) => {
        if (showTooltip.value) {
          showTooltip.value = false;
        } 

        clearTimeout(timeout);
          timeout = setTimeout(() => {
            showTooltip.value = true;
          }, props.delay);

        const {offsetX, offsetY} = e;
        // scale the X value
        time.value = offsetX * props.xScale;
        frequency.value = ((props.wrapper.clientHeight - offsetY) * props.yScale ) / 1000.0;
        tooltipLocation.value = [tooltipOffset.x + props.wrapper.offsetLeft + offsetX, tooltipOffset.y + props.wrapper.offsetTop + offsetY];
    };
    onMounted(()=> {
    props.wrapper.addEventListener('mousemove', (e: MouseEvent) => moveListener(e));
    });
    return {
        tooltipLocation,
        frequency,
        time,
        showTooltip,
    };
  },
});
</script>

<template>
  <div
    v-if="showTooltip"
    class="tooltip fade-in-image"
    style="position:absolute; z-index:50"
    :style="`left: ${tooltipLocation[0]}px; top: ${tooltipLocation[1]}px`"
  >
    <v-row dense>
      <span>{{ frequency.toFixed(1) }}KHz</span>
    </v-row>
    <v-row dense>
      <span>{{ time.toFixed(0) }}ms</span>
    </v-row>
  </div>
</template>

<style scoped>
.tooltip {
  position:absolute;
  z-index: 50;
  background-color: aliceblue;
  border-radius: 4px;
  border: 1px solid lightgray;
  padding: 10px;
}
.fade-in-image { animation: fadeIn 500ms; }
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

</style>
