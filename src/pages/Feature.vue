<template>
<div class="min-h-screen relative overflow-hidden">
    <img src="/molekul_kiriF.png" alt="ChemFind Logo" class="absolute w-[240px] h-[200px]">

    <div class="absolute inset-0 h-full w-full bg-gradient-to-b from-white to-[#4A70A9] opacity-70">
    </div>

    <div class="relative z-10 pt-10">
        <section class="py-16 px-4 md:px-8 text-center">
            <h2 class="text-4xl md:text-5xl font-extrabold mb-20 text-gray-900">
                Features
            </h2>

            <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
                
                <div class="bg-[#4A70A9] text-white p-6 rounded-xl shadow-2xl shadow-gray-700/80 h-80 flex flex-col justify-center items-center">
                    <img src="/agentic_ai.png" alt="Icon 1" class="w-20 h-20 mb-4">
                    <h3 class="text-2xl font-bold mb-2">Agentic AI System</h3>
                    <p class="text-white text-sm max-w-xs leading-relaxed">
                        AI-powered assistant that autonomously processes chemical data.
                    </p>
                </div>

                <div class="bg-[#4A70A9] text-white p-6 rounded-xl shadow-2xl shadow-gray-700/80 h-80 flex flex-col justify-center items-center">
                    <img src="/pointer.png" alt="Icon 2" class="w-20 h-20 mb-4">
                    <h3 class="text-2xl font-bold mb-2">Easy To Use</h3>
                    <p class="text-white text-sm max-w-xs leading-relaxed">
                        Easy to Use, makes chemical exploration accessible for everyone.
                    </p>
                </div>

                <div class="bg-[#4A70A9] text-white p-6 rounded-xl shadow-2xl shadow-gray-700/80 h-80 flex flex-col justify-center items-center">
                    <img src="/search.png" alt="Icon 3" class="w-20 h-20 mb-4">
                    <h3 class="text-2xl font-bold mb-2">Molecular Similarity Search</h3>
                    <p class="text-white text-sm max-w-xs leading-relaxed">
                        Find and compare similar chemical structures from extensive molecular instantly.
                    </p>
                </div>
            </div>
        </section>
            <router-link to="/AppPage" class="mb-12 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-700 transition shadow-lg 
            block mx-auto w-fit" style="background-color: #4A70A9;">Try it now!
            </router-link>   
    </div>
    <img src="/molekul_kananF.png" alt="ChemFind Logo" class="absolute bottom-0 right-0 w-[200px] h-[200px]">
</div>

</template>

