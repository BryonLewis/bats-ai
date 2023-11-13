<script lang="ts">
import { defineComponent, ref, Ref} from 'vue';
import { getProject, getProjects, getSurvey, Project, Survey, SurveyDetails } from '../api/api';
import {
  VDataTable,
} from "vuetify/labs/VDataTable";
export default defineComponent({
  components: {
    VDataTable,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const surveyDetailsList: Ref<SurveyDetails[]> = ref([]);
    const fetchSpecies = async () => {
        const data = await getSurvey(props.id);
        surveyDetailsList.value = data.items;
    };
    fetchSpecies();
    const itemsPerPage = ref(-1);
    const headers = ref([
    {
            title:'file',
            key:'fileName',
        },
        {
            title:'Auto Species',
            key:'auto',
        },
        {
            title:'Manual Species',
            key:'manual',
        },
        {
            title:'Software',
            key:'software',
        },
        {
            title:'Classifier',
            key:'classifier',
        },

    ]);
    return {
        surveyDetailsList,
        headers,
        itemsPerPage,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Surveys for Project
    </v-card-title>
    <v-card-text>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="surveyDetailsList"
        density="compact"
        class="elevation-1"
      >
      <template #item.fileName="{ item }">
          <router-link :to="`/spectrogram/${item.selectable.fileId}`">
            {{ item.selectable.fileName }}
          </router-link>
        </template>

        <template #item.auto="{ item }">
          <div>{{ item.selectable.auto.speciesCode }}</div>
          <div>{{ item.selectable.auto.common_name }}</div>
          <div>{{ item.selectable.auto.gemus }}</div>
          <div>{{ item.selectable.auto.family }}</div>
        </template>
        <template #item.manual="{ item }">
          <div>{{ item.selectable.manual.speciesCode }}</div>
          <div>{{ item.selectable.manual.common_name }}</div>
          <div>{{ item.selectable.manual.gemus }}</div>
          <div>{{ item.selectable.manual.family }}</div>
        </template>
        <template #item.software="{ item }">
          <div>{{ item.selectable.software.name }}</div>
          <div>{{ item.selectable.software.description }}</div>
          <div>{{ item.selectable.software.version }}</div>
        </template>
        <template #item.classifier="{ item }">
          <div>{{ item.selectable.classifier.name }}</div>
          <div>{{ item.selectable.classifier.description }}</div>
          <div>{{ item.selectable.classifier.public }}</div>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
