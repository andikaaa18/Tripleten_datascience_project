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

## Kesimpulan Akhir
Dari hasil pengamatan dan perhitungan yang telah dilakukan maka diperoleh hasil akhir yaitu sebagai berikut.
1. **Apakah terdapat hubungan antara memiliki anak dan probabilitas seseorang melakukan gagal bayar pinjaman?**
    
    * Nasabah yang tidak memiliki anak memiliki probabilitas gagal bayar paling kecil yaitu sebesar 7,5%. Sedangkan nasabah yang memiliki anak memiliki resiko gagal bayar lebih besar dengan probabilitas 8% hingga 9,7%.
    

2. **Apakah terdapat hubungan antara status perkawinan dan probabilitas seseorang melakukan gagal bayar pinjaman?**

    * Nasabah yang sudah pernah menikah baik yang masih langgeng, bercerai atau ditinggal mati oleh pasangannya memiliki probabilitas gagal bayar yang paling kecil yaitu pada kisaran 6,6% hingga 7,5%. Sedangkan nasabah yang belum pernah melakukan pernikahan memiliki resiko gagal bayar yang lebih besar yaitu pada kisaran 9,3% hingga 9,8%.

    * Dan diantara nasabah yang sudah pernah menikah, nasabah yang ditinggal mati oleh pasangannya memiliki probabilitas gagal bayar lebih kecil yaitu sebesar 6,6%. Sedangkan nasabah yang masih memiliki pasangan/ mantan pasangan masih hidup memiliki resiko gagal bayar lebih besar yaitu berkisar pada angka 7,1% hingga 7,5%.


3. **Apakah terdapat hubungan antara tingkat pendapatan dan probabilitas seseorang melakukan gagal bayar pinjaman?**

    * Nasabah yang memiliki pendapatan pada kategori *`high income`* dengan pendapatan diatas **31653.35** memiliki resiko gagal bayar paling kecil yaitu pada angka 7%. Sedangkan nasabah dari kategori pendapatan menengah dan rendah memiliki resiko gagal bayar paling tinggi yaitu berkisar pada angka 8% hingga 9,2%.

    * Kategori pendapatan menengah (*`lower-middle income`* dan *`upper-middle income`*) dengan pendapatan diantara **17141,1** hingga **31653.35** memiliki resiko gagal bayar paling tinggi yaitu pada kisaran angka 8,3% hingga 9,2%.

    * Dan diantara nasabah kategori pendapatan menengah, nasabah dengan pendapatan *`lower-middle income`* dengan pendapatan diantara **17141,1** hingga **22956.96** memiliki resiko gagal bayar paling tinggi yaitu sebesar 9,2%.

    
4. **Bagaimana perbedaan tujuan pinjaman memengaruhi probabilitas seseorang melakukan gagal bayar pinjaman?**

    * Nasabah yang memiliki tujuan pengajuan kredit berupa perolehan pendidikan dan mobil memiliki resiko gagal bayar paling tinggi yaitu berkisar pada 9,2% hingga 9,35%.
    * Nasabah yang memiliki tujuan untuk perolehan *property* memiliki resiko gagal bayar paling kecil yaitu sebesar 7,2%. Kemudian pada urutan kedua terdapat kelompok nasabah yang memiliki tujuan untuk pernikahan sebesar 8%.
