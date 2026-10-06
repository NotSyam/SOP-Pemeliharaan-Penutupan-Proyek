# -*- coding: utf-8 -*-
"""
Script to inject refined lean layout and interactive activities into index.html
"""
import sys
import re

html_path = r"d:\HCM Course Development\sop_pemeliharaan_penutupan_proyek\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Marker detection
start_marker = "    function renderCurrentSlide() {"
end_marker = "    // ========================================================================\n    // SWIMLANE HOTSPOT MODAL OPENER (HALAMAN 2)"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

print(f"Start index: {idx_start}, End index: {idx_end}")

if idx_start == -1 or idx_end == -1:
    print("Error: Could not locate replacement boundaries!")
    sys.exit(1)

lean_slides_code = r'''    // ========================================================================
    // UI TOKENS & HELPERS (LEAN LAYOUT: LESS IS MORE, BLUE & WHITE PALETTE)
    // ========================================================================
    const UI = {
      card: "rounded-2xl border border-slate-200 dark:border-brand-darkBorder bg-white dark:bg-brand-darkSubtle",
      label: "text-[11px] font-bold uppercase tracking-wider text-brand-primary dark:text-brand-lightBlue",
      text: "text-sm leading-relaxed text-slate-600 dark:text-slate-300",
      tabOn: "px-3.5 py-1.5 rounded-lg text-xs font-bold bg-brand-primary text-white shadow-sm cursor-pointer",
      tabOff: "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-200/50 dark:hover:bg-brand-darkSubtle cursor-pointer"
    };

    function uiTitle(title, lead) {
      return `
        <header class="mb-4 sm:mb-5">
          <h2 class="text-xl sm:text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">${title}</h2>
          ${lead ? `<p class="mt-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400">${lead}</p>` : ""}
        </header>`;
    }

    function uiTabs(group, items) {
      return `
        <div class="inline-flex flex-wrap gap-1 p-1 rounded-xl bg-slate-100 dark:bg-brand-darkBg mb-4" role="tablist">
          ${items.map((it, i) => `<button role="tab" data-tab-group="${group}" data-tab="${it.key}" onclick="switchTabGroup('${group}','${it.key}')" class="${i === 0 ? UI.tabOn : UI.tabOff}">${it.label}</button>`).join("")}
        </div>`;
    }

    function switchTabGroup(group, key) {
      playTone('click');
      document.querySelectorAll(`[data-tab-group="${group}"]`).forEach(b => b.className = b.dataset.tab === key ? UI.tabOn : UI.tabOff);
      document.querySelectorAll(`[data-panel-group="${group}"]`).forEach(p => p.classList.toggle("hidden", p.dataset.panel !== key));
    }

    // ========================================================================
    // DATA RINGKAS & DETAIL KONTEN SOP
    // ========================================================================
    const HP5_AGENDA = [
      "Pembahasan CSS 100%",
      "Hasil internal audit terhadap BA pemeriksaan bersama owner (jika ada)",
      "Evaluasi sisa waktu pemeliharaan",
      "Evaluasi penerapan mitigasi manajemen risiko",
      "Evaluasi penerapan review kontrak (finalisasi tagihan klaim)",
      "Evaluasi cash flow dan neraca proyek",
      "Evaluasi pajak",
      "Konfirmasi hutang vendor (supplier, subkont, rental alat, mandor)",
      "Rencana penggunaan biaya cadangan pemeliharaan",
      "Realisasi BPP final (PFC) berdasarkan SAP",
      "Monitoring Project Charter",
      "Pembahasan Lesson Learned Proyek (Lamp. 11)"
    ];

    const HP5_OUTPUT = [
      { t: "BA Hold Point V", d: "Didistribusikan ke Divisi Operasi/EPC & Divisi OC&SCC" },
      { t: "Laporan Tutup Buku I", d: "Disahkan Divisi Operasi; didistribusikan ke Divisi Operasi/EPC, FinAcc & OC&SCC" },
      { t: "Final ketercapaian KPI Proyek", d: "Rekapitulasi pencapaian target kinerja akhir" },
      { t: "Rencana Kerja Proyek (RKP) akhir proyek", d: "Alokasi sisa pekerjaan dan penutupan" },
      { t: "Buku karya konstruksi", d: "Termasuk Lesson Learned Proyek di dalamnya" },
      { t: "Video dokumentasi pelaksanaan proyek", d: "Dokumentasi visual siklus konstruksi" },
      { t: "Buku dokumentasi proyek (Knowledge Center)", d: "Tender · Kontrak · Teknik · Procurement · Operasional · BIM" }
    ];

    const VERIF_DEFAULT_PIC = "GM-Ops (DVO)";
    const VERIF_TB1 = [
      { doc: "As Built Drawing" },
      { doc: "Dokumentasi Proyek" },
      { doc: "Hasil Testing" },
      { doc: "Daftar Usulan Pemeliharaan" },
      { doc: "Manual Book Pekerjaan M/E" },
      { doc: "Dokumen ADM & KEU", note: "TTD PM, SM-FinHC & GM-Ops: Data Base Final/SAP · Daftar Piutang · Daftar Hutang · Perpajakan (JO: surat keterangan pencabutan perpajakan) · BA konfirmasi hutang setiap vendor" },
      { doc: "Defect List" },
      { doc: "Adendum Final dengan Pihak I (Akhir)" },
      { doc: "Berita Acara Serah Terima I (BAST I)" },
      { doc: "RKP Final" },
      { doc: "Pending Issue Kontraktual", pic: "GM-Ops (DVO)", noInfo: true },
      { doc: "Buku Karya Konstruksi", pic: "–", noInfo: true },
      { doc: "BA HP V", pic: "GM-Ops (DVO) & SVP-OC&SCC", noInfo: true }
    ];

    const VERIF_TB2 = [
      { doc: "Laporan Penutupan Proyek", pic: "GM-Ops (DVO), SM-FinHC (DVO)" },
      { doc: "Daftar Status Penyelesaian Defect", note: "Ditandatangani kedua belah pihak", pic: "GM-Ops (DVO)" },
      { doc: "Dokumentasi Foto Defect", pic: "GM-Ops (DVO)" },
      { doc: "Pending Issue Kontraktual", pic: "GM-Ops (DVO)" },
      { doc: "Daftar Akhir Bidang Pemeliharaan", pic: "GM-Ops (DVO), SM-FinHC (DVO)" },
      { doc: "Berita Acara Serah Terima II (BAST II)", pic: "GM-Ops (DVO), SM-FinHC (DVO)" }
    ];

    const LAMPIRAN_LIST = [
      "Form Pembebanan Hutang Pemeliharaan Proyek",
      "Form Rencana Anggaran Hutang Pemeliharaan",
      "Form Evaluasi Hutang Pemeliharaan Proyek",
      "Form Pengesahan Tambah/Kurang Hutang Pemeliharaan Proyek",
      "Form Tutup Buku I",
      "Form Tutup Buku II",
      "Form Berita Acara Serah Terima (BAST) I",
      "Form Berita Acara Serah Terima (BAST) II",
      "Form Serah Terima Dokumen kepada PPD",
      "Form Checklist Dokumen Tutup Buku Proyek",
      "Template Materi Lesson Learned Proyek"
    ];

    const RECORD_LIST = [
      "Rencana Anggaran Hutang Pemeliharaan Proyek",
      "Final PFC",
      "Pembebanan Hutang Pemeliharaan Proyek",
      "Berita Acara Serah Terima (BAST) I",
      "Rencana Anggaran Hutang Pemeliharaan",
      "Pengesahan Tambah/Kurang Hutang Pemeliharaan Proyek",
      "Berkas Tutup Buku II",
      "Berita Acara Serah Terima (BAST) II",
      "Serah Terima Dokumen kepada PPD"
    ];

    const RISK_LIST = [
      { no: "5.11", proc: "Proyek menginfokan ke tiap vendor terkait waktu penyelesaian proyek", risk: "Vendor lama sulit dihubungi dan tidak sepakat, sehingga potensi nilai hutang kurang valid dan terdapat perbedaan catat.", mit: "Penerbitan BA Rekonsiliasi resmi secara tertulis dengan batas waktu konfirmasi, serta pembebanan hutang proporsional." },
      { no: "5.20.1 – 5.20.4", proc: "Evaluasi masa pemeliharaan sesuai ketentuan", risk: "Potensi realisasi pemakaian hutang dalam masa pemeliharaan mengalami kenaikan melampaui plafon anggaran.", mit: "Pemberlakuan 3 jadwal evaluasi wajib (akhir tahun 31 Des, progres 50%, dan 1 bulan sebelum berakhir) via Lampiran 3." },
      { no: "5.21", proc: "Monitoring penyelesaian hak & kewajiban proyek dan status proyek pada SAP", risk: "Proses tutup buku di sistem memerlukan waktu lama akibat personil sudah ditugaskan di tempat lain serta dokumentasi kurang lengkap.", mit: "Monitoring triwulanan berkala oleh SM-FinHC DVO, review GM-Ops, pelaporan ke SVP-OC&SCC & FinAcc, dan delegasi GM-Ops bila PM mutasi." }
    ];

    const FLOW_CARD = {
      step_5_1: { t: "Penyelesaian Proyek Fisik 100%", out: "BAST-1" },
      step_5_2: { t: "Pelaksanaan Hold Point V", out: "BA HP V · Tutup Buku I · RKP Akhir · Buku Karya" },
      step_decision_pfc: { t: "Evaluasi Potensi Nilai PFC", branches: [["> 100%", "Bahas bersama Komite MR → Paparan ke BOD"], ["≤ 100% (tapi > RAPK)", "Presentasi pembahasan ke DO terkait"]] },
      step_5_11: { t: "Info Waktu Penyelesaian ke Vendor & Rekonsiliasi", out: "BA Rekonsiliasi / Konfirmasi Hutang" },
      step_5_13: { t: "Pembahasan Tutup Buku I (Maks. 1 Bulan Pasca BAST-1)", out: "BA Tutup Buku I (Tanggung jawab PM jika tak tercatat)" },
      step_5_15: { t: "Penyerahan Dokumen Tutup Buku I ke Divisi Operasi", out: "Hardcopy & softcopy BA Tutup Buku I" },
      step_5_19: { t: "Deaktivasi Akun User SAP (L/R, Neraca & Profit Center)", out: "SVP-OC&SCC & SVP-FinAcc nonaktifkan akun via helpdesk" },
      step_5_20: { t: "Evaluasi Masa Pemeliharaan (3 Momen Wajib)", out: "Evaluasi Realisasi Hutang (Lamp. 3)" },
      step_5_21: { t: "Monitoring Hak, Kewajiban & Status SAP (Triwulanan)", out: "Laporan berkala SM-FinHC ke SVP-OC&SCC & FinAcc" },
      step_5_22: { t: "Selesaikan Masa Pemeliharaan & Ajukan Tutup Buku II", out: "Draft Laporan Tutup Buku II" },
      step_decision_approval: { t: "Persetujuan Tutup Buku II oleh SVP-Ops", branches: [["Ya (Disetujui)", "Lanjut ke penandatanganan BAST II"], ["Tidak", "Dikembalikan ke proyek dengan catatan perbaikan"]] },
      step_5_27: { t: "Penandatanganan BAST II & Penutupan Akun L/R Final", out: "BAST II Sah & Penutupan Permanen Akun SAP" },
      step_5_28: { t: "Sharing Knowledge & Lesson Learned 6 Pilar", out: "Selesai Paripurna (Knowledge Center PT PP)" }
    };

    function renderFlowNode(item) {
      const c = FLOW_CARD[item.id] || { t: item.title };
      const dec = !!item.isDecision;
      return `
        <button onclick="openSwimlaneHotspot('${item.id}')" class="group w-64 shrink-0 self-stretch text-left p-3.5 rounded-xl border-2 ${dec ? "border-sky-400 bg-sky-50 dark:bg-sky-950/40" : "border-slate-200 dark:border-brand-darkBorder bg-white dark:bg-brand-darkSurface"} hover:border-brand-primary dark:hover:border-brand-lightBlue hover:shadow-md transition-all btn-tactile focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <span class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${dec ? "bg-sky-200 dark:bg-sky-900 text-sky-800 dark:text-sky-200" : "bg-slate-100 dark:bg-brand-darkSubtle text-slate-600 dark:text-slate-300"}">${dec ? "KEPUTUSAN" : item.step}</span>
              <span class="material-symbols-outlined text-sm text-slate-400 group-hover:text-brand-primary dark:group-hover:text-brand-lightBlue">touch_app</span>
            </div>
            <p class="text-xs sm:text-sm font-bold leading-snug text-slate-900 dark:text-white">${c.t}</p>
            ${c.branches ? `
              <div class="mt-2 space-y-1">
                ${c.branches.map(b => `<div class="text-[11px] leading-snug text-slate-600 dark:text-slate-300"><span class="font-bold text-brand-primary dark:text-brand-lightBlue">${b[0]}</span>: ${b[1]}</div>`).join("")}
              </div>` : ""}
            ${c.out ? `<p class="mt-2 text-[11px] text-slate-500 dark:text-slate-400 truncate"><span class="font-semibold text-brand-secondary">Output:</span> ${c.out}</p>` : ""}
          </div>
          <div class="mt-3 pt-2 border-t border-slate-100 dark:border-brand-darkBorder/60 flex items-center justify-between">
            <span class="inline-block px-2 py-0.5 rounded text-[10px] font-semibold bg-brand-primary/10 text-brand-primary dark:text-brand-lightBlue font-mono">${item.actor}</span>
            <span class="text-[10px] text-brand-primary dark:text-brand-lightBlue font-semibold group-hover:underline">Buka Detail →</span>
          </div>
        </button>`;
    }

    // ========================================================================
    // SLIDE CONTENT RENDERER (12 SLIDES SESUAI SOP - BLUE & WHITE LEAN)
    // ========================================================================
    function renderCurrentSlide() {
      const body = document.getElementById("slideBody");
      const catBadge = document.getElementById("slideCategoryBadge");
      const durLabel = document.getElementById("lblSlideDuration");
      body.className = "p-4 sm:p-6 md:p-8 flex-1 overflow-y-auto slide-enter";
      durLabel.innerText = COURSE_UNITS[state.currentSlide].duration;

      switch (state.currentSlide) {
        // ---------------------------------------------------------------- 0
        case 0:
          catBadge.innerText = "Pendahuluan";
          body.innerHTML = `
            <div class="max-w-3xl mx-auto space-y-6">
              <div class="p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-brand-primary to-[#1F548E] text-white shadow-lg">
                <p class="text-xs font-semibold text-sky-200 tracking-wide font-mono">PP/SOP/C1-050 · REV-3 · Berlaku 31 Des 2024</p>
                <h2 class="mt-2 text-2xl sm:text-3xl font-extrabold leading-tight">Masa Pemeliharaan & Penutupan Proyek Konstruksi dan EPC</h2>
                <p class="mt-3 text-sm text-blue-100 leading-relaxed">Panduan baku pelaksanaan Tutup Buku I dan II, pengendalian hutang garansi, verifikasi dokumen, dan deaktivasi akun SAP.</p>
              </div>

              <div>
                <p class="${UI.label} mb-3">4 Alasan Perubahan Prosedur (REV-3)</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  ${[
                    ["verified", "Integrasi Standar ISO", "Penerapan sistem manajemen ISO 45001:2018 (K3) dan ISO 19650:2018 (BIM)."],
                    ["monitoring", "Monitoring Berkala", "Pengawasan berkala atas pemenuhan hak & kewajiban proyek pasca BAST I & BAST II."],
                    ["account_tree", "Peningkatan Alur Proses", "Penyempurnaan titik henti Hold Point V, eskalasi PFC ke BOD, dan verifikasi SAP."],
                    ["badge", "Penyesuaian Nomenklatur", "Sinkronisasi nama divisi, departemen, dan jabatan struktural dengan SK Organisasi."]
                  ].map(r => `
                    <div class="${UI.card} p-4 flex items-start gap-3">
                      <span class="material-symbols-outlined text-brand-primary dark:text-brand-lightBlue text-xl mt-0.5">${r[0]}</span>
                      <div>
                        <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">${r[1]}</h4>
                        <p class="text-xs text-slate-600 dark:text-slate-300 leading-snug mt-1">${r[2]}</p>
                      </div>
                    </div>`).join("")}
                </div>
              </div>

              <div class="flex justify-end pt-2">
                <button onclick="goToSlide(1)" class="px-6 py-2.5 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white font-bold text-xs sm:text-sm flex items-center gap-2 shadow-md btn-tactile cursor-pointer">
                  <span>Mulai Materi Modul</span> <span class="material-symbols-outlined text-base">arrow_forward</span>
                </button>
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 1
        case 1:
          catBadge.innerText = "Poin 1–3";
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Maksud & Tujuan, Ruang Lingkup, Referensi", "Dasar kebijakan dan standar internasional yang terintegrasi.")}
              <div class="space-y-4">
                <div class="${UI.card} p-5">
                  <p class="${UI.label}">1 · Maksud & Tujuan</p>
                  <p class="mt-2 text-sm sm:text-base font-semibold text-slate-800 dark:text-slate-100">Memberikan panduan proses pelaksanaan Tutup Buku I dan II secara tertib, akuntabel, dan transparan.</p>
                </div>

                <div class="${UI.card} p-5">
                  <p class="${UI.label}">2 · Ruang Lingkup</p>
                  <ol class="mt-3 grid grid-cols-1 sm:grid-cols-4 gap-2.5">
                    ${["Persiapan memasuki masa pemeliharaan", "Saat masa pemeliharaan", "Penyerahan Tutup Buku I (atas dasar BAST-1)", "Penyerahan Tutup Buku II (atas dasar BAST-2)"].map((s, i) => `
                      <li class="p-3 rounded-xl bg-slate-50 dark:bg-brand-darkBg border border-slate-200 dark:border-brand-darkBorder">
                        <span class="text-xs font-mono font-bold text-brand-primary dark:text-brand-lightBlue">0${i + 1}</span>
                        <p class="mt-1 text-xs text-slate-700 dark:text-slate-200 leading-snug font-medium">${s}</p>
                      </li>`).join("")}
                  </ol>
                </div>

                <div class="${UI.card} p-5">
                  <p class="${UI.label}">3 · Referensi Standar</p>
                  <ul class="mt-3 divide-y divide-slate-100 dark:divide-brand-darkBorder">
                    ${[["ISO 9001:2015", "Sistem Manajemen Mutu (Quality Management System)"], ["ISO 19650:2018", "Manajemen Informasi & Digitalisasi Bangunan (BIM)"], ["ISO 45001:2018", "Sistem Manajemen Keselamatan & Kesehatan Kerja (K3)"]].map(r => `
                      <li class="py-2.5 flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4">
                        <span class="w-36 shrink-0 text-xs sm:text-sm font-bold font-mono text-brand-primary dark:text-brand-lightBlue">${r[0]}</span>
                        <span class="text-xs sm:text-sm text-slate-600 dark:text-slate-300">${r[1]}</span>
                      </li>`).join("")}
                  </ul>
                </div>
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 2
        case 2:
          catBadge.innerText = "Poin 5 · Alur Proses";
          body.innerHTML = `
            <div>
              <div class="flex flex-wrap items-end justify-between gap-2 mb-4">
                ${uiTitle("Alur Proses Penutupan Proyek (Swimlane)", "Diagram tahapan 5.1 s/d 5.28 sesuai SOP. Klik simpul untuk membaca PIC, input, output, dan klausul resmi.").replace("mb-4 sm:mb-5", "")}
                <span class="text-xs text-brand-primary dark:text-brand-lightBlue flex items-center gap-1 bg-blue-50 dark:bg-brand-darkSubtle px-2.5 py-1 rounded-lg border border-blue-200 dark:border-brand-darkBorder">
                  <span class="material-symbols-outlined text-base">swipe</span> Geser horizontal & klik node
                </span>
              </div>

              <div class="space-y-4">
                ${SWIMLANE_FLOWCHART.map((lane, lIdx) => `
                  <section class="rounded-2xl bg-brand-iceBg dark:bg-brand-darkBg border border-slate-200 dark:border-brand-darkBorder p-3 sm:p-4">
                    <p class="${UI.label} mb-3 flex items-center gap-2">
                      <span class="w-5 h-5 rounded-full bg-brand-primary text-white text-[11px] font-mono flex items-center justify-center font-bold">${lIdx + 1}</span>
                      <span>${lane.section}</span>
                    </p>
                    <div class="overflow-x-auto pb-2 -mx-1 px-1">
                      <div class="flex items-stretch gap-2.5 w-max">
                        ${lane.items.map((item, i) => `
                          ${renderFlowNode(item)}
                          ${i < lane.items.length - 1 ? `<span class="material-symbols-outlined self-center text-slate-300 dark:text-slate-600 shrink-0">arrow_forward</span>` : ""}
                        `).join("")}
                      </div>
                    </div>
                  </section>
                `).join("")}
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 3
        case 3:
          catBadge.innerText = "Ketentuan 6.1–6.3";
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Hutang Pemeliharaan Proyek", "Struktur komponen, aturan pembatasan cadangan, dan finalisasi rencana anggaran.")}
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div class="${UI.card} p-5 flex flex-col justify-between">
                  <div>
                    <p class="${UI.label}">6.1 · Komponen Hutang Pemeliharaan</p>
                    <div class="mt-3 space-y-3">
                      <div>
                        <p class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">6.1.1 Pemeliharaan Fisik</p>
                        <div class="mt-2 flex flex-wrap gap-1.5">
                          ${["Bahan", "Upah", "Alat", "Demobilisasi alat", "Gaji, pesangon & demob pegawai", "Biaya tidak langsung"].map(x => `<span class="px-2.5 py-1 rounded-lg text-xs bg-slate-50 dark:bg-brand-darkBg border border-slate-200 dark:border-brand-darkBorder text-slate-700 dark:text-slate-200">${x}</span>`).join("")}
                        </div>
                      </div>
                      ${["6.1.2 Hutang Peresmian (jika ada)", "6.1.3 Hutang Bunga Bank", "6.1.4 Cadangan Risiko / Contingency Risk (CR)"].map(x => `<p class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white pt-2.5 border-t border-slate-100 dark:border-brand-darkBorder">${x}</p>`).join("")}
                    </div>
                  </div>
                  <div class="mt-4 pt-3 border-t border-slate-100 dark:border-brand-darkBorder text-[11px] text-slate-500">
                    Besaran hutang pemeliharaan wajib diangsur proporsional sepanjang pelaksanaan proyek.
                  </div>
                </div>

                <div class="space-y-4">
                  <div class="${UI.card} p-5">
                    <p class="${UI.label}">6.2 · Aturan Penggunaan Cadangan</p>
                    <ul class="mt-3 space-y-2.5 text-xs sm:text-sm text-slate-600 dark:text-slate-300">
                      <li class="flex gap-2.5"><span class="material-symbols-outlined text-brand-primary dark:text-brand-lightBlue text-base shrink-0 mt-0.5">check_circle</span><span><strong class="text-slate-900 dark:text-white">6.2.1 Masa Berlaku:</strong> Hanya dapat digunakan setelah <b>BAST I s.d penyerahan BAST II</b>.</span></li>
                      <li class="flex gap-2.5"><span class="material-symbols-outlined text-slate-400 text-base shrink-0 mt-0.5">block</span><span><strong class="text-slate-900 dark:text-white">6.2.2 Larangan Tegas:</strong> Tidak dapat dipakai membiayai sisa pelaksanaan proyek (sebelum BAST I).</span></li>
                      <li class="flex gap-2.5"><span class="material-symbols-outlined text-sky-500 text-base shrink-0 mt-0.5">shield</span><span><strong class="text-slate-900 dark:text-white">6.2.3 Contingency Risk:</strong> Memerlukan persetujuan <b>Divisi MR</b> dengan melampirkan kronologis, tindak lanjut, dan risk register (diketahui Divisi OC&SCC).</span></li>
                    </ul>
                  </div>
                  <div class="${UI.card} p-5">
                    <p class="${UI.label}">6.3 · Finalisasi Rencana Hutang</p>
                    <p class="mt-2 text-xs sm:text-sm text-slate-700 dark:text-slate-200 leading-relaxed">Besaran Rencana Hutang Pemeliharaan Proyek sudah <b>FINAL pada saat Hold Point V</b> sesuai SOP No. PP/SOP/E6-032.</p>
                  </div>
                </div>
              </div>

              <!-- Interactive Activity 1: Simulator Kepatuhan Penggunaan Anggaran -->
              <div class="${UI.card} p-5">
                <p class="${UI.label} mb-2">Aktivitas Interaktif: Validasi Penggunaan Anggaran</p>
                <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">Uji skenario lapangan di bawah ini untuk melihat kepatuhannya terhadap Pasal 6.2:</p>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  ${["Perbaikan cat retak setelah BAST I", "Bayar kekurangan upah cor sebelum BAST I", "Pakai Contingency tanpa risk register"].map((s, i) => `
                    <button onclick="testCompliance(${i + 1})" class="p-3 rounded-xl border border-slate-200 dark:border-brand-darkBorder bg-slate-50 dark:bg-brand-darkBg text-xs text-left text-slate-700 dark:text-slate-200 hover:border-brand-primary btn-tactile cursor-pointer">
                      <span class="font-bold block text-brand-primary dark:text-brand-lightBlue mb-0.5">Skenario ${String.fromCharCode(65 + i)}</span>
                      <span>${s}</span>
                    </button>`).join("")}
                </div>
                <div id="complianceResult" class="hidden mt-3"></div>
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 4
        case 4:
          catBadge.innerText = "Ketentuan 6.4";
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Hold Point V (Progres Fisik 100%)", "Evaluasi aspek BMWK3L, 12 agenda wajib, dan 7 produk output resmi.")}
              ${uiTabs("hp5", [{ key: "agenda", label: "12 Agenda Pembahasan" }, { key: "output", label: "7 Dokumen Output Wajib" }])}

              <ol data-panel-group="hp5" data-panel="agenda" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                ${HP5_AGENDA.map((a, i) => `
                  <li class="${UI.card} p-3.5 flex items-start gap-3">
                    <span class="w-6 h-6 shrink-0 rounded-full bg-brand-primary/10 text-brand-primary dark:text-brand-lightBlue text-xs font-mono font-bold flex items-center justify-center">${i + 1}</span>
                    <span class="text-xs sm:text-sm text-slate-800 dark:text-slate-200 leading-snug">${a}</span>
                  </li>`).join("")}
              </ol>

              <ol data-panel-group="hp5" data-panel="output" class="hidden space-y-2.5">
                ${HP5_OUTPUT.map((o, i) => `
                  <li class="${UI.card} p-3.5 flex items-start gap-3">
                    <span class="w-6 h-6 shrink-0 rounded-full bg-brand-primary text-white text-xs font-mono font-bold flex items-center justify-center">${i + 1}</span>
                    <div>
                      <p class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">${o.t}</p>
                      ${o.d ? `<p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">${o.d}</p>` : ""}
                    </div>
                  </li>`).join("")}
              </ol>
            </div>`;
          break;

        // ---------------------------------------------------------------- 5
        case 5: {
          catBadge.innerText = "Ketentuan 6.6";
          const row = (r) => {
            const pic = r.pic || VERIF_DEFAULT_PIC;
            const isException = !!r.noInfo;
            return `
              <li class="py-3 flex flex-col sm:flex-row sm:items-start gap-1 sm:gap-4">
                <div class="flex-1">
                  <p class="text-xs sm:text-sm font-semibold text-slate-900 dark:text-white">${r.doc}</p>
                  ${r.note ? `<p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">${r.note}</p>` : ""}
                </div>
                <span class="sm:w-56 shrink-0 text-xs font-bold ${isException ? "text-sky-700 dark:text-sky-300" : "text-brand-primary dark:text-brand-lightBlue"}">${pic}</span>
              </li>`;
          };
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Penanggung Jawab Verifikasi Dokumen", "Matriks pembagian wewenang verifikasi dokumen Tutup Buku I & II.")}
              ${uiTabs("verif", [{ key: "tb1", label: "Tutup Buku I (13 Dokumen)" }, { key: "tb2", label: "Tutup Buku II (6 Dokumen)" }])}

              <div data-panel-group="verif" data-panel="tb1" class="${UI.card} px-4 sm:px-5">
                <p class="pt-3 pb-2 text-[11px] text-slate-500 dark:text-slate-400 border-b border-slate-100 dark:border-brand-darkBorder">Verifikator standar: <b class="text-brand-primary dark:text-brand-lightBlue">GM-Ops (DVO)</b> (diinformasikan ke SVP-OC&SCC & SVP-FinAcc).</p>
                <ul class="divide-y divide-slate-100 dark:divide-brand-darkBorder">${VERIF_TB1.map(row).join("")}</ul>
              </div>

              <div data-panel-group="verif" data-panel="tb2" class="hidden ${UI.card} px-4 sm:px-5">
                <p class="pt-3 pb-2 text-[11px] text-slate-500 dark:text-slate-400 border-b border-slate-100 dark:border-brand-darkBorder">Verifikator berkas Tutup Buku II dilakukan bersama GM-Ops dan SM-FinHC DVO.</p>
                <ul class="divide-y divide-slate-100 dark:divide-brand-darkBorder">${VERIF_TB2.map(row).join("")}</ul>
              </div>
            </div>`;
          break;
        }

        // ---------------------------------------------------------------- 6
        case 6:
          catBadge.innerText = "Ketentuan 6.7";
          body.innerHTML = `
            <div class="max-w-3xl mx-auto space-y-5">
              ${uiTitle("Penyusunan & Pengarsipan Dokumen", "Kewajiban penyimpanan ganda fisik dan cloud IT untuk akuntabilitas audit.")}
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="${UI.card} p-6 text-center">
                  <div class="w-12 h-12 rounded-xl bg-brand-primary/10 text-brand-primary dark:text-brand-lightBlue flex items-center justify-center mx-auto mb-3">
                    <span class="material-symbols-outlined text-2xl">folder</span>
                  </div>
                  <h3 class="text-base font-bold text-slate-900 dark:text-white">Hardcopy (Fisik)</h3>
                  <p class="mt-3 text-xs text-slate-500 dark:text-slate-400">Penanggung Jawab:</p>
                  <p class="text-sm font-bold text-brand-primary dark:text-brand-lightBlue">GM-Ops (DVO)</p>
                  <p class="mt-2 text-xs text-slate-600 dark:text-slate-300">Diarsipkan tertib dan rapi pada unit kerja Divisi Operasi masing-masing.</p>
                </div>

                <div class="${UI.card} p-6 text-center">
                  <div class="w-12 h-12 rounded-xl bg-brand-secondary/15 text-brand-secondary flex items-center justify-center mx-auto mb-3">
                    <span class="material-symbols-outlined text-2xl">cloud_upload</span>
                  </div>
                  <h3 class="text-base font-bold text-slate-900 dark:text-white">Softcopy (Digital)</h3>
                  <p class="mt-3 text-xs text-slate-500 dark:text-slate-400">Penyimpanan Terpusat:</p>
                  <p class="text-sm font-bold text-brand-primary dark:text-brand-lightBlue">Cloud Tim IT (Akun DVO)</p>
                  <p class="mt-2 text-xs text-slate-600 dark:text-slate-300">Diarsipkan pada penyimpanan Cloud tim IT akun DVO dan menjadi tanggung jawab DVO terkait.</p>
                </div>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-brand-darkSubtle border border-slate-200 dark:border-brand-darkBorder text-xs text-slate-600 dark:text-slate-300 flex items-center gap-2">
                <span class="material-symbols-outlined text-brand-primary text-base shrink-0">verified</span>
                <span>Penyimpanan ganda menjamin ketertelusuran (traceability) saat audit BPKP/KAP maupun keperluan klaim hukum.</span>
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 7
        case 7:
          catBadge.innerText = "Poin 7–9";
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Dokumen Terkait, Record & 11 Formulir", "Katalog referensi formal penutupan proyek PT PP.")}
              ${uiTabs("docs", [{ key: "lamp", label: "11 Lampiran Formulir (Poin 9)" }, { key: "rec", label: "9 Record (Poin 8)" }, { key: "rel", label: "Dokumen Terkait (Poin 7)" }])}

              <ol data-panel-group="docs" data-panel="lamp" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                ${LAMPIRAN_LIST.map((l, i) => `
                  <li class="${UI.card} p-3 flex items-center gap-3">
                    <span class="w-16 shrink-0 text-xs font-mono font-bold text-brand-primary dark:text-brand-lightBlue">Lamp. ${i + 1}</span>
                    <span class="text-xs sm:text-sm text-slate-700 dark:text-slate-200 leading-snug">${l}</span>
                  </li>`).join("")}
              </ol>

              <ol data-panel-group="docs" data-panel="rec" class="hidden grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                ${RECORD_LIST.map((r, i) => `
                  <li class="${UI.card} p-3 flex items-center gap-3">
                    <span class="w-10 shrink-0 text-xs font-mono font-bold text-slate-400">8.${i + 1}</span>
                    <span class="text-xs sm:text-sm text-slate-700 dark:text-slate-200 leading-snug">${r}</span>
                  </li>`).join("")}
              </ol>

              <div data-panel-group="docs" data-panel="rel" class="hidden ${UI.card} p-5 flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-brand-primary/10 text-brand-primary dark:text-brand-lightBlue flex items-center justify-center shrink-0">
                  <span class="material-symbols-outlined text-2xl">link</span>
                </div>
                <div>
                  <p class="text-xs font-mono font-bold text-brand-primary dark:text-brand-lightBlue">PP/SOP/E6-032</p>
                  <h4 class="text-sm sm:text-base font-bold text-slate-900 dark:text-white">SOP Pengawasan & Pengendalian Proyek Konstruksi</h4>
                  <p class="text-xs text-slate-500 mt-1">Pedoman rujukan untuk pengendalian biaya dan finalisasi besaran hutang pemeliharaan pada saat Hold Point V.</p>
                </div>
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 8
        case 8:
          catBadge.innerText = "Poin 10";
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Performance Measurement (Pengukuran Kinerja)", "Tolok ukur keberhasilan dan target ketersediaan dokumen penutupan proyek.")}
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="${UI.card} p-5">
                  <p class="${UI.label}">10.1 · Tujuan</p>
                  <ul class="mt-3 space-y-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300">
                    <li class="flex gap-2"><span class="text-brand-primary dark:text-brand-lightBlue font-bold">a.</span> Mengukur kelengkapan dokumen proyek yang telah selesai atau progres 100%.</li>
                    <li class="flex gap-2"><span class="text-brand-primary dark:text-brand-lightBlue font-bold">b.</span> Memastikan akurasi data yang tercatat sesuai realisasi.</li>
                  </ul>
                </div>
                <div class="${UI.card} p-5">
                  <p class="${UI.label}">10.2 · Cara Perhitungan</p>
                  <p class="mt-3 text-xs sm:text-sm font-semibold text-slate-900 dark:text-white">Seluruh dokumen yang tersyaratkan tersedia.</p>
                  <p class="mt-1 text-xs text-slate-500">Tidak ada berkas pending atau hilang.</p>
                </div>
                <div class="rounded-2xl p-5 bg-gradient-to-br from-brand-primary to-brand-secondary text-white flex flex-col justify-between">
                  <p class="text-[11px] font-bold uppercase tracking-wider text-sky-100">10.3 · Target</p>
                  <p class="my-auto py-2 text-4xl sm:text-5xl font-black font-mono text-center">100%</p>
                  <p class="text-[10px] text-center text-sky-100">Kepatuhan mutlak seluruh berkas</p>
                </div>
              </div>

              <!-- Interactive Activity 2: Checklist Simulasi Audit Kelengkapan Dokumen -->
              <div class="${UI.card} p-5">
                <div class="flex items-center justify-between mb-2">
                  <p class="${UI.label}">Aktivitas Interaktif: Simulasi Audit Dokumen</p>
                  <span id="auditGaugeScore" class="font-mono font-black text-sm text-brand-primary dark:text-brand-lightBlue">0%</span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">Centang dokumen yang telah siap untuk menguji tingkat kelengkapan audit:</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  ${[
                    "As Built Drawing & Hasil Testing Disetujui",
                    "BAST I & BAST II Ditandatangani Sah",
                    "BA Rekonsiliasi & Konfirmasi Hutang Vendor Lengkap",
                    "Penyelesaian Defect List & Foto Defect Selesai",
                    "Arsip Softcopy Terunggah di Cloud IT Akun DVO"
                  ].map(d => `
                    <label class="flex items-center gap-3 p-3 rounded-xl bg-slate-50 dark:bg-brand-darkBg border border-slate-200 dark:border-brand-darkBorder cursor-pointer text-xs sm:text-sm text-slate-700 dark:text-slate-200 hover:border-brand-primary">
                      <input type="checkbox" onchange="calcAuditScore()" class="audit-item w-4 h-4 accent-[#2B73BD] rounded cursor-pointer" />
                      <span>${d}</span>
                    </label>`).join("")}
                </div>
                <div class="mt-3 w-full bg-slate-100 dark:bg-brand-darkBg h-2 rounded-full overflow-hidden">
                  <div id="auditGaugeBar" class="bg-brand-primary dark:bg-brand-lightBlue h-full transition-all duration-300" style="width:0%"></div>
                </div>
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 9
        case 9:
          catBadge.innerText = "Poin 11";
          body.innerHTML = `
            <div class="max-w-4xl mx-auto space-y-4">
              ${uiTitle("Identifikasi Risiko (3 Critical Process)", "Potensi risiko operasional dan langkah mitigasi preventif sesuai Poin 11 SOP.")}
              <div class="space-y-3">
                ${RISK_LIST.map(r => `
                  <div class="${UI.card} p-4 sm:p-5 grid grid-cols-1 md:grid-cols-[6rem_1fr_1fr] gap-3 md:gap-5 items-start">
                    <span class="text-xs sm:text-sm font-mono font-bold text-brand-primary dark:text-brand-lightBlue px-2 py-1 rounded bg-brand-primary/10 w-max">${r.no}</span>
                    <div>
                      <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Proses Kritis</p>
                      <p class="mt-1 text-xs sm:text-sm font-bold text-slate-900 dark:text-white leading-snug">${r.proc}</p>
                    </div>
                    <div class="md:pl-4 md:border-l border-slate-100 dark:border-brand-darkBorder">
                      <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                        <span class="material-symbols-outlined text-sm text-sky-500">warning</span> Potensi Risiko & Mitigasi
                      </p>
                      <p class="mt-1 text-xs text-slate-600 dark:text-slate-300 leading-relaxed"><b class="text-slate-800 dark:text-slate-200">Risiko:</b> ${r.risk}</p>
                      <p class="mt-1 text-xs text-brand-primary dark:text-brand-lightBlue leading-relaxed"><b class="font-semibold">Mitigasi:</b> ${r.mit}</p>
                    </div>
                  </div>`).join("")}
              </div>
            </div>`;
          break;

        // ---------------------------------------------------------------- 10
        case 10:
          catBadge.innerText = "Uji Pemahaman C2";
          renderQuizSlide(body);
          break;

        // ---------------------------------------------------------------- 11
        case 11: {
          catBadge.innerText = "Penutup & Sertifikasi";
          const passed = state.quizCompleted && state.quizScore >= COURSE_CONFIG.passingScore;
          body.innerHTML = `
            <div class="max-w-3xl mx-auto space-y-5">
              <div class="p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-brand-primary to-[#1F548E] text-white shadow-lg flex flex-col sm:flex-row items-center gap-6">
                <div class="flex-1 text-center sm:text-left">
                  <p class="text-xs font-semibold text-sky-200 tracking-wide font-mono">${passed ? "STATUS: KOMPETEN (LULUS)" : "EVALUASI BELUM SELESAI"}</p>
                  <h2 class="mt-1 text-xl sm:text-2xl font-black">Masa Pemeliharaan & Penutupan Proyek</h2>
                  <p class="mt-2 text-xs text-blue-100">PP/SOP/C1-050 REV-3 · PT PP (Persero) Tbk</p>
                </div>
                <div class="text-center px-6 py-4 rounded-xl bg-white/10 border border-white/20 shrink-0">
                  <p class="text-4xl font-black font-mono">${state.quizCompleted ? state.quizScore + "%" : "–"}</p>
                  <p class="text-[10px] text-blue-100 uppercase tracking-wider mt-1">Skor Kuis</p>
                </div>
              </div>

              <div>
                <p class="${UI.label} mb-2.5">4 Poin Kunci Kepatuhan SOP</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  ${[
                    ["person_alert", "Liabilitas Hutang", "Hutang yang tidak tercatat di BA Tutup Buku I menjadi tanggung jawab PM. Jika PM mutasi sebelum masa pemeliharaan selesai, GM Ops bertanggung jawab."],
                    ["event_available", "Batasan Cadangan", "Cadangan pemeliharaan hanya boleh dipakai setelah BAST I s.d BAST II. Dilarang keras digunakan untuk pelaksanaan sebelum BAST I."],
                    ["gavel", "Eskalasi Nilai PFC", "Potensi PFC > 100% wajib dibahas bersama Komite MR dan dipaparkan langsung ke BOD sebagai pertanggungjawaban."],
                    ["savings", "Sisa Anggaran", "Hutang pemeliharaan dan Contingency Risk yang tidak digunakan menjadi pendapatan lain-lain Divisi Operasi."]
                  ].map(r => `
                    <div class="${UI.card} p-3.5 flex items-start gap-3">
                      <span class="material-symbols-outlined text-brand-primary dark:text-brand-lightBlue text-xl mt-0.5">${r[0]}</span>
                      <div>
                        <h4 class="text-xs font-bold text-slate-900 dark:text-white">${r[1]}</h4>
                        <p class="text-xs text-slate-600 dark:text-slate-300 leading-snug mt-0.5">${r[2]}</p>
                      </div>
                    </div>`).join("")}
                </div>
              </div>

              <div class="flex flex-wrap justify-center gap-3 pt-2">
                ${passed ? `
                  <button onclick="printCertificate()" class="px-6 py-3 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white font-bold text-xs sm:text-sm flex items-center gap-2 shadow-md btn-tactile cursor-pointer">
                    <span class="material-symbols-outlined text-base">print</span> Cetak Sertifikat Kelulusan (A4)
                  </button>` : `
                  <button onclick="goToSlide(10)" class="px-6 py-3 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white font-bold text-xs sm:text-sm flex items-center gap-2 shadow-md btn-tactile cursor-pointer">
                    <span class="material-symbols-outlined text-base">quiz</span> Selesaikan Uji Pemahaman (Min. ${COURSE_CONFIG.passingScore}%)
                  </button>`}
                <button onclick="goToSlide(0)" class="px-5 py-3 rounded-xl border border-slate-200 dark:border-brand-darkBorder text-slate-700 dark:text-slate-200 font-semibold text-xs sm:text-sm flex items-center gap-2 hover:bg-slate-50 dark:hover:bg-brand-darkSubtle cursor-pointer">
                  <span class="material-symbols-outlined text-base">restart_alt</span> Ulangi dari Halaman 0
                </button>
              </div>
            </div>`;
          break;
        }
      }
    }

    // ========================================================================
    // QUIZ CONTROLLER (1 SOAL PER TAMPILAN, ACAK OPSI, FEEDBACK NETRAL)
    // ========================================================================
    function shuffleArray(arr) {
      const a = arr.slice();
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    }

    function ensureQuizOrder() {
      if (!state.quizOrder) {
        state.quizOrder = QUIZ_QUESTIONS.map(q => shuffleArray(q.options.map((_, i) => i)));
      }
      if (state.quizIndex === undefined) state.quizIndex = 0;
    }

    function renderQuizSlide(container) {
      ensureQuizOrder();
      const total = QUIZ_QUESTIONS.length;
      const answered = Object.keys(state.userAnswers).length;

      // Ringkasan hasil jika selesai
      if (state.quizCompleted) {
        const passed = state.quizScore >= COURSE_CONFIG.passingScore;
        container.innerHTML = `
          <div class="max-w-3xl mx-auto space-y-5">
            <div class="${UI.card} p-6 text-center">
              <span class="material-symbols-outlined text-4xl ${passed ? 'text-brand-primary dark:text-brand-lightBlue' : 'text-slate-400'} mb-1">
                ${passed ? 'verified' : 'pending_actions'}
              </span>
              <p class="text-4xl sm:text-5xl font-black font-mono ${passed ? "text-brand-primary dark:text-brand-lightBlue" : "text-slate-700 dark:text-slate-200"}">${state.quizScore}%</p>
              <p class="mt-2 text-sm font-bold ${passed ? "text-brand-primary dark:text-brand-lightBlue" : "text-slate-600 dark:text-slate-300"}">
                ${passed ? "Selamat! Anda Memenuhi Syarat Kelulusan (Kompeten)" : `Skor Anda Belum Mencapai Ambang Batas (${COURSE_CONFIG.passingScore}%)`}
              </p>
              <div class="mt-4 flex flex-wrap justify-center gap-2.5">
                <button onclick="resetQuiz()" class="px-4 py-2 rounded-xl border border-slate-200 dark:border-brand-darkBorder text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-brand-darkBg cursor-pointer">
                  Ulangi Kuis
                </button>
                ${passed ? `<button onclick="goToSlide(11)" class="px-5 py-2 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white text-xs sm:text-sm font-bold btn-tactile cursor-pointer">Lanjut ke Penutup & Sertifikat</button>` : ""}
              </div>
            </div>

            <div>
              <p class="${UI.label} mb-3">Review Pembahasan Konsep</p>
              <div class="space-y-2.5">
                ${QUIZ_QUESTIONS.map((q, qi) => {
                  const ok = state.userAnswers[qi] === q.correctIndex;
                  return `
                    <details class="${UI.card} p-3.5 sm:p-4 group" ${ok ? "" : "open"}>
                      <summary class="flex items-start gap-3 cursor-pointer list-none">
                        <span class="material-symbols-outlined text-lg ${ok ? "text-brand-primary dark:text-brand-lightBlue" : "text-slate-400"} mt-0.5">${ok ? "check_circle" : "cancel"}</span>
                        <span class="flex-1 text-xs sm:text-sm font-bold text-slate-900 dark:text-white leading-snug">${qi + 1}. ${q.question}</span>
                        <span class="material-symbols-outlined text-slate-400 group-open:rotate-180 transition-transform">expand_more</span>
                      </summary>
                      <div class="mt-3 pl-8 space-y-1.5 border-t border-slate-100 dark:border-brand-darkBorder pt-2 text-xs">
                        ${ok ? "" : `<p class="text-slate-500 dark:text-slate-400">Pilihan Anda: <span class="font-medium text-slate-700 dark:text-slate-300">${q.options[state.userAnswers[qi]]}</span></p>`}
                        <p class="font-bold text-brand-primary dark:text-brand-lightBlue">Kunci Jawaban: ${q.options[q.correctIndex]}</p>
                        <p class="text-slate-600 dark:text-slate-300 leading-relaxed"><span class="font-semibold">Konsep SOP:</span> ${q.explanation}</p>
                      </div>
                    </details>`;
                }).join("")}
              </div>
            </div>
          </div>`;
        return;
      }

      // Satu soal per tampilan (Focus Mode)
      const qi = state.quizIndex;
      const q = QUIZ_QUESTIONS[qi];
      const order = state.quizOrder[qi];
      const selected = state.userAnswers[qi];

      container.innerHTML = `
        <div class="max-w-2xl mx-auto space-y-5">
          <div class="flex items-center justify-between gap-3 pb-2 border-b border-slate-200 dark:border-brand-darkBorder">
            <div>
              <p class="text-xs font-mono font-bold text-brand-primary dark:text-brand-lightBlue uppercase tracking-wider">Soal ${qi + 1} dari ${total}</p>
              <p class="text-[11px] text-slate-400">Pilih satu jawaban yang paling tepat</p>
            </div>
            <div class="flex gap-1.5" aria-label="Indikator Soal">
              ${QUIZ_QUESTIONS.map((_, i) => `
                <button onclick="quizJump(${i})" aria-label="Soal ${i + 1}" class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full transition-all cursor-pointer ${i === qi ? "bg-brand-primary dark:bg-brand-lightBlue ring-2 ring-brand-primary/30" : state.userAnswers[i] !== undefined ? "bg-brand-secondary" : "bg-slate-200 dark:bg-brand-darkBorder"}"></button>`).join("")}
            </div>
          </div>

          <h3 class="text-sm sm:text-base font-bold text-slate-900 dark:text-white leading-relaxed">${q.question}</h3>

          <div class="space-y-2" role="radiogroup">
            ${order.map((oIdx, pos) => {
              const isSel = selected === oIdx;
              return `
                <button role="radio" aria-checked="${isSel}" onclick="selectQuizAnswer(${qi}, ${oIdx})" class="w-full text-left p-3.5 rounded-xl border-2 text-xs sm:text-sm flex items-start gap-3 transition-all btn-tactile cursor-pointer ${isSel ? "border-brand-primary bg-blue-50/60 dark:bg-brand-primary/15 text-slate-900 dark:text-white font-semibold" : "border-slate-200 dark:border-brand-darkBorder bg-white dark:bg-brand-darkSubtle text-slate-700 dark:text-slate-200 hover:border-brand-secondary"}">
                  <span class="w-5 h-5 shrink-0 rounded-full border-2 flex items-center justify-center text-[10px] font-bold font-mono ${isSel ? "border-brand-primary bg-brand-primary text-white" : "border-slate-300 dark:border-slate-600 text-slate-500"}">${String.fromCharCode(65 + pos)}</span>
                  <span class="flex-1 leading-snug">${q.options[oIdx]}</span>
                </button>`;
            }).join("")}
          </div>

          <div class="flex items-center justify-between gap-3 pt-3 border-t border-slate-200 dark:border-brand-darkBorder">
            <button onclick="quizJump(${qi - 1})" ${qi === 0 ? "disabled" : ""} class="px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-brand-darkSubtle disabled:opacity-30 disabled:cursor-not-allowed flex items-center gap-1 cursor-pointer">
              <span class="material-symbols-outlined text-base">chevron_left</span> Sebelumnya
            </button>
            ${qi < total - 1 ? `
              <button onclick="quizJump(${qi + 1})" class="px-4 py-2 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white text-xs font-bold flex items-center gap-1 btn-tactile cursor-pointer shadow">
                Berikutnya <span class="material-symbols-outlined text-base">chevron_right</span>
              </button>` : `
              <button onclick="submitQuizEvaluation()" ${answered < total ? "disabled" : ""} class="px-5 py-2.5 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white text-xs font-bold btn-tactile disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer shadow">
                Periksa Jawaban (${answered}/${total})
              </button>`}
          </div>
        </div>`;
    }

    function quizJump(i) {
      if (i < 0 || i >= QUIZ_QUESTIONS.length) return;
      playTone('click');
      state.quizIndex = i;
      renderQuizSlide(document.getElementById("slideBody"));
    }

    function selectQuizAnswer(qIdx, oIdx) {
      if (state.quizCompleted) return;
      playTone('click');
      state.userAnswers[qIdx] = oIdx;
      renderQuizSlide(document.getElementById("slideBody"));
    }

    function submitQuizEvaluation() {
      const answeredCount = Object.keys(state.userAnswers).length;
      if (answeredCount < QUIZ_QUESTIONS.length) {
        playTone('error');
        const firstEmpty = QUIZ_QUESTIONS.findIndex((_, i) => state.userAnswers[i] === undefined);
        quizJump(firstEmpty);
        return;
      }
      let correct = 0;
      QUIZ_QUESTIONS.forEach((q, idx) => { if (state.userAnswers[idx] === q.correctIndex) correct++; });
      state.quizScore = Math.round((correct / QUIZ_QUESTIONS.length) * 100);
      state.quizCompleted = true;

      if (state.quizScore >= COURSE_CONFIG.passingScore) {
        playTone('fanfare');
        try { confetti({ particleCount: 90, spread: 70, origin: { y: 0.6 } }); } catch (e) {}
      } else {
        playTone('error');
      }
      renderQuizSlide(document.getElementById("slideBody"));
      document.getElementById("slideBody").scrollTo({ top: 0, behavior: 'smooth' });
    }

    function resetQuiz() {
      playTone('click');
      state.userAnswers = {};
      state.quizScore = 0;
      state.quizCompleted = false;
      state.quizOrder = null;
      state.quizIndex = 0;
      renderQuizSlide(document.getElementById("slideBody"));
    }

    // ========================================================================
    // INTERAKSI KECIL (HALAMAN 3 & 8)
    // ========================================================================
    function testCompliance(scenario) {
      playTone('click');
      const res = document.getElementById("complianceResult");
      const map = {
        1: ["check_circle", "DIPERBOLEHKAN (6.2.1)", "Pengeluaran fisik setelah BAST I s.d penyerahan BAST II sah dibebankan ke pos Hutang Pemeliharaan Fisik.", "border-brand-primary/40 bg-blue-50 dark:bg-brand-primary/15 text-brand-primary dark:text-brand-lightBlue"],
        2: ["block", "DILARANG KERAS (6.2.2)", "Cadangan pemeliharaan TIDAK DAPAT digunakan untuk membiayai sisa pelaksanaan proyek saat proyek belum menerima BAST I.", "border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200"],
        3: ["shield", "TIDAK SAH (6.2.3)", "Penggunaan Contingency Risk wajib persetujuan Divisi MR dengan melampirkan kronologis risiko, rencana tindak lanjut, dan risk register proyek diketahui Divisi OC&SCC.", "border-sky-300 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/40 text-sky-800 dark:text-sky-300"]
      };
      const [icon, verdict, reason, cls] = map[scenario];
      res.className = `p-3 rounded-xl border text-xs leading-relaxed flex items-start gap-2 ${cls}`;
      res.innerHTML = `<span class="material-symbols-outlined text-base mt-0.5">${icon}</span><span><b>${verdict}:</b> ${reason}</span>`;
      res.classList.remove("hidden");
    }

    function calcAuditScore() {
      playTone('click');
      const items = document.querySelectorAll(".audit-item");
      let checked = 0;
      items.forEach(i => { if (i.checked) checked++; });
      const pct = Math.round((checked / items.length) * 100);
      document.getElementById("auditGaugeScore").innerText = `${pct}% Lengkap`;
      document.getElementById("auditGaugeBar").style.width = `${pct}%`;
      if (pct === 100) {
        playTone('success');
        try { confetti({ particleCount: 50, spread: 60, origin: { y: 0.7 } }); } catch (e) {}
      }
    }
'''

new_content = content[:idx_start] + lean_slides_code + "\n" + content[idx_end:]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Success! Replaced {idx_end - idx_start} characters with {len(lean_slides_code)} characters.")
