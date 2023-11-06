<script lang="ts">
import { defineComponent, PropType} from 'vue';
import { SpectrogramBatches } from '../api/api';

export default defineComponent({
  props: {
    batches: {
        type: Array as PropType<SpectrogramBatches[]>,
        require: true,
        default: () => [],
    }
  },
  setup() {
    return {
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Species
    </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item
          v-for="(item, index) in batches"
          :key="`batch_${index}`"
          dense
        >
          <v-row v-if="item.auto">
            <v-col> Auto </v-col>
            <v-col> {{ item.auto.species_code }}</v-col>
            <v-col> {{ item.auto.family }}</v-col>
            <v-col> {{ item.auto.genus }}</v-col>
            <v-col> {{ item.auto.common_name }}</v-col>
            <v-col> {{ item.vetter }}</v-col>
          </v-row>
          <v-row v-if="item.manual">
            <v-col> Auto </v-col>
            <v-col> {{ item.manual.species_code }}</v-col>
            <v-col> {{ item.manual.family }}</v-col>
            <v-col> {{ item.manual.genus }}</v-col>
            <v-col> {{ item.manual.common_name }}</v-col>
            <v-col> {{ item.vetter }}</v-col>
          </v-row>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>
