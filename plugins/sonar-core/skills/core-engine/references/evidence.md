# Modul: Aturan Bukti

Target sistem ini bukan "model tidak pernah salah", tapi **kesalahan tertangkap sebelum sampai ke klien atau developer**. Modul ini berisi aturan yang membuat kesalahan terlihat.

## 1. Setiap temuan punya empat hal

| Field | Isi | Contoh |
|---|---|---|
| Bukti | Data konkret yang bisa dicek ulang | "canonical = https://gwenchana.digital/ di 6 template yang dicek" |
| Sumber | Dari mana bukti diambil | `chrome`, `curl`, `screaming_frog`, `gsc_windsor`, `gsc_csv`, `gsc_ui`, `ga4`, `semrush`, `user` |
| Tanggal cek | Kapan bukti diambil | 2026-10-16 |
| Keyakinan | Lihat bagian 2 | `terverifikasi` |

Temuan tanpa bukti tidak masuk deliverable.

## 2. Tingkat keyakinan

| Label | Arti | Boleh jadi instruksi ke developer/klien? |
|---|---|---|
| `terverifikasi` | Dicek langsung dari sumber primer di sesi ini | Ya |
| `dugaan` | Disimpulkan dari data tidak langsung (snippet pencarian, pola, sampel) | Tidak. Masuk laporan sebagai catatan, perlu verifikasi |
| `perlu konfirmasi` | Butuh data atau akses yang tidak tersedia, atau keputusan klien | Tidak. Masuk Tasklist sebagai "Need Confirmation", tidak masuk WRD |

Hasil ekstrapolasi (pola dari sampel yang diterapkan ke halaman lain) selalu `dugaan` dan ditandai di file (contoh lama yang baik: baris kuning di sampel Precicon M.E.T.A).

## 3. Hitung dengan kode, bukan dari ingatan

Semua angka yang muncul di laporan dihitung dengan kode dari data, lalu **satu angka dipakai di semua tempat**. Termasuk: jumlah halaman, jumlah temuan per prioritas, total klik/impresi, panjang karakter title/meta, jumlah link di artikel, jumlah keyword.

Alasannya ada di handover lama: satu sesi P.R.O.B.E menyebut 36, 44, dan 45 halaman untuk situs yang sama, dan 15 vs 20 item P0; satu checklist N.E.X.U.S menyatakan semua link lulus padahal beberapa hilang.

Cara: simpan angka di variabel atau file ringkasan saat membuat deliverable, lalu ambil angka untuk pesan chat dari sana. Sebelum mengirim ringkasan, cocokkan angka di chat dengan angka di file.

## 4. Fakta tentang klien

- Klaim tentang klien (waktu produksi, sertifikasi, garansi, status distributor resmi, harga, cakupan layanan) hanya dari `seo.claims.approved` di context profile, dokumen resmi klien, atau pernyataan user di sesi itu.
- Selain itu, tulis `[KLAIM PERLU KONFIRMASI: ...]`.
- Cek `seo.claims.forbidden` dan `seo.decisions` sebelum menulis copy, judul, brief, atau rekomendasi topik.

## 5. Fakta eksternal dan statistik

- Jangan mengarang data SERP, statistik, kutipan, atau sumber. Kalau tidak ada sumber, pakai placeholder `[Sumber diperlukan: ...]`.
- Untuk konten YMYL (kesehatan, keuangan, hukum, keselamatan): setiap statistik dicek dengan membuka sumbernya, dan isi klaim dibandingkan dengan sumber. Contoh kesalahan lama yang lolos: klaim kelompok usia tertinggi penyakit jantung koroner yang ternyata menyesatkan menurut sumbernya.
- Sebutkan tahun dan lembaga untuk setiap statistik.

## 6. Data yang tidak lengkap

- Sebutkan secara eksplisit data yang tidak tersedia dan dampaknya ke kesimpulan. Contoh: "Data Page Indexing tidak tersedia (Windsor tidak menyediakan, akses GSC UI belum ada). Tahap Index dinilai dari crawl saja."
- Jangan menjalankan analisis yang menurut aturan butuh data wajib, lalu diam-diam mengisi celahnya dengan perkiraan. Kalau memakai perkiraan (misalnya volume dari pengetahuan umum), labeli `dugaan` di setiap baris. Contoh lama yang harus dihindari: laporan C.L.U.S.T.E.R Gwenchana yang mengisi volume dan KD dari "industry knowledge".

## 7. Pemeriksaan akhir sebelum deliverable dikirim

Jalankan dengan kode bila memungkinkan:

- [ ] Angka di chat sama dengan angka di file
- [ ] Setiap baris punya status, sumber, dan keyakinan
- [ ] Tidak ada item `dugaan` atau `perlu konfirmasi` yang tertulis sebagai instruksi pasti
- [ ] Panjang karakter title/meta dihitung ulang dengan kode
- [ ] Link di artikel atau dokumen dihitung dan dicek ulang dengan kode
- [ ] Klaim tentang klien cocok dengan `claims.approved`
- [ ] Periode data dan versi C.O.R.E tertulis di file
- [ ] Nama file mengikuti `handoff.md`
