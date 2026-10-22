# Changelog

## 3.0.0-alpha.3 (S.O.N.A.R) / 2.0.0-alpha.3 (C.O.R.E) — 2026-10-22

### Ditambahkan
- Folder `commands/` di `sonar-core`: 15 command dari tabel Commands di SKILL.md sekarang jadi slash command beneran (`/sonar-core:core`, `/sonar-core:import`, `/sonar-core:diagnose`, `/sonar-core:gsc`, `/sonar-core:ctr`, `/sonar-core:inspect`, `/sonar-core:gate`, `/sonar-core:ledger`, `/sonar-core:handoff`, dan command context profile `validate`, `export`, `update`, `status`, `upgrade`, `reset`), sama seperti plugin NEXUS dan Wagyu. Sebelumnya hanya muncul satu entri (`sonar-core:core`).
- Setiap command hanya memanggil skill `core` dan menunjuk modul yang tepat; aturannya tetap ditulis sekali di `references/`.

## 3.0.0-alpha.2 (S.O.N.A.R) / 2.0.0-alpha.2 (C.O.R.E) — 2026-10-16

Hasil uji pertama router di situs nyata (situs agency sendiri), mode Ringan+: sitemap dan crawl HTML mentah lewat curl, GSC performa lewat Windsor, GSC Page Indexing lewat Claude in Chrome.

### Terbukti jalan
- Resep head tag dan render di modul browser berjalan di Chrome pada situs nyata.
- curl dari sandbox membaca robots.txt, sitemap, dan 160 halaman tanpa hambatan; menutup masalah web_fetch yang dulu dialami P.R.O.B.E.
- GSC UI terbaca lewat sesi Chrome yang sudah login, termasuk drilldown dan contoh URL. Ini menutup celah Windsor yang tidak punya data indexing.
- Aturan "hulu dulu" dan "absen dari GSC bukan berarti tidak ter-crawl" langsung mengubah kesimpulan: masalah utama ada di Index, bukan Click.

### Diubah
- Router: nama alasan GSC disesuaikan dengan UI, ditambah aturan membaca tampilan "All known pages" vs "All submitted pages" dan arti kolom Validation; aturan saat status index per URL belum tersedia.
- Browser: langkah GSC UI yang teruji.
- Sumber data: cara memindahkan data Windsor ke file supaya bisa dihitung dengan kode, rekonsiliasi query yang dianonimkan, dan crawl ringan lewat curl dalam potongan.
- Pemilik repo: Dandy. Usulan perubahan untuk NEXUS disetujui Lawrence Philemon.

### Masih terbuka
- Ekspor status index per URL (butuh izin download atau ekspor oleh user) belum diuji.
- Tahap Convert (GA4 dan network tracking) belum diuji.
- Script bersama dan template masih belum ada.

## 3.0.0-alpha.1 (S.O.N.A.R) / 2.0.0-alpha.1 (C.O.R.E) — 2026-10-16

Struktur awal S.O.N.A.R v3 dan C.O.R.E v2.0.

### Ditambahkan
- Marketplace `sonar` berisi plugin `sonar-core` dan entri `nexus` yang menunjuk ke `lawzphilemon/nexus-plugin`.
- Skill `core` dengan modul: router diagnostik, sumber data, browser inspection, CTR, biaya & gate SEMrush, aturan bukti, handoff & penamaan.
- Blok `seo` di context profile (aditif, file v1.1 tetap valid), termasuk `claims` dan `decisions`.
- Ledger biaya SEMrush dengan tiga baris awal dari handover (agregat sesi, bukan per report).
- Spesifikasi lima project dan peta migrasi di `projects/README.md`.

### Diubah
- Alur context profile C.O.R.E v1.1 (Full/Quick Mode) dipindah ke `references/context/`, label readiness mengikuti nama project baru.
- Definisi CTR disatukan: hanya posisi 1–10,5, query non-branded, rasio terhadap benchmark, minimal 100 impresi.
- Model biaya SEMrush: harga per baris × baris yang kembali, gate menampilkan estimasi realistis dan batas atas.

### Belum
- Script bersama (`normalize_gsc.py`, `build_url_master.py`, `classify_funnel.py`, `classify_ctr.py`, `estimate_semrush.py`).
- Template Excel/Word (keyword bank, snippet queue, page copy, tasklist, WRD) di `templates/`.
- Instruksi project per folder di `projects/`.
- Snippet JavaScript di modul browser baru dicek sintaksnya, belum diuji di Claude in Chrome pada situs nyata.
- Ambang angka dan tabel harga SEMrush belum diuji di klien.
