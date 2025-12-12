<template>
  <AppHeader />
  <div class="min-h-screen bg-white px-6 py-10">
  
  <h1 class="text-4xl font-bold text-center mb-12">History</h1>
  <img src="/molekul_atasHis.png" class="absolute top-24 left-0 w-[200px] h-[200px]">
  <div class="space-y-10 max-w-5xl mx-auto">
    <div class="w-full border-b pb-6 flex justify-between items-start relative">
      <div class="text-gray-700 space-y-1">
        <p><span class="font-semibold">pIC50:</span> 0.87</p>
        <p><span class="font-semibold">Atom Count:</span> 29</p>
        <p><span class="font-semibold">LogP:</span> 4.6</p>
      </div>

      <button class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800">
        View Details
      </button>
    </div>
     <img
        src="/molekul_kananHis.png"
        class="absolute right-5 top-1/2 -translate-y-1/2 w-[220px] h-[300px]"
      >
    <!-- Repeat Item -->
    <div class="w-full border-b pb-6 flex justify-between items-start relative">
      <div class="text-gray-700 space-y-1">
        <p><span class="font-semibold">pIC50:</span> 0.87</p>
        <p><span class="font-semibold">Atom Count:</span> 29</p>
        <p><span class="font-semibold">LogP:</span> 4.6</p>
      </div>

      <button class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800">
        View Details
      </button>

      
    </div>

    <!-- Repeat Item -->
    <div class="w-full border-b pb-6 flex justify-between items-start relative">
      <div class="text-gray-700 space-y-1">
        <p><span class="font-semibold">pIC50:</span> 0.87</p>
        <p><span class="font-semibold">Atom Count:</span> 29</p>
        <p><span class="font-semibold">LogP:</span> 4.6</p>
      </div>

      <button class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800">
        View Details
      </button>

    </div>

  </div>
  
</div>
<img src="/molekul_kiriHis.png" class="absolute bottom-0 left-0 w-[300px] h-[220px]">

</template>
<script setup>
import AppHeader from '../components/AppHeader.vue';
</script setup>
