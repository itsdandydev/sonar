# S.O.N.A.R v3

**S**ignal · **O**bserve · **N**avigate · **A**nalyze · **R**ank

Ekosistem SEO/GEO untuk tim content dan SEO. Repo ini berisi fondasi bersama (C.O.R.E) dan menarik plugin produksi artikel (NEXUS) dari repo-nya sendiri.

```
                  C.O.R.E (fondasi bersama, plugin sonar-core)
   context profile · router diagnostik · sumber data · browser
   CTR · biaya & gate SEMrush · aturan bukti · handoff & penamaan

  PINTU DIAGNOSA (website sudah jalan)      PINTU GROWTH (konten baru)
          router diagnostik                         Discovery
                 │                                      │
   ┌─────────┬───┴────────┬──────────┐                  ▼
Technical  Optimization  Strategy  Discovery ──►  Production (NEXUS)
```

## Isi repo

| Path | Isi |
|---|---|
| `.claude-plugin/marketplace.json` | Marketplace S.O.N.A.R: plugin `sonar-core` (repo ini) dan `nexus` (dari `lawzphilemon/nexus-plugin`) |
| `plugins/sonar-core/` | Plugin C.O.R.E v2.0 berisi skill `core` dan 15 slash command (`/sonar-core:core`, `/sonar-core:diagnose`, dst.) |
| `data/semrush_cost_ledger.csv` | Log biaya SEMrush aktual, sumber harga per baris |
| `projects/` | Spesifikasi lima project dan peta migrasi dari project lama |

## Install (Claude Code)

```text
/plugin marketplace add itsdandydev/sonar
/plugin install sonar-core@sonar
/plugin install nexus@sonar
```

Menambahkan marketplace ini sekaligus mendaftarkan NEXUS, karena entri `nexus` di `marketplace.json` menunjuk ke repo GitHub NEXUS. NEXUS tetap dikembangkan di repo-nya sendiri.

Untuk claude.ai, cara memasang skill dari repo ini tergantung pengaturan workspace (plugin organisasi atau upload skill). Isi skill-nya sama.

## Sebelum memasang: hindari skill ganda

- `sonar-core` menggantikan skill `core-context-profile` (C.O.R.E v1.1). Copot yang lama supaya tidak ada dua skill yang sama-sama terpicu untuk context profile. File `context_profile.json` lama tetap terbaca.
- Plugin `nexus` membawa skill `humanizer-id` dan `humanizer-en` versi NEXUS (34 dan 32 pola). Kalau workspace sudah punya skill dengan nama sama dari sumber lain, copot salah satunya supaya tidak bentrok.

## Lima project

| Project | Alias lama | Spesifikasi |
|---|---|---|
| Discovery | P.I.N.G + S.P.E.A.R | `projects/README.md` |
| Strategy | S.O.N.A.R v2.1 | `projects/README.md` |
| Production | N.E.X.U.S | Repo `lawzphilemon/nexus-plugin` |
| Optimization | M.E.T.A + S.C.O.U.T + aksi C.L.U.S.T.E.R | `projects/README.md` |
| Technical | P.R.O.B.E | `projects/README.md` |

## Cara memperbarui aturan

1. Ubah file di `plugins/sonar-core/skills/core/references/`, bukan di project.
2. Catat perubahannya di `CHANGELOG.md` dan naikkan versi di `plugin.json` dan `marketplace.json`.
3. Ambang angka (CTR, minimal impresi, 30% site-level) dan tabel harga SEMrush hanya diubah berdasarkan data: hasil uji klien atau ledger.

## Kredit

- P.I.N.G, S.P.E.A.R, M.E.T.A: tercatat author Dandy. C.L.U.S.T.E.R menyebut dirinya bagian dari "Dandy Pradana AI Marketing System". Author S.O.N.A.R v2.1, P.R.O.B.E, S.C.O.U.T, dan C.O.R.E v1.1 tidak tercatat di handover: [isi].
- NEXUS Content Pipeline: Lawrence Philemon.
- Pemilik repo: Dandy.
