<script lang="ts">
import { defineComponent, ref, Ref} from 'vue';
import { getSpecies, Species } from '../api/api';
import {
  VDataTable,
} from "vuetify/labs/VDataTable";
export default defineComponent({
  components: {
    VDataTable,
  },
  setup() {
    const speciesList: Ref<Species[]> = ref([]);
    const fetchSpecies = async () => {
        const species = await getSpecies();
        speciesList.value = species.results;
    };
    fetchSpecies();
    const itemsPerPage = ref(-1);
    const headers = ref([
    {
            title:'Species Code',
            key:'species_code',
        },
        {
            title:'Family',
            key:'family',
        },
        {
            title:'Genus',
            key:'genus',
        },
        {
            title:'Common Namee',
            key:'common_name',
        },
    ]);
    return {
        speciesList,
        headers,
        itemsPerPage,
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
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="speciesList"
        density="compact"
        item-value="species_code"
        class="elevation-1"
      />
    </v-card-text>
  </v-card>
</template>
