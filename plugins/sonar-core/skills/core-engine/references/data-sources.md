# Modul: Sumber Data

Modul ini mengatur dari mana data diambil dan bentuk akhirnya. Prinsipnya: **banyak jalur masuk, satu format keluar.** Project hilir tidak perlu tahu data datang dari Windsor, CSV, atau browser.

## Daftar isi
1. Google Search Console (tiga jalur)
2. GA4
3. Crawl website (Screaming Frog)
4. Akses HTTP langsung (curl)
5. Format ternormalisasi
6. Aturan periode

---

## 1. Google Search Console

Tanyakan pilihan jalur ke user **hanya kalau `seo.access.gsc.via` di context profile kosong**. Kalau sudah terisi, pakai itu dan sebutkan jalurnya.

| Jalur | Pakai untuk | Batasan yang harus disebut ke user |
|---|---|---|
| **A. Windsor.ai** | Data performa: query × page, clicks, impressions, CTR, posisi | Menurut catatan C.L.U.S.T.E.R, data coverage/indexing tidak tersedia lewat Windsor. Tools Windsor kadang tidak ter-load di sesi; kalau begitu, tawarkan jalur B atau C |
| **B. Export CSV manual** | Cadangan untuk data performa | Export dari UI GSC dibatasi 1.000 baris per tabel, dan tab Queries dan Pages terpisah tanpa pemetaan query ke page |
| **C. GSC UI lewat Claude in Chrome** | Laporan Page Indexing beserta alasannya, URL Inspection, Crawl Stats | Butuh profil Chrome yang sudah login ke GSC. Lambat. Download file butuh izin user per kali. Ikuti `browser-inspection.md` |

Default yang disarankan: **A untuk performa, C untuk indexing, B kalau A tidak tersedia.**

### Jalur A — Windsor.ai

1. `get_connectors` untuk melihat akun GSC yang tersedia. Nama connector yang tercatat dipakai di project lama: `searchconsole`, akun berbentuk `sc-domain:<domain>`.
2. `get_fields` untuk memastikan nama field. Field yang tercatat dipakai: `page`, `query`, `clicks`, `impressions`, `ctr`, `position`, plus tanggal.
3. `get_data` dengan rentang tanggal eksplisit (lihat bagian 6), bukan hanya preset, supaya periode bisa ditulis persis di laporan.
4. Windsor tidak dihitung biaya SEMrush, jadi tidak perlu API gate SEMrush. Tetap sebutkan berapa baris yang ditarik.

Jangan menebak nama connector atau field. Selalu cek lewat `get_connectors` dan `get_fields`, karena nama bisa berbeda antar akun.

**Data Windsor masuk ke percakapan, bukan ke file.** Hasil `get_data` muncul sebagai teks di konteks, tidak otomatis tersimpan di sandbox, padahal aturan bukti meminta hitungan dikerjakan dengan kode. Cara yang teruji:
- Tarik dua kali dengan field sesedikit mungkin: sekali per halaman (`page`, `clicks`, `impressions`, `position`) untuk total yang akurat, sekali per query × halaman untuk analisis query.
- Salin tabel yang akan dihitung ke file TSV/CSV di sandbox (cukup kolom yang dipakai), lalu hitung dari file itu.
- Untuk data besar (ratusan baris ke atas), lebih efisien pakai export CSV (jalur B) atau destinasi Windsor ke Google Sheets lalu baca dari sana.

Rekonsiliasi wajib: di uji pertama, data per query hanya 169 baris dengan klik nol, sementara data per halaman menunjukkan 50 klik dan 2.405 impresi. Selisihnya adalah query yang dianonimkan GSC. Jangan menilai CTR halaman dari data per query saja.

### Jalur B — Export CSV manual

Instruksi untuk user:

| File | Cara export | Catatan |
|---|---|---|
| Performance | GSC → Performance → Search results → atur tanggal → Export | Berisi beberapa tab (Queries, Pages, Countries, Devices, dst.). Simpan semua |
| Query per halaman (opsional) | Di Performance, filter Page = URL tertentu → tab Queries → Export | Satu file per halaman penting. Ini satu-satunya cara CSV mendapat pemetaan query → page |
| Page Indexing | GSC → Indexing → Pages → klik tiap alasan (mis. "Crawled - currently not indexed") → Export | Satu file per alasan |

Setelah diterima: baca semua file, cek kolom wajib ada, laporkan jumlah baris dan periode yang terbaca, lalu normalisasi.

### Jalur C — GSC UI lewat browser

Detail langkah ada di `browser-inspection.md` bagian GSC. Mode default **hanya membaca**. Tombol "Request Indexing", "Validate Fix", atau perubahan setting apa pun tidak boleh diklik tanpa izin eksplisit user di chat.

---

## 2. GA4

| Jalur | Isi | Catatan |
|---|---|---|
| Windsor.ai | Landing page, sessions, active users, engagement time, key events | Cek nama connector GA4 lewat `get_connectors`. Property ID dicatat di `seo.access.ga4.property_id` |
| Export CSV | GA4 → Reports → Engagement → Landing page → Export | Periode harus sama dengan periode GSC |

GA4 hanya dipakai untuk tahap **Convert** di router. GA4 tidak bisa mendiagnosa crawl atau index.

Batasan yang perlu disebut: GA4 mencatat landing page sebagai path (sering tanpa domain dan bisa berisi parameter). Normalisasi ke URL lengkap sebelum digabung dengan GSC. GA4 juga mencatat semua channel, jadi filter ke organic search kalau yang dianalisis performa SEO.

---

## 3. Crawl website (Screaming Frog)

Screaming Frog adalah sumber utama untuk tahap Discover, Crawl, Render, dan Index teknis kalau situsnya lebih dari beberapa puluh halaman. Browser dan curl dipakai untuk verifikasi dan sampel.

Export standar yang diminta ke user:

| Export | Untuk |
|---|---|
| Internal → HTML (semua kolom) | Inventaris URL, status, indexability, title, meta, H1, canonical, word count, crawl depth, inlinks |
| Response Codes → semua | 3xx, 4xx, 5xx |
| Directives | noindex, nofollow, X-Robots-Tag |
| Canonicals | Canonical ke halaman lain, canonical hilang |
| Sitemaps (kalau mode crawl sitemap aktif) | URL di sitemap yang tidak ditemukan crawl (orphan), URL non-indexable di sitemap |
| Hreflang | Kalau situs multibahasa |
| Bulk Export → Links → All Inlinks | Internal link, orphan |
| Content → Near Duplicates (kalau diaktifkan) | Konten duplikat atau tipis |

Untuk situs berbasis JavaScript (Webflow dengan interaksi berat, SPA, Shopify theme tertentu), minta crawl dengan rendering JavaScript aktif, atau minimal bandingkan sampel lewat `browser-inspection.md` bagian render.

---

## 4. Akses HTTP langsung (curl)

Kalau sandbox mengizinkan akses jaringan, `curl` dari bash adalah cara tercepat untuk data mentah, dan mengatasi kegagalan `web_fetch` yang tercatat di P.R.O.B.E (robots.txt dan sitemap gagal dibaca).

```bash
# Status, redirect, dan header (termasuk X-Robots-Tag)
curl -sSIL -A "Mozilla/5.0 (compatible; SONAR-CORE audit)" https://domain.com/halaman

# Isi robots.txt dan sitemap
curl -sSL -A "Mozilla/5.0 (compatible; SONAR-CORE audit)" https://domain.com/robots.txt
curl -sSL --compressed -A "Mozilla/5.0 (compatible; SONAR-CORE audit)" https://domain.com/sitemap.xml
```

Aturan:
- **Jangan menyamar sebagai Googlebot** (jangan pakai user-agent Googlebot). Hasilnya bisa menyesatkan dan bisa melanggar kebijakan situs.
- Curl melihat HTML mentah, bukan hasil render JavaScript. Untuk render, pakai browser.
- Kalau curl kena 403, halaman challenge, atau proteksi bot, jangan coba mengakalinya. Pindah ke browser, atau minta export Screaming Frog.
- Beri jeda antar request (minimal 1 detik) dan batasi jumlahnya. Ini audit, bukan crawl massal.

Untuk crawl ringan seluruh sitemap (puluhan sampai beberapa ratus URL), curl dengan jeda 0,5–1 detik per URL layak dipakai sebagai pengganti sementara Screaming Frog untuk status, canonical, robots, title, meta, H1, dan jumlah kata HTML mentah. Proses latar belakang (`nohup ... &`) bisa terhenti saat satu pemanggilan bash selesai, jadi jalankan di depan dalam beberapa potongan dengan kemampuan melanjutkan (lewati URL yang sudah ada di file hasil).

Urutan akses yang disarankan untuk satu URL: **curl** (cepat, header lengkap) → **browser** (render, situs yang memblokir curl, GSC UI) → **web_fetch** (cadangan terakhir).

---

## 5. Format ternormalisasi

Semua jalur harus berakhir di tabel dengan kolom berikut sebelum dianalisis. Simpan sebagai CSV di folder kerja supaya bisa dihitung ulang dengan kode.

### `gsc_page_query`
| Kolom | Keterangan |
|---|---|
| `period_start`, `period_end` | Tanggal ISO |
| `page` | URL lengkap, dinormalisasi (lihat aturan di bawah) |
| `query` | Kosong kalau sumbernya tab Pages saja |
| `clicks`, `impressions` | Integer |
| `ctr` | Desimal 0–1, dihitung ulang dari clicks/impressions, bukan disalin dari sumber |
| `position` | Rata-rata posisi |
| `is_branded` | `true`/`false` dari `seo.brand_terms` (lihat `ctr.md`) |
| `source` | `windsor`, `csv`, `chrome` |

### `ga4_landing`
`period_start`, `period_end`, `page`, `channel`, `sessions`, `active_users`, `engagement_time_sec`, `key_events`, `source`.

### Aturan normalisasi URL
Huruf kecil untuk skema dan host, hapus fragmen `#...`, hapus parameter pelacakan (`utm_*`, `fbclid`, `gclid`), pertahankan parameter lain apa adanya (bisa jadi masalah teknis yang perlu terlihat), dan konsisten soal trailing slash sesuai yang dipakai situs. Catat setiap URL yang digabung karena normalisasi, jangan diam-diam.

### Rekonsiliasi angka
Total clicks dan impressions di tabel ternormalisasi harus dicocokkan dengan total di sumber. Kalau berbeda (data query dianonimkan GSC sering membuat jumlah per query lebih kecil dari total halaman), sebutkan selisihnya di laporan.

---

## 6. Aturan periode

- Default **90 hari**, dibandingkan dengan **90 hari sebelumnya**.
- Akhiri periode beberapa hari sebelum hari ini, karena data GSC hari-hari terakhir belum final. Tulis tanggal awal dan akhir persis di setiap laporan.
- Halaman yang terbit kurang dari 4 minggu sebelum akhir periode tidak dinilai di tahap Rank, Click, dan Convert (aturan lama M.E.T.A: data GSC butuh 3–4 minggu). Tandai sebagai `terlalu baru`.
- GSC menyimpan data sekitar 16 bulan. Untuk tren tahunan, tarik lebih awal sebelum data lama hilang.
