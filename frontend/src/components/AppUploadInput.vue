<template>
    <div class="input">
        <input 
            id="custom-input"
            ref="inputRef" 
            class="input__native"

            type="file" 
            :multiple="multiple"
            @change="uploadData"
            :webkitdirectory="uploadFolder"
        >
        <label for="custom-input" class="input__label">
            <a-button
                @click.prevent="inputRef?.click()"
                :loading="isLoading"
                :disabled="disabled"
                :type="buttonType"
            >
                {{ 
                    uploadFolder ? 'Загрузить папку с файлами' : 'Загрузить файлы'
                }}
            </a-button>
        </label>
        
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';


type TProps = {
    files: FileList | null
    multiple: boolean
    uploadFolder: boolean
    disabled?: boolean
    isLoading?: boolean
    buttonType?: 'primary'
}

defineProps<TProps>()
const emits = defineEmits(['update:files'])

const inputRef = ref<null | HTMLInputElement>(null)


const uploadData = (e: Event) => {
    const target = e.target as HTMLInputElement
    const files = target.files
    emits('update:files', files)
}
</script>

<style lang="scss">
.input {
    &__native {
        display: none;
    }
    &__label {
        display: block;
    }
}
</style>