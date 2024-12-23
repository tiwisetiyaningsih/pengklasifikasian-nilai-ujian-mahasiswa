import streamlit as st
import time
import pandas as pd

# Fungsi Bubble Sort (Iteratif)
def bubble_sort(mahasiswa):
    n = len(mahasiswa)
    for i in range(n):
        for j in range(0, n-i-1):
            if mahasiswa[j]['nilai'] < mahasiswa[j+1]['nilai']:  # Urutkan dari yang tertinggi
                mahasiswa[j], mahasiswa[j+1] = mahasiswa[j+1], mahasiswa[j]
    return mahasiswa

# Fungsi Merge Sort (Rekursif)
def merge_sort(mahasiswa):
    if len(mahasiswa) > 1:
        mid = len(mahasiswa) // 2
        left_half = mahasiswa[:mid]
        right_half = mahasiswa[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i]['nilai'] > right_half[j]['nilai']:
                mahasiswa[k] = left_half[i]
                i += 1
            else:
                mahasiswa[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            mahasiswa[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            mahasiswa[k] = right_half[j]
            j += 1
            k += 1

    return mahasiswa

# Fungsi untuk menghitung efisiensi waktu eksekusi (dalam milidetik)
def hitung_efisiensi(algoritma, mahasiswa):
    start_time = time.time()
    algoritma(mahasiswa)
    end_time = time.time()
    return (end_time - start_time) * 1000  # Konversi ke milidetik

# Streamlit UI
st.title("Pengklasifikasian Nilai Ujian Mahasiswa")

st.write("""
Masukkan data mahasiswa (format: Nama, Nilai, Passing Grade) dan tekan tombol untuk mengurutkan.
""")

# Input data mahasiswa
data_input = st.text_area("Masukkan Data Mahasiswa (Format: Nama, Nilai, Passing Grade)", height=200)

# Proses data saat tombol ditekan
if st.button("Proses Data"):
    mahasiswa_data = data_input.splitlines()

    mahasiswa = []
    for data in mahasiswa_data:
        parts = data.split(",")
        if len(parts) == 3:
            nama, nilai, passing_grade = parts
            mahasiswa.append({
                'nama': nama.strip(),
                'nilai': float(nilai.strip()),
                'passing_grade': int(passing_grade.strip())
            })

    # Memfilter mahasiswa yang memenuhi passing grade
    mahasiswa_valid = [m for m in mahasiswa if m['nilai'] >= m['passing_grade']]

    # Menghitung waktu eksekusi Bubble Sort
    bubble_sort_mahasiswa = mahasiswa_valid.copy()
    bubble_sort_time = hitung_efisiensi(bubble_sort, bubble_sort_mahasiswa)

    # Menghitung waktu eksekusi Merge Sort
    merge_sort_mahasiswa = mahasiswa_valid.copy()
    merge_sort_time = hitung_efisiensi(merge_sort, merge_sort_mahasiswa)

    # Tampilkan waktu eksekusi dan hasil pengurutan
    st.write(f"**Waktu Eksekusi:**")
    st.write(f"Bubble Sort: {bubble_sort_time:.2f} ms")
    st.write(f"Merge Sort: {merge_sort_time:.2f} ms")

    # Hasil Bubble Sort
    st.write("**Hasil Pengurutan (Bubble Sort):**")
    bubble_sort_df = pd.DataFrame(bubble_sort_mahasiswa)
    bubble_sort_df['Status'] = bubble_sort_df['nilai'].apply(lambda x: 'Lulus' if x >= 70 else 'Tidak Lulus')
    st.dataframe(bubble_sort_df)

    # Hasil Merge Sort
    st.write("**Hasil Pengurutan (Merge Sort):**")
    merge_sort_df = pd.DataFrame(merge_sort_mahasiswa)
    merge_sort_df['Status'] = merge_sort_df['nilai'].apply(lambda x: 'Lulus' if x >= 70 else 'Tidak Lulus')
    st.dataframe(merge_sort_df)

    # Grafik waktu eksekusi
    st.write("**Perbandingan Waktu Eksekusi Algoritma**")
    st.bar_chart({
        'Bubble Sort': bubble_sort_time,
        'Merge Sort': merge_sort_time
    })

    # Kesimpulan Lulus dan Tidak Lulus
    total_mahasiswa = len(mahasiswa)
    lulus = len([m for m in mahasiswa if m['nilai'] >= 70])
    tidak_lulus = total_mahasiswa - lulus

    st.write(f"### Kesimpulan:")
    st.write(f"Jumlah Mahasiswa: {total_mahasiswa}")
    st.write(f"Mahasiswa Lulus: {lulus}")
    st.write(f"Mahasiswa Tidak Lulus: {tidak_lulus}")

# Menambahkan Footer
st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.markdown("🤍🥰 &copy; 2024 @tiwias_aisyqur 🥰🤍", unsafe_allow_html=True)
