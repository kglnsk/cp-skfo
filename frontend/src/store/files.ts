import type { ITableData } from "@/types"
import { DICT } from "@/utils"
import axios from "axios"
import { defineStore } from "pinia"


interface IState {
    isLoading: boolean
    tableData: null | ITableData[]
    error: null | string
}

export const useFilesStore = defineStore('files', {
    state: (): IState => ({
        isLoading: false,
        // tableData: [
        //     {
        //         "folder_name": "10",
        //         "class": DICT['Red_Deer'],
        //         "date_registration_start": new Date("2023-01-02T18:32:33Z").toLocaleString(),
        //         "date_registration_end": new Date("2023-01-02T18:23:33Z").toLocaleString(),
        //         "count": 3
        //     },
        //     {
        //         "folder_name": "10",
        //         "class": DICT['Red_Deer'],
        //         "date_registration_start": new Date("2023-01-02T21:32:33Z").toLocaleString(),
        //         "date_registration_end": new Date("2023-01-02T18:33:33Z").toLocaleString(),
        //         "count": 1
        //     }
        // ],
        tableData: null,
        error: null
    }),
    actions: {
        async uploadFiles(files: FileList, folderName: string) {
            this.isLoading = true
            const formData = new FormData()
            formData.append('folder_name', folderName)
            for (const file of files) {
                formData.append(file.name, file)
            }

            try {
                const res = await axios.post('', formData)
                if (res?.data) {
                    this.tableData = res.data.map((item: ITableData) => {
                        return {
                            ...item,
                            date_registration_start: new Date(item.date_registration_start).toLocaleString(),
                            date_registration_end: new Date(item.date_registration_end).toLocaleString(),
                            folder_name: folderName,
                            class: DICT[item.class],
                        } 
                    })
                }
            } catch(e) {
                console.log('uploadFiles error', e)
                this.error = 'Произошла ошибка при загрузке файлов'

                setTimeout(() => {
                    this.error = null
                }, 1000)
            } finally {
                this.isLoading = false
            }
        }
    }
})