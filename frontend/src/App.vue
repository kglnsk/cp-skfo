<template>
  <a-layout class="layout">
      <a-layout-header class="layout__header">
        <h2>Ultra detector</h2>
      </a-layout-header>
      <a-layout-content class="layout__content" >
        <div class="layout__content-wrap">
          <RouterView />
        </div>
      </a-layout-content>
    </a-layout>

</template>

<script lang="ts" setup></script>

<style lang="scss">
.layout {
  background-color: #fff;
  &__header {
    background: linear-gradient(144deg, #62C13A 0%, #62A2DB 100%)!important;
    h2 {
      color: #fff;
      text-align: center;
    }
  }
  &__content {
    padding: 2rem 1rem;
    height: calc(100vh - 64px);
    // &-wrap {
    //   height: 100%;
    //   border-radius: 1rem;
    //   padding: 1rem;
    //   background-color: blue;
    // }
  }
}
</style>
