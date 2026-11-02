# Modul: Router Diagnostik

Pintu masuk untuk website yang sudah jalan. Router memeriksa funnel SEO dari hulu ke hilir, menemukan tahap paling awal yang rusak di tiap URL, lalu mengarahkan temuan ke project yang tepat. Mesin diagnosa C.L.U.S.T.E.R (index gap, cluster trust score) dilebur ke sini.

## Daftar isi
1. Funnel
2. Aturan dasar
3. Mode Lengkap vs Ringan
4. Langkah kerja
5. URL master
6. Pemeriksaan per tahap
7. Alasan Page Indexing GSC → tahap
8. Site-level vs page-level
9. Ringkasan per cluster (Trust Score)
10. Routing ke project
11. Output

---

## 1. Funnel

```
Discover → Crawl → Render → Index → Rank → Click → Convert
```

| Tahap | Pertanyaan |
|---|---|
| Discover | Apakah Google tahu URL ini ada (sitemap, internal link)? |
| Crawl | Apakah Googlebot bisa mengaksesnya? |
| Render | Apakah konten dan link penting ada tanpa bergantung pada JavaScript yang gagal? |
| Index | Apakah halaman masuk index, dengan canonical yang benar? |
| Rank | Apakah posisinya bagus untuk query yang relevan? |
| Click | Apakah diklik sewajarnya di posisinya? (`ctr.md`) |
| Convert | Apakah pengunjung organik melakukan sesuatu yang berharga? |

## 2. Aturan dasar

1. **Hulu dulu.** URL dinilai tahap demi tahap. Kalau rusak di satu tahap, tahap sesudahnya untuk URL itu ditandai `tertahan`, tidak dinilai. Alasannya: memperbaiki title halaman yang tidak ter-index adalah kerja sia-sia.
2. **Gejala bukan penyebab.** Halaman "tidak ranking" bisa disebabkan canonical salah (tahap Index). Selalu cari tahap paling awal yang rusak.
3. **Absen dari laporan Performance GSC tidak sama dengan tidak ter-crawl.** Laporan Performance hanya memuat halaman yang punya impresi. Status ter-crawl dan ter-index ditentukan dari crawl dan laporan Page Indexing.
4. **Tanpa bukti, tanpa label.** Setiap label tahap wajib punya bukti dan sumber (`evidence.md`). Kalau datanya tidak tersedia, statusnya `perlu konfirmasi`, bukan tebakan.
5. **Halaman terlalu baru** (terbit kurang dari 4 minggu) tidak dinilai di Rank, Click, Convert.
6. Semua penggabungan tabel dan hitungan dikerjakan dengan kode.

## 3. Mode Lengkap vs Ringan

| Mode | Data | Kapan |
|---|---|---|
| **Lengkap** | Export Screaming Frog + GSC performa (query × page) + Page Indexing + GA4 | Audit klien, situs besar, sebelum keputusan besar |
| **Ringan** | Sitemap (curl/browser) + GSC performa + sampel halaman lewat browser | Cek cepat, situs kecil, belum ada export Screaming Frog |

Sebutkan mode yang dipakai dan data apa yang hilang di awal laporan. Di mode Ringan, tahap Discover dan Crawl hanya bisa dinilai untuk URL sampel; tulis ini di bagian keterbatasan.

## 4. Langkah kerja

1. **Muat context profile.** Ambil domain, `page_types`, `brand_terms`, `markets`, `access`, `decisions`. Kalau tidak ada profile, minta minimal domain, pasar, dan istilah brand.
2. **Kumpulkan data** sesuai mode, lewat jalur di `data-sources.md`. Laporkan jumlah baris dan periode tiap sumber. Kalau status index per URL tidak tersedia (laporan GSC hanya dibaca agregat), URL sitemap tanpa impresi diberi tahap `Index (perlu konfirmasi)` dengan keyakinan `dugaan`, dan Trust Score per cluster ditunda.
3. **Cek blocker site-level lebih dulu** (bagian 8): robots.txt, noindex atau canonical massal, redirect domain, sertifikat. Ini murah dan bisa mengubah seluruh diagnosa.
4. **Bangun URL master** (bagian 5) dari gabungan semua sumber.
5. **Nilai tiap URL per tahap** (bagian 6), berhenti di tahap rusak pertama.
6. **Agregasi site-level vs page-level** (bagian 8).
7. **Ringkas per cluster** (bagian 9).
8. **Susun antrean per project** (bagian 10) dan output (bagian 11).

## 5. URL master

Satu baris per URL yang diketahui dari sumber mana pun (sitemap, crawl, GSC, GA4, daftar dari klien).

| Kelompok | Kolom |
|---|---|
| Identitas | `url`, `page_type`, `cluster`, `published_date` |
| Discover | `in_sitemap`, `in_crawl`, `crawl_depth`, `inlinks` |
| Crawl | `status_code`, `redirect_target`, `robots_blocked` |
| Render | `raw_vs_rendered_note` (hanya URL sampel) |
| Index | `indexable`, `meta_robots`, `x_robots_tag`, `canonical`, `canonical_is_self`, `gsc_index_status`, `gsc_index_reason`, `word_count`, `near_duplicate_of` |
| Rank | `in_gsc_performance`, `impressions`, `clicks`, `position`, `top_queries`, `competing_urls` |
| Click | `ctr_label`, `clicks_lost` (dari `ctr.md`) |
| Convert | `ga4_sessions_organic`, `ga4_engagement_sec`, `ga4_key_events` |
| Hasil | `stage_broken`, `issue`, `evidence`, `source`, `confidence`, `scope` (site/page), `route`, `priority` |

URL yang hanya muncul di GSC tapi tidak di sitemap maupun crawl patut dicurigai: parameter, URL lama, atau URL yang dibuat sistem (contoh nyata: ratusan URL `?products/*` di TrueMission dan Gwenchana).

## 6. Pemeriksaan per tahap

| Tahap | Rusak kalau | Sumber bukti | Route |
|---|---|---|---|
| Discover | Ada di sitemap tapi tidak ditemukan crawl (orphan); penting tapi kedalaman klik > 3; sitemap berisi URL non-200, non-canonical, atau noindex; halaman penting tidak ada di sitemap | Screaming Frog, sitemap | Technical |
| Crawl | Status 4xx/5xx untuk URL yang ditautkan atau ada di sitemap; redirect berantai (> 1 lompatan) atau loop; diblokir robots.txt padahal seharusnya diindex | curl, Screaming Frog, GSC | Technical |
| Render | Konten utama atau link navigasi hanya muncul setelah JavaScript; canonical/robots berbeda antara HTML mentah dan hasil render | Browser (resep render) | Technical |
| Index (teknis) | noindex/X-Robots-Tag tidak disengaja; canonical ke URL lain padahal halaman seharusnya berdiri sendiri; Google memilih canonical berbeda | Browser, Screaming Frog, GSC | Technical |
| Index (kualitas) | Crawled/Discovered - not indexed pada halaman yang secara teknis bersih; konten tipis; near-duplicate; soft 404 | GSC, Screaming Frog | Optimization (Refresh) |
| Rank: kanibalisasi | Dua URL atau lebih mendapat impresi untuk query utama yang sama dan saling bergantian posisi | GSC query × page | Optimization (Refresh) |
| Rank: intent | SERP query utama didominasi tipe halaman berbeda dari halaman klien | Browser (SERP) | Optimization (Refresh/Page) |
| Rank: authority | Halaman layak dan intent cocok, tapi kompetitor di SERP punya authority jauh lebih tinggi | SEMrush backlink | Strategy |
| Rank: tidak ada halaman | Query non-branded dengan impresi berarti, tidak ada URL yang benar-benar menjawabnya | GSC | Discovery |
| Rank: peluang | Posisi 10,5–20,5 dengan impresi berarti | GSC | Optimization (Refresh) |
| Click | Label merah atau kuning di `ctr.md` | GSC, browser | Optimization (Snippet) |
| Convert: tracking | GTM/GA4 tidak terpasang atau tidak mengirim | Browser (network) | Technical |
| Convert: halaman | Sesi organik berarti tapi engagement rendah atau key event nol, padahal tracking terbukti berjalan | GA4 | Optimization (Page) |

Angka seperti "impresi berarti" memakai ambang yang sama dengan modul CTR (minimal 100 impresi non-branded dalam periode) kecuali disebut lain. Semua ambang di tabel ini adalah titik awal yang diuji di beberapa klien sebelum dikunci.

## 7. Alasan Page Indexing GSC → tahap

| Alasan di GSC | Tahap | Catatan |
|---|---|---|
| Server error (5xx) | Crawl | Technical |
| Redirect error | Crawl | Technical |
| Blocked by robots.txt | Crawl | Cek apakah memang disengaja |
| Blocked due to unauthorized request (401), access forbidden (403), other 4xx | Crawl | Technical |
| Not found (404) | Crawl | Masalah hanya kalau URL masih ditautkan, ada di sitemap, atau dulu punya traffic/backlink |
| Page with redirect | Crawl | Biasanya wajar. Masalah kalau URL itu ada di sitemap atau ditautkan internal |
| Excluded by 'noindex' tag | Index (teknis) | Konfirmasi apakah disengaja |
| Alternative page with proper canonical tag | Index (teknis) | Biasanya wajar. Cek target canonical memang benar |
| Duplicate without user-selected canonical | Index (teknis) | Technical: tetapkan canonical |
| Duplicate, Google chose different canonical than user | Index | Teknis dan kualitas. Cek lewat URL Inspection, lalu Technical + Optimization |
| Soft 404 | Index | Halaman tipis atau kosong: Optimization. Halaman error yang mengembalikan 200: Technical |
| Crawled - currently not indexed | Index (kualitas) | Optimization (Refresh), kecuali halaman baru atau masalah teknis ditemukan |
| Discovered - currently not indexed | Discover | Technical (internal link, sitemap). Kalau jumlahnya besar, bisa juga sinyal kualitas situs |

Nama alasan bisa berubah di UI GSC (contoh: UI menulis "Alternative page with proper canonical tag" dan "Discovered – currently not indexed" dengan tanda pisah panjang). Cocokkan tanpa memedulikan tanda baca. Kalau menemukan alasan yang tidak ada di tabel ini, catat apa adanya dan tandai `perlu klasifikasi`.

**Baca dua tampilan, bukan satu.** Tampilan "All known pages" bercampur dengan URL yang tidak pernah Anda kirim (sering URL spam atau URL lama). Tampilan "All submitted pages" hanya berisi URL sitemap, dan rasio indexed vs not indexed di sana adalah angka paling jujur untuk kesehatan index situs. Contoh dari uji pertama: "All known pages" menunjukkan 14,6 ribu not indexed (sebagian besar 404 spam), sedangkan "All submitted pages" menunjukkan 98 dari 151 URL sitemap tidak terindeks. Dua angka itu menunjuk ke dua masalah berbeda.

**Kolom Validation** menunjukkan apakah seseorang pernah menekan "Validate Fix" dan hasilnya (Not Started, Started, Failed, Passed). Failed pada URL spam yang terus ditemukan dari link luar adalah wajar; Failed pada URL sitemap berarti masalahnya belum selesai.

## 8. Site-level vs page-level

**Blocker site-level** (cek di langkah 3, selalu P0):
- robots.txt memblokir seluruh situs atau direktori utama
- noindex di template yang dipakai banyak halaman
- Canonical banyak halaman mengarah ke satu URL (contoh Gwenchana: semua halaman canonical ke homepage)
- Versi domain tidak konsisten (http/https, www/non-www) tanpa redirect yang benar
- Seluruh situs bergantung pada JavaScript yang gagal render

Kalau ada blocker site-level, URL yang terdampak ditandai `tertahan` di tahap setelahnya, dan antrean Optimization/Discovery untuk URL itu disusun sebagai **persiapan**, bukan untuk dieksekusi dulu.

**Agregasi per jenis halaman:** kalau masalah yang sama mengenai **30% atau lebih** URL dari satu `page_type` (minimal 5 URL), jadikan satu temuan site-level (masalah template) ke Technical, bukan puluhan temuan per halaman. Di bawah ambang itu, tetap per halaman.

## 9. Ringkasan per cluster (Trust Score)

Diwarisi dari C.L.U.S.T.E.R v2.0, dipakai untuk melihat topik mana yang sudah dipercaya Google.

**Deteksi cluster:** pakai `page_types` dan pilar konten di context profile sebagai jangkar. Sisanya kelompokkan dari slug URL: tokenisasi, buang kata umum, kelompokkan URL yang berbagi 2+ kata bermakna. Jangan memakai daftar cluster yang di-hardcode.

**Rumus (0–100):**
```
Trust Score = (proporsi URL ter-index × 40)
            + (rata-rata klik GSC per URL, dinormalisasi 0–30 terhadap cluster tertinggi)
            + (rata-rata sesi organik GA4 per URL, dinormalisasi 0–20 terhadap cluster tertinggi)
            + 10 jika ada minimal satu URL di posisi ≤ 10
```
Tanpa data GA4, komponen GA4 bernilai 0 dan disebut di laporan (skor maksimal jadi 80).

| Skor | Tingkat |
|---|---|
| 80–100 | Sangat kuat |
| 60–79 | Kuat |
| 40–59 | Menengah |
| 20–39 | Lemah |
| 0–19 | Belum dipercaya |

Pakai Trust Score untuk memilih arah, bukan sebagai bukti tunggal: cluster kuat cocok untuk perluasan konten (Discovery), cluster lemah dengan banyak URL tidak ter-index cocok untuk konsolidasi (Optimization) atau pemeriksaan teknis.

## 10. Routing ke project

| Project | Menerima dari router |
|---|---|
| **Technical** (eks P.R.O.B.E) | Blocker site-level, Discover, Crawl, Render, Index teknis, tracking |
| **Optimization** (eks M.E.T.A, S.C.O.U.T, bagian aksi C.L.U.S.T.E.R) | Index kualitas, kanibalisasi, intent, peluang posisi 11–20, Click, Convert halaman |
| **Strategy** (eks S.O.N.A.R v2.1) | Kekalahan authority, cluster lemah yang butuh rencana topikal |
| **Discovery** (eks P.I.N.G + S.P.E.A.R) | Query tanpa halaman, cluster kuat yang layak diperluas |
| **Production** (NEXUS) | Tidak langsung dari router. Lewat Discovery atau Strategy |

Batas tanggung jawab yang sering tumpang tindih:
- Title/meta **duplikat atau hilang** dideteksi router atau Technical; **penulisan ulangnya** dikerjakan Optimization.
- **Rencana redirect atau konsolidasi** disusun Optimization; **instruksi implementasi untuk developer** (WRD) ditulis Technical.
- **Data GSC** diambil lewat modul ini. Project lain tidak membuat versi sendiri.

## 11. Output

**File:** `[Klien]_CORE_Diagnosis_[YYYY-MM-DD].xlsx` (penamaan lengkap di `handoff.md`).

| Sheet | Isi |
|---|---|
| 1 Ringkasan | Mode, periode, sumber data dan jumlah barisnya, keterbatasan, 5 temuan terpenting |
| 2 Site-level | Blocker dan masalah template, dengan bukti |
| 3 URL Master | Tabel bagian 5 |
| 4 Cluster | Trust Score per cluster |
| 5 Antrean | Satu bagian per project tujuan, terurut prioritas |
| 6 Bukti | Daftar bukti (URL, cuplikan data, sumber, tanggal cek) |
| 7 Metodologi | Ambang yang dipakai, benchmark CTR yang dipakai, versi C.O.R.E |

Plus satu file handoff per project tujuan (`handoff.md`).

**Di chat:** maksimal 5 temuan terpenting, urut dari hulu, masing-masing dengan angka dan project tujuannya. Detail ada di file. Jangan menulis ulang isi file di chat.

**Prioritas:** P0 = blocker site-level atau masalah yang mengenai halaman bernilai bisnis utama; P1 = masalah page-level di halaman penting atau masalah template non-blocker; P2 = perbaikan bernilai kecil. Label ini sama dengan P.R.O.B.E supaya bisa langsung masuk Tasklist.
