<script lang="ts">
import { defineComponent, ref, Ref} from 'vue';
import { getProjects, Project } from '../api/api';
import {
  VDataTable,
} from "vuetify/labs/VDataTable";
export default defineComponent({
  components: {
    VDataTable,
  },
  setup() {
    const projectsList: Ref<Project[]> = ref([]);
    const fetchSpecies = async () => {
        const projects = await getProjects();
        projectsList.value = projects.items;
    };
    fetchSpecies();
    const itemsPerPage = ref(-1);
    const headers = ref([
    {
            title:'Name',
            key:'name',
        },
        {
            title:'Description',
            key:'description',
        },
        {
            title:'Geometry Names',
            key:'eventGeometryName',
        },
        {
            title:'Survey Count',
            key:'surveys',
        },
    ]);
    return {
        projectsList,
        headers,
        itemsPerPage,
    };
  },
});
</script>

<template>
  <v-card>
    <v-card-title>
      Projects
    </v-card-title>
    <v-card-text>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="projectsList"
        density="compact"
        class="elevation-1"
      >
        <template #item.name="{ item }">
          <router-link :to="`/project/${item.selectable.projectKey}`">
            {{ item.selectable.name }}
          </router-link>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
