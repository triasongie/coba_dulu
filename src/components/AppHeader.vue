<template>
  <nav class="flex justify-between items-right px-20 py-5 border-b">
    
    <div class="flex items-center space-x-2 w-48"> 
      <img src="/chem.png" alt="ChemFind Logo" class="w-[48px] h-[61px]"> 
      <span class="font-bold text-lg">ChemFind</span>
    </div>

    <div class="flex items-center space-x-8">
      <router-link to="/" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">
        Home
      </router-link>
      <router-link to="/appPage" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">ChemFind</router-link>
      <router-link to="/history" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">History</router-link>
    </div>
  </nav>
</template>