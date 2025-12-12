<template>
  <AppHeader />
  <div class="min-h-screen bg-white flex flex-col items-center">
    <div class="flex flex-col lg:flex-row items-center mt-10 space-y-10 lg:space-y-0 lg:space-x-20 max-w-5xl w-full">    
        <div class="flex-shrink-0 w-full max-w-xs lg:w-1/3">
            <img src="/molekul.png" class="w-full h-auto object-contain max-h-80" alt="Molecule"/>
        </div>

        <div class="max-w-xl w-full">
            
            <div class="text-center mb-14">
              <h1 class="text-4xl font-extrabold text-gray-900 tracking-tight">
                Chemical Compound Search
              </h1>
              <p class="text-gray-500 text-base mt-2">With Agentic AI</p>
            </div>

            <div v-if="error" class="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              {{ error }}
            </div>

            <div class="flex items-center justify-between mb-6">
                <label class="w-1/2 text-xl font-bold text-gray-700">pIC50</label>
                <div class="flex items-center space-x-2 w-1/2">
                    <input type="number" placeholder="Min" v-model="pic50_min" 
                            class="w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center font-semibold text-gray-700" />
                    <span class="text-2xl text-gray-400">—</span>
                    <input type="number" placeholder="Max" v-model="pic50_max" 
                            class="w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center font-semibold text-gray-700" />
                </div>
            </div>

            <div class="flex items-center justify-between mb-6">
                <label class="w-1/2 text-xl font-bold text-gray-700">Jumlah Atom</label>
                <div class="flex items-center space-x-2 w-1/2">
                    <input type="number" placeholder="Min" v-model="atom_min" 
                            class="w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center font-semibold text-gray-700" />
                    <span class="text-2xl text-gray-400">—</span>
                    <input type="number" placeholder="Max" v-model="atom_max" 
                            class="w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center font-semibold text-gray-700" />
                </div>
            </div>

            <div class="flex items-center justify-between mb-10">
                <label class="w-1/2 text-xl font-bold text-gray-700">logP</label>
                <div class="flex items-center space-x-2 w-1/2">
                    <input type="number" placeholder="Min" v-model="logP_min" 
                            class="w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center font-semibold text-gray-700" />
                    <span class="text-2xl text-gray-400">—</span>
                    <input type="number" placeholder="Max" v-model="logP_max" 
                            class="w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center font-semibold text-gray-700" />
                </div>
            </div>

            <div class="flex justify-center">
                <button @click="submitSearch" :disabled="loading"
                        class="w-3/4 py-3 bg-[#4A70A9] text-white text-lg font-semibold rounded-lg shadow-md hover:bg-[#8FABD4] transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed">
                    {{ loading ? 'Processing...' : 'Search' }}
                </button>
            </div>
        </div>
    </div>
    
  </div>
  <div class="fixed bottom-0 right-0 w-20 h-20 bg-[#4A70A9] rounded-tl-full"></div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import AppHeader from '../components/AppHeader.vue'; 

const router = useRouter()

const pic50_min = ref('')
const pic50_max = ref('')
const atom_min = ref('')
const atom_max = ref('')
const logP_min = ref('')
const logP_max = ref('')
const loading = ref(false)
const error = ref('')

async function submitSearch() {
  // Validasi input
  if (!pic50_min.value || !pic50_max.value || !atom_min.value || !atom_max.value || !logP_min.value || !logP_max.value) {
    error.value = 'Semua field harus diisi'
    return
  }

  if (parseFloat(atom_min.value) % 1 !== 0 || parseFloat(atom_max.value) % 1 !== 0) {
      error.value = 'Jumlah Atom harus bilangan bulat.';
      return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        pic50_min: parseFloat(pic50_min.value),
        pic50_max: parseFloat(pic50_max.value),
        atom_min: parseFloat(atom_min.value),
        atom_max: parseFloat(atom_max.value),
        logP_min: parseFloat(logP_min.value),
        logP_max: parseFloat(logP_max.value)
      })
    })

    if (!response.ok) {
 // Coba baca response body untuk error yang lebih spesifik dari FastAPI
      const errData = await response.json();
      throw new Error(errData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json()

    if (data.success) {
      
      sessionStorage.setItem('search_results', JSON.stringify(data.results));
      router.push({
        path: '/results',
      })
    } else {
      error.value = data.error || 'Error saat memproses request'
    }
  } catch (err) {
    error.value = 'Gagal menghubungi server: ' + err.message
    console.error('API Error:', err)
  } finally {
    loading.value = false
  }
}
</script>