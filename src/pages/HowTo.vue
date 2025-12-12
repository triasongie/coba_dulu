<template>
<div class="min-h-screen relative overflow-hidden bg-white">
    <img src="/molekul_kiri_atasH.png" alt="ChemFind Logo" class="absolute w-[200px] h-[160px]">
    <div class="absolute inset-0 opacity-20 bg-no-repeat bg-cover" style="background-color: #f7f9fc;">
        </div>
    <div class="relative z-10 pt-16 pb-24 px-4 md:px-8 text-center">
        
        <h2 class="text-4xl md:text-5xl font-extrabold mb-16 text-gray-900">
            How To Use
        </h2>

        <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
            
            <div class="bg-black text-white p-6 rounded-xl shadow-2xl shadow-gray-700/80 h-80 flex flex-col justify-center items-center">
                <p class="text-7xl font-extrabold mb-4">1</p>
                <h3 class="text-2xl font-bold mb-2">Enter Input</h3>
                <p class="text-white text-sm max-w-xs leading-relaxed">
                    Enter text or data related to the desired chemical topic. xxxxx
                </p>
            </div>

            <div class="bg-black text-white p-6 rounded-xl shadow-2xl shadow-gray-700/80 h-80 flex flex-col justify-center items-center">
                <p class="text-7xl font-extrabold mb-4">2</p>
                <h3 class="text-2xl font-bold mb-2">AI Processing</h3>
                <p class="text-white text-sm max-w-xs leading-relaxed">
                    The system will analyzes the input and generates recommendations
                </p>
            </div>

            <div class="bg-black text-white p-6 rounded-xl shadow-2xl shadow-gray-700/80 h-80 flex flex-col justify-center items-center">
                <p class="text-7xl font-extrabold mb-4">3</p>
                <h3 class="text-2xl font-bold mb-2">View Output</h3>
                <p class="text-white text-sm max-w-xs leading-relaxed">
                    Relevant results and insights are displayed for further exploration.
                </p>
            </div>
        </div>
        <router-link to="/AppPage" class="mb-12 mt-12 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-700 transition shadow-lg 
        block mx-auto w-fit" style="background-color: #4A70A9;">Try it now!
        </router-link>
    </div>
        <img src="/molekul_bawah.png" alt="ChemFind Logo" class="absolute bottom-0 left-0 w-[370px] h-[320px]">


</div>

</template>

