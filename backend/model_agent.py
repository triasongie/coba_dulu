# ====================================================================
# SCRIPT INI MENGGABUNGKAN LOGIC AGENTIC AI DAN MODEL ML DARI TIM ML
# Bertindak sebagai Agentic Backend Service.
# Dependencies: langchain, langchain-google-genai, joblib, rdkit, numpy
# ====================================================================

import os
from typing import List, Dict, Any, Optional
import json
import base64
from io import BytesIO

# --- RDKIT & NUMPY ---
# Pastikan library ini terinstal
try:
    from rdkit import Chem
    from rdkit.Chem import Draw, AllChem, Descriptors
    import numpy as np
    RDKIT_AVAILABLE = True
except ImportError:
    print("Warning: RDKit not found. Chemical prediction and drawing will fail.")
    RDKIT_AVAILABLE = False
    
# --- LANGCHAIN & GOOGLE GENAI ---
# Ganti dengan import yang lebih sederhana untuk environment production
from langchain_google_genai import GoogleGenerativeAI 
from langchain.tools import tool
# Ganti dengan joblib untuk memuat model PKL
import joblib 

# Gunakan BaseModel dari Pydantic (diperlukan untuk FastAPI)
from pydantic import BaseModel 

# ====================================================================
# 1. INIASIALISASI MODEL DAN LLM
# ====================================================================

# Konfigurasi LLM (Ambil API Key dari Environment Variable)
API_KEY = os.getenv("GOOGLE_API_KEY", "INSERT_YOUR_KEY_HERE")
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7,
    google_api_key=API_KEY
)

# ====================================================================
# 2. CLASS REGRESSOR MODEL ML (PropsRegressor)
# ====================================================================

class PropsRegressor:
    """Mengelola pemuatan dan prediksi model ML dari file .pkl."""
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.property_names = ["pic50", "logp", "atoms"]
        
        if model_path and os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print(f"✓ Loaded model from {model_path}")
            except Exception as e:
                print(f"Error loading model from {model_path}: {e}")
                self.model = None

    def smiles_to_fingerprint(self, smiles: str, radius: int = 2, n_bits: int = 2048) -> Optional[np.ndarray]:
        if not RDKIT_AVAILABLE: return None
        mol = Chem.MolFromSmiles(smiles)
        if mol is None: return None
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        # Mengembalikan array numpy yang merepresentasikan fingerprint
        return np.array(fp)

    def predict(self, smiles: str) -> Optional[Dict[str, float]]:
        if not RDKIT_AVAILABLE: return None
        mol = Chem.MolFromSmiles(smiles)
        if mol is None: return None
        
        # Fallback jika model gagal dimuat
        if self.model is None:
            return {
                "pic50": None,
                "logp": None,
                "atoms": mol.GetNumAtoms()
            }
        
        fp = self.smiles_to_fingerprint(smiles)
        if fp is None: return None
        
        try:
            # Model Anda memprediksi 3 target: [pic50, logp, atoms]
            predictions = self.model.predict([fp])[0]
            return {
                "pic50": float(predictions[0]),
                "logp": float(predictions[1]),
                "atoms": int(round(predictions[2]))
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

# INISIALISASI MODEL ML (akan dimuat saat server dijalankan)
predictor = PropsRegressor(model_path="multitarget_model.pkl")

# ====================================================================
# 3. FUNGSI UTILITAS (Parsing & Validasi)
# ====================================================================

def parse_constraints(text: str) -> Dict[str, tuple]:
    """Mengurai teks constraint menjadi dict {prop_name: (min, max)}."""
    constraints = {}
    text = text.lower().replace(":", " ").replace(",", "\n")
    
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line: continue
        
        parts = line.split()
        if len(parts) < 2: continue
        
        prop_name = parts[0]
        # Mengambil range min-max
        for part in parts[1:]:
            if "-" in part and not part.startswith("-"):
                try:
                    min_val, max_val = part.split("-")
                    constraints[prop_name] = (float(min_val), float(max_val))
                    break
                except:
                    continue
    
    return constraints

def validate_properties(props: Dict[str, float], constraints: Dict[str, tuple]) -> bool:
    """Memeriksa apakah properti molekul memenuhi semua batasan."""
    for prop_name, (min_val, max_val) in constraints.items():
        if prop_name not in props or props[prop_name] is None:
            return False
        if not (min_val <= props[prop_name] <= max_val):
            return False
    return True

# ====================================================================
# 4. TOOLS AGENTIC (Fungsi yang Dapat Dipanggil LLM/Orkestrasi)
# ====================================================================

class GenerateInput(BaseModel):
    constraints: str

@tool(args_schema=GenerateInput)
def generate_and_validate_molecules(constraints: str) -> str:
    """
    TOOL 1: Menggunakan LLM untuk Generate SMILES, kemudian menggunakan ML model
    untuk memprediksi dan memvalidasi properti terhadap constraints.
    Mengembalikan hasil dalam format JSON.
    """
    constraint_dict = parse_constraints(constraints)
    if not constraint_dict:
        return json.dumps({"error": "Could not parse constraints"}, indent=2)
    
    # Prompt untuk LLM untuk menghasilkan SMILES
    gen_prompt = f"""Generate 4 potentially novel chemically valid SMILES strings for drug-like molecules.

        Target properties:
        {constraints}

        Return ONLY SMILES strings, one per line. NO explanations, NO numbering.
        setx GOOGLE_API_KEY "AIzaSyBEHJe9RXD3q6wClSOccxqtjg3Le3D65ys"

        Example format:
        CCO
        c1ccccc1
        CC(C)O
        """

    try:
        smiles_raw = llm.invoke(gen_prompt)
        # Filter output agar hanya SMILES yang valid

        # ====== PERBAIKAN 1: DEBUGGING RAW OUTPUT ======
        # Ini akan membantu Anda melihat jika LLM merespons dengan format yang buruk
        print("--- LLM RAW SMILES OUTPUT START ---")
        print(smiles_raw.strip())
        print("--- LLM RAW SMILES OUTPUT END ---")
        # =============================================
        smiles_list = [
            s.strip() 
            for s in smiles_raw.split("\n") 
            if s.strip() and not any(s.strip().startswith(x) for x in ["#", "```", "1.", "2.", "3."])
        ]

        if not smiles_list:
            return json.dumps({
                "error": "LLM generated no valid SMILES strings matching the expected format (output was filtered).",
                "raw_output": smiles_raw.strip()
            }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"LLM generation failed: {str(e)}"}, indent=2)
    
    results = []
    valid_count = 0
    
    for i, smiles in enumerate(smiles_list[:5], 1):
        if not RDKIT_AVAILABLE:
            props = {"pic50": None, "logp": None, "atoms": None}
            validity_error = "RDKit missing"
        else:
            props = predictor.predict(smiles)
            validity_error = None
        
        mol = Chem.MolFromSmiles(smiles) if RDKIT_AVAILABLE else None

        if mol is None:
            validity_error = validity_error or "Invalid SMILES structure"
        
        if props is None or any(v is None for v in props.values()):
            validity_error = validity_error or "Property prediction failed"
        
        # Jika ada error, anggap tidak valid
        if validity_error:
            results.append({
                "id": i,
                "smiles": smiles,
                "valid": False,
                "error": validity_error
            })
            continue
        
        is_valid = validate_properties(props, constraint_dict)
        if is_valid:
            valid_count += 1
        
        results.append({
            "id": i,
            "smiles": smiles,
            "valid": is_valid,
            "properties": {
                "pIC50": round(props["pic50"], 2), # pIC50 (Camel Case) untuk output JSON
                "logP": round(props["logp"], 2),
                "atoms": props["atoms"]
            }
        })
    
    return json.dumps({
        "constraints": constraint_dict,
        "total_generated": len(results),
        "valid_molecules": valid_count,
        "results": results
    }, indent=2)

class JustifyInput(BaseModel):
    smiles: str
    properties: dict
    constraints: dict

@tool(args_schema=JustifyInput)
def generate_justification(smiles: str, properties: dict, constraints: dict) -> str:
    """
    TOOL 2: Menggunakan LLM untuk membuat justifikasi ilmiah.
    """
    if not RDKIT_AVAILABLE:
        return "Error: RDKit missing, cannot generate justification context."

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return "Error: Invalid SMILES structure for justification."
    
    # Ambil data tambahan untuk konteks
    formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
    mw = Descriptors.MolWt(mol)
    
    prompt = f"""You are a medicinal chemist. Provide a brief scientific justification for why this molecule is a valid candidate.

SMILES: {smiles}
Molecular Formula: {formula}
Molecular Weight: {mw:.2f} g/mol

Predicted Properties:
- pIC50: {properties.get('pIC50', 'N/A')}
- logP: {properties.get('logP', 'N/A')}
- Atom count: {properties.get('atoms', 'N/A')}

Target Constraints:
{json.dumps(constraints, indent=2)}

Provide a 2-3 sentence justification explaining:
1. Why the predicted properties satisfy the constraints
2. What structural features contribute to these properties
3. Brief assessment of drug-likeness

Keep it concise and scientific. Do NOT include the SMILES or property values again."""

    try:
        justification = llm.invoke(prompt)
        return justification.strip()
    except Exception as e:
        return f"Error generating justification: {str(e)}"

class ImageInput(BaseModel):
    smiles: str

@tool(args_schema=ImageInput)
def generate_molecule_image(smiles: str) -> str:
    """
    TOOL 3: Membuat gambar 2D molekul dari SMILES.
    Mengembalikan Base64-encoded PNG.
    """
    if not RDKIT_AVAILABLE:
        return json.dumps({"success": False, "error": "RDKit not available"})

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return json.dumps({"success": False, "error": "Invalid SMILES structure"})
    
    try:
        # Gunakan ukuran yang sedikit lebih kecil dari 400x400 agar cepat dimuat di web
        img = Draw.MolToImage(mol, size=(300, 300))
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64_data = base64.b64encode(buf.getvalue()).decode()
        
        return json.dumps({
            "success": True,
            "image_base64": b64_data, # Kunci ini yang akan diambil oleh main.py
            "format": "PNG"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

# ====================================================================
# 5. ORKESTRASI UTAMA (Fungsi yang dipanggil oleh FastAPI)
# ====================================================================

def run_with_manual_orchestration(constraints: str) -> Dict[str, Any]:
    """
    Fungsi utama yang menjalankan seluruh alur kerja Agentic (generate, validate, justify, image).
    """
    # 1. Generate dan Validasi SMILES
    print("Agent Step 1: Generating and validating molecules...")
    result_json = generate_and_validate_molecules.invoke({
        "constraints": constraints,
    })
    
    try:
        results_container = json.loads(result_json)
    except:
        return {"error": "Failed to parse generation results from LLM."}
    
    if "error" in results_container:
        return {"error": results_container["error"]}
    
    # 2. Proses Justifikasi dan Gambar untuk Molekul yang Valid
    print(f"Agent Step 2: Processing {results_container.get('valid_molecules', 0)} valid molecules...")
    
    processed_results = []
    
    for molecule in results_container["results"]:
        if not molecule.get("valid", False):
            # Termasuk molekul yang tidak valid (jika perlu ditampilkan error)
            processed_results.append(molecule)
            continue
        
        # Generate justification (LLM call)
        justification = generate_justification.invoke({
            "smiles": molecule["smiles"],
            "properties": molecule["properties"],
            "constraints": results_container["constraints"]
        })
        molecule["justification"] = justification
        
        # Generate image (RDKit call)
        image_result_json = generate_molecule_image.invoke({
            "smiles": molecule["smiles"]
        })
        
        try:
            image_data = json.loads(image_result_json)
            if image_data.get("success"):
                # Simpan BASE64 data
                molecule["image_base64"] = image_data["image_base64"] 
            else:
                molecule["image_error"] = image_data.get("error", "Image generation failed.")
        except:
            molecule["image_error"] = "Failed to parse image result."
        
        processed_results.append(molecule)
        
    print("✓ Agent processing complete!")
    
    # Mengembalikan struktur data yang sama dengan output LangChain (tapi sudah lengkap)
    results_container["results"] = processed_results
    
    return results_container

# ====================================================================
# SCRIPT END
# ====================================================================