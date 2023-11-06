<script lang="ts">
import { defineComponent, ref, Ref} from 'vue';
import { getAcoustFilesS3Exists, AcousticFiles } from '../api/api';

export default defineComponent({
  setup() {
    const fileList: Ref<AcousticFiles[]> = ref([]);
    const getFiles = async () => {
        const files = await getAcoustFilesS3Exists();
        fileList.value = files.results;
    };
    getFiles();
    return {
        fileList,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Files
    </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item
          v-for="item in fileList"
          :key="item.id"
          :to="`/spectrogram/${item.id}`"
          dense
        >
          {{ item.file_name }}
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>
