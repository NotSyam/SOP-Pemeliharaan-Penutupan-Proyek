# Panduan & Dokumentasi Pengembangan Modul E-Learning Interaktif SOP
## SOP to Interactive Microlearning Course Playbook (PT PP Persero Tbk)

Dokumen ini merangkum seluruh standar arsitektur, pedoman desain instruksional, panduan aksesibilitas WCAG 2.2 AA, serta catatan kritis perbaikan bug (*lessons learned*) yang dihasilkan selama pengembangan modul interaktif **PP/SOP/C1-050 REV-3: Masa Pemeliharaan & Penutupan Proyek Konstruksi dan EPC**.

---

## 1. Pedoman Visual & Design System

### 1.1 Palet Warna Korporat (Strict Blue & White - Zero Brown/Beige)
- **Aturan Mutlak**: Hindari penggunaan aksen warna cokelat, *beige*, atau *tan*. Gunakan identitas resmi korporat PT PP (Persero) Tbk.
- **Konfigurasi Tailwind CSS**:
  ```javascript
  colors: {
    brand: {
      primary: '#2B73BD',       // Primary Corporate Blue (Header, CTA, Active State)
      primaryHover: '#205c99',  // Hover State
      secondary: '#5A89B8',     // Steel Blue (Border sub-aktif, chip outline)
      secondaryLight: '#7eabd9',
      lightBlue: '#38BDF8',      // Sky Blue Accent (Highlight, Dark Mode Progress)
      iceBg: '#F0F4F7',          // Ice Canvas White (Latar belakang sejuk)
      surfaceLight: '#FFFFFF',   // Latar Kartu & Panel Terang
      borderLight: '#D9E3EA',
      darkBg: '#09111E',        // Deep Slate Dark Canvas (Mode Gelap)
      darkSurface: '#111C2E',   // Dark Surface Kartu
      darkBorder: '#1F2F4A',
      darkSubtle: '#16233B'
    }
  }
  ```

### 1.2 Adaptabilitas Logo Perusahaan
- **Penempatan**: Logo PT PP ditempatkan **hanya pada `#topHeader`**. Jangan menduplikasi logo di banner hero atau badan sertifikat agar antarmuka tetap bersih (*clean layout*).
- **Adaptasi Latar Belakang (Transparansi & Dark Mode)**:
  - Jangan membungkus elemen logo dengan kartu putih statis (`bg-white rounded-lg p-0.5`).
  - Gunakan gambar PNG transparan berkualitas tinggi (atau SVG).
  - Terapkan kelas utilitas:
    ```html
    <img src="assets/logo_pp.png" alt="PT PP" class="h-8 w-auto object-contain shrink-0 dark:brightness-0 dark:invert transition-all" />
    ```
  - Efek `dark:brightness-0 dark:invert` memastikan logo otomatis menjadi putih bersih saat header dalam mode gelap dan kembali ke biru korporat asli saat mode terang.

### 1.3 Prinsip "Less is More" & Kebersihan Teks
- Modul pelatihan adalah alat belajar, bukan salinan mentah buku pedoman tebal.
- Jangan tampilkan istilah pedagogis internal seperti **"C2"**, **"Kognitif C2"**, atau taksonomi Bloom kepada peserta akhir. Ganti dengan bahasa yang bersahabat: **"Uji Pemahaman"**, **"Soal Evaluasi"**, atau **"Studi Kasus SOP"**.
- Layout teks harus tertata rapi, hierarkis, dengan kontras tinggi (minimal `text-xs font-medium text-slate-600 dark:text-slate-300`, hindari teks `10px` pudar / `text-slate-400` di latar putih).

---

## 2. Arsitektur Interaktivitas & Performa Front-End

### 2.1 Pembaruan DOM In-Place vs. Re-render Penuh
- **Masalah**: Memanggil fungsi render ulang menyeluruh (misal `renderCurrentSlide()`) saat pengguna memilih filter dropdown atau mengubah status lokal akan:
  1. Menghapus dan membangun ulang seluruh isi `innerHTML`.
  2. Mereset posisi *scroll* horizontal/vertikal ke posisi 0.
  3. Menghilangkan fokus elemen (`document.activeElement`) dari dropdown.
  4. Memicu kembali animasi masuk CSS yang mengganggu kenyamanan belajar.
- **Solusi Baku (In-Place DOM Mutation)**:
  Tandai elemen anak dengan kelas khusus (misal `.flow-card-node`, `.role-badge`) dan data atribut (`data-actor`). Ubah kelas Tailwind secara langsung melalui JavaScript:
  ```javascript
  function filterSwimlaneRole(role) {
    state.selectedSwimlaneRole = role;
    const isFiltered = role && role !== 'Semua';
    document.querySelectorAll('.flow-card-node').forEach(node => {
      const actor = node.getAttribute('data-actor') || '';
      const matches = !isFiltered || actor.includes(role);
      node.classList.toggle('opacity-35', !matches);
      node.classList.toggle('ring-2', isFiltered && matches);
      node.classList.toggle('ring-brand-primary', isFiltered && matches);
      const badge = node.querySelector('.role-badge');
      if (badge) badge.classList.toggle('hidden', !(isFiltered && matches));
    });
  }
  ```

### 2.2 Closed Captions (CC) Dock
- Hindari kelas `line-clamp-2` atau `line-clamp-3` bersamaan dengan `overflow-y-auto`. `line-clamp` memotong teks secara permanen dan menonaktifkan bilah gulir.
- Gunakan struktur:
  ```html
  <p id="captionText" class="text-slate-700 dark:text-slate-200 font-medium leading-relaxed flex-1 text-xs overflow-y-auto max-h-16 pr-1">
  ```

### 2.3 Tombol Navigasi Header & Integrasi Sidebar Desktop/Mobile
- Jika ada tombol pintasan di header (misal tombol "Lampiran"), tombol tersebut harus cerdas memeriksa breakpoint layar dan status sidebar:
  ```javascript
  function openSidebarTabMobile(tab) {
    switchSidebarTab(tab);
    if (window.innerWidth < 1024) {
      // Buka drawer mobile
      state.isMobileDrawerOpen = true;
      document.getElementById("courseSidebar").classList.remove("-translate-x-full");
    } else {
      // Jika di desktop dan sidebar sedang terlipat, otomatis uncollapse
      if (state.isDesktopSidebarCollapsed) {
        state.isDesktopSidebarCollapsed = false;
        const sb = document.getElementById("courseSidebar");
        sb.style.width = "";
        sb.style.opacity = "1";
        sb.style.pointerEvents = "auto";
        document.getElementById("sidebarToggleIcon").innerText = "dock_to_left";
      }
    }
  }
  ```

---

## 3. Aksesibilitas Web (WCAG 2.2 AA)

### 3.1 Isolasi Keyboard Event Listener
- **Masalah Umum**: Event listener global `window.addEventListener("keydown")` sering kali menangkap tombol panah (`ArrowLeft`, `ArrowRight`) dan tombol Spasi (`Space`), sehingga ketika pengguna sedang memilih opsi di `<select>`, menekan tombol `<button>`, membuka `<details>`, atau mengetik di form, slide tiba-tiba berpindah atau audio menyala tanpa sengaja.
- **Pola Baku Pengamanan Event**:
  ```javascript
  window.addEventListener("keydown", (e) => {
    // 1. Abaikan jika dialog HTML5 sedang terbuka
    if (document.querySelector("dialog[open]")) return;

    const target = e.target;
    const activeEl = document.activeElement;
    const tag = target.tagName;

    const isInteractiveElement = (el) => {
      if (!el) return false;
      const t = el.tagName;
      return t === 'BUTTON' || t === 'SUMMARY' || t === 'SELECT' || t === 'A' || 
             t === 'INPUT' || t === 'TEXTAREA' || el.isContentEditable;
    };

    // 2. Tombol Spasi: Hanya toggle audio jika BUKAN elemen form/interaktif
    if (e.key === " " || e.code === "Space") {
      if (isInteractiveElement(activeEl) || isInteractiveElement(target) ||
          target.closest('button, summary, select, a, input, textarea, [contenteditable="true"]')) {
        return; // Izinkan aksi native (klik tombol, toggle details)
      }
      e.preventDefault();
      togglePlay();
      return;
    }

    // 3. Lindungi tombol panah jika fokus berada di dalam kontrol interaktif
    if (isInteractiveElement(target) || isInteractiveElement(activeEl)) return;

    // 4. Navigasi Slide Global
    if (state.currentSlide === 10 && !state.quizCompleted) return; // Kunci saat kuis
    if (e.key === "ArrowRight") goToNextSlide();
    else if (e.key === "ArrowLeft") goToPrevSlide();
  });
  ```

### 3.2 WAI-ARIA Tablist Pattern (Roving Tabindex & Panel IDs)
- Setiap tombol tab harus memiliki atribut:
  - `role="tab"`
  - `id="tab-${group}-${key}"`
  - `aria-controls="panel-${group}-${key}"`
  - `aria-selected="true/false"`
  - `tabindex="0"` (tab aktif) atau `tabindex="-1"` (tab non-aktif)
- Setiap kontainer isi panel tab harus memiliki atribut inisial:
  - `role="tabpanel"`
  - `id="panel-${group}-${key}"`
  - `aria-labelledby="tab-${group}-${key}"`
- **Navigasi Keyboard Tablist**: Mendukung `ArrowRight` (tab selanjutnya), `ArrowLeft` (tab sebelumnya), `Home` (tab pertama), dan `End` (tab terakhir).

### 3.3 WAI-ARIA Radiogroup Pattern untuk Kuis
- Kontainer opsi kuis bertanda `role="radiogroup"`.
- Setiap opsi tombol bertanda `role="radio"` dan `aria-checked="true/false"`.
- Mendukung navigasi panah `ArrowDown` / `ArrowRight` dan `ArrowUp` / `ArrowLeft` untuk berpindah dan memilih opsi.

### 3.4 Target Sentuh Minimum (Touch Target Size >= 44x44px)
- Seluruh tombol nomor soal kuis dan kontrol sentuh seluler wajib berukuran minimal 44x44 piksel:
  ```html
  class="w-11 h-11 min-w-[44px] min-h-[44px] rounded-xl text-xs sm:text-sm font-mono font-bold ..."
  ```
- **Navigasi Nomor Soal**: Disusun dalam format **Stack 5/5 Atas-Bawah** (`grid grid-cols-5 gap-1.5`) agar simetris, rapi, dan mudah dijangkau dengan ibu jari pada perangkat seluler.

---

## 4. Sertifikat Kelulusan & Optimasi Cetak (Print CSS)

### 4.1 Layout Cetak A4 Landscape Presisi
- Sertifikat dibuat menggunakan kontainer `@media print` terisolasi:
  ```css
  @media print {
    * {
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    html, body {
      width: 297mm;
      height: 210mm;
      overflow: hidden !important;
    }
    @page {
      size: A4 landscape;
      margin: 0;
    }
    body * { visibility: hidden; }
    #certificatePrintArea, #certificatePrintArea * { visibility: visible; }
    #certificatePrintArea {
      position: fixed;
      left: 0;
      top: 0;
      width: 297mm;
      height: 210mm;
      margin: 0;
      padding: 15mm;
      box-sizing: border-box;
      background: white !important;
      color: #000 !important;
      display: flex !important;
    }
  }
  ```
- Atribut `-webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;` mutlak diperlukan agar warna latar biru, bingkai ganda, dan badge kelulusan tidak dihapus oleh peramban saat dicetak.

### 4.2 Data Sertifikat Dinamis
- Nomor registrasi dan tanggal cetak harus dinamis:
  ```javascript
  const randNum = Math.floor(1000 + Math.random() * 9000);
  document.getElementById("certNumberLabel").innerText = `No. Reg: PP/HCM-QA/C1-050/${new Date().getFullYear()}/${randNum}`;
  document.getElementById("certDateVal").innerText = new Date().toLocaleDateString('id-ID', { year: 'numeric', month: 'long', day: 'numeric' });
  ```

---

## 5. Mesin Narasi Audio Edge-TTS

### 5.1 Spesifikasi Suara & Tempo
- **Model Suara**: `id-ID-ArdiNeural` (Pria formal, berwibawa, cocok untuk standar korporat konstruksi/BUMN).
- **Tempo Bicara**: `-4%` (*Relaxed Cadence Rate*). Memberikan artikulasi yang jelas dan jeda napas yang nyaman untuk memahami klausul hukum/teknis.

### 5.2 Single-Pass Phonetic Respelling Engine
Edge-TTS membutuhkan transliterasi fonetis agar singkatan dan istilah teknis dibaca dengan tepat dalam bahasa Indonesia:
```python
PHONETIC_DICTIONARY = {
    "PP/SOP/C1-050": "Pe-Pe, Es-O-Pe, C-satu strip nol lima puluh",
    "ISO 9001:2015": "I-S-O sembilan ribu satu, tahun dua ribu lima belas",
    "ISO 19650:2018": "I-S-O sembilan belas enam ratus lima puluh, tahun dua ribu delapan belas",
    "ISO 45001:2018": "I-S-O empat puluh lima ribu satu, tahun dua ribu delapan belas",
    "BAST I": "B-A-S-T Satu",
    "BAST II": "B-A-S-T Dua",
    "Hold Point V": "Hold Point Lima",
    "HP V": "Ha-Pe Lima",
    "PFC": "P-F-C",
    "SVP-OC&SCC": "Es-Ve-Pe O-C dan S-C-C",
    "SVP-FinAcc": "Es-Ve-Pe Fin-Ak",
    "GM-Ops": "Ji-Em Ops",
    "SM-FinHC": "Es-Em Fin-Ha-Se",
    "PM": "Pe-Em",
    "SAP": "S-A-P",
    "BIM": "Bim",
}
```

---

## 6. Standarisasi Kontainer Aktivitas Interaktif & Umpan Balik (Feedback UX)

### 6.1 Desain Kontainer Simetris & Profesional
Aktivitas interaktif di dalam modul (seperti *Validasi Penggunaan Anggaran* dan *Studi Kasus Percabangan PFC*) wajib memiliki struktur visual yang sejajar (*consistent anatomy*):
1. **Header Kontainer Terpadu**:
   - Memiliki ikon dalam kotak bundar (*icon box*) dengan warna aksen lembut (`bg-brand-primary/10 text-brand-primary`).
   - Judul aktivitas yang tegas (`text-sm font-bold`) disertai subjudul panduan tindakan peserta (`text-[11px] text-slate-500`).
   - *Pill badge* rujukan pasal SOP (`Klausul 6.2`, `Pasal 5.8 & 5.9`) dengan indikator titik berdenyut (`animate-pulse`).
2. **Kartu Pilihan Skenario 3 Kolom (`grid grid-cols-1 sm:grid-cols-3 gap-3`)**:
   - Setiap tombol skenario memuat:
     - Header kartu: Label kode skenario (`Skenario A`, `Opsi B`) dan ikon sentuh/tindakan (`touch_app`).
     - Judul skenario yang padat dan jelas.
     - Penjelasan ringkas konteks lapangan.
3. **Indikator Status Aktif (*Active Ring Highlighting*)**:
   - Saat pengguna mengklik salah satu skenario, kartu yang dipilih langsung diberi aksen visual aktif:
     `border-2 border-brand-primary bg-blue-50/80 dark:bg-brand-primary/20 ring-2 ring-brand-primary/30 shadow-sm`.
   - Kartu yang tidak dipilih kembali ke status netral tanpa merusak tata letak.
4. **Kotak Hasil Umpan Balik (*Feedback Alert Box*)**:
   - Ikon status (`check_circle`, `block`, `warning`, `shield`) diletakkan di dalam kontainer berukuran pasti `w-8 h-8 rounded-xl shrink-0 mt-0.5` agar tidak pernah tertekan (*squashed*) saat teks alasan memanjang.
   - Menggunakan kode status yang tegas dan jelas:
     - Hijau/Emerald: `DIPERBOLEHKAN (PASAL 6.2.1)` / `TEPAT & SESUAI SOP`.
     - Merah/Rose: `DILARANG KERAS (PASAL 6.2.2)` / `DILARANG KERAS (PELANGGARAN AKUNTANSI)`.
     - Amber: `TIDAK SAH / DITOLAK (PASAL 6.2.3)` / `TIDAK TEPAT (PELANGGARAN TATA KELOLA)`.
   - Penjelasan klausul SOP ditulis terpisah di bawah judul putusan agar alur baca nyaman dan mudah dipahami.

---

## 7. Arsitektur Tree Diagram 3 Kolom & Kanvas Interaktif (Pan & Zoom)

### 7.1 Merefleksikan Struktur Asli Dokumen SOP
Dokumen SOP asli PT PP (Persero) Tbk (*Halaman 4, 5, 6*) menggunakan bagan alir vertikal 3 kolom yang ketat:
* **Kolom 1: Dokumen Input** (Referensi SOP, BAST-1, Saldo SAP, Form OP4-A, Laporan Manajemen Risiko).
* **Kolom 2: Aktivitas & Pohon Keputusan (Tree Diagram)** (Rantai proses Tahap 5.1 s.d 5.28 beserta cabang PFC $\le$ 100% vs PFC > 100%, paralel de-aktivasi SAP L/R & Neraca, dan loop approval SVP-Ops).
* **Kolom 3: Dokumen Output** (BAST-1, BA Hold Point V, Tutup Buku I & II, RKP Akhir, BA Rekonsiliasi, Penutupan Akun SAP).

### 7.2 Mesin Kanvas Mandiri (Zero-Dependency Matrix Transform) & Scrolling Suite
Alih-alih menggunakan pustaka eksternal berbayar atau berbobot besar (DHTMLX/yFiles/Treant.js) yang rawan lisensi dan membebani SCORM/LMS:
- Kanvas dibangun dengan **CSS Matrix Transform** murni (`transform: translate(${x}px, ${y}px) scale(${scale})`).
- **Fitur Navigasi & Pengguliran (*Rich Scrolling Suite*)**:
  - *Natural Mouse Wheel / Trackpad Scroll*: Menggulirkan roda mouse atau trackpad secara alami menggeser bagan alir ke atas dan ke bawah (vertikal) secara mulus tanpa memperbesar/memperkecil diagram secara tidak sengaja.
  - *Shift + Wheel*: Menggulir secara horizontal (kiri/kanan).
  - *Ctrl + Wheel / Pinch-to-Zoom*: Memperbesar atau memperkecil skala kanvas (batas rentang 0.4x s.d 2.0x).
  - *Dedicated Interactive Vertical Scrollbar*: Bilah gulir vertikal khusus di sisi kanan kanvas lengkap dengan *draggable thumb*. Pengguna dapat mengklik trek bilah gulir atau menyeret *thumb* langsung untuk melompat ke bagian proses manapun.
  - *Floating Quick Scroll Dock*: Tombol gulir cepat di pojok kanan bawah kanvas:
    - *Top* (`vertical_align_top`): Langsung lompat ke awal (Tahap 5.1).
    - *Up* (`keyboard_arrow_up`): Gulir bertahap ke atas.
    - *Down* (`keyboard_arrow_down`): Gulir bertahap ke bawah.
    - *Bottom* (`vertical_align_bottom`): Langsung lompat ke Selesai Paripurna (Tahap 5.28).
  - *Real-Time Phase Breadcrumb Badge*: Indikator status di pojok kiri atas kanvas yang otomatis mendeteksi posisi gulir dan memperbarui label fase aktif (`Fase 1`, `Fase 2`, `Fase 3`) secara dinamis.
  - *Phase Jump Anchors*: Tombol pintas di toolbar atas untuk melompat instan ke *Fase 1*, *Fase 2*, atau *Fase 3*.
  - *Filter Peran In-Place*: Menyaring kartu aktor lapangan (*PM*, *GM-Ops*, *SM-FinHC*, *SVP-FinAcc*, *SVP-Ops*, *SVP-OC&SCC*) dengan efek peredupan simpul lain (`opacity-35`) tanpa me-reset posisi kanvas.
- **Hotspot Interaktif**: Seluruh 16 simpul aktivitas pada kanvas terhubung ke modal `<dialog id="hotspotModal">`, menampilkan klausul detail, aktor, dokumen input, dan dokumen output saat diklik.

### 7.3 Perbaikan Batas Gulir Bawah (*Bottom Clearance & Dynamic Tree Height*)
- **Akar Masalah**:
  Pengguna melaporkan bahwa diagram pohon tidak dapat digulir sampai bawah sehingga tahapan akhir Fase 3 (termasuk keputusan approval BAST II, penutupan akun SAP, dan simpul akhir Tahap 5.28) terpotong.
  Hal ini disebabkan oleh pembatasan `minY = -(contentHeight * scale - viewportHeight + 100)` di mana `contentHeight` sebelumnya hanya mengandalkan `inner.scrollHeight || 3000`. Karena elemen kanvas bertipe `position: absolute` dengan transformasi CSS, peramban mengembalikan estimasi tinggi yang lebih kecil (~3000px), padahal rentang dokumen diagram alir mencapai >4800px. Akibatnya, batas `minY` mengunci posisi kanvas sebelum mencapai bagian dasar.
- **Solusi Rekayasa**:
  1. **Fungsi Pengukur Tinggi Dinamis (`getTreeContentHeight()`)**:
     Mengukur offset posisi nyata simpul `#fase-3` dan tombol terminal `step_5_28` dari puncak kanvas, dikombinasikan dengan `offsetHeight` elemen anak, dengan ambang batas dasar aman minimal 4800px.
  2. **Elemen Buffer (*Clearance Spacer*)**:
     Menambahkan elemen pembatas bawah setinggi 176px (`<div class="h-44 ...">`) di bawah simpul *Selesai Paripurna* agar konten akhir tidak pernah terhimpit tepi bawah bingkai.
  3. **Penyesuaian Batas `minY`**:
     Batas bawah diperlebar dengan ekstra kelonggaran 140px, memungkinkan peserta menggulirkan alur proses sampai tuntas ke simpul paling akhir.

### 7.4 Tata Letak HUD Mengambang Kanvas (*Side-by-Side Floating HUD*)
- **Kebutuhan Pengguna**:
  Pengguna meminta agar kontainer teks penunjuk tahapan aktif (`Fase 1/2/3 : Tahap ...`) diposisikan berdampingan langsung di samping kontainer panduan gulir (*Scroll mouse/trackpad*) pada bilah status mengambang atas, sehingga tidak menumpuk (*overlap*) atau menutupi alur pohon diagram di bawahnya.
- **Implementasi**:
  1. Menggunakan pembungkus flex `flex flex-wrap items-center gap-2 max-w-[calc(100%-4rem)] pointer-events-none`.
  2. Kontainer instruksi navigasi (`mouse`) dan kontainer lencana fase dinamis (`#treeCurrentPhaseBadge`) diletakkan berdampingan horizontal dalam satu baris status HUD.
  3. Menggunakan latar belakang *frosted glass* semi-transparan (`bg-white/95 dark:bg-brand-darkSurface/95 backdrop-blur-sm border shadow-md`) dengan tipografi monospaced tebal warna biru korporat PT PP, menjaga keterbacaan tinggi tanpa menghalangi pandangan simpul alur proses.

### 7.5 Perbaikan Sinkronisasi & Interaktivitas Fase 3
- **Identifikasi Bug pada Fase 3**:
  1. *Pergeseran Koordinat Lompatan (Coordinate Scale Drift)*: Fungsi `jumpToPhase('fase-3')` sebelumnya menghitung `-target.offsetTop + 40` tanpa memperhitungkan faktor pembesaran kanvas (`canvasPanZoom.scale`). Saat kanvas di-zoom in atau di-zoom out, lompatan ke Fase 3 meleset jauh dari pandangan pengguna.
  2. *Ambang Batas Lencana Fase Tidak Akurat*: Fungsi `updatePhaseBadgeUI()` sebelumnya menggunakan angka pixel statis (`y < -2400`) yang tidak peka terhadap zoom, sehingga saat pengguna melihat Fase 3 dalam kondisi zoom out, lencana status masih tertulis "Fase 2".
  3. *Atribut Filter Peran pada Simpul Keputusan*: Dua cabang keputusan Persetujuan Tutup Buku II pada Fase 3 belum dilengkapi kelas `flow-card-node`, `data-actor="SVP-Ops"`, dan badge peran, sehingga ketika pengguna memilih dropdown peran, kartu keputusan tidak ikut bereaksi/tersaring dengan benar.
- **Solusi yang Diterapkan**:
  1. Memperbarui `jumpToPhase(phaseId)` agar mengalikan `target.offsetTop * canvasPanZoom.scale`, menjamin posisi kepala Fase 3 mendarat tepat di titik atas pandangan pada tingkat pembesaran berapa pun.
  2. Menjadikan ambang batas `updatePhaseBadgeUI()` dinamis membaca posisi offset elemen `#fase-2` dan `#fase-3` yang diskalakan secara real-time.
  3. Menambahkan sinkronisasi styling tombol toolbar Fase 1, 2, dan 3 yang menyala aktif sesuai fase yang sedang berada di layar.
  4. Melengkapi simpul keputusan Fase 3 dengan kelas `flow-card-node`, atribut aktor, dan lencana "Peran Anda" yang responsif terhadap filter.

---

## 8. Penyelarasan Ikon Google Material Symbols & Standar UI

### 8.1 Pencegahan Pergeseran Baseline Ikon (*Baseline Drift*)
Secara default, font Google Material Symbols dapat tampak naik atau turun dari garis teks jika hanya menggunakan `display: inline-block`. Aturan CSS baku yang wajib diterapkan adalah:
```css
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  user-select: none;
}
```

### 8.2 Aturan `shrink-0` di Flex Parent
Setiap kali elemen ikon `<span class="material-symbols-outlined ...">` disandingkan dengan teks di dalam kontainer `flex` atau `grid`:
- **Wajib pasang kelas `shrink-0`** pada ikon.
- Tanpa `shrink-0`, peramban akan memampatkan (*squash*) lebar ikon menjadi lonjong atau pipih saat teks di sebelahnya meregang atau melipat baris (*wrap*) di layar sempit.

### 8.3 Waspada Regex Manipulasi pada Template Literals JavaScript
- **Penyebab Utama Layar Blank / Konten Tidak Muncul**:
  Ketika melakukan manipulasi string regex otomatis (seperti penambahan kelas utilitas `shrink-0`), jika regex mencocokkan `class="..."` secara sembrono di dalam *template literal* JavaScript (backtick `` ` ``), regex dapat memotong ekspresi ternary seperti `${ok ? "text-primary" : "text-muted"}` di tanda kutip pertama dan menyisipkan atribut ke tengah kode JavaScript (`${ok ? shrink-0"text-primary...`).
- Hal ini menyebabkan `SyntaxError: Unexpected string` saat peramban mem-parsing berkas skrip. Akibatnya, seluruh JavaScript berhenti berjalan, fungsi `DOMContentLoaded` dan `goToSlide(0)` tidak pernah dieksekusi, tombol tidak merespons klik, dan kontainer slide tampak kosong.
- **Solusi Pencegahan**:
  Selalu lakukan validasi sintaksis skrip peramban secara otomatis (`vm.Script` atau `new Function(...)` di Node.js) setelah melakukan transformasi kode otomatis untuk memastikan tidak ada kesalahan interpretasi (*zero runtime syntax error*).

---

## 9. Catatan Temuan & Rekomendasi Redaksional Klausul SOP PP/SOP/C1-050 REV-3

Selama pengujian komprehensif dan verifikasi klausul antara dokumen fisik resmi *PP/SOP/C1-050 REV-3* dengan implementasi modul e-learning, ditemukan 3 hal penting yang telah diselaraskan di seluruh file modul:

### 9.1 Koreksi Nomor Klausul Penjelasan Kuis No. 2 (Klausul 5.1 vs 5.17)
- **Temuan Awal**: Pada penjelasan evaluasi kuis soal No. 2, rujukan teks sebelumnya tertulis:  
  *"...namun Klausul 5.17 menegaskan: 'Apabila sebelum masa pemeliharaan selesai PM dimutasi ke tempat lain, maka yang bertanggung jawab adalah GM-Ops terkait.'"*
- **Fakta Dokumen Resmi SOP**:
  - **Klausul 5.1**: Merupakan klausul otentik yang mengatur ketentuan mutasi personil: *"Apabila Project Manager (PM) telah dimutasi sebelum masa pemeliharaan selesai maka seluruh hutang pemeliharaan proyek menjadi tanggung jawab langsung GM Ops."*
  - **Klausul 5.17**: Sebenarnya mengatur verifikasi dan pengarsipan berkas Tutup Buku I: *"Penanggung jawab verifikasi dan pengarsipan mengacu pada poin 6.5."*
- **Tindakan Perbaikan**: Pertanyaan dan penjelasan kuis No. 2 pada `index_tree_canvas.html`, `index.html`, `TEMPLATE_SOP_TO_MODUL.html`, dan `index_clean_ui.html` telah diperbarui merujuk secara akurat ke **Klausul 5.1 & 5.14**.

### 9.2 Sinkronisasi Penomoran Tabel Verifikasi Dokumen (Bagan Alur 6.5 vs Bab 6 Tabel 6.6)
- **Fakta Dokumen Resmi SOP**:
  - Pada bagan alur proses SOP (Klausul 5.17 untuk Tutup Buku I dan Klausul 5.26 untuk Tutup Buku II), teks tertulis: *"mengacu pada ketentuan khusus poin 6.5"*.
  - Namun pada Bab 6 (Ketentuan Khusus) halaman 9 dokumen fisik, tabel matriks penanggung jawab verifikasi dokumen Tutup Buku I dan II diberi nomor **Tabel 6.6** (*Penanggung jawab verifikasi dokumen untuk tutup buku I dan tutup buku II*), sedangkan poin 6.5 membahas perincian teknis lainnya.
- **Tindakan Perbaikan**:
  - Seluruh modul e-learning secara konsisten menggunakan penomoran baku **Tabel 6.6**.
  - Pada daftar klausul 5.17 dan 5.26, serta pada audio naskah/transkrip Slide 5, telah disematkan penjelasan harmonisasi: *"Tabel Ketentuan Khusus Poin 6.6 (pada bagan alir SOP tertulis poin 6.5)"* sehingga peserta diklat maupun auditor internal tidak mengalami kebingungan referensi.

### 9.3 Penyelarasan Otorisasi Cadangan Risiko (*Contingency Risk*)
- **Fakta Dokumen Resmi SOP**:
  - **Definisi Poin 4.18 & Klausul 5.18**: Otorisasi formal persetujuan pengeluaran hutang contingency risk disebutkan disahkan oleh **SVP-RM** dan **SVP-Legal**.
  - **Klausul 6.2.3**: Menyebutkan pengajuan persetujuan penggunaan pos contingency risk ditujukan ke **Divisi MR** (didukung kronologis risiko, rencana tindak lanjut, dan risk register proyek) dengan tembusan/diketahui **Divisi OC&SCC**.
- **Tindakan Perbaikan**:
  - Modul e-learning menjembatani perbedaan perspektif struktural vs operasional ini secara elegan melalui Callout Box edukatif *"Harmonisasi Otorisasi Contingency Risk"* pada Slide 3 dan soal kuis No. 3 pada Slide 10:
    - *Secara operasional & kajian teknis risiko*: Diverifikasi oleh **Divisi MR** didukung data risk register dan diketahui **Divisi OC&SCC** (Klausul 6.2.3).
    - *Secara legal-struktural korporasi*: Otorisasi formal pengesahan pencairan anggaran ditandatangani oleh **SVP-RM** dan **SVP-Legal** (Poin 4.18 & Klausul 5.18).

### 9.4 Penyederhanaan UI: Penyembunyian Subtitle pada Sidebar Navigasi (*Clean Minimalist Sidebar*)
- **Kebutuhan Desain**:
  Untuk mewujudkan antarmuka yang bersih (*clean & minimalist*), tidak padat teks, dan lebih mengutamakan keterbacaan judul utama serta ikonografi, seluruh teks subtitle penjelas di bawah judul unit pada sidebar navigasi (*Daftar Materi*) disembunyikan.
- **Implementasi Teknis**:
  - Pada fungsi `updateOutlineUI()`, baris template `<div class="text-xs text-slate-500 ...">${u.subtitle}</div>` dihilangkan.
  - Padding item tombol disesuaikan menjadi `py-2 px-2.5` agar tinggi baris (*row height*) simetris, rapi, dan proporsional terhadap ikon indikator di sisi kiri dan durasi di sisi kanan.
  - Perubahan ini disinkronkan ke seluruh file modul (`index_tree_canvas.html`, `index.html`, `TEMPLATE_SOP_TO_MODUL.html`, `index_clean_ui.html`, dan `template_elearning_player_blue.html`).

---

*Dokumentasi ini disahkan sebagai standar acuan pengalihan SOP operasional menjadi media kursus interaktif di lingkungan Divisi HCM PT PP (Persero) Tbk.*



