<script lang="ts">
import { defineComponent, ref, Ref} from 'vue';
import { getSpectrogram, Spectrogram } from '../api/api';
import SpeciesIndicator from '../components/SpeciesIndicator.vue';
import WaveSurfer from '../components/WaveSurfer.vue';
import { AudioAnnotation } from '../components/WaveSurferUtils/utils';


const frequencyHeight = 10000;
const offsetWidth = 100;

export default defineComponent({
  components: {
    WaveSurfer,
    SpeciesIndicator,
  },
  props: {
    id: {
        type: String,
        required: true
    }
  },
  setup(props) {
    const spectroData: Ref<Spectrogram | null> = ref(null);
    const annotations: Ref<AudioAnnotation[]> = ref([]);
    const getData = async () => {
        const response = await getSpectrogram(props.id);
        spectroData.value = response;
        if (response.annotations) {
            response.annotations.forEach((annotation) => {
                const freq = annotation.frequency;
                const offset = annotation.offset;
                annotations.value.push({
                    start: offset - (offsetWidth),
                    end:  offset,
                    minFreq: freq - (0.5*frequencyHeight),
                    maxFreq: freq + (0.5*frequencyHeight)
                });
            });
        }
    };
    getData();
    return {
        spectroData,
        annotations,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-text v-if="spectroData">
      <species-indicator
        v-if="spectroData.batches && spectroData.batches.length"
        :batches="spectroData.batches"
      />
      <wave-surfer
        :media="spectroData.url"
        :annotations="annotations"
      />
    </v-card-text>
  </v-card>
</template>
