# Credit Scoring Analysis
## Deskripsi
Menganalisa histori kredit sejumlah nasabah untuk melakukan penilaian kredit untuk calon nasabah baru. Proses penilaian meliputi kriteria jumlah anak, status perkawinan, penghasilan bulanan, dan tujuan pengajuan kredit setiap nasabah terhadap resiko gagal bayar.

## Tujuan Projek
Tujuan dari projek ini adalah untuk membantu Divisi Kredit untuk menentukan kemampuan nasabah dalam menyelesaikan kredit. Parameter historis *gagal bayar* nasabah yang pernah melakukan kredit pada masa sebelumnya akan menjadi informasi dasar sebagai proyeksi untuk calon nasabah ke depannya. Output dari projek ini adalah dapat memberi informasi mengenai kriteria khas dari nasabah yang berpotensi mengalami gagal bayar dan yang melunasi kredit dengan baik.

Adapun hipotesis yang akan diuji pada projek ini adalah sebagai berikut.
1. Jumlah anak yang lebih sedikit dalam keluarga akan meningkatkan kemampuan nasabah dalam melunasi kredit.
2. Nasabah yang belum membina keluarga akan memiliki potensi lebih kecil untuk mengalami gagal bayar dibandingkan nasabah yang telah berkeluarga.
3. Nasabah dengan pendapatan yang lebih kecil memiliki potensi lebih besar untuk gagal bayar.
4. Tujuan atas pengajuan kredit akan menentukan kemampuan pelunasan pinjaman oleh nasabah.

# Deskripsi Data
* `children` : jumlah anak dalam keluarga
* `days_employed`: berapa lama nasabah telah bekerja
* `dob_years`: usia nasabah
* `education`: tingkat pendidikan nasabah
* `educationid`: pengidentifikasi untuk tingkat pendidikan nasabah
* `family_status`: status perkawinan nasabah
* `family_status_id`: pengidentifikasi untuk status perkawinan nasabah
* `gender`: jenis kelamin nasabah
* `income_type`: jenis pendapatan nasabah
* `debt`: apakah nasabah pernah melakukan gagal bayar pinjaman
* `total_income`: pendapatan bulanan
* `purpose`: alasan mengambil pinjaman

## Library yang Digunakan
1. Pandas
2. Numpy

## Daftar Isi
- Menganalisis Risiko Gagal Bayar Peminjam
- Tujuan Proyek   
  - Membuka *file* data dan membaca informasi umumnya. 
  - Transformasi data   
- Bekerja dengan nilai yang hilang    
    - Memperbaiki nilai yang hilang di `total_income` 
    - Memperbaiki nilai di `days_employed` 
  - Pengkategorian Data  
  - Memeriksa hipotesis 
- Kesimpulan umum   
