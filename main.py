import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Laporan Kas Kelas 7 SMPI AL-HAYAN", layout="centered")
st.title("📘 Laporan Kas Kelas 7 SMPI AL-HAYAN")

# Inisialisasi session
if "kas_data" not in st.session_state:
    st.session_state.kas_data = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Tambah atau edit data
st.subheader("➕ Tambah / ✏️ Edit Data Kas")
with st.form("form_kas", clear_on_submit=True):
    if st.session_state.edit_index is not None:
        # Ambil data lama untuk diedit
        data_edit = st.session_state.kas_data[st.session_state.edit_index]
        nama = st.text_input("Nama Siswa", value=data_edit["Nama"])
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"], index=["Senin", "Selasa", "Rabu", "Kamis", "Jumat"].index(data_edit["Hari"]))
        kas_masuk = st.number_input("Uang Kas Masuk (Rp)", min_value=0, value=data_edit["Kas Masuk"])
        pengeluaran = st.text_input("Keterangan Pengeluaran", value=data_edit["Pengeluaran"])
        biaya_keluar = st.number_input("Biaya Keluar (Rp)", min_value=0, value=data_edit["Biaya Keluar"])
        submit_label = "Simpan Perubahan"
    else:
        nama = st.text_input("Nama Siswa")
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
        kas_masuk = st.number_input("Uang Kas Masuk (Rp)", min_value=0)
        pengeluaran = st.text_input("Keterangan Pengeluaran (jika ada)")
        biaya_keluar = st.number_input("Biaya Keluar (Rp)", min_value=0)
        submit_label = "Tambah"

    submitted = st.form_submit_button(submit_label)

    if submitted:
        new_data = {
            "Nama": nama,
            "Hari": hari,
            "Kas Masuk": kas_masuk,
            "Pengeluaran": pengeluaran,
            "Biaya Keluar": biaya_keluar
        }

        if st.session_state.edit_index is not None:
            st.session_state.kas_data[st.session_state.edit_index] = new_data
            st.success("✅ Data berhasil diperbarui!")
            st.session_state.edit_index = None
        else:
            st.session_state.kas_data.append(new_data)
            st.success("✅ Data kas berhasil ditambahkan!")

# Tampilkan data
if st.session_state.kas_data:
    df_kas = pd.DataFrame(st.session_state.kas_data)

    st.subheader("📋 Rekap Data Kas")
    st.dataframe(df_kas)

    # Pilih baris untuk diedit
    st.subheader("✏️ Edit Data")
    edit_options = [f"{i + 1}. {row['Nama']} ({row['Hari']})" for i, row in df_kas.iterrows()]
    selected_row = st.selectbox("Pilih baris yang mau diedit", options=["Pilih..."] + edit_options)

    if selected_row != "Pilih...":
        row_index = edit_options.index(selected_row)
        if st.button("Edit Data Ini"):
            st.session_state.edit_index = row_index
            st.experimental_rerun()

    # Ringkasan
    st.subheader("💰 Ringkasan Kas")
    total_masuk = df_kas["Kas Masuk"].sum()
    total_keluar = df_kas["Biaya Keluar"].sum()
    saldo_akhir = total_masuk - total_keluar

    st.metric("Total Kas Masuk", f"Rp {total_masuk:,.0f}")
    st.metric("Total Biaya Keluar", f"Rp {total_keluar:,.0f}")
    st.metric("Saldo Akhir", f"Rp {saldo_akhir:,.0f}")

    # Unduh laporan Excel
    st.subheader("⬇️ Unduh Laporan")
    output = BytesIO()
    df_kas.to_excel(output, index=False)
    st.download_button("📥 Unduh Laporan (.xlsx)",
                       data=output.getvalue(),
                       file_name="laporan_kas_kelas7.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.info("Belum ada data kas. Tambahkan data terlebih dahulu.")
