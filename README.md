# GitHub Contributions Generator

Skrip ini adalah sebuah alat untuk men-*generate* riwayat commit GitHub (kotak-kotak hijau) dengan tampilan Web UI sederhana agar Anda dapat menyesuaikan hari, tanggal, dan jumlah *commit* yang Anda inginkan.

## Persyaratan
1. Pastikan Anda sudah menginstal **Python 3**.
2. Pastikan file ini berada dalam direktori yang merupakan **Git Repository** (sudah diinisialisasi dengan `git init`).
3. Pastikan email Git yang terkonfigurasi di komputer Anda sesuai dengan email di akun GitHub Anda:
   ```bash
   git config user.email
   ```

## Cara Menjalankan

1. Buka Terminal (atau Command Prompt).
2. Arahkan *directory* (folder) Anda ke lokasi file `generate_contributions.py` ini.
3. Jalankan perintah berikut:
   ```bash
   python3 generate_contributions.py
   ```
4. Jika berhasil dijalankan, sebuah server lokal akan menyala dan browser Anda akan **otomatis terbuka** (mengarah ke http://localhost:8080).

## Cara Menggunakan (Web UI)

1. **Step 1: Konfigurasi Tanggal dan Range**
   - Secara bawaan, *Start Date* dan *End Date* akan otomatis disetel ke tanggal hari ini. Anda bisa mengubahnya sesuka hati.
   - Atur batas *Minimal* dan *Maksimal* jumlah commit per harinya.
   - Klik **"Preview Rencana Commit"**.

2. **Step 2: Meninjau dan Mengedit Rencana Commit**
   - Sebuah tabel akan muncul memaparkan rincian commit yang sudah digenerate secara acak untuk setiap harinya.
   - Anda bisa **mengubah** angka jumlah commit secara manual pada kolom yang tersedia.
   - Anda juga bisa **menghapus** tanggal tertentu (jika pada hari itu Anda ingin dikosongkan) dengan menekan tombol **"Hapus"**.

3. **Step 3: Eksekusi**
   - Jika rencana sudah final, tekan tombol biru **"Eksekusi Commits Sekarang!"**.
   - Tunggu beberapa saat karena Git harus menulis memori riwayat *commit* ke dalam file `contributions.txt` secara *looping* di balakang layar.
   - Jika sudah ada tulisan **Berhasil**, Anda dapat kembali ke Terminal dan menekan `Ctrl+C` untuk mematikan Web UI.

## Langkah Terakhir (Push ke GitHub)
Jika eksekusi di lokal sudah selesai, hal terakhir yang perlu Anda lakukan adalah melempar (Push) log commit tersebut ke repositori jarak jauh (GitHub) agar muncul pada grafik profil Anda:

```bash
git push -f origin main
```
> **Catatan:** Ganti kata `main` dengan `master` jika *branch* utama Anda menggunakan *master*. Pembaruan grafik GitHub biasanya memakan waktu beberapa detik/menit untuk muncul selengkapnya.
