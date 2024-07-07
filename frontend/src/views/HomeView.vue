<template>
    <div class="home">
        <UploadData />
        <DataTable v-if="tableData" />
    </div>
</template>

<script setup lang="ts">
import UploadData from '@/components/UploadData.vue';
import DataTable from '@/components/DataTable.vue';
import { storeToRefs } from 'pinia';
import { useFilesStore } from '@/store/files';

const {tableData} = storeToRefs(useFilesStore())

</script>

<style lang="scss">
.home {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}
</style>