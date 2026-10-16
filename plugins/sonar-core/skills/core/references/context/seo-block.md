# Blok `seo` di context_profile.json

Blok ini menggantikan enam intake terpisah yang dulu ada di P.I.N.G (Fase 0B), S.O.N.A.R (Fase 0–1), S.P.E.A.R (niche-fit), C.L.U.S.T.E.R (Step 0.5), P.R.O.B.E (Fase 0), dan S.C.O.U.T (brand voice). Isi sekali, pakai di semua project. Project yang menemukan blok ini sudah terisi **tidak boleh bertanya ulang**; cukup tampilkan ringkasannya dan tanya apakah ada yang berubah.

## Field dan cara mengisinya

| Field | Isi | Cara mengisi |
|---|---|---|
| `domains.primary` | Domain utama tanpa protokol, contoh `pamanpack.co.id` | Tanya. Cek versi www vs non-www dan http vs https lewat curl (lihat `../data-sources.md`) |
| `domains.others` | Subdomain, domain negara lain, domain lama yang di-redirect | Tanya, lalu cek redirect-nya |
| `markets[]` | Satu baris per pasar: negara, bahasa, database SEMrush (huruf kecil: `id`, `sg`, `us`), parameter SERP `gl`/`hl` | Tanya. Default database = negara pasar, **bukan** `sg` (bias lama C.L.U.S.T.E.R) |
| `brand_terms[]` | Semua cara orang menulis nama brand, termasuk salah ketik umum dan nama produk unggulan yang bersifat navigasional | Tanya, lalu lengkapi dari query GSC yang jelas branded. Dipakai modul CTR untuk memisahkan query branded |
| `cms` | WordPress, Webflow, Shopify, Shopline, custom, dll. | Deteksi dari HTML (meta generator, pola path) lalu konfirmasi |
| `page_types[]` | Jenis halaman + pola URL, contoh `{"type":"product","url_pattern":"/produk/*"}` | Susun dari sitemap, konfirmasi ke user. Dipakai router untuk aturan site-level vs page-level |
| `niche_fit` | Topik yang bisa dimenangkan dan yang tidak (contoh: supplier industri tidak mengejar query gejala kesehatan) | Tanya. Ini aturan "niche-fit di atas volume" dari S.P.E.A.R v1.2 |
| `competitors[]` | Domain kompetitor. `kind`: `business` (pesaing bisnis), `search` (pesaing di SERP walau bukan pesaing bisnis), `both` | Tanya untuk `business`. Isi `search` dari hasil cek SERP |
| `register` | Formal ("Anda"), semi-formal, atau kasual ("kamu"/"lo-gue") | Ambil dari tone di blok brand. Satu nilai per klien supaya tidak berganti antar halaman |
| `access` | Status akses tiap sumber data dan jalurnya | Tanya. `status`: `connected`, `export_only`, `requested`, `none` |
| `claims.approved[]` | Klaim yang boleh dipakai beserta sumbernya (contoh: waktu produksi, sertifikasi, garansi, status distributor resmi) | Hanya dari user/klien atau dokumen resmi klien. Jangan diisi dari tebakan |
| `claims.forbidden[]` | Klaim yang dilarang dan alasannya | Tanya. Contoh nyata: arahan ElectGO "jangan serang brand China" |
| `exclusions` | Topik di luar scope dan lokasi daftar konten existing | Tanya |
| `decisions[]` | Log keputusan klien yang berlaku lintas project | Tambah setiap kali ada keputusan baru. Jangan hapus entri lama; kalau keputusan berubah, tambah entri baru yang menyebut entri lama |

## Kenapa `claims` dan `decisions` wajib

Dua masalah nyata dari handover lama yang menjadi alasannya:

- **Klaim bertabrakan.** Waktu produksi PamanPack tertulis 7 hari, 1 hari kerja, dan 1–3 hari kerja di tiga run S.C.O.U.T. Kalau klaim hanya boleh diambil dari `claims.approved`, tabrakan seperti itu tidak bisa terjadi.
- **Keputusan hilang di satu project.** P.I.N.G mencatat anime licensing dikeluarkan dari scope Gwenchana, sementara S.O.N.A.R menjadikannya content moat. Keputusan yang hanya tersimpan di memory satu project tidak terlihat oleh project lain.

Aturan pakai: sebelum menulis copy, judul, atau brief yang menyebut fakta tentang klien, cek `claims.approved`. Kalau klaimnya tidak ada di sana, tulis sebagai placeholder `[KLAIM PERLU KONFIRMASI: ...]`, bukan sebagai fakta. Sebelum merekomendasikan topik atau halaman, cek `decisions` dan `exclusions`.

## Contoh entri `decisions`

```json
{
  "date": "2026-10-16",
  "decision": "Anime licensing / IP anime dikeluarkan dari scope riset dan konten",
  "scope": "Discovery, Strategy, Production",
  "decided_by": "[isi: siapa yang memutuskan]",
  "source": "Memory project P.I.N.G (areas/gwenchana-seo.md); bertentangan dengan Content Moat di Excel S.O.N.A.R, perlu dikonfirmasi"
}
```

## Profil lama tanpa blok `seo`

File v1.1 tetap dipakai apa adanya. Saat pertama kali dipakai untuk kerja SEO, isi blok `seo` lewat pertanyaan singkat (domain, pasar, istilah brand, akses data dulu; sisanya boleh menyusul), lalu bump `_meta.version` minor dan `_meta.last_updated`.
