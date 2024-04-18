# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import geopandas as gpd

st.set_page_config(
    page_title="Prediksi Keberhasilan Startup",
    page_icon="📊",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Baca dataset
dataset1 = 'big_startup_secsees_dataset.csv'
df1 = pd.read_csv(dataset1)

dataset = 'startupp (5).csv'
df = pd.read_csv(dataset)

# Sidebar untuk navigasi
with st.sidebar:
    st.header("Prediksi Keberhasilan Startup")
    page_names = ['Pengenalan', 'Visualisasi Data', "Prediksi"]
    page = st.radio('Main Menu', page_names)

# Halaman Home
if page == "Pengenalan":
    st.title("PREDIKSI KEBERHASILAN STARTUP")
    st.image('https://thereviewstories.com/wp-content/uploads/2019/01/Startup.png', use_column_width=True)
    # st.write("Halo! Selamat Datang! :wave:")
    st.write("""
             Dashboard ini berisi tentang data-data startup yang ada pada crunchbase. 
             Data tersebut kemudian diolah atau diproses untuk membuat prediksi keberhasilan startup yang nantinya dapat digunakan oleh beberapa pihak untuk menganalisis startup  yang akan atau sedang dibangun.
             """)
    st.write("""Saat ini, banyak orang berlomba-lomba untuk membangun sebuah startup. 
             Tentunya, tidak semua startup akan berhasil dan mendapat kejayaannya. 
             Banyak startup yang gagal karena tidak dapat menyusun strategi dengan baik. 
             Oleh karena itu, hasil prediksi ini dapat digunakan oleh beberapa pihak sebagai acuan dalam membangun startup.
             """)

    st.subheader("""
    Berikut adalah data Startup dari crunchbase:""")
    st.write(df1)

    st.markdown("""
                Tabel di atas memiliki 14 kolom dan 66368 baris. 
                1. **permalink**: Berisi link ke organisasi perushaan tersebut di crunchbase.
                2. **name**: Berisi nama startup.
                3. **homepage_url**: Kolom ini berisikan situs dari startup nya.
                4. **category_list**: Berisi jenis atau kategori dari startup tersebut, seperti finance, sports, dll.
                5. **funding_total_usd**: Berisi total pendaan startup dalam USD.
                6. **status**: Berisi status dari startup seperti operating, closed, acquired, dan ipo.
                7. **country_code**: Berisi kode negara dari startup.
                8. **state_code**: Berisi Kode Negara lokasi perusahaan.
                9. **region**: Berisi Wilayah lokasi perusahaan.
                10. **city**: Berisi Kota lokasi perusahaan.
                11. **funding_rounds**: Berisi jumlah putaran pendanaan startup.
                12. **founded_at**: Berisi tanggal didirikannya perusahaan/startup.
                13. **first_funding_at**: Berisi tanggal pendanaan pertama startup.
                14. **last_funding_at**: Berisi tanggal pendanaan terakhir startup.
                """)
    
    st.subheader("""
    Berikut adalah data yang sudah di mapping:""")
    st.write(df)

    st.write("""
             Data ini disesuaikan untuk keperluan prediksi. Dengan menghapus beberapa kolom yang kurang relevan dan menambah atau membuat kolom baru yang lebih relevan. 
             Dimana status dibuat menjadi 3 class atau kategori saja, yaitu Fail, Operating, dan Success. Status ipo dan acquired digabung dengan Success.
             Begitupun founded_at diganti menjadi founded_year dengan mengambil tahunnya saja. Jumlah data nya pun tidak semua digunakan, melainkan hanya menggunakan sampel sebanyak 10% secara random.
             """)

# Halaman Visualisasi Data
elif page == "Visualisasi Data":
    selected_category = st.sidebar.selectbox("Halaman",
                                             ["Distribusi Data", "Analisis Perbandingan", "Analisis Hubungan", "Analisis Komposisi"])

    if selected_category == "Distribusi Data":
        st.subheader("Jumlah Startup Berdasarkan Funding Rounds")
        plt.figure(figsize=(12,6))
        sns.barplot(x=df1['funding_rounds'].value_counts().index, y=df1['funding_rounds'].value_counts())
        plt.title('Jumlah Startup berdasarkan funding_rounds',size=18)
        plt.ylabel('Jumlah startup',size=14)
        plt.xlabel('Jumlah funding_rounds', size=14)
        plt.grid(axis='y')
        plt.yscale('log')

        def addlabels(x,y):
            for i in x:
                plt.text(i-1.25,y[i],y[i])

        addlabels(df1['funding_rounds'].value_counts().index,df1['funding_rounds'].value_counts())
        st.pyplot()

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - Sekitar 40000 lebih perusahaan melakukan pendanaan hanya 1 kali.
                    - Disusul oleh putaran pendanaan 2 kali dilakukan oleh sekitar 12000 startup.
                    - Untuk putaran pendanaan sebanyak 6 - 19 kali hanya dilakukan oleh sedikit startup.
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Mayoritas startup hanya melakukan putarann pendanaan sebanyak 1 kali atau 2 kali.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Pemangku kepentingan dapat mempertimbangkan untuk melakukan putaran pendanaan sebanyak berapa kali sesuai dengan insight yang ada.
                    """)
        #####

        st.subheader("Persebaran Lokasi Startup")
        countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        iso_counts = df1.groupby('country_code').size().reset_index(name='counts')
        merged = countries.merge(iso_counts, left_on='iso_a3', right_on='country_code')
        merged.plot(column='counts', cmap='OrRd', legend=True, figsize=(10,6))
        plt.title('Persebaran Lokasi Startup oleh Warna')
        plt.show()
        st.pyplot()

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - Persebaran yang paling menonjol ada di USA.
                    - Karena ada begitu banyak startup yang berlokasi di AS sehingga semua negara lain ditampilkan di bawah 5000.
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Mayoritas besar dari startup yang ada pada dataset berlokasi di USA.
                    - Warga negara USA sudah mulai minat dalam dunia startup.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Negara-negara yang memiliki jumlah startup yang lebih sedikit dapat mencari kemitraan dengan Amerika Serikat 
                    untuk memperluas akses mereka ke sumber daya, mentorship, dan modal. Hal ini dapat dilakukan melalui kerja sama dengan universitas, 
                    lembaga riset, dan organisasi kewirausahaan di Amerika Serikat.
                    """)

    elif selected_category == "Analisis Perbandingan":
        st.subheader("Perbandingan Jumlah Startup Berdasarkan Tahun Pendirian")
        startup_count_by_year = df['founded_year'].value_counts().sort_index()

        # Buat plot
        plt.figure(figsize=(10, 6))
        startup_count_by_year.plot(kind='bar', color='skyblue')
        plt.title('Perbandingan Jumlah Startup Berdasarkan Tahun Pendirian')
        plt.xlabel('Tahun Pendirian')
        plt.ylabel('Jumlah Startup')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Tampilkan plot
        plt.tight_layout()
        plt.show()
        st.pyplot()

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - Jumlah startup yang paling banyak ada pada sekitar tahun 2011/2012 yaitu lebih dari 2000 startup.
                    - Jumlah startup terlihat mulai meningkat pada sekitar tahun 2000an.
                    - Jumlah startup terlihat mulai menurun sekitar tahun 2012/2013.
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Pasar startup di dunia mengalami pertumbuhan yang sangat pesat dalam beberapa tahun terakhir terutama pada tahun 2011/2012. 
                    Hal ini menunjukkan bahwa semakin banyak orang yang tertarik untuk memulai startup dan ekosistem startup di dunia semakin matang.
                    - Jumlah startup yang tiba-tiba melonjak tinggi dapat disebabkan oleh beberapa faktor, seperti berkambangnya teknologi digital,
                    meningkatnya minat investor terhadap startup, dan kebijakan pemerintah yang mendukung startup.
                    - Terjadinya tren penurunan jumlah startup juga dapat disebabkan oleh beberapa faktor.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Para pemangku kepentingan perlu melakukan analisis terhadap penyebab penurunan dan pertumbuhan startup. Identifikasi faktor-faktor yang menyebabkan hal tersebut. 
                    Dengan itu, dapat menghindarkan startup dari risiko-risiko yang ada dan membuat startup semakin sukses.
                    - Jika lonjakan jumlah startup pada tahun 2011/2012 disebabkan oleh berkembangnya ekosistem startup, maka perlu diperkuat lagi faktor-faktor yang mendukung pertumbuhan tersebut. 
                    Ini termasuk memperluas infrastruktur pendukung seperti ruang kerja bersama, akses pendanaan, mentorship, dan akses pasar.
                    - Dengan mengetahui bahwa jumlah startup bisa berfluktuasi secara signifikan, penting untuk membangun startup yang tahan terhadap perubahan pasar. 
                    Fokus pada pembangunan model bisnis yang berkelanjutan, diversifikasi portofolio produk atau layanan, dan membangun hubungan yang kuat dengan pelanggan dan mitra.
                    - Para pemangku kepentingan terkait dapat menggunakan wawasan dari analisis tren ini untuk membuat keputusan yang lebih baik dalam pengembangan dan manajemen startup. 
                    Berdasarkan pemahaman tentang faktor-faktor yang memengaruhi pertumbuhan dan penurunan, perhatikan tindakan yang dapat diambil untuk meminimalkan risiko dan memaksimalkan peluang kesuksesan startup di masa depan.
                    """)

        #####

        st.subheader("Jumlah Startup dengan Status Operating berdasarkan Negara")
        operating_df = df1[df1["status"] == "operating"]
        country_counts = operating_df["country_code"].value_counts()

        plt.figure(figsize=(20, 6))
        plt.bar(country_counts.index, country_counts.values)
        plt.xlabel("Country")
        plt.ylabel("Startup dengan Status Operating")
        plt.title("Jumlah Startup dengan Status Operating berdasarkan Negara")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability

        plt.xlim(20, 0)

        plt.tight_layout()
        plt.show()
        st.pyplot()

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - Jumlah startup dengan status Operating paling banyak berada di USA, dengan jumlah hampir 30 ribu startup.
                    - Dibandingkan dengan negara lain USA memimpin sangat jauh untuk startup yang berstatus Operating.
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Banyak warga negara USA yang mulai tertarik dengan dunia startup. Terbukti dengan jumlah nya yang melonjak tinggi dibandingkan negara lain.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Negara lain dapat memperkuat kerja sama dan kemitraan dengan Amerika Serikat dalam hal teknologi, inovasi, dan pengembangan ekosistem startup.
                    - Negara lain dapat belajar dari kesuksesan ekosistem startup di Amerika Serikat untuk meningkatkan dukungan dan infrastruktur bagi para pengusaha lokal. 
                    Hal ini meliputi pendanaan yang mudah diakses, akses ke mentorship dan sumber daya, serta lingkungan bisnis yang ramah bagi inovasi dan pertumbuhan.
                    """)

    elif selected_category == "Analisis Hubungan":
        st.subheader("Hubungan Antara Funding Rounds dan Status Perusahaan")
        status_funding_counts = df.groupby(['status_class', 'funding_rounds']).size().unstack(fill_value=0)

        # Buat plot
        status_funding_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Hubungan Antara Funding Rounds dan Status Perusahaan')
        plt.xlabel('Status Perusahaan')
        plt.ylabel('Jumlah Perusahaan')
        plt.xticks(rotation=45)
        plt.legend(title='Funding Rounds')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        st.pyplot()

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - Perusahaan yang berhasil mendapatkan lebih banyak putaran pendanaan cenderung memiliki kemungkinan yang lebih tinggi untuk bertahan dan mencapai status yang lebih stabil, seperti 'Operating' atau 'Acquired'.
                    - Sementara perusahaan yang gagal mendapatkan pendanaan tambahan cenderung memiliki kemungkinan yang lebih tinggi untuk ditutup ('Closed').
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Perusahaan yang berhasil melewati beberapa putaran pendanaan umumnya memiliki potensi pertumbuhan dan kelangsungan hidup yang lebih besar. Ini menunjukkan bahwa investor percaya pada visi dan potensi bisnis perusahaan tersebut.
                    - Status perusahaan 'Closed' cenderung lebih sering terjadi pada perusahaan yang gagal mendapatkan pendanaan tambahan atau tidak mampu menghasilkan pendapatan yang cukup untuk bertahan.
                    - Perusahaan yang berhasil mencapai status 'Acquired' atau 'IPO' mungkin telah melewati beberapa putaran pendanaan yang sukses dan mampu menarik minat investor atau perusahaan lain untuk mengakuisisi mereka atau melakukan penawaran umum perdana.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Pemangku kepentingan terkait harus fokus pada upaya mendapatkan pendanaan tambahan melalui putaran pendanaan yang lebih lanjut
                    jika ingin meningkatkan kemungkinan kelangsungan hidup dan kesuksesan startup.
                    - Startup yang kesulitan mendapatkan pendanaan tambahan setelah putaran awal perlu melakukan evaluasi mendalam terhadap model bisnis, strategi pemasaran, dan kinerja operasional mereka.
                    """)

        #####

        st.subheader("Hubungan Antara Status dan Funding Rounds")
        # Hitung jumlah perusahaan dalam setiap kategori status dan putaran pendanaan
        status_funding_counts = df.groupby(['status_class', 'funding_rounds']).size().reset_index(name='Frequency')

        # Plotting
        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='funding_rounds', y='status_class', size='Frequency', sizes=(20, 1000), alpha=0.7, data=status_funding_counts)

        plt.title('Hubungan Antara Funding Rounds dan Status Perusahaan')
        plt.xlabel('Funding Rounds')
        plt.ylabel('Status Perusahaan')
        plt.grid(True)
        plt.show()
        st.pyplot()

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - jumlah putaran pendanaan dapat memberikan gambaran tentang seberapa sukses atau berkelanjutannya bisnis startup.
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Perusahaan yang masih beroperasi ('Operating') cenderung memiliki jumlah putaran pendanaan yang lebih tinggi dibandingkan dengan perusahaan yang telah ditutup ('Closed'). 
                    Ini menunjukkan bahwa jumlah putaran pendanaan bisa menjadi indikator kesuksesan dan kelangsungan hidup perusahaan.
                    - Perusahaan yang telah diakuisisi ('Acquired') atau melakukan penawaran umum perdana ('IPO') juga dapat memiliki jumlah putaran pendanaan yang signifikan. Ini menunjukkan bahwa investor dan pasar percaya pada potensi pertumbuhan dan nilai perusahaan tersebut.
                    - Perusahaan yang telah ditutup ('Closed') cenderung memiliki jumlah putaran pendanaan yang lebih rendah atau bahkan tidak ada. Ini bisa menunjukkan bahwa perusahaan tersebut mengalami kesulitan dalam mendapatkan pendanaan tambahan atau gagal menarik minat investor 
                    untuk mempertahankan operasionalnya.
                    - Ada kemungkinan bahwa perusahaan dengan jumlah putaran pendanaan yang rendah namun masih beroperasi bisa berada dalam tahap awal pengembangan atau memiliki model bisnis yang lebih mandiri.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Startup yang ingin meningkatkan kesempatan mereka untuk bertahan dan berhasil dapat mempertimbangkan untuk melakukan lebih banyak putaran pendanaan.
                    - Startup yang telah mencapai tahap yang lebih maju seperti 'Acquired' atau 'IPO' tetap harus memperhatikan manajemen keuangan dan alokasi dana dengan bijaksana. 
                    Meskipun telah mencapai kesuksesan, masih penting untuk menjaga keberlanjutan dan pertumbuhan jangka panjang.
                    - Pada startup yang menghadapi kesulitan dalam mendapatkan pendanaan tambahan, pemangku kepentingan terkait dapat melakukan evaluasi mendalam terhadap strategi bisnis mereka.
                    - Untuk startup yang sekiranya mendekati tahap Closed, harus segera mengambil langkah-langkah untuk mengatasi masalah keuangann atau operasional 
                    """)

    else:
        st.subheader("Komposisi Status Startup dalam Pie Chart")
        fig, ax = plt.subplots()
        status_counts = df1['status'].value_counts()
        colors = {'0': 'khaki', '1': 'moccasin', '2': 'lightgoldenrodyellow'}
        status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=360, colors=colors.values())
        plt.title("Persentase Status Startup")
        st.pyplot(fig)

        st.markdown("**1. Interpretasi**")
        st.markdown("""
                    - Sebanyak 79.9% startup berstatus 'Operating'.
                    - Sebanyak 9.4% startup berstatus 'Closed'.
                    - Sebanyak 8.4% startup berstatus 'Acquired'.
                    - Sebanyak 2.3% startup berstatus 'IPO'.
                    """)
        
        st.markdown("**2. Insight**")
        st.markdown("""
                    - Mayoritas startup masih beroperasi (79.9%). Menunjukkaan bahwa masih banyak perusahaan yang masih dalam tahap awal pengembangan.
                    - Masih ada risiko kegagalan untuk startup walau tidak terlalu tinggi (9.4%) dengan tutupnya perusahaan.
                    - Cukup sedikit startup yang mencapai kesuksesan melalui akuisisi (8.4%).
                    - Hanya sedikit startup yang mencapai IPO (2.3%). Menunjukkan bahwa masih banyak startup yang membutuhkan waktu dan sumber daya yang lebih baik untuk mencapai tahap pertumbuhan yang matang.
                    """)
        
        st.markdown("**3. Actionable**")
        st.markdown("""
                    - Pemerintah ataupun pemangku kepentingan terkait perlu terus memberikan dukungan kepada startup yang sedang beroperasi agar dapat terus berkembang dan dapat mencapai kesuksesan.
                    Dukungan dapat diberikan dalam bentukk pendanaan ataupun yang lainnya.
                    - Melihat masih ada risiko kegagalan walau tidak terlalu tinggi, para pemangku kepentingan terkait perlu menyusun strategi, model bisnis, keuangan, atau hal-hal lain yang sekiranya diperlukan agar tidak meraih kegagalan nantinya.
                    - Melihat masih ada peluang untuk startup diakuisisi, para pemangku kepentingan terkait perlu memperluas jaringan dan hubungan dengan perusahaan yang mungkin tertarik untuk mengakuisisi startup yang dimiliki. 
                    Dan memastikan bahwa startup yang dimiliki memiliki nilai yang jelas dan menarik bagi calon pembeli.
                    """)

# Halaman Prediksi
else:
    st.subheader("Silakan Prediksi.")
    # Dropdown untuk kolom "funding_total_usd"
    funding_total_usd = int(st.text_input('Input Funding Total in USD', 0))

    # Dropdown untuk kolom "funding_rounds"
    funding_rounds = st.selectbox('Input funding_rounds', [i for i in sorted(df['funding_rounds'].unique())])

    # Dropdown untuk kolom "founded_year"
    founded_year = st.selectbox('Input founded_year', [i for i in sorted(df['founded_year'].unique())])

    # Dropdown untuk kolom "funding_total_category"
    funding_total_category = st.selectbox('Input funding_total_category', [i for i in sorted(df['funding_total_category'].unique())])

    data = pd.DataFrame({
        'funding_total_usd': [funding_total_usd],
        'funding_rounds': [df[df['funding_rounds'] == funding_rounds].index[0]],
        'founded_year': [df[df['founded_year'] == founded_year].index[0]],
        'funding_total_category': [df[df['funding_total_category'] == funding_total_category].index[0]]
    })
    button = st.button('Predict')

    if button:

        with open ('knnnew.pkl','rb') as file:
            loaded_model = pickle.load(file)

        predicted = loaded_model.predict(data)
        
        if predicted[0] == 0:
            st.write('Fail')
        elif predicted[0] == 1:
            st.write('Operating')
        elif predicted[0] == 2:
            st.write('Success')
        else:
            st.write('Not Defined')
