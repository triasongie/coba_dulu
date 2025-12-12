from fastapi import FastAPI
from pydantic import BaseModel
# >>> PASTIKAN model_agent.py SUDAH ADA DAN BERISI KODE LENGKAP YANG SAYA BERIKAN
from model_agent import run_with_manual_orchestration # Ganti dari 'run_model'
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

app = FastAPI(
    title="Chemical Discovery Agent API",
    description="Endpoint untuk menjalankan alur kerja penemuan molekul dengan LLM dan ML.",
    version="1.0.0"
)
origins = [
    "http://localhost:5173",
    "ttps://github.com/triasongie", 
    "https://github.com/triasongie/coba_dulu"
]
# Konfigurasi CORS (Sudah Benar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    """Skema input dari frontend (app.vue)"""
    pic50_min: float
    pic50_max: float
    atom_min: float
    atom_max: float
    logP_min: float
    logP_max: float


@app.post("/predict")
def predict(data: InputData) -> Dict[str, Any]:
    """
    Menjalankan Agentic AI pipeline (generate, validate, justify, image)
    dan mengembalikan hasil yang siap ditampilkan di frontend.
    """
    try:
        # 1. FORMAT INPUT: Mengubah 6 variabel min/max menjadi 1 string constraints
        # Constraint string harus sesuai format yang diharapkan oleh parse_constraints di model_agent.py
        constraints_text = f"""
        pIC50: {data.pic50_min}-{data.pic50_max}
        logP: {data.logP_min}-{data.logP_max}
        atoms: {int(data.atom_min)}-{int(data.atom_max)}
        """
        
        print("Constraints Dibuat:", constraints_text.strip())

        # 2. MENJALANKAN AGENTIC ORCHESTRATION DARI TIM ML
        # run_with_manual_orchestration mengembalikan dict dengan key 'results', 'constraints', dll.
        raw_agent_output = run_with_manual_orchestration(
            constraints=constraints_text
        )

        # Cek jika ada error dari Agent
        if "error" in raw_agent_output:
             raise Exception(f"Agent Error: {raw_agent_output['error']}")

        print("RAW AGENT OUTPUT:", raw_agent_output)

        # 3. NORMALISASI OUTPUT: Mengubah format Agent ke format yang diharapkan Vue.js
        results_for_frontend: List[Dict[str, Any]] = []
        
        # Iterasi hanya pada molekul yang berhasil dibuat dan divalidasi
        for item in raw_agent_output.get("results", []):
            
            # Kita hanya mengirim molekul yang 'valid' dan punya 'image_base64'
            if item.get("valid") and item.get("image_base64"):
                
                props = item.get("properties", {})
                
                results_for_frontend.append({
                    "smiles": item.get("smiles"),
                    "justification": item.get("justification", "No scientific justification available."),
                    # Mengambil image_base64 dari Agent. 
                    # Kita asumsikan frontend yang menambahkan prefix 'data:image/png;base64,'
                    "image": item.get("image_base64"), 
                    
                    # Properti Disesuaikan dengan key yang digunakan di detail.vue (pIC50, logP, atom_count)
                    "properties": {
                        "pIC50": props.get("pIC50"), # pIC50 (Camel Case)
                        "logP": props.get("logP"), # logP
                        "atom_count": props.get("atoms"), # atoms -> atom_count
                    }
                })

        return {
            "success": True,
            "results": results_for_frontend, # Kirim list of final, valid molecules
            "count": len(results_for_frontend),
        }

    except Exception as e:
        # Jika terjadi error saat parsing, koneksi LLM, atau error lainnya
        print(f"SERVER ERROR: {e}")
        return {
            "success": False,
            "error": f"Gagal memproses permintaan: {str(e)}",
            "results": []
        }


@app.get("/health")
def health_check():
    """Endpoint sederhana untuk mengecek status server."""
    return {"status": "ok"}
