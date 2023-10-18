<script lang="ts" setup>
import { onMounted, ref, watch, Ref, nextTick } from 'vue';
import WaveSurfer from 'wavesurfer.js';
import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram';
import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline';
import { drawAnnotation, AudioAnnotation } from './WaveSurferUtils/utils';
import ToolTip from './WaveSurferUtils/ToolTip.vue';
import * as d3 from 'd3';
const media = './3517_SE_20220627_224246_759.wav';
type SpectroWindowFunc = "bartlett" | "bartlettHann" | "blackman" | "cosine" | "gauss" | "hamming" | "hann" | "lanczoz" | "rectangular" | "triangular" | undefined;
type CustomSpectro = Spectrogram & 
{ frequencyMin: number; frequencyMax: number;
  buffer: AudioBuffer, fftSamples: number;
  windowFunc: SpectroWindowFunc;
  canvas: HTMLCanvasElement;
  labelsEl: HTMLCanvasElement;
  width: number;
  height: number;
  wrapper: HTMLDivElement;
};

const annotation: AudioAnnotation = {
    start: 40,
    end: 80,
    minFreq: 37000,
    maxFreq: 50000,
};


function formatTimeCallback(seconds: number,) {
    const milliseconds = (seconds * 1000);
    return `${milliseconds.toFixed(0)}ms`;
}
const generateColors = (steps: number) => {
        const baseColors = ['#0000FF','#00FFFF','#00FF00', '#FFFF00','#FF0000'];
        const positions = [0, 0.15, 0.30, 0.50, 0.75];
        const domain = positions.map((pos) => pos * steps);
        const colorScale = d3.scaleLinear()
            .domain(domain)
            // D3 allows color strings but says it requires numbers for type definitions
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            .range(baseColors as any[]);
        const colors: number[][] = [];
        for (var i = 0; i < steps; ++i) {
            const color = colorScale(i) as unknown as d3.RGBColor;
            const rgb = d3.color(color).rgb();
            colors.push([rgb.r / 256.0, rgb.b / 256.0, rgb.g / 256.0, 1]);
        }
        return colors;
    };


let ws: WaveSurfer;
let wsDisplay: WaveSurfer; // Displayed Waveform;
let spectrogram: CustomSpectro;
const frequencyMin = ref(0);
const frequencyMax = ref(0);
const sampleRate = ref(0);
const fftSamples = ref(4096);
const fftSampleOptions = ref([32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]);
const windowFunc: Ref<SpectroWindowFunc | 'default'> =ref('default');
const windowFunctionOptions = ref(["bartlett", "bartlettHann", "blackman", "cosine", "gauss", "hamming", "hann", "lanczoz", "rectangular", "triangular", 'default']);
const ready = ref(false);

const rangeSlider = ref([0, 128000]);

const zoomVal = ref(100);

const verticalZoom  = ref(500);

const resizeCanvas = () => {
    if (spectrogram.canvas) {
      spectrogram.canvas.style.height = `${verticalZoom.value}px`;
    }
    if (spectrogram.labelsEl) {
      spectrogram.labelsEl.style.display = 'none';
    }
    if (spectrogram.wrapper) {
        spectrogram.wrapper.style.maxHeight = `${verticalZoom.value}px`;

    }
};

const spectrogramCanvas: Ref<null | HTMLCanvasElement> = ref(null);
const spectrogramWrapper: Ref<null | HTMLDivElement> = ref(null);
const xScale = ref(1);
const yScale = ref(1);
const init = () => {
    const colors = generateColors(256);
    const bottomTimline = TimelinePlugin.create({
      timeInterval: 0.1,
      primaryLabelInterval: 1,
      secondaryLabelInterval: 0.5,
      formatTimeCallback,
      style: {
        fontSize: '10px',
        color: '#FF0000',
      },
    });

    wsDisplay = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'rgb(200, 0, 200)',
        progressColor: 'rgb(100, 0, 100)',
        url: media,
        hideScrollbar: true,
        barHeight: 10,
        sampleRate: 256000,
        minPxPerSec: 100,
        plugins: [bottomTimline],
    });

    ws = WaveSurfer.create({
        container: '#waveformhidden',
        waveColor: 'rgb(200, 0, 200)',
        progressColor: 'rgb(100, 0, 100)',
        url: media,
        hideScrollbar: true,
        sampleRate: 256000,
        height: 0,
        minPxPerSec: 100,
    });
    spectrogram = Spectrogram.create({
        container: '#spectrogram',
        labels: true,
        splitChannels: false,
        colorMap: colors,
        height: 500,
        fftSamples: fftSamples.value
    }) as CustomSpectro;

    ws.registerPlugin(
        spectrogram,
    );
    ws.once('interaction', () => {
        ws.seekTo(0);
        ws.play();
    });
    ws.once('ready', () => {
      ready.value = true;
      //ws.getWrapper().style.display = 'none';
      if (spectrogram) {
          rangeSlider.value = [spectrogram.frequencyMin, spectrogram.frequencyMax];
          frequencyMin.value = spectrogram.frequencyMin;
          frequencyMax.value = spectrogram.frequencyMax;
          sampleRate.value = spectrogram.buffer.sampleRate;
          windowFunc.value = spectrogram.windowFunc;
          nextTick(() => updateDrawings());
          //resizeCanvas();
          if (spectrogram.labelsEl) {
            spectrogram.labelsEl.style.display = 'none';
          }
        spectrogram.wrapper.addEventListener('scroll', (e: Event) => {
          if (e.target) {
            const leftScroll = (e.target as HTMLDivElement).scrollLeft;
            const wrapper = wsDisplay.getWrapper();
            const parent = wrapper.parentElement;
            if (parent) {
              parent.scrollTo(leftScroll, 0);
            }
          }
        });
      }
    });
    spectrogram.wrapper.addEventListener('wheel', (e: WheelEvent) => {
      e.preventDefault();
      if (e.getModifierState('Control')) {
        zoomVal.value += -e.deltaY ;
        zoomVal.value = Math.max(zoomVal.value, 100);
        zoomVal.value = Math.min(zoomVal.value, 5000);
        zoom();
      } else {
       verticalZoom.value += -e.deltaY;
       verticalZoom.value = Math.min(3000, verticalZoom.value);
       verticalZoom.value = Math.max(500, verticalZoom.value);
       resizeCanvas();
       nextTick(() => updateLegend());
      }
    });
};
let legendCanvas: HTMLCanvasElement | undefined;
const updateLegend = () => {
  if (!legendCanvas) {
    legendCanvas = document.createElement("canvas");
    spectrogram.wrapper.prepend(legendCanvas);
  } 
  
  if (legendCanvas) {
    spectrogramCanvas.value = spectrogram.canvas;
    spectrogramWrapper.value = spectrogram.wrapper;
    legendCanvas.width = Math.max(spectrogram.width, spectrogram.canvas.offsetWidth);
    // We used the scaled height
    legendCanvas.height = parseFloat(spectrogram.canvas.style.height.replace('px', ''));
    legendCanvas.style.position = spectrogram.canvas.style.position;
    legendCanvas.style.zIndex = spectrogram.canvas.style.zIndex + 1;

  }

  const ctx = legendCanvas.getContext("2d");
  const startValue = rangeSlider.value[0];
  const endValue = rangeSlider.value[1];
  const legendHeight = legendCanvas.height;
  const scale = d3.scaleLinear().domain([startValue, endValue]).range([0, legendHeight]);
  const stepSize = (endValue - startValue) / 10; // You can adjust the number of labels as needed
  const outsidelabel = document.getElementById('outside-label') as HTMLCanvasElement;
  const spectroEl = document.getElementById('spectrogram');
  if (outsidelabel && spectroEl) {
    const rect = spectroEl.getBoundingClientRect();
    outsidelabel.style.left = `${rect.left - 75}px`;
    outsidelabel.style.top = `${rect.top + window.scrollY}px`;
    outsidelabel.width = 75;
    outsidelabel.height = spectrogram.canvas.height;
    const labelCtx = outsidelabel.getContext('2d');
    if (labelCtx) {
      labelCtx.clearRect(0, 0, outsidelabel.width, legendCanvas.height);
      labelCtx.fillStyle = "black";
      labelCtx.font = `15px Arial`;
      labelCtx.strokeStyle = 'black';
      labelCtx.lineWidth= legendHeight / 500;
      for (let i = startValue; i <= endValue; i += stepSize) {
        const yPosition = legendHeight - scale(i);
        labelCtx.fillText(`${(i / 1000).toFixed(1)}kHz`, 0, yPosition);
        labelCtx.beginPath();
        labelCtx.moveTo(0, yPosition);
        labelCtx.lineTo(outsidelabel.width, yPosition);
        labelCtx.stroke();

      }

    }

  }
  if (ctx) {
    ctx.clearRect(0, 0, legendCanvas.width, legendCanvas.height);
    // Add number labels at regular intervals
    ctx.fillStyle = "black";
    ctx.font = `15px Arial`;
    ctx.strokeStyle = 'black';
    ctx.lineWidth= legendHeight / 500;
    for (let i = startValue; i <= endValue; i += stepSize) {
      const yPosition = legendHeight - scale(i);
      //ctx.fillText(`${(i / 1000).toFixed(1)}kHz`, 0, yPosition);
      ctx.beginPath();
      ctx.moveTo(0, yPosition);
      ctx.lineTo(legendCanvas.width, yPosition);
      ctx.stroke();
    }
  }
};
const duration = ref(0);
const updateDrawings = () => {
  updateLegend();
  duration.value = spectrogram.buffer.duration * 1000; //ms
  xScale.value = duration.value / spectrogram.wrapper.clientWidth;
  yScale.value = (spectrogram.frequencyMax - spectrogram.frequencyMin)/ spectrogram.wrapper.clientHeight;
  drawAnnotation(spectrogram.canvas, {duration: duration.value, minFreq: spectrogram.frequencyMin, maxFreq: spectrogram.frequencyMax }, annotation);
};

onMounted(() => init());
const updateSpectro = () => {
  spectrogram.frequencyMax = rangeSlider.value[1];
    spectrogram.frequencyMin = rangeSlider.value[0];
    spectrogram.fftSamples = fftSamples.value;
    spectrogram.windowFunc = windowFunc.value === 'default' ? undefined : windowFunc.value;
    spectrogram.height = fftSamples.value / 2.0;
    const decodedData = ws.getDecodedData();
    if (decodedData) {
        const frequencyData = spectrogram.getFrequencies(decodedData);
        spectrogram.drawSpectrogram(frequencyData);
    }
    resizeCanvas();
    nextTick(() => updateDrawings());


};
watch([fftSamples, windowFunc], () => {
  updateSpectro();
  //spectrogram.canvas.style.height = '500px';
});

const waveformEl: Ref<HTMLDivElement | null> = ref(null);
const zoom = () => {
if (wsDisplay) {
  wsDisplay.zoom(zoomVal.value);
  const width  = wsDisplay.getWrapper().style.width;
  spectrogram.wrapper.style.overflow = 'auto';
  spectrogram.canvas.style.width = width;
  spectrogram.width = parseFloat(width);
  resizeCanvas();
  nextTick(() => updateDrawings());
}

};

</script>

<template>
  <v-container
    style="max-width: 90%;"
    @resize="updateSpectro()"
  >
    <tool-tip
      v-if="spectrogramCanvas && spectrogramWrapper"
      :canvas="spectrogramCanvas"
      :wrapper="spectrogramWrapper"
      :x-scale="xScale"
      :y-scale="yScale"
    />
    <div
      id="waveform"
      ref="waveformEl"
    />
    <div id="waveformhidden" />
    <div
      id="spectrogram"
    />
    <canvas id="outside-label" />
  </v-container>
  <v-container
    v-if="ready"
    id="controls"
    class="pt-4"
  >
    <v-row
      dense
      align="center"
      justify="center"
    >
      <v-slider
        v-model="zoomVal"
        label="zoom"
        step="1"
        min="100"
        max="5000"
        @update:model-value="zoom()"
      />
    </v-row>

    <v-row
      dense
      align="center"
      justify="center"
    >
      <v-range-slider
        v-model="rangeSlider"
        min="0"
        step="1"
        :max="sampleRate/2.0"
        @end="updateSpectro()"
      >
        <template #prepend>
          <span style="min-width: 35px"> {{ rangeSlider[0].toFixed(0) }}</span>
        </template>
        <template #append>
          <span style="min-width: 35px"> {{ rangeSlider[1].toFixed(0) }}</span>
        </template>
      </v-range-slider>
    </v-row>
    <v-row>
      <v-select
        v-model="fftSamples"
        :items="fftSampleOptions"
        label="FFT Samples"
      />
    </v-row>
    <v-row>
      <v-select
        v-model="windowFunc"
        :items="windowFunctionOptions"
        label="Window Function"
      />
    </v-row>
  </v-container>
</template>

<style scoped>
#outside-label {
  position: absolute;
}
#spectrogram {
  overflow: visible;
}
</style>