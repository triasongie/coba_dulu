<template>
  <div id="app">
    <Navbar v-if="!$route.meta.hideNavbar" />
      <main class="container mx-auto">
        <router-view></router-view> 
    </main>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'; 

</script>