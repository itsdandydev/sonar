# Modul: Handoff dan Penamaan

Aturan serah-terima antar project S.O.N.A.R, supaya output satu project bisa langsung dipakai project lain tanpa copy-paste ulang atau riset ulang.

## 1. Kode project

| Kode | Project | Eks |
|---|---|---|
| `CORE` | Router diagnostik dan context profile | C.L.U.S.T.E.R (diagnosa), core-context-profile |
| `DSC` | Discovery | P.I.N.G + S.P.E.A.R |
| `STR` | Strategy | S.O.N.A.R v2.1 |
| `PRD` | Production | N.E.X.U.S (claude.ai) / plugin `nexus` |
| `OPT` | Optimization | M.E.T.A + S.C.O.U.T + aksi C.L.U.S.T.E.R |
| `TEC` | Technical | P.R.O.B.E |

## 2. Nama file

```
[Klien]_[KODE]_[Artefak]_[YYYY-MM-DD].[ext]
```

- `Klien`: PascalCase tanpa spasi, sama di semua file klien itu. Contoh: `PamanPack`, `Gwenchana`, `ElectGO-ID`, `ElectGO-SG` (pakai tanda hubung untuk pasar).
- `Artefak`: PascalCase singkat. Contoh di bawah.
- Tanggal = tanggal file dibuat.

| Contoh | Isi |
|---|---|
| `Gwenchana_CORE_Diagnosis_2026-10-20.xlsx` | Hasil router |
| `Gwenchana_CORE_ContextProfile_2026-10-20.json` | Context profile (nama lama `[Klien]_context_profile.json` tetap dibaca) |
| `PamanPack_DSC_KeywordBank_2026-10-20.xlsx` | Keyword bank |
| `PamanPack_STR_Strategy_2026-10-20.xlsx` | Deliverable Strategy |
| `Precicon_OPT_SnippetQueue_2026-10-20.xlsx` | Antrean title/meta |
| `PamanPack_OPT_PageCopy-kardus-sepatu_2026-10-20.xlsx` | Copy satu halaman (slug halaman di artefak) |
| `SeloProperties_TEC_Tasklist_2026-10-20.xlsx` | Tasklist teknis |
| `SeloProperties_TEC_WRD_2026-10-20.docx` | Website Requirement Document |
| `Gwenchana_DSC-to-PRD_Handoff_2026-10-20.md` | Catatan serah-terima |

Pengecualian: file yang dibuat plugin `nexus` mengikuti konvensi NEXUS sendiri (`nexus-output/<NXS-code>_<slug>/`). Catat kode NXS di handoff supaya bisa dilacak.

## 3. Template catatan serah-terima

Nama: `[Klien]_[DARI]-to-[KE]_Handoff_[YYYY-MM-DD].md`

```markdown
# Handoff: [DARI] → [KE]
Klien: [nama] | Domain: [domain] | Tanggal: [YYYY-MM-DD]
Versi C.O.R.E: [x.y] | Context profile: [nama file + versi]

## Yang diserahkan
[file terlampir + ringkasan satu kalimat per file]

## Item untuk dikerjakan
| # | Item | Tahap funnel | Prioritas | Bukti/sumber | Keyakinan |
|---|---|---|---|---|---|

## Data yang sudah ditarik (jangan ditarik ulang)
[report SEMrush/GSC beserta tanggal, database, dan lokasi datanya. Berlaku 30 hari]

## Keputusan yang berlaku
[entri dari seo.decisions yang relevan, plus keputusan baru di sesi ini]

## Item terbuka
[pertanyaan untuk klien/user, data yang belum ada]

## Langkah berikutnya di project tujuan
[satu sampai tiga langkah konkret]
```

Keputusan baru di bagian "Keputusan yang berlaku" juga harus ditambahkan ke `seo.decisions` di context profile. Handoff hanya membawa pesan; context profile yang menyimpannya.

## 4. Format keyword bank standar

Discovery memakai satu format: template sheet Keywords dari S.P.E.A.R v1.2 (18 kolom, header 3 baris), karena itu yang sudah dipakai tim content. Kolom: No, Month - Year, Keywords, Volume, Judul Artikel, Lang, Notes, Notes from Clients, Google Docs, URL, Date Created, PIC, Review, Notes, (pemisah kosong), Info, URL, Date Published.

Notes wajib tiga komponen:
```
Edukasi: [apa yang ingin dipelajari pembaca berdasarkan intent SERP]
Komersial: [angle yang menghubungkan ke produk/jasa klien]
CTA: [satu CTA spesifik]
```

Format 11 kolom P.I.N.G dan Master Cluster S.O.N.A.R tidak dipakai lagi untuk keyword bank. Strategy boleh punya sheet analisis sendiri, tapi daftar artikel yang diserahkan ke Production tetap memakai format ini.

## 5. Kontrak ke Production (NEXUS)

Plugin `nexus` memulai artikel lewat `/research` (keyword + pasar) dan mengonfirmasi beberapa hal di `/outline`. Supaya tidak ditanya ulang, handoff ke Production menyertakan per artikel:

| Field | Untuk tahap NEXUS |
|---|---|
| Keyword utama, pasar (negara + bahasa) | `/research` |
| Judul usulan, Notes (Edukasi/Komersial/CTA), keyword pendukung | `/improve`, `/outline` |
| Domain untuk internal link + daftar URL kandidat | `/outline` |
| Voice: `brand` atau `third-party` | `/outline` |
| FAQ delivery: `body` atau `metabox` | `/outline` |
| Tujuan CTA dan label tombol (dari context profile) | `/convert` |
| Klaim yang boleh dipakai dan yang dilarang | `/firstdraft`, `/convert` |
| YMYL atau bukan | Verifikasi fakta di `/finaldraft` |

Setelah NEXUS memberi kode `NXS-...`, catat kode itu di keyword bank (kolom Info) supaya artikel bisa dilacak dari Discovery sampai terbit.

## 6. Kembali ke router

Halaman yang sudah terbit masuk ke diagnosa router pada siklus berikutnya (minimal 4 minggu setelah terbit). Dari situ, temuan Click dan Convert masuk ke Optimization. Ini yang menutup loop: Discovery → Production → terbit → router → Optimization.
