---
name: update
description: Perbarui satu field context profile tanpa membangun ulang seluruh profil
argument-hint: "[nama field]"
---

# C.O.R.E — /update

Argumen: $ARGUMENTS

1. Panggil skill `sonar-core:core` dulu, lalu baca modul `references/context/output-schema.md` sebelum mulai. Aturan di skill itu berlaku penuh.
2. Baca context_profile.json yang ada dulu, perbarui field di argumen, naikkan versi profil dan `_meta.last_updated`.
