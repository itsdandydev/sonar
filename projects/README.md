# Lima project S.O.N.A.R v3

Status: spesifikasi awal. Instruksi project dan knowledge file per project akan ditulis di folder masing-masing (`projects/discovery/`, dst.) saat migrasi project itu dimulai. Semua project membaca skill `core` untuk context profile, data, CTR, SEMrush, bukti, dan handoff, dan tidak menyimpan versi sendiri dari aturan itu.

Urutan migrasi yang disepakati: C.O.R.E → uji router di Gwenchana (hasil pertama kemungkinan besar ke Technical: bug canonical) → Discovery → Optimization → Production → Strategy. Project lama diarsipkan setelah project barunya lulus uji dengan satu klien nyata, tidak dihapus.

---

## Discovery (eks P.I.N.G + S.P.E.A.R)

**Tugas:** mengubah peluang keyword menjadi keyword bank yang siap ditulis.

**Pintu masuk:** (A) dari nol lewat gap hunt SEMrush; (B) list keyword dari klien; (C) query tanpa halaman dari router.

**Alur:** context profile → gap hunt dengan gate (dilewati di pintu B) → filter niche-fit → clustering berbasis SERP lewat browser (aturan URL lengkap, ≥ 4/5 URL sama untuk gabung) → klasifikasi tipe SERP → judul + Notes Edukasi/Komersial/CTA → keyword bank format standar → handoff ke Production atau Strategy.

**Yang berubah dari versi lama:**
- Judul hanya dibuat sekali, di tahap SERP. Tahap gap hunt tidak lagi menulis judul dan deskripsi (dulu ditulis ulang S.P.E.A.R).
- Tag yang lahir di chat P.I.N.G diresmikan: Expert Gap (volume 0, nilai editorial), US proxy, Early Mover, Defend & Push.
- Nama report dan biaya ikut modul SEMrush C.O.R.E (`phrase_these`, harga per baris).
- Nama file keyword bank ikut konvensi baru: `[Klien]_DSC_KeywordBank_[YYYY-MM-DD].xlsx`.

## Strategy (eks S.O.N.A.R v2.1)

**Tugas:** rencana SEO menyeluruh untuk klien baru atau perencanaan kuartalan/tahunan.

**Dipertahankan:** 6 pain pillar + Core Tension Statement, SERP reality check (5 kategori kompetitor), link intelligence (Track A audit, Track B peluang, deteksi toxic, disavow), topical authority map, Content Moat, Two-Track Execution, sprint plan 3 bulan.

**Yang berubah:**
- Fase 0–1 onboarding memakai context profile.
- Fase 2–3 (seed + validasi SEMrush) menjadi "impor keyword bank Discovery, validasi hanya KD/CPC yang belum ada".
- Fase 3.5 (GSC) dipindah ke router C.O.R.E. Track A (CTR Recovery) memakai daftar merah dari modul CTR.
- Instruksi yang terpotong dan 12 konflik di handover diselesaikan saat penulisan ulang.

## Production (N.E.X.U.S, plugin `nexus`)

**Sumber:** repo `lawzphilemon/nexus-plugin` (v2.5.0 per 14 Okt 2026), ditarik lewat marketplace repo ini.

Catatan: repo NEXUS sudah jauh lebih maju dari project N.E.X.U.S di claude.ai yang dibahas di handover. Beberapa masalah di handover sudah selesai di repo (file command lengkap, riset SERP live lewat browser, kode proyek `NXS-...`, `/resume`, `/constructive-self-criticize`, mode FAQ delivery, voice). Project claude.ai lama sebaiknya diarsipkan atau disinkronkan ke repo.

**Kontrak masuk:** lihat `handoff.md` bagian 5 di skill `core`.

**Usulan untuk repo NEXUS (disetujui Lawrence Philemon, 2026-10-16; dikerjakan di repo NEXUS):** membaca context profile C.O.R.E untuk klaim, voice, dan tujuan CTA; menyamakan snippet browser dengan modul browser C.O.R.E; verifikasi statistik YMYL dengan membuka sumber.

## Optimization (eks M.E.T.A + S.C.O.U.T + aksi C.L.U.S.T.E.R)

**Tugas:** memperbaiki halaman yang sudah terbit, berdasarkan antrean dari router.

**Tiga mode:**
- **Snippet** (cara kerja M.E.T.A): title dan meta banyak halaman. Input: daftar merah/kuning modul CTR. Title ≤ 60 karakter, meta ≤ 155, dihitung dengan kode.
- **Page** (cara kerja S.C.O.U.T): rewrite penuh satu halaman dengan zone system SEO/Conversion/Hybrid, fan-out, dan skill `page-copy-architect` untuk struktur.
- **Refresh & Consolidate** (baru): konten tipis, duplikat, kanibalisasi, intent salah, peluang posisi 11–20. Rencana redirect diserahkan ke Technical untuk WRD.

**Yang berubah:** keyword mapping skala besar (seperti 458 halaman Precicon) dan audit teknis tidak lagi dikerjakan di sini tanpa alasan; keyword baru diminta ke Discovery, temuan teknis ke Technical.

## Technical (eks P.R.O.B.E)

**Tugas:** audit teknis mendalam dan dokumen untuk developer.

**Dipertahankan:** fase Platform, Render & Crawlability, On-Page, Build & Performance, E-E-A-T; status Ok / Ok with Revision / Need Revision / Need Confirmation; prioritas P0–P2; deliverable Tasklist (Excel) + WRD (Word).

**Yang berubah:**
- Versi `.md` dan `.docx` (keduanya berlabel v1.0) digabung jadi satu.
- Pengecekan robots, sitemap, canonical, schema, render, tracking, PageSpeed, dan Rich Results memakai modul browser dan curl C.O.R.E.
- `/intelligence` = jalankan modul sumber data C.O.R.E.
- Deteksi title/meta bermasalah tetap di sini; penulisan ulang diserahkan ke Optimization.
- Item Need Confirmation masuk Tasklist, tidak masuk WRD (aturan bukti).

---

## Peta migrasi project lama

| Project lama | Status | Pindah ke |
|---|---|---|
| P.I.N.G | Dilebur | Discovery (gap hunt) |
| S.P.E.A.R | Dilebur | Discovery (clustering SERP, judul, keyword bank) |
| S.O.N.A.R v2.1 | Diganti nama | Strategy |
| C.L.U.S.T.E.R | Dilebur | Router C.O.R.E (diagnosa, Trust Score) + Optimization (aksi) |
| M.E.T.A | Dilebur | Optimization mode Snippet |
| S.C.O.U.T | Dilebur | Optimization mode Page |
| N.E.X.U.S (claude.ai) | Diganti repo | Production = plugin `nexus` |
| P.R.O.B.E | Diganti nama | Technical |
| skill `core-context-profile` | Diganti | Skill `core` (C.O.R.E v2.0) |
