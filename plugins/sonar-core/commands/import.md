---
name: import
description: Buat context profile Quick Mode B1 langsung dari website klien
argument-hint: "[url website klien]"
---

# C.O.R.E — /import

Argumen: $ARGUMENTS

1. Panggil skill `sonar-core:core` dulu, lalu baca modul `references/context/quick-mode.md` sebelum mulai. Aturan di skill itu berlaku penuh.
2. Jalankan Quick Mode B1: fetch website di argumen, isi field dari isi situs, beri awalan [INFERRED] pada field tebakan.
