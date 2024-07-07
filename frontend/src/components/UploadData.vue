<template>
  <div class="upload-files">
    <h4>Загрузка файлов или папки</h4>
    <div class="upload-files__buttons">
      <app-upload-input :multiple="true" :disabled="isLoading"  :upload-folder="false" v-model:files="files" />
      <app-upload-input :multiple="false" :disabled="isLoading"  button-type="primary" :upload-folder="true" v-model:files="files" />
    </div>
  </div>

</template>
<script lang="ts" setup>
import AppUploadInput from '@/components/AppUploadInput.vue'
import { useFilesStore } from '@/store/files';
import { storeToRefs } from 'pinia';
import { ref, watch } from 'vue';
import { notification } from 'ant-design-vue';

const {uploadFiles} = useFilesStore()
const {isLoading, error} = storeToRefs(useFilesStore())


const files = ref<FileList | null>(null)


watch(files, (val) => {
  if (!val) return
  const folderName = getFolderName(val) || ''
  uploadFiles(val, folderName)
})

watch(error, (val) => {
  if (!val) return
  
  notification.error({
    message: 'При загрузке данных произошла ошибка',
  });
})

const getFolderName = (filesList: FileList) => {
  return filesList[0].webkitRelativePath.split('/').shift() 
}

</script>

<style lang="scss">
.upload-files {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-radius: .5rem;
  border: 2px solid #ccc;
  &__buttons {
    display: flex;
    gap: 1rem;
  }
}
</style>