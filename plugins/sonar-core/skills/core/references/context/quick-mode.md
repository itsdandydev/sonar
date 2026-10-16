# Quick Mode — B1 (Website Fetch) & B2 (Pertanyaan Ringkas)

Dipakai kalau user pilih **B** di Fase 0, atau langsung kasih URL website (skip ke B1 tanpa perlu tanya ulang mode). Quick Mode menghasilkan JSON dan summary yang sama persis strukturnya dengan Full Mode (lihat `references/output-schema.md`) — bedanya cuma sumber datanya lebih ringkas, dan gap-nya diisi lewat inferensi.

## Rules Quick Mode

1. **Tidak ada konfirmasi per blok** — kumpulkan semua input dulu (dari fetch atau dari jawaban user), baru generate sekali jalan. Ini yang bikin Quick Mode jauh lebih cepat dari Full Mode.
2. Field yang tidak terisi → **diinfer**, bukan dikosongkan. Kosong itu lebih buruk untuk downstream framework daripada tebakan yang jelas ditandai sebagai tebakan.
3. Setelah generate, tampilkan summary dan tanya apakah ada yang perlu dikoreksi.
4. Kalau ada koreksi, update field spesifik itu saja — tidak perlu rebuild seluruh profile dari awal.

Kalau user belum pilih antara B1 dan B2, tanya:

> "Mau kasih info kliennya gimana?
>
> **B1 — Fetch dari website**
> Kasih domain, gue analisis sendiri — homepage, about, services, blog.
> Cocok kalau klien punya website lengkap.
>
> **B2 — Jawab pertanyaan singkat**
> Beberapa pertanyaan ringkas, langsung generate setelah selesai.
> Cocok kalau belum ada website atau website tidak lengkap.
>
> Pilih B1 atau B2."

---

## B1 — Website Fetch

Ini bagian yang jalan pakai tool beneran (`web_search`, `web_fetch`), bukan sekadar deskripsi ke user — itu yang membedakan skill ini dari versi manual sebelumnya.

**Langkah:**

1. Kalau user hanya kasih nama brand tanpa URL, jalankan `web_search` dulu untuk menemukan domain resminya. Kalau user langsung kasih URL, lanjut ke langkah 2.
2. `web_fetch` homepage. Baca hasilnya untuk menemukan link internal ke halaman `/about`, `/services` atau `/products`, dan `/blog` (atau nav yang setara di bahasa/struktur situs itu). **Jangan menebak path URL sendiri** (misal `domain.com/about-us` tanpa pernah melihat link itu) — `web_fetch` menolak URL yang belum pernah muncul di hasil pencarian/fetch sebelumnya, jadi selalu ambil link yang benar-benar ada di konten halaman.
3. `web_fetch` tiap halaman yang ditemukan di langkah 2. Untuk blog, cukup fetch 2–3 artikel terbaru — tujuannya membaca tone of voice dan tema konten, bukan mengarsip semua artikel.
4. Dari seluruh halaman yang sudah di-fetch, ekstrak:
   - Nama brand, industri, tagline
   - Daftar produk/jasa beserta deskripsinya
   - Tone of voice dari copy yang ada (formal/casual/warm/dll — simpulkan dari gaya tulisan asli, jangan menebak generic)
   - Klaim diferensiasi yang eksplisit disebutkan
   - Target audience yang disebutkan (langsung atau tersirat dari bahasa yang dipakai)
   - Pola CTA yang dipakai di situs

**Setelah ekstraksi, tampilkan hasil parsing:**

```
[C.O.R.E Quick — Website Parse Result]

Brand     : [nama yang terdeteksi]
Industry  : [industri]
Products  : [X] produk/jasa terdeteksi
Tone      : [deskripsi tone dari copy]
Gaps      : [field yang tidak bisa diisi dari website saja —
             biasanya pricing internal, purchase barriers, kompetitor, persona detail]

Ada info tambahan yang mau lo tambahkan sebelum gue generate?
(pricing internal, target audience, kompetitor, dll — atau ketik 'generate' untuk langsung lanjut)
```

5. Terima input tambahan kalau ada, lalu generate JSON + summary langsung (lihat aturan inferensi di bawah untuk gap yang tetap tidak terisi).

Kalau `web_fetch` gagal untuk sebagian halaman (misalnya blog tidak ada atau URL ditolak), tetap lanjut dengan halaman yang berhasil — jangan hentikan seluruh proses karena satu halaman gagal, cukup catat itu sebagai gap.

---

## B2 — Quick Questions

Kirim semua pertanyaan dalam **satu pesan sekaligus** — tidak perlu konfirmasi per blok seperti Full Mode:

```
[C.O.R.E Quick — Pertanyaan Ringkas]

1. IDENTITAS BRAND
   • Nama brand?
   • Industri?
   • Masalah apa yang diselesaikan brand ini?
   • Elevator pitch dalam 2 kalimat?

2. PRODUK & HARGA
   • Daftar produk/jasa + harga (satu per baris)?
   • Fitur atau bahan utama?
   • Apa yang membedakan dari kompetitor?

3. TARGET AUDIENCE
   • Siapa target utamanya? (usia, lokasi, pekerjaan, lifestyle)
   • Pain points utama mereka?
   • Keberatan yang sering muncul saat mau beli?

4. VOICE & CHANNEL
   • Tone of voice brand?
   • Platform utama yang digunakan?
   • Minimal 3 kompetitor?
   • Ada contoh copy yang bagus? (paste atau skip)

5. KONTEKS TAMBAHAN (opsional)
   • Visi jangka panjang?
   • Core values atau brand do's/don'ts?
   • Review pelanggan atau bukti sosial yang relevan?

Jawab semua yang bisa dijawab — field yang kosong akan gue infer.
Setelah lo kirim jawaban, gue langsung generate context profile.
```

Setelah user kirim jawaban → langsung generate JSON + summary, tanpa konfirmasi per blok.

---

## Aturan Inferensi (berlaku untuk B1 dan B2)

Kalau ada field yang tidak terisi dari fetch atau jawaban user, isi dengan inferensi berdasarkan:
- Industri dan tipe produk
- Target audience yang disebutkan (kalau ada)
- Competitive landscape yang umum diketahui untuk industri itu
- Best practice konten untuk industri tersebut

**Field hasil inferensi wajib diberi prefix `[INFERRED]`** di value-nya, plus alasan singkat kenapa itu masuk akal — supaya user bisa langsung menilai apakah tebakan itu perlu dikoreksi.

Contoh:
```json
"brand_archetype": "[INFERRED] The Caregiver — umum untuk brand skincare lokal yang positioning-nya hangat dan inklusif",
"north_star_metric": "[INFERRED] Monthly Active Buyers atau Repeat Purchase Rate"
```

Setelah JSON dan summary jadi, tampilkan:

```
[C.O.R.E Quick — Generated]

✅ context_profile.json siap
✅ summary.md siap

Field yang diinfer: [X] field
Field kosong      : [Y] field (ditandai [INFERRED])

Ada yang mau dikoreksi atau dilengkapi?
Ketik '/update [nama field]' untuk update field spesifik,
'/upgrade' untuk convert ke Full Mode dan isi ulang semua field [INFERRED] dengan data asli,
atau '/export' kalau sudah oke.
```
