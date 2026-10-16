# Full Mode — Wawancara 9 Blok

Dipakai kalau user pilih **A** di Fase 0. Tujuannya profil paling dalam dan akurat, jadi jangan buru-buru — kualitas jawaban di sini menentukan kualitas semua konten yang dibuat framework downstream nanti.

## Aturan wajib

1. Kerjakan fase berurutan — **jangan lompat blok**, karena beberapa blok belakangan (misalnya content strategy) butuh konteks dari blok awal (persona, produk) supaya suggestion-nya relevan, bukan generic.
2. **Konfirmasi tiap blok** sebelum lanjut ke blok berikutnya: "Ada yang mau dikoreksi sebelum gue lanjut?"
3. **Jangan generate JSON** sebelum semua field wajib terisi (lihat checklist validasi di bawah).
4. Kalau ada field yang user tidak bisa jawab sekarang, flag eksplisit ke user sebelum export — jangan diam-diam dikosongkan.

## Blok 1 — Identitas Brand

```
1. Nama brand / klien?
2. Industri? (satu kalimat deskriptif)
3. Kenapa brand ini ada? (masalah apa yang diselesaikan — bukan feature list)
4. Pitch brand ini dalam 2 kalimat ke orang asing di lift?
5. Brand archetype? (The Sage / The Caregiver / The Hero / lainnya —
   kalau user tidak tahu, minta dia deskripsikan karakternya dan bantu detect)
6. 3–6 kata yang mendeskripsikan kepribadian brand?
```

## Blok 2 — Produk & Jasa

Per produk/jasa, tanya:

```
1. Nama produk/jasa?
2. Harga atau model harga?
3. Fitur atau spesifikasi utama? (fakta, bukan marketing copy)
4. Mekanisme atau proses yang bikin cara kerjanya berbeda dari kompetitor?
5. Bukti konkret yang bisa dicantumkan? (sertifikasi, award, angka, data, testimonial)
```

Ulangi per produk — tanya "Ada produk lain?" sampai user ketik `selesai`.

Setelah semua produk terkumpul, tanya tambahan:

```
6. Model harga keseluruhan? (per unit / subscription / custom quote / lainnya)
7. Positioning harga? (budget / mid-range / premium / enterprise)
8. Apa yang bikin calon klien ragu untuk beli atau lanjut?
   (purchase barriers — dorong user jujur, ini penting untuk konten yang menangani objection)
```

## Blok 3 — Target Audience

Per persona (minimal 1, idealnya 2–3):

```
1. Nama persona? (internal label, bukan nama orang nyata)
2. Demographics? (jabatan, usia, ukuran perusahaan, lokasi)
3. Apa yang paling mereka value dalam pekerjaan atau hidup mereka?
4. Apa yang paling mereka takutkan atau ingin hindari?
5. Apa yang biasanya jadi trigger mereka untuk mulai cari solusi?
6. Satu kalimat messaging yang paling pas untuk persona ini?
```

Tanya "Ada persona lain?" sampai user ketik `selesai`.

## Blok 4 — Purchase Psychology

Kalau user tampak tidak familiar dengan istilah "awareness stage", jelaskan dulu dengan contoh konkret sebelum mulai tanya — jangan asumsikan dia paham framework ini.

Per stage (Unaware → Problem Aware → Solution Aware → Product Aware → Most Aware):

```
1. Mindset orang di stage ini seperti apa?
2. Konten apa yang paling cocok untuk menjangkau mereka di stage ini?
3. Satu kalimat messaging yang paling pas?
```

Tambahan khusus **Product Aware**:
```
4. Keberatan spesifik yang sering muncul di stage ini, dan bagaimana cara mengatasinya?
```

Tambahan khusus **Most Aware**:
```
4. Apa yang biasanya jadi conversion trigger di stage ini?
```

## Blok 5 — Voice, Kompetitor & Channel

```
1. Tone of voice brand? (atau deskripsikan bebas — bantu formulasikan jadi istilah yang jelas)
2. Platform utama yang digunakan untuk konten/marketing?
3. Minimal 3 kompetitor — nama dan kenapa mereka relevan sebagai benchmark?
4. Contoh copy existing yang bagus menurut user? (headline, tagline, caption, artikel —
   minta ditempel langsung atau kasih URL)
```

## Blok 6 — Visual Identity *(opsional)*

```
1. Style foto yang cocok untuk brand ini?
2. Style video?
3. Representasi model/talent yang ideal?
4. Visual do's — apa yang harus selalu ada?
5. Visual don'ts — apa yang harus dihindari?
```

Kalau user memilih skip blok ini, tetap lanjut — tandai `visual_identity` sebagai `[INCOMPLETE - visual identity not defined]` di JSON output nanti, jangan dikosongkan tanpa penjelasan.

## Blok 7 — Vision & Values

```
1. Long-term vision brand? (5–10 tahun ke depan)
2. Core values? (2–5 nilai — dorong user hindari kata korporat generik
   seperti "integritas" tanpa konteks; minta contoh konkret bagaimana nilai itu terlihat)
3. North star metric — satu angka yang paling mencerminkan
   apakah brand ini berhasil atau tidak?
4. Brand do's — 4–6 hal yang selalu dilakukan?
5. Brand don'ts — 4–6 hal yang tidak pernah dilakukan?
6. Crisis response approach — bagaimana brand merespons kalau ada masalah publik?
```

## Blok 8 — Tech & Channels

```
1. Sales channels? (website, marketplace, direct sales, partnership, dll)
2. Customer journey touchpoints — dari pertama tahu brand sampai akhirnya beli?
```

## Blok 9 — Content Strategy

Blok paling penting untuk Strategy dan Production (NEXUS) — jangan skip, karena ini yang langsung menentukan arah konten yang akan diproduksi.

```
1. Topik atau tema apa yang paling relevan untuk konten brand ini?
```

Sebelum user jawab, generate dulu 4–5 saran content pillar berdasarkan produk dan persona yang sudah terkumpul di blok sebelumnya, tampilkan, lalu minta user konfirmasi atau modifikasi — ini biasanya lebih cepat daripada minta user mikir dari nol.

```
2. CTA utama per level:
   - Soft CTA (engagement, awareness)
   - Medium CTA (consideration)
   - Hard CTA (conversion)

3. Hook formula yang biasa dipakai atau ingin dicoba?
   (kalau belum ada, generate berdasarkan pain points persona yang sudah terkumpul)
```

## Validasi sebelum export

Sebelum generate JSON, jalankan dan tampilkan checklist ini ke user:

```
[C.O.R.E — Pre-Export Validation]

Field Wajib:
✅/❌  general_overview (semua key terisi)
✅/❌  product_details.products (min 1)
✅/❌  ideal_customer_profiles (min 1 persona)
✅/❌  purchase_psychology (min 3 stages)
✅/❌  key_differentiators (min 3 poin)
✅/❌  content_strategy.primary_content_pillars (min 3 pillar)

Field Opsional:
⚠️/✅  visual_identity
⚠️/✅  brand_dos_and_donts

Ecosystem Flags:
✅/❌  Discovery ready (mode P.I.N.G terdeteksi dari industri + produk)
✅/❌  Strategy ready (content pillars + persona + purchase psychology terisi)
✅/❌  Production ready (tone + CTA + hook formulas terisi)
✅/❌  SEO block terisi (lihat seo-block.md: domain, market + database SEMrush, istilah brand, akses data)
```

Kalau ada field wajib yang ❌:

> "Ada [X] field wajib yang belum lengkap. Mau gue tanya sekarang, atau ada data yang mau lo tambahkan dulu?"

Jangan generate JSON kalau masih ada field wajib yang kosong — lanjutkan ke `references/output-schema.md` hanya setelah checklist ini semua ✅ (field opsional boleh ⚠️).
