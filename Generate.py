98% penyimpanan digunakan … Jika ruang penyimpanan sudah penuh, Anda tidak dapat menyimpan ke Drive, mencadangkan Google Foto, atau menggunakan Gmail. Dapatkan penyimpanan sebesar 30 GB seharga Rp 14.500,00 Rp 3.500,00/bulan untuk 3 bulan.
import pandas as pd
from faker import Faker
import random
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import os

fake = Faker('id_ID')
jumlah_kontrak = 5
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

tipe_produk = ['Motor Baru', 'Motor Bekas', 'Mobil Baru', 'Mobil Bekas']
profesi_list = ['PNS', 'Karyawan Swasta', 'Pengusaha', 'Driver Online', 'Freelancer']
status_tempat_tinggal = ['Milik Sendiri', 'Milik Keluarga', 'Sewa', 'Kontrak', 'Kost']
branch_list = ['Jakarta', 'Bandung', 'Surabaya', 'Semarang']

kontrak_data = []
pembayaran_data = []

for _ in range(jumlah_kontrak):
    nomor_kontrak = random.randint(10000000, 80000000)
    nomor_debitur = random.randint(10000000, 80000000)
    nama = fake.name()
    tanggal_lahir = fake.date_of_birth(minimum_age=21, maximum_age=55)
    tanggal_akad = fake.date_between(start_date='-2y', end_date='-1y')

    otr = random.randint(20_000_000, 80_000_000)
    dp_percent = random.uniform(0.1, 0.3)
    dp = int(otr * dp_percent)
    plafon = otr - dp

    tenor = random.choice([12, 18, 24, 30, 36])
    bunga_tahunan = random.uniform(10, 24)
    bunga_bulanan = bunga_tahunan / 12 / 100
    angsuran = round((plafon + (plafon * bunga_bulanan * tenor)) / tenor, -3)

    income = random.randint(angsuran * 2, angsuran * 4)
    bunga = round(bunga_tahunan, 2)
    tanggungan = random.randint(0, 3)
    profesi = random.choice(profesi_list)
    cmo = fake.first_name()
    branch = random.choice(branch_list)
    tempat_tinggal = random.choice(status_tempat_tinggal)

    kontrak_data.append([
        nomor_kontrak, nomor_debitur, nama, tanggal_lahir.strftime('%Y-%m-%d'),
        tanggal_akad.strftime('%Y-%m-%d'), random.choice(tipe_produk), angsuran,
        otr, dp, income, tenor, bunga, tanggungan, profesi, cmo, branch, tempat_tinggal
    ])

  
    today = datetime.today()
    periode_berjalan = (today.year - tanggal_akad.year) * 12 + today.month - tanggal_akad.month + 1
    max_periode = min(tenor, periode_berjalan + random.randint(0, 4))

    tanggal_pelunasan_terakhir = None

    for p in range(1, max_periode + 1):
        jatuh_tempo = tanggal_akad + relativedelta(months=p)

        # Pilih jenis pelunasan: tepat waktu, lebih cepat, atau terlambat
        jenis_pelunasan = random.choices(
            ['tepat_waktu', 'lebih_cepat', 'terlambat'],
            weights=[0.5, 0.2, 0.3],  # 50% tepat waktu, 20% lebih cepat, 30% terlambat
            k=1
        )[0]

        if jenis_pelunasan == 'tepat_waktu':
            tanggal_lunas = jatuh_tempo
        elif jenis_pelunasan == 'lebih_cepat':
            tanggal_lunas = jatuh_tempo - timedelta(days=random.randint(1, 5))
        else:  # terlambat
            tanggal_lunas = jatuh_tempo + timedelta(days=random.randint(1, 10))

        # Pastikan tanggal pelunasan tidak mundur dari sebelumnya
        if tanggal_pelunasan_terakhir and tanggal_lunas <= tanggal_pelunasan_terakhir:
            tanggal_lunas = tanggal_pelunasan_terakhir + timedelta(days=1)

        tanggal_pelunasan_terakhir = tanggal_lunas

        denda = 0 if tanggal_lunas <= jatuh_tempo else random.randint(10_000, 100_000)

        pembayaran_data.append([
            nomor_kontrak,
            p,
            jatuh_tempo.strftime('%Y-%m-%d'),
            angsuran,
            denda,
            tanggal_lunas.strftime('%Y-%m-%d')
        ])

# DataFrame
df_kontrak = pd.DataFrame(kontrak_data, columns=[
    '*Nomor Kontrak', '*Nomor Debitur', '*Nama', '*Tanggal Lahir (YYYY-MM-DD)',
    '*Tanggal Akad (YYYY-MM-DD)', '*Tipe Prodak', '*Installment', '*Agreement OTR Amount',
    '*DP', '*Income', '*tenor', '*Bunga', '*Tanggungan', '*Profesi', '*CMO (Marketer)',
    '*Branch Cabang', '*Status Tempat Tinggal'
])

df_pembayaran = pd.DataFrame(pembayaran_data, columns=[
    '*Nomor Kontrak', '*Periode', '*Jatuh Tempo', 'installment', 'Denda', 'Tanggal pelunasan'
])

# Simpan output
os.makedirs('output', exist_ok=True)
df_pembayaran.sort_values(by=['*Nomor Kontrak', '*Periode'], inplace=True)
df_kontrak.to_csv(f"output/[{current_time}] Template_Import_Kontrak.csv", index=False, sep=';')
df_pembayaran.to_csv(f"output/[{current_time}] Template_Import_Detailpembayaran.csv", index=False, sep=';')

print(f"✅ Data berhasil disimpan dengan timestamp {current_time}")
print(f"Kontrak: {len(df_kontrak)} | Pembayaran: {len(df_pembayaran)}")