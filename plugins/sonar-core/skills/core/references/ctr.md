# Modul: CTR

Satu definisi CTR untuk seluruh S.O.N.A.R. Modul ini menggantikan lima definisi lama yang saling berbeda (lihat tabel migrasi di bagian akhir). Semua hitungan di modul ini dikerjakan dengan kode dari tabel `gsc_page_query` (`data-sources.md`), bukan dihitung manual.

## 1. Posisi CTR di funnel

CTR hanya menjawab satu pertanyaan: **halaman yang sudah tampil di halaman 1, apakah diklik sewajarnya?** Jadi:

| Posisi rata-rata | Diperlakukan sebagai |
|---|---|
| 1 sampai 10,5 | Dinilai dengan modul ini (tahap **Click**) |
| di atas 10,5 sampai 20,5 | **Peluang ranking** (tahap Rank), bukan masalah CTR. CTR rendah di sini wajar |
| di atas 20,5 | Masalah ranking. CTR tidak dinilai |

Jangan pernah melabeli halaman di posisi 15 sebagai "CTR darurat". Perbaikannya ranking, bukan title/meta.

## 2. Langkah perhitungan

1. **Pisahkan query branded.** Query yang mengandung salah satu `seo.brand_terms` (pencocokan tanpa huruf besar/kecil, termasuk tanpa spasi) diberi `is_branded = true`. Query branded hampir selalu punya CTR tinggi dan akan membuat halaman terlihat sehat. Yang dinilai hanya **non-branded**. Kalau `brand_terms` kosong, minta diisi dulu atau isi sementara dari nama brand dan domain, lalu tandai `[INFERRED]`.
2. **Agregasi per halaman** (non-branded saja): `clicks` dan `impressions` dijumlah; `ctr = clicks / impressions`; posisi = rata-rata tertimbang impresi.
3. **Saring data tipis.** Halaman dengan impresi non-branded di bawah **100** dalam periode diberi label `data kurang` dan tidak dinilai. Halaman yang terbit kurang dari 4 minggu diberi label `terlalu baru`.
4. **Tentukan kelompok posisi** dan ambil benchmark (bagian 3).
5. **Hitung rasio** = CTR aktual / CTR benchmark.
6. **Beri label** (bagian 4).
7. **Cek SERP dulu sebelum menyalahkan snippet** (bagian 5).

## 3. Benchmark

### Benchmark default

Angka minimum dari M.E.T.A, dipakai sebagai default:

| Kelompok | Rentang posisi rata-rata | CTR benchmark |
|---|---|---|
| P1 | 1 sampai di bawah 1,5 | 28% |
| P2 | 1,5 sampai di bawah 2,5 | 15% |
| P3 | 2,5 sampai di bawah 3,5 | 10% |
| P4–5 | 3,5 sampai di bawah 5,5 | 6% |
| P6–10 | 5,5 sampai 10,5 | 2% |

Rentang ditulis tanpa celah supaya posisi desimal seperti 4,6 selalu punya kelompok (celah ini tidak diatur di M.E.T.A lama).

Angka ini titik awal, bukan kebenaran. Kurva CTR publik sudah bergeser sejak AI Overview, dan perlu diuji di 2–3 klien sebelum dikunci. Setiap perubahan angka dicatat di CHANGELOG repo.

### Benchmark terkalibrasi (opsional)

Kalau situs punya data cukup, hitung benchmark situs sendiri: median CTR non-branded per kelompok posisi. Syarat: minimal **30 halaman** dengan impresi ≥ 100 di kelompok itu. Kalau syarat tidak terpenuhi di satu kelompok, kelompok itu memakai angka default. Laporan wajib menyebut benchmark mana yang dipakai per kelompok.

Situs kecil hampir selalu memakai angka default. Itu bukan kegagalan, tapi perlu disebut supaya pembaca tahu dasarnya.

## 4. Label

| Label | Syarat | Arti |
|---|---|---|
| 🔴 Merah | Rasio di bawah 0,5 | CTR kurang dari separuh kewajaran. Prioritas perbaikan snippet |
| 🟡 Kuning | Rasio 0,5 sampai di bawah 0,9 | Di bawah wajar. Antrean perbaikan berikutnya |
| 🟢 Aman | Rasio 0,9 atau lebih | Jangan diubah hanya demi berubah (aturan M.E.T.A) |
| ⚪ Data kurang | Impresi non-branded di bawah 100 | Tidak dinilai |
| ⚪ Terlalu baru | Terbit kurang dari 4 minggu | Tidak dinilai |

Urutan prioritas di dalam label merah dan kuning: **klik yang hilang** = impresi × (CTR benchmark − CTR aktual). Ini mengurutkan berdasarkan dampak nyata, bukan hanya seberapa jelek rasionya.

Halaman posisi 1–2 dengan label aman diperlakukan sebagai **dilindungi**: perubahan title/meta di halaman ini butuh alasan kuat dan persetujuan user (kebiasaan lama M.E.T.A Precicon).

## 5. Cek SERP sebelum menyalahkan snippet

CTR rendah tidak selalu salah title/meta. Untuk halaman berlabel merah dengan klik hilang terbesar (minimal 5 teratas), cek query utamanya lewat `browser-inspection.md` bagian 9. Catat penyebab yang paling mungkin:

| Temuan di SERP | Penyebab | Arah perbaikan |
|---|---|---|
| AI Overview menjawab langsung, featured snippet milik situs lain | Klik dicuri fitur SERP | Optimization (struktur jawaban, FAQ), bukan sekadar title |
| SERP didominasi halaman produk/marketplace, halaman klien artikel | Intent tidak cocok | Optimization (mode Refresh) atau halaman lain yang lebih cocok. Contoh nyata: `kotak-nasi-kardus` PamanPack |
| Hasil lain punya angka, harga, atau manfaat jelas di title | Snippet kalah menarik | Optimization (mode Snippet) |
| Title/meta yang tampil di SERP berbeda dari yang ditulis di halaman | Google menulis ulang snippet | Optimization (mode Snippet), cek kecocokan title dengan isi |

## 6. Output standar

Kolom per halaman: `page`, `period`, `position_weighted`, `position_group`, `impressions_nonbranded`, `clicks_nonbranded`, `ctr`, `benchmark`, `benchmark_source` (`default` / `kalibrasi`), `ratio`, `label`, `clicks_lost`, `top_queries` (3 query non-branded teratas), `serp_note`, `route`.

## 7. Tabel migrasi dari definisi lama

| Project lama | Definisi lama | Diganti dengan |
|---|---|---|
| C.L.U.S.T.E.R | Impression Trap: impresi > 1.000 dan CTR < 0,5%. CTR Anomaly: posisi ≤ 10 dan CTR < 1% | Label merah/kuning modul ini. Impresi besar tercermin di urutan klik hilang |
| S.O.N.A.R | CTR Emergency: CTR < 2% dan impresi > 500 | Label merah modul ini. Track A Strategy memakai daftar merah |
| M.E.T.A | P1 Quick Win posisi 5–15, P2 CTR Fix posisi 1–4, di bawah benchmark minimum | Posisi 1–10,5 dinilai di sini; 10,5–15 pindah ke peluang ranking |
| S.C.O.U.T | Gap: posisi > 10 atau CTR 0%. Partial: posisi 3–10, CTR di bawah rata-rata | Posisi > 10 masuk tahap Rank. CTR dinilai dengan rasio benchmark |
| P.R.O.B.E | CTR Emergency List: impresi tinggi dan CTR rendah, tanpa angka | Technical tidak lagi menyusun daftar CTR. Daftar diambil dari modul ini |
