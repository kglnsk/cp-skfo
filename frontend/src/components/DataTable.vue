<template>
    <div class="table">
        <a-table 
            :columns="columns"
            :dataSource="tableData"
            bordered size="middle"
            :loading="isLoading"
            :locale="{
                emptyText: 'Ничего не найдено',
                filterConfirm: 'Применить',
                filterReset: 'Сбросить', 
                triggerDesc: 'Нажмите для сортировки по убыванию',
                triggerAsc: 'Нажмите для сортировки по возрастанию',
                cancelSort: 'Нажмите, чтобы отменить сортировку'
            }"
        />
    </div>
</template>

<script setup lang="ts">
import { useFilesStore } from '@/store/files';
import { storeToRefs } from 'pinia';

const { tableData, isLoading } = storeToRefs(useFilesStore())


const columns = [
    {
        title: 'Класс животного',
        dataIndex: 'class',
        key: 'class',
        filters: [{
            text: "Медведь",
            value: "Медведь"
        }, {
            text: "Кошка",
            value: "Кошка"
        }, {
            text: "Косуля",
            value: "Косуля"
        }, {
            text: "Лось",
            value: "Лось"
        }, {
            text: "Олень",
            value: "Олень"
        }, {
            text: "Кабарга",
            value: "Кабарга"
        }, {
            text: "Волк",
            value: "Волк"
        }, {
            text: "Куница",
            value: "Куница"
        }, {
            text: "Заяц",
            value: "Заяц"
        }, {
            text: "Собака",
            value: "Собака"
        }, {
            text: "Горный козел",
            value: "Горный козел"
        }, {
            text: "Барсук",
            value: "Барсук"
        }, {
            text: "Лиса",
            value: "Лиса"
        }, {
            text: "Снежный барс",
            value: "Снежный барс"
        }, {
            text: "Рысь",
            value: "Рысь"
        }, {
            text: "Росомаха",
            value: "Росомаха"
        }, {
            text: "Енотовидная собака",
            value: "Енотовидная собака"
        }, {
            text: "Белка",
            value: "Белка"
        }, {
            text: "Горал",
            value: "Горал"
        }, {
            text: "Тигр",
            value: "Тигр"
        }, {
            text: "Бизон",
            value: "Бизон"
        }],
        onFilter: (value: string, record: any) => record.class.indexOf(value) === 0,
    },
    {
        title: 'Количество особей',
        dataIndex: 'count',
        key: 'count',
        sorter: (a: any, b: any) => a.count - b.count,
    },
    {
        title: 'Время начала регистрации',
        dataIndex: 'date_registration_start',
        key: 'date_registration_start',
        sorter: (a: any, b: any) => {
            return new Date(b.date_registration_start).getTime() - new Date(a.date_registration_start).getTime()
        },
    },
    {
        title: 'Время окончания регистрации',
        dataIndex: 'date_registration_end',
        key: 'date_registration_end',
        sorter: (a: any, b: any) => {
            return new Date(b.date_registration_end).getTime() - new Date(a.date_registration_end).getTime()
        },
    },
    {
        title: 'Название папки',
        dataIndex: 'folder_name',
        key: 'folder_name'
    },
]
</script>

<style lang="scss"></style>