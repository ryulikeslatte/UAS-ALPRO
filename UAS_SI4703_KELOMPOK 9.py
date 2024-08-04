import sqlite3
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns

def tabel_data_gedung():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("""CREATE TABLE IF NOT EXISTS data_gedung (
                     ID_Gedung INTEGER PRIMARY KEY,
                     nama_gedung TEXT NOT NULL,
                     harga INTEGER NOT NULL)""")
    print("Tabel 'tabel_gedung' berhasil dibuat.")
    conn_0309.commit()
    conn_0309.close()

def tabel_data_penyewa():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("""CREATE TABLE IF NOT EXISTS data_penyewa (
                     ID_Penyewa INTEGER PRIMARY KEY AUTOINCREMENT,
                     nama_penyewa TEXT NOT NULL,
                     ID_Gedung INTEGER NOT NULL,
                     nama_gedung TEXT NOT NULL,
                     tanggal DATE NOT NULL,
                     jam_mulai TIME NOT NULL,
                     durasi INTEGER NOT NULL,
                     jam_selesai TIME NOT NULL,
                     harga INTEGER NOT NULL,
                     nominal_pembayaran INTEGER NOT NULL,
                     status TEXT,
                     FOREIGN KEY (ID_Gedung) REFERENCES data_gedung (ID_Gedung),
                     FOREIGN KEY (harga) REFERENCES data_gedung(harga))""")
    print("Tabel 'data_penyewa' berhasil dibuat.")
    conn_0309.commit()
    conn_0309.close()

def tabel_data_inventaris():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("""CREATE TABLE IF NOT EXISTS data_inventaris (
                     ID_Inventaris INTEGER PRIMARY KEY AUTOINCREMENT,
                     ID_Gedung INTEGER NOT NULL,
                     nama_gedung TEXT NOT NULL,
                     tanggal DATE NOT NULL,
                     nama_barang TEXT NOT NULL,
                     harga_barang INTEGER NOT NULL,
                     jumlah_barang INTEGER NOT NULL,
                     total_harga INTEGER NOT NULL,
                     FOREIGN KEY (ID_Gedung) REFERENCES data_gedung(ID_Gedung))""")
    print("Tabel 'tabel_inventaris' berhasil dibuat.")
    conn_0309.commit()
    conn_0309.close()

def buat_gedung(ID_Gedung_0309, nama_gedung_0309, harga_0309):
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("INSERT INTO data_gedung (ID_Gedung, nama_gedung, harga) VALUES (?, ?, ?)", 
    (ID_Gedung_0309, nama_gedung_0309, harga_0309),)
    print("Data gedung telah dimasukkan ke dalam database")
    conn_0309.commit()
    conn_0309.close()

def input_data_gedung():
    #handling error id 
    while True:
        try:
            ID_Gedung_0309 = int(input("\nMasukkan ID Gedung: "))
            break
        except ValueError:
            print("ID Gedung harus berupa angka. Silakan coba lagi.")
    
    nama_gedung_0309 = input("Masukkan nama gedung: ")

    #handling error harga 
    while True:
        try:
            harga_0309 = int(input("Masukkan harga gedung: Rp"))
            break
        except ValueError:
            print("Harga Gedung harus berupa angka. Silakan coba lagi.")
    
    buat_gedung(ID_Gedung_0309, nama_gedung_0309, harga_0309)

    print(f"\nData gedung untuk '{nama_gedung_0309}' telah ditambahkan ke dalam database.")

def input_data_sewa():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    
    nama_penyewa_0309 = input("\nMasukkan nama penyewa: ")
    
    # Handling error ID Gedung 
    while True:
        try:
            ID_Gedung_0309 = int(input("Masukkan ID Gedung yang disewa : "))
            break
        except ValueError:
            print("ID Gedung harus berupa angka. Silakan masukkan kembali.")
    
    cur_0309.execute('SELECT nama_gedung, harga FROM data_gedung WHERE ID_Gedung = ?', (ID_Gedung_0309,))
    hasil_0309 = cur_0309.fetchone()
    
    if hasil_0309:
        nama_gedung_0309 = hasil_0309[0]
        
        # Handling error tanggal 
        while True:
            try:
                tanggal_0309 = input("Masukkan tanggal sewa (YYYY-MM-DD): ")
                datetime.strptime(tanggal_0309, "%Y-%m-%d")
                break
            except ValueError:
                print("Format tanggal harus sesuai dengan YYYY-MM-DD. Silakan masukkan kembali.")
        
        # Handling jam mulai 
        while True:
            try:
                jam_mulai_0309 = input("Masukkan jam mulai sewa (HH:MM): ")
                jam_mulai_datetime_0309 = datetime.strptime(jam_mulai_0309, "%H:%M")
                break
            except ValueError:
                print("Format jam mulai harus sesuai dengan HH:MM. Silakan masukkan kembali.")
        
        # Handling durasi 
        while True:
            try:
                durasi_0309 = int(input("Masukkan durasi pemakaian (dalam jam): "))
                break
            except ValueError:
                print("Durasi harus berupa angka. Silakan masukkan kembali.")
        
        harga_gedung_0309 = hasil_0309[1]
        
        # Perhitungan jam selesai
        jam_selesai_datetime_0309 = jam_mulai_datetime_0309 + timedelta(hours=durasi_0309)
        jam_selesai_0309 = jam_selesai_datetime_0309.strftime("%H:%M")

        while True:
            # Memeriksa apakah slot waktu sudah terisi
            cur_0309.execute('SELECT COUNT(*) FROM data_penyewa WHERE tanggal = ? AND ((jam_mulai <= ? AND jam_selesai > ?) OR (jam_mulai <= ? AND jam_selesai > ?))', 
                             (tanggal_0309, jam_mulai_0309, jam_mulai_0309, jam_selesai_0309, jam_selesai_0309))
            count_0309 = cur_0309.fetchone()[0]
            
            if count_0309 == 0:
                # Memeriksa nominal pembayaran
                if durasi_0309 > 5:
                    harga_user_0309 = hasil_0309[1] * durasi_0309  - hasil_0309[1] * 0.95  
                    print(f"Nominal yang harus Anda bayarkan: Rp{harga_user_0309}")
                else:
                    harga_user_0309 = hasil_0309[1] * durasi_0309 
                print(f"Nominal yang harus Anda bayarkan: Rp{harga_user_0309}")
                nominal_pembayaran_0309 = int(input("Masukkan nominal pembayaran: Rp"))
                if nominal_pembayaran_0309 >= harga_user_0309:
                    kembalian_0309 = nominal_pembayaran_0309 - harga_user_0309
                    print(f"Kembalian anda: Rp{kembalian_0309}")
                    status_0309 = "Pending"
                    
                    # Insert data penyewa
                    cur_0309.execute('INSERT INTO data_penyewa (nama_penyewa, ID_Gedung, nama_gedung, tanggal, jam_mulai, durasi, jam_selesai, harga, nominal_pembayaran, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                                     (nama_penyewa_0309, ID_Gedung_0309, nama_gedung_0309, tanggal_0309, jam_mulai_0309, durasi_0309, jam_selesai_0309, harga_gedung_0309, harga_user_0309, status_0309,))
                    cur_0309.execute("SELECT MAX(ID_Penyewa) FROM data_penyewa")
                    result_0309 = cur_0309.fetchone()
                    
                    if result_0309[0] is not None:
                        nomor_antrian_0309 = result_0309[0] 
                    else:
                        nomor_antrian_0309 = 1
                    
                    print(f"Nomor antrian/ID kamu adalah {nomor_antrian_0309}")

                    conn_0309.commit()
                    conn_0309.close()
                    break
                else:
                    print("Nominal yang anda masukkan kurang! Silakan masukkan kembali.")
            else:
                print("Slot waktu sudah terisi. Silakan pilih waktu lain.")
                while True:
                    try:
                        jam_mulai_0309 = input("Masukkan jam mulai sewa (HH:MM): ")
                        jam_mulai_datetime_0309 = datetime.strptime(jam_mulai_0309, "%H:%M")
                        break
                    except ValueError:
                        print("Format jam mulai harus sesuai dengan HH:MM. Silakan masukkan kembali.")
                while True:
                    try:
                        durasi_0309 = int(input("Masukkan durasi pemakaian (dalam jam): "))
                        break
                    except ValueError:
                        print("Durasi harus berupa angka. Silakan masukkan kembali.")
                # Perhitungan ulang jam selesai
                jam_selesai_datetime_0309 = jam_mulai_datetime_0309 + timedelta(hours=durasi_0309)
                jam_selesai_datetime_0309 = jam_selesai_datetime_0309.strftime("%H:%M")
    else:
        print(f"ID gedung {ID_Gedung_0309} tidak ditemukan. Pastikan ID gedung sudah terdaftar.")
    conn_0309.close()

def hapus_gedung(ID_Gedung_0309):
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("DELETE FROM data_gedung WHERE ID_Gedung = ?", 
                 (ID_Gedung_0309,))
    print("Data Gedung berhasil dihapus!")
    conn_0309.commit()
    conn_0309.close()

def update_data_penyewa(ID_Penyewa_0309, status_0309):
    conn_0309 =  sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("UPDATE data_penyewa SET status = ? WHERE ID_Penyewa = ?", 
                     (status_0309, ID_Penyewa_0309,))
    conn_0309.commit()
    conn_0309.close()

def search_status_sewa(ID_Penyewa_0309 : int):
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT ID_Penyewa, nama_penyewa, ID_Gedung, nama_gedung, tanggal, jam_mulai, jam_selesai, nominal_pembayaran, status FROM data_penyewa WHERE ID_Penyewa = ?", (ID_Penyewa_0309,))
    result_0309 = cur_0309.fetchall()
    tabel_0309= PrettyTable()
    tabel_0309.field_names = ["ID Penyewa", "Nama", "ID Gedung", "Nama Gedung", "Tanggal", "Jam Mulai", "Jam Selesai", "Nominal Pembayaran", "Status"]
    for baris_0309 in result_0309:
        tabel_0309.add_row(baris_0309)
    print(tabel_0309)
    conn_0309.commit()
    conn_0309.close()
    return result_0309

def search_status_bayar(ID_Penyewa_0309 : int):
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT ID_Penyewa, nama_penyewa, ID_Gedung, nama_gedung, status FROM data_penyewa WHERE ID_Penyewa = ?", (ID_Penyewa_0309,))
    result_0309 = cur_0309.fetchall()
    conn_0309.close()
    
    if result_0309:
        tabel_0309 = PrettyTable()
        tabel_0309.field_names = ["ID Penyewa", "Nama", "ID Gedung", "Nama Gedung", "Status"]
        for baris_0309 in result_0309:
            tabel_0309.add_row(baris_0309)
        print(tabel_0309)
        return result_0309
    else:
        print("ID Penyewa not found.")

def display_penyewa():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT ID_Penyewa, nama_penyewa, ID_Gedung, nama_gedung, tanggal, jam_mulai, jam_selesai, durasi, harga, nominal_pembayaran, status FROM data_penyewa")
    result_0309 = cur_0309.fetchall()
    tabel_0309 = PrettyTable()
    tabel_0309.field_names = ["ID Penyewa", "Nama", "ID Gedung", "Nama Gedung", "Tanggal", "Jam Mulai", "Jam Selesai", "Durasi", "Harga per Jam", "Total Biaya", "Status"]
    for baris in result_0309:
        tabel_0309.add_row(baris)
    print(tabel_0309)
    conn_0309.close()
    valid_ids_0309 = [row[0] for row in result_0309]
    return valid_ids_0309

def display_gedung():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT * FROM data_gedung")
    result_0309 = cur_0309.fetchall()
    if result_0309:
        tabel_0309 = PrettyTable()
        tabel_0309.field_names = ["ID Gedung", "Nama Gedung", "Harga Gedung per Jam"]
        for baris in result_0309:
            tabel_0309.add_row(baris)
        print(tabel_0309)
        conn_0309.close()
        valid_ids_0309 = [row[0] for row in result_0309]
    return valid_ids_0309

def create_inventaris():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    found_gedung_0309 = False
    
    while not found_gedung_0309:
        try:
            ID_Gedung_0309 = int(input("Masukkan ID Gedung yang disewa: "))
        except ValueError:
            print("ID Gedung harus berupa angka. Silakan masukkan kembali.")
            continue
        
        cur_0309.execute('SELECT nama_gedung FROM data_gedung WHERE ID_Gedung = ?', (ID_Gedung_0309,))
        hasil_0309 = cur_0309.fetchone()
        
        if hasil_0309:
            nama_gedung_0309 = hasil_0309[0]
            
            while True:
                tanggal_0309 = input("Masukkan tanggal sewa (YYYY-MM-DD): ")
                try:
                    datetime.strptime(tanggal_0309, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Format tanggal salah. Silakan masukkan kembali dengan format YYYY-MM-DD.")
            
            nama_barang_0309 = input("Masukkan nama barang: ")
            
            while True:
                try:
                    harga_barang_0309 = int(input("Masukkan harga satuan barang: Rp"))
                    break
                except ValueError:
                    print("Harga barang harus berupa angka. Silakan masukkan kembali.")
            
            while True:
                try:
                    jumlah_barang_0309 = int(input("Masukkan jumlah barang: "))
                    break
                except ValueError:
                    print("Jumlah barang harus berupa angka. Silakan masukkan kembali.")
            
            total_harga_0309 = harga_barang_0309 * jumlah_barang_0309
            
            cur_0309.execute('INSERT INTO data_inventaris (ID_Gedung, nama_gedung, tanggal, nama_barang, harga_barang, jumlah_barang, total_harga) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                             (ID_Gedung_0309, nama_gedung_0309, tanggal_0309, nama_barang_0309, harga_barang_0309, jumlah_barang_0309, total_harga_0309))
            conn_0309.commit()
            found_gedung_0309 = True
        else:
            print(f"ID gedung {ID_Gedung_0309} tidak ditemukan. Pastikan ID gedung sudah terdaftar.")
    
    print(f"\nData baru inventaris telah ditambahkan ke dalam database.")
    conn_0309.close()

def display_inventaris():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT * FROM data_inventaris")
    result_0309 = cur_0309.fetchall()
    tabel_0309 = PrettyTable()
    tabel_0309.field_names = ["ID Inventaris", "ID Gedung", "Nama Gedung", "Tanggal", "Nama Barang", "Harga Barang", "Jumlah Barang", "Total Harga"]
    for baris in result_0309:
        tabel_0309.add_row(baris)
    print(tabel_0309)

def histori_penyewaan():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT ID_Penyewa, nama_penyewa, ID_Gedung, nama_gedung, tanggal, jam_mulai, jam_selesai, nominal_pembayaran FROM data_penyewa WHERE status='approved'")
    result_0309 = cur_0309.fetchall()
    conn_0309.close()

    tabel_0309 = PrettyTable()
    tabel_0309.field_names = ["ID Penyewa", "Nama", "ID Gedung", "Nama Gedung", "Tanggal", "Jam Mulai", "Jam Selesai", "Total Biaya"]
    for baris in result_0309:
        tabel_0309.add_row(baris)
    print(tabel_0309)
    
    total_0309 = sum(baris[7] for baris in result_0309)
    print(f"Total pemasukan adalah: Rp{total_0309}")

def visualisasi_gedung_sering():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    
    # Visualisasi frekuensi gedung yang dipakai
    cur_0309.execute("SELECT nama_gedung, COUNT(*) FROM data_penyewa WHERE status = 'approved' GROUP BY nama_gedung")
    gedung_result_0309 = cur_0309.fetchall()
    
    gedung_0309 = [row[0] for row in gedung_result_0309]
    frekuensi_gedung_0309 = [row[1] for row in gedung_result_0309]
    
    plt.figure(figsize=(10, 6))
    plt.bar(gedung_0309, frekuensi_gedung_0309, color='skyblue')
    plt.xlabel('Nama Gedung')
    plt.ylabel('Frekuensi Penggunaan')
    plt.title('Frekuensi Penggunaan Gedung')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualisasi_rata2_durasi_penyewaan():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    
    cur_0309.execute(" SELECT nama_gedung, AVG(durasi) as rata2_durasi FROM data_penyewa WHERE status = 'approved' GROUP BY nama_gedung")
    gedung_result_0309 = cur_0309.fetchall()
    
    gedung_0309 = [row[0] for row in gedung_result_0309]
    rerata_durasi_0309 = [row[1] for row in gedung_result_0309]
    plt.figure(figsize=(10, 6))
    plt.bar(gedung_0309, rerata_durasi_0309, color='skyblue')
    plt.xlabel('Nama Gedung')
    plt.ylabel('Rata-rata Durasi Penyewaan (jam)')
    plt.title('Rata-rata Durasi Penyewaan per Gedung')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def filtering_gedung():
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute("SELECT data_gedung.ID_Gedung, data_gedung.nama_gedung, COUNT(data_penyewa.ID_Gedung) as jumlah, data_gedung.harga FROM data_penyewa JOIN data_gedung ON data_penyewa.ID_Gedung = data_gedung.ID_Gedung WHERE status = 'approved' GROUP BY data_gedung.ID_Gedung, data_gedung.nama_gedung, data_gedung.harga HAVING jumlah >= 2")
    result_0309 = cur_0309.fetchall()
    conn_0309.close()

    tabel_0309 = PrettyTable()
    tabel_0309.field_names = ["ID Gedung", "Nama Gedung", "Jumlah Peminjaman", "Harga Gedung"]
    for baris in result_0309:
        tabel_0309.add_row(baris)
    print(tabel_0309)

def visualisasi_data(x_col_0309, y_col_0309, chart_type_0309):
    conn_0309 = sqlite3.connect('sewa_gedung.db')
    cur_0309 = conn_0309.cursor()
    cur_0309.execute(f'SELECT {x_col_0309}, {y_col_0309} FROM data_penyewa')
    data_0309 = cur_0309.fetchall()
    conn_0309.close()

    if data_0309:
        df_0309 = pd.DataFrame(data_0309, columns=[x_col_0309, y_col_0309])
        plt.figure(figsize=(10, 6))
        
        if chart_type_0309 == 'bar':
            sns.barplot(data=df_0309, x=x_col_0309, y=y_col_0309)
        elif chart_type_0309 == 'line':
            sns.lineplot(data=df_0309, x=x_col_0309, y=y_col_0309)
        elif chart_type_0309 == 'scatter':
            sns.scatterplot(data=df_0309, x=x_col_0309, y=y_col_0309)
        else:
            print("Jenis chart tidak valid")
            return
        
        plt.xlabel(f'{x_col_0309}')
        plt.ylabel(f'{y_col_0309}')
        plt.title(f'Visualisasi {x_col_0309} vs {y_col_0309}')
        plt.show()
    else:
        print("Tidak ada data untuk divisualisasikan.")

def visualisasi_custom():
    x_col_0309 = input("Masukkan nama kolom untuk sumbu X: ")
    y_col_0309 = input("Masukkan nama kolom untuk sumbu Y: ")
    print("\nPilih jenis chart: ")
    print("1. Bar Chart")
    print("2. Line Chart")
    print("3. Scatter Plot")
    chart_type_input_0309 = int(input("Pilih jenis chart: "))
    
    chart_type_dict_0309 = {1: 'bar', 2: 'line', 3: 'scatter'}
    chart_type_0309 = chart_type_dict_0309.get(chart_type_input_0309, 'bar')

    visualisasi_data(x_col_0309, y_col_0309, chart_type_0309)

def input_password():
    password_0309 = input("Masukkan password: ").upper()
    return password_0309

def verifikasi_password(password_0309, role_0309):
    authenticator_0309 = {
        "admin": "PA123",   
        "finansial": "PF123",  
        "maintenance": "PM123"  
    }
    return password_0309 == authenticator_0309.get(role_0309, "")

tabel_data_gedung()
tabel_data_penyewa()
tabel_data_inventaris()

while True:
    print("\nSelamat datang di penyewaan gedung Telkom University!")
    print("Pilih Role:")
    print("1. Penyewa: membuat sewa, search status sewa")
    print("2. Administrator: create gedung, read gedung, delete gedung, update status penyewa, filtering")
    print("3. Finansial: read, visualisasi data")
    print("4. Maintenance: create inventaris, read inventaris")

    while True:
        try:
            pilih_role_0309 = int(input("Pilih role Anda: "))
            break
        except ValueError:
            print("Role harus berupa angka. Silakan masukkan kembali.")

    if pilih_role_0309 == 1:
        while True:
            print("\nMenu Penyewa: ")
            print("1. Membuat reservasi sewa gedung")
            print("2. Cek status penyewaan")
            print("0. Kembali ke menu utama")

            try:
                pilih_menu_penyewa_0309 = int(input("Pilih menu: "))
            except ValueError:
                print("Menu harus berupa angka. Silakan masukkan kembali.")
                continue

            if pilih_menu_penyewa_0309 == 1:
                display_gedung()
                input_data_sewa()
            elif pilih_menu_penyewa_0309 == 2:
                while True:
                    try:
                        ID_Penyewa_0309 = int(input("Cek status ID Penyewa: "))
                        break
                    except ValueError:
                        print("ID Penyewa harus berupa angka. Silakan masukkan kembali.")
                search_status_sewa(ID_Penyewa_0309)
            elif pilih_menu_penyewa_0309 == 0:
                break  
            else:
                print("Pilihan menu tidak valid.")
            
    elif pilih_role_0309 == 2:
        while True:
            password_0309 = input_password()
            if verifikasi_password(password_0309, "admin"):
                print("Akses diberikan")
                while True:
                    print("\nMenu Administrator: ")
                    print("1. Membuat data gedung")
                    print("2. Tampilkan seluruh data gedung")
                    print("3. Update status data penyewa")
                    print("4. Hapus data gedung (by ID)")
                    print("5. Tampilkan seluruh penyewa")
                    print("6. Filtering gedung yang sering disewa > 2")
                    print("0. Kembali ke menu utama")

                    try:
                        pilih_menu_administrator_0309 = int(input("Pilih menu: "))
                    except ValueError:
                        print("Menu harus berupa angka. Silakan masukkan kembali.")
                        continue

                    if pilih_menu_administrator_0309 == 1:
                        input_data_gedung()
                    elif pilih_menu_administrator_0309 == 2:
                        display_gedung()
                    elif pilih_menu_administrator_0309 == 3:
                        update_lanjut_0309 = True
                        while update_lanjut_0309:
                            valid_ids_0309 = display_penyewa()  # Get the list of valid IDs
                            while True:
                                try:
                                    ID_Penyewa_0309 = int(input("Masukkan ID Penyewa yang ingin diupdate: "))
                                    if ID_Penyewa_0309 in valid_ids_0309:
                                        break
                                    else:
                                        print("ID Penyewa tidak ada. Silakan masukkan ID yang valid.")
                                except ValueError:
                                    print("ID Penyewa harus berupa angka. Silakan masukkan kembali.")
                            
                            while True:
                                status_0309 = input("Masukkan status (rejected/approved): ").strip().lower()
                                if status_0309 in ["rejected", "approved"]:
                                    break
                                else:
                                    print("Status harus 'approved' atau 'rejected'. Silakan masukkan kembali.")
                            
                            update_data_penyewa(ID_Penyewa_0309, status_0309)
                            valid_ids = display_penyewa()  # Update the list of valid IDs
                            
                            while True:
                                update_lagi_0309 = input("Apakah ingin update lagi (y/n)?: ").strip().lower()
                                if update_lagi_0309 == 'y':
                                    break  # Kembali ke loop utama untuk update lagi
                                elif update_lagi_0309 == 'n':
                                    update_lanjut_0309 = False  # Menghentikan loop utama
                                    break
                                else:
                                    print("Input tidak valid. Silakan masukkan 'y' untuk yes atau 'n' untuk no.")

                    elif pilih_menu_administrator_0309 == 4:
                        valid_ids_0309 = display_gedung()  
                        while True:
                            try:
                                ID_Gedung_0309 = int(input("Masukkan ID Gedung yang ingin dihapus: "))
                                if ID_Gedung_0309 in valid_ids_0309:
                                    break
                                else:
                                    print("ID Gedung tidak ada. Silakan masukkan ID Gedung yang tersedia.")
                            except ValueError:
                                print("ID Gedung harus berupa angka. Silakan masukkan kembali.")
                        hapus_gedung(ID_Gedung_0309)
                        display_gedung()
                    elif pilih_menu_administrator_0309 == 5:
                        display_penyewa()
                    elif pilih_menu_administrator_0309 == 6:
                        filtering_gedung()
                    elif pilih_menu_administrator_0309 == 0:
                        break
                    else:
                        print("Pilihan menu tidak valid.")
                break
            else:
                print("Akses ditolak, masukkan password yang sesuai!")
    
    elif pilih_role_0309 == 3:
        while True:
            password_0309 = input_password()
            if verifikasi_password(password_0309, "finansial"):
                print("Akses diberikan")
                while True:
                    print("\nMenu Finansial: ")
                    print("1. Cek status pembayaran penyewa")
                    print("2. Histori pembayaran")
                    print("3. Visualisasi gedung yang sering disewa")
                    print("4. Visualisasi rata2 durasi penyewaan per gedung")
                    print("5. Visualisasi custom")
                    print("0. Kembali ke menu utama")
                    try:
                        pilih_menu_finansial_0309 = int(input("Pilih menu: "))
                    except ValueError:
                        print("Menu harus berupa angka. Silakan masukkan kembali.")
                        continue
                    if pilih_menu_finansial_0309 == 1:
                        while True:
                            try:
                                ID_Penyewa_0309 = int(input("Masukkan ID Penyewa yang akan dicek statusnya: "))
                                search_status_bayar(ID_Penyewa_0309)
                                break
                            except ValueError:
                                print("ID Penyewa harus berupa angka. Silakan masukkan kembali.")
                    elif pilih_menu_finansial_0309 == 2:
                        histori_penyewaan()
                    elif pilih_menu_finansial_0309 == 3:
                        visualisasi_gedung_sering()
                    elif pilih_menu_finansial_0309 == 4:
                        visualisasi_rata2_durasi_penyewaan()
                    elif pilih_menu_finansial_0309 == 5:
                        visualisasi_custom()
                    elif pilih_menu_finansial_0309 == 0:
                        break
                    else:
                        print("Pilihan menu tidak valid.")
                break
            else:
                print("Akses ditolak, masukkan password yang sesuai!")
            
    elif pilih_role_0309 == 4:
        while True:
            password_0309 = input_password()
            if verifikasi_password(password_0309, "maintenance"):
                print("Akses diberikan")
                while True:
                    print("\nMenu Maintenance: ")
                    print("1. Menambahkan inventaris yang rusak")
                    print("2. Histori penambahan inventaris")
                    print("0. Kembali ke menu utama")
                    try:
                        pilih_menu_maintenance_0309 = int(input("Pilih menu: "))
                    except ValueError:
                        print("Menu harus berupa angka. Silakan masukkan kembali.")
                        continue
                    if pilih_menu_maintenance_0309 == 1:
                        display_gedung()
                        create_inventaris()
                    elif pilih_menu_maintenance_0309 == 2:
                        display_inventaris()
                        
                    elif pilih_menu_maintenance_0309 == 0:
                        break
                    else:
                        print("Pilihan menu tidak valid.")
                break
            else:
                print("Akses ditolak, masukkan password yang sesuai!")
    else:
        print("Pilihan role tidak valid.")
        
    