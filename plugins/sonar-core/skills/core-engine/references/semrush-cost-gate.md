# Modul: Biaya dan Gate SEMrush

Satu model biaya dan satu protokol gate untuk semua project. Menggantikan tiga referensi lama yang saling berbeda: `SEMRUSH_API_COST_KNOWLEDGE (1).md` (P.I.N.G, S.O.N.A.R), `SEMRUSH_API_COSTS_UNIVERSAL.md` (C.L.U.S.T.E.R, masih berisi placeholder `[ISI]`), dan angka inline M.E.T.A.

## 1. Kenapa model lama meleset

Referensi lama menulis biaya sebagai **rata-rata per call** (misalnya `phrase_this` ~57 per call), hasil rata-rata 428 call di Maret 2026 dengan jumlah baris yang berbeda-beda. Itu bukan tarif. Akibatnya estimasi meleset ke dua arah:

- P.I.N.G Gwenchana (2 Okt 2026): estimasi ~6.583 unit, aktual 1.370. Terlalu tinggi karena `phrase_these` hanya menagih baris yang mengembalikan data.
- S.O.N.A.R Gwenchana Track A (3 Agu 2026): estimasi 460–760, aktual 1.360. Terlalu rendah karena domain dengan banyak backlink PBN mengembalikan lebih banyak baris.

## 2. Model biaya

```
estimasi = Σ (harga per baris × baris yang diperkirakan kembali)
batas_atas = Σ (harga per baris × display_limit atau jumlah keyword)
```

Gate selalu menampilkan **dua angka**: estimasi realistis dan batas atas. Sebutkan asumsi baris yang dipakai.

## 3. Tabel harga teramati

Status: `teramati` = cocok dengan pemakaian nyata yang tercatat; `referensi lama` = dari dokumen lama, belum dicocokkan dengan pemakaian nyata. Tabel ini diperbarui dari ledger (bagian 7). Harga yang belum teramati jangan dipakai sebagai angka pasti; tulis sebagai perkiraan.

| Report | Harga per baris | Status | Sumber |
|---|---|---|---|
| `phrase_these` | ~10 per keyword yang mengembalikan data | teramati | P.I.N.G Gwenchana 2 Okt; M.E.T.A Precicon (estimasi 36 × 10 = 360, aktual ~320); heuristik S.O.N.A.R |
| `phrase_this` | belum teramati per baris (rata-rata lama ~57 per call) | referensi lama | Knowledge file lama |
| `domain_organic` | belum teramati per baris (rata-rata lama ~356 per domain di limit default) | referensi lama | Knowledge file lama, gate P.I.N.G |
| `backlinks_overview` | 40 per baris | referensi lama | Knowledge file lama (dicatat sebagai cost/row 40) |
| `backlinks_refdomains`, `backlinks_anchors` | bervariasi, bisa melonjak di domain dengan profil backlink spam | teramati (lonjakan) | S.O.N.A.R Track A Gwenchana |
| `phrase_organic` dengan ERROR 50 (tidak ada data) | 0 | teramati | Chat S.O.N.A.R |
| Call gagal (400/500) | umumnya 0 | referensi lama | Best practice file biaya C.L.U.S.T.E.R |
| Call metadata (`get_report_schema`) | 0 | referensi lama | Knowledge file lama |

Kalau connector SEMrush menyediakan cara melihat saldo unit, catat saldo sebelum dan sesudah eksekusi. Itu cara paling pasti untuk mengisi tabel ini. Kalau tidak tersedia, pakai hitungan baris yang kembali.

## 4. Aturan hemat sebelum gate

Sebelum menyusun gate, cek dulu apakah datanya sudah ada:

1. **Pakai ulang data 30 hari terakhir.** Kalau keyword dan database yang sama sudah ditarik dalam 30 hari terakhir (ada di ledger, handoff file, atau keyword bank dari project lain), pakai data itu. Contoh pemborosan nyata: S.O.N.A.R Euromedica nyaris memvalidasi ulang 42 keyword yang sudah ditarik P.I.N.G.
2. **Batch.** Pakai `phrase_these` (keyword dipisah titik koma), jangan loop `phrase_this`.
3. **`display_limit` selalu eksplisit.** Mulai kecil (10) untuk screening, perbesar hanya untuk domain atau keyword utama.
4. **Satu database dulu.** Database kedua (misalnya US sebagai proxy untuk SG) hanya untuk subset tanpa data, dengan gate terpisah.
5. **Ekspansi (`phrase_related`, `phrase_fullsearch`, `phrase_questions`) hanya untuk seed yang sudah terbukti punya volume.**
6. Panggil `get_report_schema` untuk report yang belum pernah dipakai di sesi itu sebelum `execute_report`.

## 5. Protokol gate (wajib, tanpa pengecualian)

Sebelum **setiap** pemanggilan SEMrush yang bisa memakan unit:

```
🔒 SEMrush API Gate
Project : [Discovery / Strategy / Optimization / Technical]
Klien   : [nama] | Database: [id / sg / us ...]

| Report | Parameter | Baris diperkirakan | Batas atas | Unit realistis | Unit maksimal | Status harga |
|---|---|---|---|---|---|---|
| phrase_these | 24 keyword | ~15 berdata | 24 | ~150 | 240 | teramati |

Total: ~150 unit (maksimal 240)
Data yang dipakai ulang tanpa biaya: [daftar / "tidak ada"]

Ketik `lanjut` untuk eksekusi, atau `skip` untuk lewati.
```

Jawaban yang dianggap lanjut: `lanjut`, `yes`, `ya`, `ok`, `y`, `go`, `gas`, `proceed`.
Jawaban yang dianggap lewati: `skip`, `batal`, `no`, `n`, `lewati`, `tidak`.

Aturan:
1. **Tanpa jawaban lanjut yang eksplisit, tidak ada eksekusi.** Jangan menutup gate dengan "lanjut eksekusi" lalu langsung jalan. Pelanggaran ini pernah terjadi dua kali (S.O.N.A.R 3 Agu, M.E.T.A Precicon).
2. User pindah topik atau memberi tugas baru tanpa menjawab gate: anggap **skip**. Kalau tugas baru itu butuh SEMrush, tampilkan gate baru.
3. Skip: tandai item terkait `[SKIPPED - tanpa data SEMrush]` dan lanjut dengan data yang ada.
4. Satu gate berlaku untuk satu eksekusi yang tertulis di tabel. Menambah report atau keyword di luar tabel butuh gate baru.
5. Unit habis atau akses terblokir: berhenti, laporkan ke user (sertakan tautan upgrade yang diberikan oleh pesan error SEMrush kalau ada), dan jangan diam-diam pindah ke tool lain. Tawarkan alternatif (Ubersuggest, data yang sudah ada, atau tunda) dan tunggu pilihan user.
6. ERROR 50 (tidak ada data): catat sebagai "tidak ada data", jangan di-retry tanpa gate baru. Untuk `phrase_organic`, ERROR 50 bisa berarti peluang (SERP kosong), bukan kegagalan.

## 6. Setelah eksekusi

Laporkan ke user dalam satu baris: estimasi vs aktual. Contoh: "Estimasi ~150 unit, aktual 140 unit (14 dari 24 keyword berdata)." Lalu catat ke ledger.

## 7. Ledger biaya

File: `data/semrush_cost_ledger.csv` di repo S.O.N.A.R. Satu baris per eksekusi report.

| Kolom | Isi |
|---|---|
| `date` | Tanggal ISO |
| `project` | `discovery`, `strategy`, `optimization`, `technical` |
| `client` | Nama klien |
| `report` | Nama report |
| `database` | `id`, `sg`, `us`, ... |
| `params` | Ringkas: jumlah keyword/domain, `display_limit` |
| `rows_requested` | Jumlah keyword atau batas baris yang diminta |
| `rows_returned` | Baris yang benar-benar kembali |
| `units_estimated` | Angka realistis di gate |
| `units_actual` | Dari saldo sebelum-sesudah, atau hitungan baris × harga teramati |
| `units_actual_method` | `saldo` atau `hitung_baris` |
| `notes` | Anomali (ERROR 50, lonjakan, retry) |

Di claude.ai, Claude tidak bisa menulis langsung ke repo. Tampilkan baris ledger yang siap ditempel di akhir sesi, atau simpan sebagai file CSV di outputs supaya user menambahkannya ke repo. Di Claude Code yang membuka repo, tambahkan langsung ke file.

Setiap bulan (atau setelah 50 baris baru), hitung ulang harga per baris per report dari ledger, lalu perbarui tabel di bagian 3 dan catat di CHANGELOG.
