<template>
    <AppHeader />
  <div class="min-h-screen bg-white">
    
    <!-- Main Content -->
    <div class="pt-12 pb-20 px-8 lg:px-12 flex flex-col lg:flex-row items-start space-y-10 lg:space-y-0 lg:space-x-16 max-w-7xl mx-auto">
      <!-- Left Side - Molecule Image -->
      <div class="flex-shrink-0 w-full max-w-sm lg:w-96">
        <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
          <img v-if="moleculeImage" 
               :src="moleculeImage" 
               class="w-full h-auto object-contain" 
               alt="Molecule Structure"/>
          <img v-else 
               src="/molekul.png" 
               class="w-full h-auto object-contain opacity-50" 
               alt="Default Molecule"/>
        </div>
      </div>

      <!-- Right Side - Chemical Details -->
      <div class="flex-1 max-w-2xl">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">Chemical Details</h1>

        <!-- SMILES Section -->
        <div class="mb-6 pb-6 border-b border-gray-300">
          <h2 class="text-base font-bold text-gray-800 mb-3">SMILES</h2>
          <p class="text-sm text-gray-700 font-mono break-all leading-relaxed bg-gray-50 p-3 rounded">
            {{ smiles || 'N/A' }}
          </p>
        </div>

        <!-- Properties Section -->
        <div class="mb-6 pb-6 border-b border-gray-300">
          <h2 class="text-base font-bold text-gray-800 mb-4">Properties</h2>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between items-center py-2 px-3 bg-gray-50 rounded">
              <span class="text-gray-700 font-medium">pIC50:</span>
              <span class="font-bold text-gray-900">{{ properties.pic50 || 'N/A' }}</span>
            </div>
            <div class="flex justify-between items-center py-2 px-3 bg-gray-50 rounded">
              <span class="text-gray-700 font-medium">Atom Count:</span>
              <span class="font-bold text-gray-900">{{ properties.atom_count || 'N/A' }}</span>
            </div>
            <div class="flex justify-between items-center py-2 px-3 bg-gray-50 rounded">
              <span class="text-gray-700 font-medium">LogP:</span>
              <span class="font-bold text-gray-900">{{ properties.logP || 'N/A' }}</span>
            </div>
          </div>
        </div>

        <!-- Justifications Section -->
        <div class="mb-8">
          <h2 class="text-base font-bold text-gray-800 mb-4">Justifications</h2>
          <div class="bg-gray-50 border border-gray-200 p-5 rounded-lg text-sm text-gray-800 leading-relaxed">
            {{ justification || 'No justification available for this compound.' }}
          </div>
        </div>

        <!-- Back Button -->
        <div class="mt-10">
          <button 
            @click="goBack"
            class="bg-black text-white px-6 py-3 rounded-md text-sm font-semibold hover:bg-gray-800 active:bg-gray-900 transition-colors duration-200 flex items-center space-x-2">
            <span>←</span>
            <span>Back to Results</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import AppHeader from '../components/AppHeader.vue'; 

const router = useRouter()
const route = useRoute()

const smiles = ref('')
const moleculeImage = ref('')
const properties = ref({
  pic50: '',
  atom_count: '',
  logP: ''
})
const justification = ref('')

onMounted(() => {
  console.log('Detail page mounted')
  
  // Priority 1: Check sessionStorage (most reliable)
  const storedData = sessionStorage.getItem('selectedCompound')
  
  if (storedData) {
    console.log('Loading data from sessionStorage')
    try {
      const data = JSON.parse(storedData)
      console.log('Parsed stored data:', data)
      
      smiles.value = data.smiles || ''
      moleculeImage.value = data.image || ''
      properties.value = {
      pic50: data.properties?.pIC50 || '',
      atom_count: data.properties?.atom_count || '',
      logP: data.properties?.logP || ''
    };

      justification.value = data.justification || ''
      
      // Clear sessionStorage after reading
      sessionStorage.removeItem('selectedCompound')
      console.log('Data loaded successfully from sessionStorage')
    } catch (err) {
      console.error('Error parsing sessionStorage data:', err)
    }
  } 
  // Priority 2: Fallback to route query
  else if (route.query.smiles) {
    console.log('Only SMILES available from query. Properties/Justification missing.')
    smiles.value = route.query.smiles
  }

  else {
    console.log('No data found in any source')
  }
})    

function goBack() {
  router.back()
}
</script>