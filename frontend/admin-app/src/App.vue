<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 宽屏PC适配 */
@media (min-width: 1200px) {
  #app {
    width: 100%;
    max-width: 100%;
  }
}

/* 大宽屏PC适配 */
@media (min-width: 1600px) {
  #app {
    width: 100%;
    max-width: 100%;
  }
}

/* 超宽屏PC适配 */
@media (min-width: 2000px) {
  #app {
    width: 100%;
    max-width: 100%;
  }
}
</style>