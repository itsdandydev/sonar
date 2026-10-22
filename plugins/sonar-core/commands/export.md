---
name: export
description: Generate file context profile JSON dan ringkasan .md klien
argument-hint: ""
---

# C.O.R.E — /export

Argumen: $ARGUMENTS

1. Panggil skill `sonar-core:core` dulu, lalu baca modul `references/context/output-schema.md` sebelum mulai. Aturan di skill itu berlaku penuh.
2. Generate `[Klien]_CORE_ContextProfile_[YYYY-MM-DD].json` dan ringkasan `.md` sebagai file, lalu serahkan ke user. Jangan generate kalau field wajib Full Mode belum terisi.
