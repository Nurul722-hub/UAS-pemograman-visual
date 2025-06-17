import tkinter as tk
from tkinter import messagebox
import sqlite3

# === Fungsi Koneksi & Setup Database ===
def koneksi_db():
    conn = sqlite3.connect('pembayaran.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS histori (
            nama TEXT,
            nim TEXT,
            invoice TEXT,
            jumlah INTEGER,
            metode TEXT
        )
    ''')
    conn.commit()
    conn.close()

# === Fungsi Simpan ke DB ===
def simpan_ke_db(nama, nim, invoice, jumlah, metode):
    conn = sqlite3.connect('pembayaran.db')
    c = conn.cursor()
    c.execute("INSERT INTO histori VALUES (?, ?, ?, ?, ?)", (nama, nim, invoice, jumlah, metode))
    conn.commit()
    conn.close()

# === Fungsi Ambil dari DB ===
def ambil_semua_histori():
    conn = sqlite3.connect('pembayaran.db')
    c = conn.cursor()
    c.execute("SELECT * FROM histori")
    rows = c.fetchall()
    conn.close()
    return rows

# === Fungsi Tombol Bayar ===
def bayar_sekarang():
    nama = entry_nama.get()
    nim = entry_nim.get()
    invoice = entry_invoice.get()
    jumlah = entry_jumlah.get()
    metode = metode_var.get()

    if not (nama and nim and invoice and jumlah and metode):
        messagebox.showwarning("Peringatan", "Semua data wajib diisi!")
        return

    try:
        jumlah = int(jumlah)
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus berupa angka!")
        return

    simpan_ke_db(nama, nim, invoice, jumlah, metode)
    update_histori()

    messagebox.showinfo("Sukses", f"Pembayaran berhasil!\n{nama} | NIM: {nim} | Invoice: {invoice} | Rp{jumlah} | {metode}")

# === Tampilkan Histori dari Database ===
def update_histori():
    text_histori.config(state='normal')
    text_histori.delete(1.0, tk.END)
    semua_data = ambil_semua_histori()
    for idx, data in enumerate(semua_data, 1):
        nama, nim, invoice, jumlah, metode = data
        text_histori.insert(tk.END, f"{idx}. {nama} | NIM: {nim} | Invoice: {invoice} | Rp{jumlah} | {metode}\n")
    text_histori.config(state='disabled')

# === GUI Utama ===
root = tk.Tk()
root.title("Pembayaran Ma'had")
root.geometry("420x600")

# --- Form Input ---
tk.Label(root, text="Nama Lengkap").pack()
entry_nama = tk.Entry(root)
entry_nama.pack()

tk.Label(root, text="NIM / Nomor Santri").pack()
entry_nim = tk.Entry(root)
entry_nim.pack()

tk.Label(root, text="Nomor Invoice").pack()
entry_invoice = tk.Entry(root)
entry_invoice.pack()

tk.Label(root, text="Jumlah Pembayaran (Rp)").pack()
entry_jumlah = tk.Entry(root)
entry_jumlah.pack()

# --- Metode Pembayaran ---
tk.Label(root, text="\nMetode Pembayaran").pack()
metode_var = tk.StringVar()
tk.Radiobutton(root, text="Transfer Bank", variable=metode_var, value="Transfer Bank").pack()
tk.Radiobutton(root, text="QRIS", variable=metode_var, value="QRIS").pack()
tk.Radiobutton(root, text="E-Wallet", variable=metode_var, value="E-Wallet").pack()
tk.Radiobutton(root, text="Tunai", variable=metode_var, value="Tunai").pack()

# --- Tombol Bayar ---
tk.Button(root, text="Bayar", command=bayar_sekarang, bg="green", fg="white").pack(pady=15)

# --- Histori Pembayaran ---
tk.Label(root, text="Histori Pembayaran").pack()
text_histori = tk.Text(root, height=10, width=50, state='disabled', wrap='word')
text_histori.pack(pady=5)

# === Inisialisasi ===
koneksi_db()
update_histori()
root.mainloop()
