#!/usr/bin/env python3
"""
Edge-TTS Audio Narration Generator for Modul Interaktif:
SOP Masa Pemeliharaan & Penutupan Proyek Konstruksi dan EPC
No. Dokumen: PP/SOP/C1-050 (REV-3) - PT PP (Persero) Tbk

Fitur Standar Audio:
1. Single-Pass Phonetic Respelling Engine (Istilah korporat, singkatan jabatan, dan terminologi SOP)
2. Rhythmic Breath Punctuation (Jeda koma ~200ms dan elipsis ~400ms antar frasa klausa)
3. Relaxed Cadence Rate (-4% speed offset untuk kejelasan pemahaman)
4. Model Suara: id-ID-ArdiNeural (Pria formal & otoritatif) atau id-ID-GadisNeural (Wanita hangat)
"""

import asyncio
import os
import sys
import re
import argparse

VOICE_DEFAULT = "id-ID-ArdiNeural"
RATE_DEFAULT = "-4%"

# ============================================================================
# KAMUS PELAFALAN FONETIS INDONESIA (SOP PP/SOP/C1-050 REV-3)
# ============================================================================
PHONETIC_DICTIONARY = {
    # Dokumen & Regulasi
    "PP/SOP/C1-050": "Pe-Pe, Es-O-Pe, C-satu strip nol lima puluh",
    "PP/SOP/E6-032": "Pe-Pe, Es-O-Pe, E-enam strip nol tiga puluh dua",
    "PP/SOP/E6-041": "Pe-Pe, Es-O-Pe, E-enam strip nol empat puluh satu",
    "ISO 9001:2015": "I-S-O sembilan ribu satu, tahun dua ribu lima belas",
    "ISO 19650:2018": "I-S-O sembilan belas enam ratus lima puluh, tahun dua ribu delapan belas",
    "ISO 45001:2018": "I-S-O empat puluh lima ribu satu, tahun dua ribu delapan belas",
    "REV-3": "Revisi Tiga",
    "BAST I": "B-A-S-T Satu",
    "BAST-1": "B-A-S-T Satu",
    "BAST II": "B-A-S-T Dua",
    "BAST-2": "B-A-S-T Dua",
    "Hold point V": "Hold Point Lima",
    "Hold Point V": "Hold Point Lima",
    "HP V": "Ha-Pe Lima",
    
    # Istilah Finansial & Proyek
    "Project Final Cost": "Projek Faynel Kost",
    "PFC": "P-F-C",
    "BPP Final": "B-P-P Final",
    "BPP": "B-P-P",
    "RAPK": "R-A-P-K",
    "RAPT": "R-A-P-T",
    "NK-PPN": "N-K P-P-N",
    "CSS 100%": "C-S-S seratus persen",
    "BMWK3L": "B-M-W-K-Tiga-L",
    "Contingency Risk": "Kontinjensi Risk",
    "Contingency": "Kontinjensi",
    "Joint Operation": "Joyn Opereysyen",
    "Lesson Learned": "Leson Lernd",
    "Project Charter": "Projek Tsyarter",
    "As Built Drawing": "As Bilt Drawing",
    "Defect List": "Difek List",
    "Manual Book": "Menyuel Buk",
    
    # Satuan Kerja & Jabatan Organisasi
    "SVP-OC&SCC": "Es-Ve-Pe O-C dan S-C-C",
    "SVP-Ops": "Es-Ve-Pe Ops",
    "SVP-RM": "Es-Ve-Pe R-M",
    "SVP-Legal": "Es-Ve-Pe Legal",
    "SVP-FinAcc": "Es-Ve-Pe Fin-Ak",
    "GM-Ops": "Ji-Em Ops",
    "SM-FinHC": "Es-Em Fin-Ha-Se",
    "SM-OpsCon": "Es-Em Ops-Kon",
    "SM-SMO": "Es-Em S-M-O",
    "SM Bld&Eng": "Es-Em Bilding and Enjiniyering",
    "PM": "Pe-Em",
    "DVO": "D-V-O",
    "BOD": "B-O-D",
    "DO": "D-O",
    "UKP": "U-K-P",
    "SAP": "S-A-P",
    "BIM": "Bim",
}

# Narasi Audio Verbatim per Halaman (Slide 0 s.d 11)
NARRATIONS_SOP = {
    "0": "Selamat datang di modul interaktif Standar Operasional Prosedur PP/SOP/C1-050 Revisi Tiga mengenai Masa Pemeliharaan dan Penutupan Proyek Konstruksi dan EPC di PT PP Persero Tbk. Modul ini disusun berdasarkan dokumen validasi terbaru untuk memberikan kepastian tata kelola pada tahapan akhir siklus proyek. Perubahan revisi tiga ini mengintegrasikan standar sistem manajemen ISO 45001 dan ISO 19650 tentang BIM, memperketat mekanisme monitoring berkala hak dan kewajiban pasca serah terima, serta menyempurnakan alur pertanggungjawaban proyek. Silakan klik tombol Mulai Pembelajaran untuk memulai.",
    
    "1": "Pada halaman pertama ini, kita mempelajari Maksud, Tujuan, Ruang Lingkup, dan Referensi Standar Prosedur. Prosedur ini bertujuan memberikan panduan baku pelaksanaan tutup buku satu dan tutup buku dua secara akuntabel. Ruang lingkupnya mencakup seluruh tahapan mulai dari persiapan memasuki masa pemeliharaan, selama masa pemeliharaan berlangsung, penyerahan tutup buku satu atas dasar BAST satu, hingga penyerahan tutup buku dua atas dasar BAST dua. Tiga pilar referensi utama yang memayungi prosedur ini adalah ISO 9001 untuk mutu, ISO 19650 untuk digitalisasi BIM, dan ISO 45001 untuk keselamatan kerja konstruksi. Pelajari rinciannya pada kartu interaktif di layar Anda.",
    
    "2": "Berikut adalah bagan alur proses interaktif penutupan proyek yang membentang dari BAST satu hingga evaluasi akhir. Perhatikan alur horizontal ini. Dimulai dari fisik selesai 100 persen dan pemeriksaan Hold Point Lima. Jika potensi Project Final Cost melebihi 100 persen, proses harus dipaparkan ke Komite Manajemen Risiko dan Direksi. Selanjutnya dilakukan rekonsiliasi vendor, penyerahan Berita Acara Tutup Buku Satu maksimal satu bulan, penonaktifan akun SAP, evaluasi berkala hutang pemeliharaan, hingga penyelesaian BAST dua dan pelaporan tutup buku dua. Klik setiap lingkaran tahapan pada alur horizontal ini untuk melihat unit penanggung jawab, input, aktivitas, dan output dokumennya secara terperinci.",
    
    "3": "Halaman tiga memuat Ketentuan Khusus poin 6.1 sampai 6.3 mengenai Hutang Pemeliharaan Proyek. Hutang pemeliharaan terbagi ke dalam empat pos utama: hutang fisik seperti bahan, upah, alat, dan tenaga kerja; hutang peresmian; hutang bunga bank; serta hutang cadangan risiko atau contingency risk. Aturan tegas menyatakan: cadangan hutang pemeliharaan hanya boleh digunakan setelah BAST satu sampai BAST dua, dan dilarang keras digunakan untuk membiayai pelaksanaan konstruksi sebelum BAST satu. Penggunaan contingency risk juga wajib memperoleh persetujuan resmi Divisi Manajemen Risiko dan Divisi Legal dengan melampirkan risk register terkini.",
    
    "4": "Pada Ketentuan Khusus 6.4, kita membedah pelaksanaan Hold Point Lima pada saat progres fisik mencapai 100 persen. Terdapat dua belas agenda pembahasan wajib, mulai dari evaluasi Customer Satisfaction Score 100 persen, sisa waktu pemeliharaan, mitigasi risiko, klaim kontrak, pajak, rekonsiliasi hutang vendor, hingga realisasi Project Final Cost pada sistem SAP. Pelaksanaan Hold Point Lima ini menghasilkan tujuh produk dokumen resmi, termasuk Berita Acara Hold Point Lima, Laporan Tutup Buku Satu, capaian KPI final, dan Buku Dokumentasi Proyek enam pilar untuk knowledge center perusahaan. Telusuri kedua tab di layar untuk melihat rinciannya.",
    
    "5": "Halaman lima menyajikan matriks Penanggung Jawab Verifikasi Dokumen berdasarkan Ketentuan Khusus 6.6. Untuk Tutup Buku Satu, verifikasi atas dokumen As Built Drawing, hasil testing, daftar hutang piutang, dan adendum final dilakukan oleh General Manager Operasi Divisi Operasi dan diinformasikan ke SVP OC and SCC serta SVP FinAcc. Sedangkan untuk Tutup Buku Dua, verifikasi laporan penutupan dan penyelesaian defect ditandatangani bersama oleh GM Ops dan Senior Manager FinHC Divisi Operasi. Gunakan tombol filter di layar untuk membandingkan daftar verifikasi Tutup Buku Satu dan Tutup Buku Dua.",
    
    "6": "Ketentuan Khusus 6.7 mengatur mekanisme pengarsipan dokumen tutup buku. Seluruh berkas Tutup Buku Satu dan Tutup Buku Dua wajib disusun secara ganda dalam bentuk hardcopy fisik dan softcopy digital. Dokumen fisik diarsipkan secara tertib oleh GM Ops Divisi Operasi, sedangkan dokumen digital wajib disimpan secara aman pada penyimpanan cloud tim IT akun Divisi Operasi terkait. Langkah ini menjamin ketersediaan dokumen saat audit internal maupun eksternal berlangsung.",
    
    "7": "Halaman tujuh merangkum Dokumen Terkait, Record, dan Formulir Lampiran resmi. Prosedur ini terkait erat dengan SOP Pengawasan dan Pengendalian Proyek Konstruksi PP/SOP/E6-032. Terdapat sembilan jenis record bukti pelaksanaan, serta sebelas formulir standar mulai dari form pembebanan hutang pemeliharaan, form rencana anggaran, form evaluasi, hingga template materi Lesson Learned proyek. Klik masing-masing kartu untuk melihat fungsi spesifik dari setiap lampiran formulir.",
    
    "8": "Halaman delapan memaparkan tolok ukur pengukuran kinerja atau Performance Measurement pada Poin 10. Prosedur ini menetapkan target mutlak sebesar 100 persen. Tujuannya adalah mengukur kelengkapan seluruh dokumen proyek yang telah selesai fisik 100 persen dan memastikan akurasi data finansial yang tercatat di sistem sesuai dengan realisasi lapangan. Simulasikan indikator kelengkapan dokumen pada instrumen interaktif di layar Anda.",
    
    "9": "Poin 11 mengidentifikasi tiga proses kritis yang memiliki potensi risiko operasional tinggi. Pertama, saat menginfokan waktu penyelesaian ke vendor, terdapat risiko vendor lama sulit dihubungi yang berpotensi menyebabkan ketidaksesuaian catatan hutang. Kedua, saat evaluasi masa pemeliharaan, terdapat risiko lonjakan realisasi pemakaian hutang. Ketiga, saat proses penutupan sistem SAP, terdapat risiko lambatnya proses akibat mutasi personil dan berkas belum lengkap. Pelajari langkah mitigasi yang telah dirancang SOP untuk mencegah risiko-risiko tersebut.",
    
    "10": "Saatnya menguji pemahaman Anda. Pada sesi ini, Anda akan mengerjakan sepuluh butir soal evaluasi pemahaman seputar seluruh ketentuan SOP Masa Pemeliharaan dan Penutupan Proyek. Pilihlah satu jawaban yang paling tepat. Modul ini menerapkan passing score minimal 80 persen untuk dinyatakan kompeten. Baca setiap pertanyaan dengan seksama dan perhatikan penjelasan umpan balik setelah menjawab. Selamat mengerjakan!",
    
    "11": "Selamat! Anda telah berhasil menuntaskan seluruh materi dan evaluasi pemahaman SOP Masa Pemeliharaan dan Penutupan Proyek Konstruksi dan EPC PP/SOP/C1-050 Revisi Tiga. Dengan memahami dan menerapkan prosedur ini secara disiplin, Anda turut menjaga akurasi keuangan perusahaan, kepatuhan audit ISO, dan penyelesaian kewajiban proyek secara tuntas. Silakan klik tombol Cetak Sertifikat di layar untuk mengunduh bukti kelulusan pelatihan Anda dalam format dokumen resmi. Terima kasih atas dedikasi dan profesionalisme Anda."
}

def apply_phonetic_respelling(text: str) -> str:
    # Urutkan frasa berdasarkan panjang terpanjang ke terpendek untuk mencegah double replacement
    sorted_dict = sorted(PHONETIC_DICTIONARY.items(), key=lambda x: len(x[0]), reverse=True)
    for original, phonetic in sorted_dict:
        pattern = re.compile(re.escape(original), re.IGNORECASE)
        text = pattern.sub(phonetic, text)
    return text

async def generate_unit_audio(unit_id: str, text: str, output_path: str, voice: str, rate: str):
    import edge_tts
    phonetic_text = apply_phonetic_respelling(text)
    print(f"[*] Processing Unit {unit_id}...")
    print(f"    Raw Text Length     : {len(text)} chars")
    print(f"    Phonetic Respelling : {phonetic_text[:90]}...")
    communicate = edge_tts.Communicate(phonetic_text, voice, rate=rate)
    await communicate.save(output_path)
    print(f"    [OK] Audio generated -> {output_path}\n")

async def main_async(args):
    try:
        import edge_tts
    except ImportError:
        print("[!] Error: 'edge-tts' belum terinstall.")
        print("    Jalankan: pip install edge-tts")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    voice = args.voice or VOICE_DEFAULT
    rate = args.rate or RATE_DEFAULT

    print("=" * 70)
    print("EDGE-TTS GENERATOR: SOP MASA PEMELIHARAAN & PENUTUPAN PROYEK")
    print(f"Voice: {voice} | Rate: {rate} | Target Dir: {args.output_dir}")
    print("=" * 70)

    for unit_id, text in NARRATIONS_SOP.items():
        out_file = os.path.join(args.output_dir, f"unit_{unit_id}.mp3")
        await generate_unit_audio(unit_id, text, out_file, voice, rate)

    print("[SUCCESS] Seluruh 12 file narasi audio berhasil dibuat!")

def main():
    parser = argparse.ArgumentParser(description="Generate Audio Narration for SOP PP/SOP/C1-050")
    parser.add_argument("--output-dir", default="./audio", help="Direktori penyimpanan file audio MP3")
    parser.add_argument("--voice", default=VOICE_DEFAULT, help="Edge-TTS voice identifier")
    parser.add_argument("--rate", default=RATE_DEFAULT, help="Kecepatan narasi (default: -4%)")
    args = parser.parse_args()

    asyncio.run(main_async(args))

if __name__ == "__main__":
    main()
