<template>
  <div class="min-h-screen flex items-center justify-center">
    <button 
      class="absolute top-5 left-5  px-3 py-1 rounded hover:bg-[#8FABD4] text-5xl"
      @click="$router.push('/')"
    >
      🡐
    </button>
    <div class="max-w-6xl w-full flex bg-white shadow-xl rounded-xl overflow-hidden min-h-[600px]">
      <div class="w-full lg:w-1/2 p-10 flex flex-col justify-center relative h-full">
        <div class="absolute top-6 left-10 flex items-center">
          <img src="/chem.png" alt="ChemFind Logo" class="w-[48px] h-[61px]"> 
          <span class="ml-2 font-semibold text-lg text-gray-800">ChemFind</span>
        </div>

        <h2 class="text-4xl font-bold text-gray-800 mb-8 mt-24 text-center">Sign In</h2>

        <form @submit.prevent="handleLogin" class="space-y-6 pb-36">
          <div>
            <input
              type="email"
              placeholder="Email"
              v-model="email"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              v-model="password"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <a href="#" class="text-sm text-gray-500  block text-right">
            Forgot your password?
          </a>

          <button
            type="submit"
            class="w-full py-3 bg-[#4A70A9] text-white font-semibold rounded-lg shadow-md"
          >
            Sign In
          </button>
        </form>
        <img src="/molekul_bawah.png" alt="ChemFind Logo" class="absolute bottom-0 left-0 w-[280px] h-[220px]">
      </div>
      
      
      <div class="hidden lg:block lg:w-1/2 p-12 bg--700 text-white relative">
        <div class="absolute inset-0 bg-[#4A70A9] rounded-l-[350px]"></div>
       
        <div class="relative z-10 h-full flex flex-col items-center justify-center text-center space-y-6">
          <h2 class="text-4xl font-light">Hello, Friend!</h2>
          <p class="text-sm max-w-xs">
            Register with your personal details to use all of site features
          </p>
          <router-link
            to="/register" 
            class="mt-4 px-10 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-[#4A70A9] transition duration-300 inline-block"
          >
            Sign Up
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

</script>
