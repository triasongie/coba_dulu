# Gunakan image Python yang sudah memiliki RDKit atau Conda
# Contoh RDKit/Conda image:
FROM continuumio/miniconda3

# Buat lingkungan Conda dan instal RDKit serta dependensi lainnya
RUN conda create -n chem_env python=3.10
RUN echo "conda activate chem_env" > ~/.bashrc
ENV PATH /opt/conda/envs/chem_env/bin:$PATH

# Instal RDKit dan dependensi dari requirements.txt
RUN conda install -c conda-forge rdkit -y
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin semua file proyek Anda ke container
COPY . /app
WORKDIR /app

# Perintah untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
