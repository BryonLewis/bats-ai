<script lang="ts" setup>
import { defineComponent, inject, computed, onMounted, ref, watch, PropType, Ref, nextTick } from 'vue';
import WaveSurfer from 'wavesurfer.js';
import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram';
import * as d3 from 'd3';
const media = './CORA-74449729.wav';
type SpectroWindowFunc = "bartlett" | "bartlettHann" | "blackman" | "cosine" | "gauss" | "hamming" | "hann" | "lanczoz" | "rectangular" | "triangular" | undefined;
type CustomSpectro = Spectrogram & 
{ frequencyMin: number; frequencyMax: number;
  buffer: AudioBuffer, fftSamples: number;
  windowFunc: SpectroWindowFunc;
  canvas: HTMLCanvasElement;
  labelsEl: HTMLCanvasElement;
  wrapper: HTMLDivElement;
};
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

const resizeCanvas = () => {
    if (spectrogram.canvas) {
      const context = spectrogram.canvas.getContext('2d');
      if (context) {
        spectrogram.canvas.style.height = '500px';
      }
    }
    if (spectrogram.labelsEl) {
      console.log(spectrogram.labelsEl);
      spectrogram.labelsEl.style.display = 'none';
    }
    console.log(spectrogram.wrapper);
    if (spectrogram.wrapper) {
        console.log(spectrogram.wrapper.style.height);
        spectrogram.wrapper.style.maxHeight = '500px';
        console.log(spectrogram.wrapper.style.height);

    }
};
const init = () => {
    const colors = generateColors(256);
    ws = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'rgb(200, 0, 200)',
        progressColor: 'rgb(100, 0, 100)',
        url: media,
        sampleRate: 256000,
        minPxPerSec: 100,
    });
    spectrogram = Spectrogram.create({
        container: '#spectrogram',
        labels: true,
        splitChannels: false,
        colorMap: colors,
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
        if (spectrogram) {
            rangeSlider.value = [spectrogram.frequencyMin, spectrogram.frequencyMax];
            frequencyMin.value = spectrogram.frequencyMin;
            frequencyMax.value = spectrogram.frequencyMax;
            sampleRate.value = spectrogram.buffer.sampleRate;
            windowFunc.value = spectrogram.windowFunc;
            ready.value = true;
            resizeCanvas();

        }
    });
    
};
onMounted(() => init());
const updateSpectro = () => {
  spectrogram.frequencyMax = rangeSlider.value[1];
    spectrogram.frequencyMin = rangeSlider.value[0];
    console.log('update spectro');
    spectrogram.fftSamples = fftSamples.value;
    spectrogram.windowFunc = windowFunc.value === 'default' ? undefined : windowFunc.value;
    const decodedData = ws.getDecodedData();
    if (decodedData) {
        spectrogram.drawSpectrogram(spectrogram.getFrequencies(decodedData));
    }

};
watch([fftSamples, windowFunc], () => {
  updateSpectro();
  resizeCanvas();
});

const waveformEl: Ref<HTMLDivElement | null> = ref(null);
const zoom = () => {
if (ws) {
ws.zoom(zoomVal.value);
}

};

</script>

<template>
  <div ref="waveformEl" id="waveform" />
  <div
    id="spectrogram"
  />
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
    <v-slider label="zoom" v-model="zoomVal" step="1" min="10" max="1000" @update:model-value="zoom()" />
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

      <!-- <v-text-field
        v-model.number="frequencyMin"
        type="numer"
        :min="0"
        :max="sampleRate/2.0"
        label="Freq Min"
        class="mx-2"
        @change="updateSpectro()"
      />
      <v-text-field
        v-model.number="frequencyMax"
        type="number"
        :min="0"
        :max="sampleRate/2.0"
        label="Freq Max"
        class="mx-2"
        @change="updateSpectro()"
      /> -->
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
