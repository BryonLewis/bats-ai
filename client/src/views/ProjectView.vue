<script lang="ts">
import { defineComponent, ref, Ref} from 'vue';
import { getProject, Survey } from '../api/api';
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
    const surveyList: Ref<Survey[]> = ref([]);
    const fetchSpecies = async () => {
        const projects = await getProject(props.id);
        surveyList.value = projects.items;
    };
    fetchSpecies();
    const itemsPerPage = ref(-1);
    const headers = ref([
    {
            title:'Created',
            key:'createdDate',
        },
        {
            title:'Modified',
            key:'modifiedDate',
        },
        {
            title:'Time Range',
            key:'startTime',
        },
        {
            title:'Description',
            key:'surveyTypeDesc',
        },
        {
            title:'files',
            key:'fileCount',
        },

    ]);
    return {
        surveyList,
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
        :items="surveyList"
        density="compact"
        class="elevation-1"
      >
        <template #item.createdDate="{ item }">
          <div><b>{{ item.selectable.createdBy }}</b></div>
          <div>{{ item.selectable.createdDate }}</div>
        </template>
        <template #item.modifiedDate="{ item }">
          <div><b>{{ item.selectable.modifiedBy }}</b></div>
          <div>{{ item.selectable.modifiedDate }}</div>
        </template>
        <template #item.startTime="{ item }">
          <div>{{ item.selectable.startTime }}<b> to: </b>{{ item.selectable.endTime }}</div>
        </template>
        <template #item.fileCount="{ item }">
          <router-link :to="`/survey/${item.selectable.uuid}`">
            {{ item.selectable.fileCount }}
          </router-link>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
