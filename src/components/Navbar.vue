<template>
  <nav class="flex justify-between items-center px-20 py-5 border-b">
    
    <div class="flex items-center space-x-2 w-48"> 
      <img src="/chem.png" alt="ChemFind Logo" class="w-[48px] h-[61px]"> 
      <span class="font-bold text-lg">ChemFind</span>
    </div>

    <div class="flex items-center space-x-8">
      <router-link to="/" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">
        Overview
      </router-link>
      <router-link to="/features" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">Features</router-link>
      <router-link to="/howToUse" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">How to use</router-link>
      <router-link to="/contact" active-class="border-b-2 border-black pb-1 text-black" class="text-gray-700 hover:text-black-600">Contact</router-link>
    </div>

      <router-link to="/auth" class="bg-black text-white px-5 py-2 rounded-md hover:bg-gray-800">
        Login/Register
      </router-link>

  </nav>
</template>