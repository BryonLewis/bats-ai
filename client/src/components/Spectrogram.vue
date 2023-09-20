<script lang="ts" setup>
import { defineComponent, inject, computed, onMounted } from 'vue';
import AudioBufferSlice from '../spectrogram/audiobuffer-slice';
import Spectrogram from '../spectrogram/spectrogram';
import * as d3 from 'd3';
const media = [
    {
    file: './CORA-74449729.wav',
    slice: {start: 0, end: -1}
  }
];


let audioContext: AudioContext;
let spectro: Spectrogram;
const init = () => {
    spectro = new Spectrogram(document.getElementById('canvas') as HTMLCanvasElement, {
        canvas: {
            width: () => window.innerWidth,
            height: () => window.innerHeight*.80,
        },
        audio: {
            enable: true,
        },
        colors: (steps: number) => {
        const baseColors = ['#0000FF','#00FFFF','#00FF00', '#FFFF00','#FF0000'];
        const positions = [0, 0.15, 0.30, 0.50, 0.75];
        const domain = positions.map((pos) => pos * steps);
        const colorScale = d3.scaleLinear()
            .domain(domain)
            // D3 allows color strings but says it requires numbers for type definitions
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            .range(baseColors as any[]);
        const colors: string[] = [];
        for (var i = 0; i < steps; ++i) {
            const color = colorScale(i) as unknown as d3.RGBColor;
            const colorString = d3.color(color).formatHex();
            colors.push(colorString);
        }
        return colors;
      }
    });
    try {
    audioContext = new AudioContext();
  } catch (e) {
    alert('No web audio support in this browser!');
  }
};

const loadMedia = (callback: (buffer: AudioBuffer | undefined) => void) => {
    const request = new XMLHttpRequest();
    request.open('GET', media[0].file, true);
    request.responseType = 'arraybuffer';

    request.onload = () => {
        audioContext.decodeAudioData(request.response, (buffer: AudioBuffer) => {
            const slice = media[0].slice;
            AudioBufferSlice(buffer, slice.start, slice.end, (error, buf) => {
                callback(buf);
            });
        });
    };
    request.send();
};

const playSong = () => {
    init();
    loadMedia((songBuffer: AudioBuffer | undefined) => {
        if (songBuffer && audioContext && spectro) {
        spectro.connectSource(songBuffer, audioContext);
        spectro.start(0);
        }
    });
};


</script>

<template>
  <v-btn @click="playSong()">Play</v-btn>
  <canvas id="canvas"/>
</template>
