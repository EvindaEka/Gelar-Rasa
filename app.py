import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px
import plotly.graph_objects as go

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Dashboard Analisis Finansial Generasi Z Indonesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* {font-family: 'Inter', sans-serif;}
.stApp {background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);}
.main .block-container {padding-top: 0; padding-bottom: 0; max-width: 100%;}

.dashboard-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem; border-bottom: 4px solid #e74c3c;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.dashboard-header h1 {
    color: white; font-size: 2.2rem; font-weight: 700;
    text-align: center; margin: 0;
}
.dashboard-subheader {
    background: rgba(255,255,255,0.95); padding: 1rem 2rem;
    border-bottom: 2px solid #bdc3c7; text-align: center;
    font-weight: 600; color: #2c3e50;
}
.stat-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 2px solid #e0e6ed; border-radius: 10px;
    padding: 1.2rem 1rem; text-align: center;
    transition: all 0.3s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.stat-card:hover {transform: translateY(-3px);}
.stat-value {font-size: 1.6rem; font-weight: 700; color: #1e3c72;}
.stat-label {font-size: 0.85rem; color: #7f8c8d;}
.section-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 1rem 1.5rem; margin: 1rem 0 0.5rem 0; border-radius: 12px;
}
.section-header h3 {color: white; font-size: 1.1rem; margin: 0;}
.insight-box {
    background: linear-gradient(135deg, #e8f4f8 0%, #d1e7f4 100%);
    padding: 1.2rem; border-radius: 8px; border-left: 4px solid #1e3c72;
    margin: 0.8rem 0;
}
.insight-box h4 {color: #2c3e50; font-weight: 600; font-size: 0.95rem;}
.insight-box p {color: #34495e; font-size: 0.85rem; margin: 0.3rem 0;}
            
/* === SIDEBAR COLOR THEME === */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
}

section[data-testid="stSidebar"] .css-1wvsk86, 
section[data-testid="stSidebar"] .css-1d391kg {
    color: white !important;
}

/* Label di sidebar */
section[data-testid="stSidebar"] label {
    color: #e8eefc !important;
    font-weight: 600;
}

/* Selectbox background & text */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.15);
    color: white !important;
    border-radius: 8px;
}

/* Header Filter */
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

</style>""", unsafe_allow_html=True)

# ==================== FUNGSI PEMBERSIHAN ====================
def parse_rupiah_range(value):
    if pd.isna(value):
        return np.nan
    value = str(value).replace("Rp", "").replace(".", "").replace(",", "").strip()
    if "-" in value:
        parts = re.split(r"[-–]", value)
        try:
            nums = [int(p.strip()) for p in parts if p.strip().isdigit()]
            if len(nums) == 2:
                return np.mean(nums)
        except:
            return np.nan
    elif value.isdigit():
        return float(value)
    else:
        return np.nan

# ==================== LOAD DATA ====================
@st.cache_data
def load_data():
    paths = {
        "profile": "D:/Gelar Rasa/Dashboard Analysis/GenZ_Financial_Profile.csv",
        "literacy": "D:/Gelar Rasa/Dashboard Analysis/GenZ_Financial_Literacy_Survey.csv",
        "regional": "D:/Gelar Rasa/Dashboard Analysis/Regional_Economic_Indicators.csv",
    }

    def read_file(path):
        try:
            return pd.read_csv(path, delimiter=";", encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(path, delimiter=";", encoding="ISO-8859-1")

    df_profile = read_file(paths["profile"])
    df_literacy = read_file(paths["literacy"])
    df_regional = read_file(paths["regional"])

    return df_profile, df_literacy, df_regional

df_profile, df_literacy, df_regional = load_data()

# ==================== PEMBERSIHAN DATA ====================
df_profile["avg_monthly_income"] = df_profile["avg_monthly_income"].apply(parse_rupiah_range)
df_profile["avg_monthly_expense"] = df_profile["avg_monthly_expense"].apply(parse_rupiah_range)

# ==================== PEMBERSIHAN DATA REGIONAL ====================
df_regional.columns = df_regional.columns.str.strip().str.lower()

# Ubah nama kolom agar konsisten
df_regional = df_regional.rename(columns={
    "provinsi": "province",
    "jumlah rekening penerima pinjaman aktif (entitas)": "active_loan_accounts",
    "jumlah dana yang diberikan (rp miliar)": "loan_amount_billion",
    "jumlah rekening pemberi pinjaman (akun)": "lender_accounts",
    "twp 90%": "twp_90",
    "jumlah penerima pinjaman (akun)": "borrowers",
    "outstanding pinjaman (rp miliar)": "outstanding_billion",
    "jumlah penduduk (ribu)": "population_thousand",
    "pdrb (ribu rp)": "pdrb_thousand_rp",
    "urbanisasi (%)": "urbanization_rate"
})

# Bersihkan isi kolom numerik dari karakter selain angka dan titik
num_cols = [
    "loan_amount_billion",
    "outstanding_billion",
    "population_thousand",
    "pdrb_thousand_rp",
    "urbanization_rate"
]

for col in num_cols:
    if col in df_regional.columns:
        df_regional[col] = (
            df_regional[col]
            .astype(str)
            .str.replace(r"[^\d,\.]", "", regex=True)  # hapus karakter aneh
            .str.replace(",", ".", regex=False)        # ubah koma ke titik
        )
        df_regional[col] = pd.to_numeric(df_regional[col], errors="coerce")

# Hapus baris yang tidak punya nilai provinsi atau data penting
df_regional = df_regional.dropna(subset=["province", "loan_amount_billion"], how="any")

# ==================== HEADER ====================
st.markdown("""
<div class="dashboard-header">
    <h1>DASHBOARD ANALISIS FINANSIAL GENERASI Z DI INDONESIA</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="dashboard-subheader">
    Analisis Interaktif Literasi Keuangan, Perilaku Finansial, dan Indikator Ekonomi Regional
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR FILTER ====================
with st.sidebar:
    st.header("🔍 Filter Data")
    provinces = df_profile["province"].dropna().unique()
    genders = df_profile["gender"].dropna().unique()
    selected_prov = st.selectbox("Pilih Provinsi", ["Semua"] + list(provinces))
    selected_gender = st.selectbox("Pilih Jenis Kelamin", ["Semua"] + list(genders))

    st.markdown("""
    <div style="
        margin-top: 30px; 
        padding: 15px; 
        background: rgba(255,255,255,0.15); 
        border-radius: 10px;
        color: white;
    ">
        <h4 style="margin-bottom: 10px; color: #ffffff;">👥 Dibuat oleh:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #e8eefc;">
            <li>Evinda Eka Ayudia Lestari</li>
            <li>R. Aj Maria Shovia Fadinda</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

df_filtered = df_profile.copy()
if selected_prov != "Semua":
    df_filtered = df_filtered[df_filtered["province"] == selected_prov]
if selected_gender != "Semua":
    df_filtered = df_filtered[df_filtered["gender"] == selected_gender]

# ==================== QUICK STATS ====================
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='stat-card'><div class='stat-label'>Jumlah Responden</div><div class='stat-value'>{len(df_filtered)}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='stat-card'><div class='stat-label'>Rata-rata Usia</div><div class='stat-value'>{df_filtered['birth_year'].apply(lambda x: 2025-x).mean():.1f}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='stat-card'><div class='stat-label'>Pendapatan Rata-rata</div><div class='stat-value'>Rp {df_filtered['avg_monthly_income'].mean():,.0f}</div></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='stat-card'><div class='stat-label'>Pengeluaran Rata-rata</div><div class='stat-value'>Rp {df_filtered['avg_monthly_expense'].mean():,.0f}</div></div>", unsafe_allow_html=True)

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Ringkasan Umum",
    "💰 Profil Keuangan",
    "🧠 Literasi & Perilaku Keuangan",
    "📊 Indikator Ekonomi Regional"
])

# ==================== TAB 1: RINGKASAN UMUM ====================
with tab1:
    st.markdown('<div class="section-header"><h3>🗺 Distribusi Responden per Provinsi</h3></div>', unsafe_allow_html=True)
    
    # Hitung jumlah responden per provinsi
    prov_count = df_filtered["province"].value_counts().reset_index()
    prov_count.columns = ["Provinsi", "Jumlah Responden"]

    # Histogram kolom vertikal (tanpa label nilai)
    fig_prov = px.bar(
        prov_count.sort_values("Jumlah Responden", ascending=False),
        x="Provinsi",
        y="Jumlah Responden",
        color="Jumlah Responden",
        color_continuous_scale="Blues",
        title="Sebaran Responden Gen Z per Provinsi"
    )

    fig_prov.update_layout(
        xaxis_title="Provinsi",
        yaxis_title="Jumlah Responden",
        template="plotly_white",
        height=600,
        margin=dict(t=80, b=150),
        xaxis_tickangle=45,
        coloraxis_showscale=False  # sembunyikan skala warna agar lebih bersih
    )
    st.plotly_chart(fig_prov, use_container_width=True)

    # ==================== Distribusi Gender dan Pekerjaan ====================
    st.markdown('<div class="section-header"><h3>👥 Komposisi Demografis Responden</h3></div>', unsafe_allow_html=True)
    col_demo1, col_demo2 = st.columns(2)
    
    with col_demo1:
        gender_count = df_filtered["gender"].value_counts().reset_index()
        gender_count.columns = ["Gender", "Jumlah"]
        fig_gender = px.pie(
            gender_count,
            values="Jumlah",
            names="Gender",
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="Proporsi Jenis Kelamin"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col_demo2:
        if "employment_status" in df_filtered.columns:
            job_count = df_filtered["employment_status"].value_counts().reset_index()
            job_count.columns = ["Status Pekerjaan", "Jumlah"]
            fig_job = px.bar(
                job_count,
                x="Status Pekerjaan",
                y="Jumlah",
                color="Jumlah",
                color_continuous_scale="Tealgrn",
                title="Distribusi Status Pekerjaan"
            )
            fig_job.update_layout(
                xaxis_title="",
                yaxis_title="Jumlah Responden",
                template="plotly_white",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_job, use_container_width=True)

    # ==================== Insight Naratif ====================
    st.markdown(f"""
    <div class='insight-box'>
        <h4>💡 Insight Umum</h4>
        <p>Provinsi dengan jumlah responden terbanyak adalah <b>{prov_count.iloc[0,0]}</b>.</p>
        <p>Visualisasi ini memberikan gambaran awal mengenai sebaran demografis Gen Z di Indonesia.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 2 ====================
with tab2:
    # ==================== DISTRIBUSI PENDAPATAN & PENGELUARAN ====================
    st.markdown('<div class="section-header"><h3>Distribusi Pendapatan & Pengeluaran</h3></div>', unsafe_allow_html=True)

    # Ubah menjadi long/melt format
    df_melted = df_filtered.melt(
        value_vars=["avg_monthly_income", "avg_monthly_expense"],
        var_name="Jenis",
        value_name="Jumlah"
    )

    # Grouped histogram
    fig_hist = px.histogram(
        df_melted,
        x="Jumlah",
        color="Jenis",
        nbins=20,
        barmode="group",    # 👈 histogram berdampingan
        opacity=0.75,
        color_discrete_map={
            "avg_monthly_income": "#1e3c72",
            "avg_monthly_expense": "#e74c3c"
        }
    )

    fig_hist.update_layout(
        xaxis_title="Jumlah (Income / Expense)",
        yaxis_title="Frekuensi",
        legend_title="Kategori"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    # Pendapatan & Pengeluaran per Provinsi
    st.markdown('<div class="section-header"><h3>📊 Pendapatan dan Pengeluaran Rata-rata per Provinsi</h3></div>', unsafe_allow_html=True)
    df_avg = (
        df_filtered.groupby("province")[["avg_monthly_income", "avg_monthly_expense"]]
        .mean()
        .reset_index()
    )

    fig_income_expense = go.Figure()
    fig_income_expense.add_trace(go.Bar(
        x=df_avg["province"],
        y=df_avg["avg_monthly_income"],
        name="Pendapatan Rata-rata",
        marker_color="#1e3c72",
        hovertemplate="<b>%{x}</b><br>Pendapatan: Rp %{y:,.0f}<extra></extra>"
    ))
    fig_income_expense.add_trace(go.Bar(
        x=df_avg["province"],
        y=df_avg["avg_monthly_expense"],
        name="Pengeluaran Rata-rata",
        marker_color="#5dade2",  # Lighter blue
        hovertemplate="<b>%{x}</b><br>Pengeluaran: Rp %{y:,.0f}<extra></extra>"
    ))
    fig_income_expense.update_layout(
        barmode="group",
        xaxis_title="Provinsi",
        yaxis_title="Nilai (Rupiah)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        height=650,
        margin=dict(t=100, b=100),
        title_font_color="#1e3c72"
    )
    fig_income_expense.update_xaxes(tickangle=45, tickfont=dict(size=11))
    st.plotly_chart(fig_income_expense, use_container_width=True)

    # 🔸 Dua grafik berdampingan: Pengeluaran per Gender dan Penggunaan E-Wallet
    if "gender" in df_filtered.columns or "main_fintech_app" in df_filtered.columns:
        st.markdown('<div class="section-header"><h3>🚻 Rata-rata Pengeluaran per Gender & Penggunaan E-Wallet</h3></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        # Grafik 1: Pengeluaran per Gender
        with col1:
            if "gender" in df_filtered.columns:
                df_gender_exp = df_filtered.groupby("gender")["avg_monthly_expense"].mean().reset_index()
                fig_gender_exp = px.bar(
                    df_gender_exp,
                    x="gender",
                    y="avg_monthly_expense",
                    color="gender",
                    color_discrete_sequence=["#1e3c72", "#2a5298", "#5dade2"],
                    title="Rata-rata Pengeluaran Bulanan per Gender"
                )
                fig_gender_exp.update_layout(
                    xaxis_title="Gender",
                    yaxis_title="Rata-rata Pengeluaran (Rp)",
                    template="plotly_white",
                    showlegend=False,
                    title_font_color="#1e3c72"
                )
                st.plotly_chart(fig_gender_exp, use_container_width=True)

        # Grafik 2: Distribusi Penggunaan E-Wallet
        with col2:
            if "main_fintech_app" in df_filtered.columns:
                ewallet_count = df_filtered["main_fintech_app"].value_counts().reset_index()
                ewallet_count.columns = ["E-Wallet", "Jumlah Pengguna"]

                fig_ewallet = px.bar(
                    ewallet_count.sort_values("Jumlah Pengguna", ascending=True),
                    x="Jumlah Pengguna",
                    y="E-Wallet",
                    orientation="h",
                    color="E-Wallet",
                    color_discrete_sequence=["#1e3c72", "#2a5298", "#3c7dd9", "#5dade2", "#85c1e9"],
                    title="Distribusi Penggunaan E-Wallet Utama"
                )
                fig_ewallet.update_layout(
                    xaxis_title="Jumlah Responden",
                    yaxis_title="",
                    template="plotly_white",
                    showlegend=False,
                    title_font_color="#1e3c72"
                )
                st.plotly_chart(fig_ewallet, use_container_width=True)

    # ==================== HUBUNGAN PENDAPATAN VS PENGELUARAN ====================
    st.markdown('<div class="section-header"><h3>Hubungan Pendapatan vs Pengeluaran</h3></div>', unsafe_allow_html=True)

    fig5 = px.scatter(
        df_filtered,
        x="avg_monthly_income",
        y="avg_monthly_expense",
        color="gender",
        trendline="ols"
    )

    st.plotly_chart(fig5, use_container_width=True)

# ==================== TAB 3 ====================
with tab3:
    st.markdown('<div class="section-header"><h3>Analisis Literasi Keuangan</h3></div>', unsafe_allow_html=True)

    # Normalisasi nama kolom
    df_literacy.columns = df_literacy.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

    # Daftar item literasi keuangan
    literacy_items = [
        "I am able to identify risks and discrepancies and view numbers in a complex way",
        "I am able to recognize a good financial investment",
        "I am able to understand what is behind the numbers",
        "I am able to and divide it accordingly across an allotted period to the right concerned areas",
        "I am able to project the amount of cash that will be available to me in the future",
        "I am able to plan ahead to avoid impulse spending",
        "I am able to understand numbers and financial metrics",
        "I am able to understand what drives cash flow and profits",
        "I am able to understand the company's financial statements and some core performance measures",
        "Awareness about the potential of financial risk in using digital financial provider or fintech such as the legality of the fintech provider interest rate and transaction fee",
        "Having experience in using the product and service of fintech for digital payment",
        "Experience in using the product and service of fintech for financing (loan) and investment",
        "Experience in using the product and service of fintech for asset management",
        "Having a good understanding of digital payment products such as E-Debit E-Credit  E-Money   Mobile/Internet banking  E -wallet",
        "Having a good understanding of product digital asset management",
        "Having a good understanding of digital alternatives",
        "Having a good understanding of digital insurance",
        "Having a good understanding of customer rights and protection as well as the procedure to complain about the service from digital  financial providers"
    ]

    # Terjemahan item
    translations_literacy = {
        literacy_items[0]: "Kemampuan mengidentifikasi risiko dan memahami angka secara kompleks",
        literacy_items[1]: "Kemampuan mengenali investasi keuangan yang baik",
        literacy_items[2]: "Kemampuan memahami makna di balik angka",
        literacy_items[3]: "Kemampuan membagi keuangan sesuai periode dan area yang tepat",
        literacy_items[4]: "Kemampuan memperkirakan jumlah uang tunai di masa depan",
        literacy_items[5]: "Kemampuan merencanakan keuangan untuk menghindari pengeluaran impulsif",
        literacy_items[6]: "Pemahaman terhadap angka dan metrik keuangan",
        literacy_items[7]: "Pemahaman terhadap faktor yang memengaruhi arus kas dan laba",
        literacy_items[8]: "Pemahaman terhadap laporan keuangan dan indikator kinerja utama",
        literacy_items[9]: "Kesadaran terhadap risiko keuangan dalam penggunaan fintech",
        literacy_items[10]: "Pengalaman menggunakan fintech untuk pembayaran digital",
        literacy_items[11]: "Pengalaman menggunakan fintech untuk pembiayaan dan investasi",
        literacy_items[12]: "Pengalaman menggunakan fintech untuk pengelolaan aset",
        literacy_items[13]: "Pemahaman produk pembayaran digital (e-money, e-wallet, mobile banking)",
        literacy_items[14]: "Pemahaman produk pengelolaan aset digital",
        literacy_items[15]: "Pemahaman terhadap alternatif digital",
        literacy_items[16]: "Pemahaman terhadap produk asuransi digital",
        literacy_items[17]: "Pemahaman terhadap hak konsumen dan prosedur pengaduan layanan fintech"
    }

    # Pencocokan kolom fleksibel
    matched_literacy = [col for item in literacy_items for col in df_literacy.columns if item.lower().strip() in col.lower().strip()]

    if len(matched_literacy) >= 10:
        # Konversi ke numerik
        df_literacy[matched_literacy] = df_literacy[matched_literacy].apply(pd.to_numeric, errors="coerce")

        # Hitung skor rata-rata
        df_literacy["avg_literacy_score"] = df_literacy[matched_literacy].mean(axis=1)
        avg_literacy = df_literacy["avg_literacy_score"].mean()

        avg_scores = df_literacy[matched_literacy].mean().sort_values(ascending=False).reset_index()
        avg_scores.columns = ["Aspek", "Rata-rata Skor"]

        # Ringkasan umum
        st.markdown(f"""
        <div class='insight-box'>
            <h4>📚 Rangkuman Literasi Keuangan</h4>
            <p>Rata-rata skor literasi keuangan responden adalah <b>{avg_literacy:.2f}</b> dari 4.</p>
            <p>Nilai ini mencerminkan tingkat pemahaman Gen Z terhadap konsep, risiko, dan produk keuangan digital.</p>
        </div>
        """, unsafe_allow_html=True)

        # Visualisasi
        fig_lit = px.bar(
            avg_scores,
            x="Rata-rata Skor",
            y="Aspek",
            orientation="h",
            color="Rata-rata Skor",
            color_continuous_scale="Blues",
            title="Rata-rata Skor per Aspek Literasi Keuangan"
        )
        fig_lit.update_layout(template="plotly_white", xaxis_title="Skor (1–4)", yaxis_title="")
        st.plotly_chart(fig_lit, use_container_width=True)

        # ==================== INSIGHT OTOMATIS ====================
        top_aspect = avg_scores.iloc[0]["Aspek"]
        low_aspect = avg_scores.iloc[-1]["Aspek"]

        top_trans = translations_literacy.get(top_aspect, top_aspect)
        low_trans = translations_literacy.get(low_aspect, low_aspect)

        top_mean = avg_scores.iloc[0]["Rata-rata Skor"]
        low_mean = avg_scores.iloc[-1]["Rata-rata Skor"]

        # Interpretasi otomatis
        if top_mean >= 3.5:
            top_note = "menunjukkan bahwa responden memiliki pemahaman yang sangat baik dalam aspek ini."
        elif top_mean >= 2.8:
            top_note = "menggambarkan bahwa responden cukup memahami aspek ini, meski masih bisa ditingkatkan."
        else:
            top_note = "menunjukkan bahwa pemahaman responden dalam aspek ini masih perlu diperkuat."

        if low_mean <= 2:
            low_note = "menandakan bahwa aspek ini merupakan kelemahan utama yang memerlukan peningkatan signifikan."
        elif low_mean <= 2.8:
            low_note = "menunjukkan bahwa pemahaman responden di aspek ini masih terbatas."
        else:
            low_note = "menandakan tingkat pemahaman yang sedang pada aspek ini."

        # Insight naratif yang natural
        st.markdown(f"""
        <div class='insight-box'>
            <h4>💡 Insight Utama Literasi Keuangan</h4>
            <p><b>Aspek tertinggi:</b> {top_trans} (<b>{top_mean:.2f}</b>) — {top_note}</p>
            <p><b>Aspek terendah:</b> {low_trans} (<b>{low_mean:.2f}</b>) — {low_note}</p>
            <hr>
            <p>Secara keseluruhan, hasil ini menunjukkan bahwa <b>Gen Z unggul dalam {top_trans.lower()}</b>, 
            namun masih perlu penguatan dalam <b>{low_trans.lower()}</b>. 
            Hal ini menandakan perlunya peningkatan <b>edukasi literasi digital, pemahaman risiko finansial, dan keterampilan pengelolaan keuangan</b> agar Gen Z mampu membuat keputusan finansial yang lebih bijak dan strategis di era digital.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Kolom literasi keuangan tidak lengkap ditemukan dalam dataset.")

    st.markdown('<div class="section-header"><h3>Analisis Perilaku & Pengambilan Keputusan Keuangan</h3></div>', unsafe_allow_html=True)

    # Normalisasi kolom
    df_literacy.columns = df_literacy.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

    # ==================== DEFINISI ITEM ====================
    behavior_items = [
        "I take part in domestic expense planning", "I usually have a critical view of the way my friends deal with money",
        "I like to participate in family decision making when we buy something expensive for home",
        "I advise others on money matters", "I always try to save some money to do things I really like",
        "I always like to negotiate prices when I buy", "I suggest at home that we keep money aside for emergencies",
        "I keep an eye on promotions and discounts", "I like to think thoroughly before deciding to buy something",
        "I like to research prices whenever I buy something", "I pay attention to news about the economy as it may affect my family",
        "I often do things without giving them much thought", "I am impulsive", "I say things before I have thought them through"
    ]

    decision_items = [
        "I am able to quickly change my financial decisions as per the changes in circumstance",
        "Appraise of personal risk helps me in better financial decision making",
        "I make sound financial decision by comparing results over the time",
        "I make sound financial decisions by comparing results over expenses involved",
        "I am able to search for economic options during financial decision making",
        "I am able to foresee the long term and short-term consequences of the financial decisions I undertake",
        "Previously used decision strategies help me in better financial decision making",
        "I am becoming financially secure", "I am securing my financial future",
        "I will achieve the financial goals that I have set for myself",
        "I have saved (or will be able to save) enough money to last me to the end of my life",
        "Because of my money situation I feel I will never have the things I want in life",
        "I am behind with my finances", "My finances control my life",
        "Whenever I feel in control of my finances something happens that sets me back",
        "I am unable to enjoy life because I obsess too much about money"
    ]

    combined_items = behavior_items + decision_items

    # ==================== TRANSLASI ====================
    translations_behavior = {
        "I take part in domestic expense planning": "Berpartisipasi dalam perencanaan pengeluaran rumah tangga",
        "I usually have a critical view of the way my friends deal with money": "Memiliki pandangan kritis terhadap cara teman mengelola uang",
        "I like to participate in family decision making when we buy something expensive for home": "Terlibat dalam keputusan pembelian besar keluarga",
        "I advise others on money matters": "Memberi nasihat kepada orang lain tentang uang",
        "I always try to save some money to do things I really like": "Selalu mencoba menabung untuk hal yang disukai",
        "I always like to negotiate prices when I buy": "Suka menawar harga saat membeli",
        "I suggest at home that we keep money aside for emergencies": "Menyarankan menabung untuk keadaan darurat",
        "I keep an eye on promotions and discounts": "Memperhatikan promo dan diskon",
        "I like to think thoroughly before deciding to buy something": "Berpikir matang sebelum membeli",
        "I like to research prices whenever I buy something": "Membandingkan harga sebelum membeli",
        "I pay attention to news about the economy as it may affect my family": "Memperhatikan berita ekonomi yang berdampak pada keluarga",
        "I am impulsive": "Cenderung impulsif",
        "I often do things without giving them much thought": "Melakukan hal tanpa berpikir panjang",
        "I say things before I have thought them through": "Sering bertindak sebelum mempertimbangkan dampaknya",
        "I am unable to enjoy life because I obsess too much about money": "Sulit menikmati hidup karena terlalu fokus pada uang",
        "I am able to foresee the long term and short-term consequences of the financial decisions I undertake": "Mampu memperkirakan dampak jangka pendek dan panjang keputusan keuangan",
        "I am becoming financially secure": "Mulai mencapai kestabilan finansial",
        "I am securing my financial future": "Menjamin masa depan finansial",
        "I will achieve the financial goals that I have set for myself": "Berkomitmen mencapai tujuan finansial pribadi"
    }

    # ==================== PENCARIAN KOLOM ====================
    matched_behavior = []
    for item in combined_items:
        match = [col for col in df_literacy.columns if item.lower().strip() in col.lower().strip()]
        if match:
            matched_behavior.append(match[0])

    # ==================== ANALISIS ====================
    if len(matched_behavior) >= 10:
        # Konversi semua kolom ke numerik agar bisa dihitung
        df_literacy[matched_behavior] = df_literacy[matched_behavior].apply(pd.to_numeric, errors="coerce")

        # Hitung skor rata-rata per responden dan per aspek
        df_literacy["avg_behavior_score"] = df_literacy[matched_behavior].mean(axis=1)
        avg_behavior = df_literacy["avg_behavior_score"].mean()
        avg_scores_b = df_literacy[matched_behavior].mean().sort_values(ascending=False).reset_index()
        avg_scores_b.columns = ["Aspek", "Rata-rata Skor"]
        avg_scores_b["Rata-rata Skor"] = avg_scores_b["Rata-rata Skor"].fillna(0)

        # ==================== VISUALISASI ====================
        st.markdown(f"""
        <div class='insight-box'>
            <h4>💰 Rangkuman Perilaku & Pengambilan Keputusan Keuangan</h4>
            <p>Rata-rata skor adalah <b>{avg_behavior:.2f}</b> dari 4.</p>
            <p>Menunjukkan sejauh mana Gen Z menerapkan kebiasaan keuangan sehat dan kemampuan mengambil keputusan finansial yang bijak.</p>
        </div>
        """, unsafe_allow_html=True)

        fig_beh = px.bar(
            avg_scores_b,
            x="Rata-rata Skor", y="Aspek",
            orientation="h", color="Rata-rata Skor", color_continuous_scale="Greens",
            title="Rata-rata Skor per Aspek Perilaku & Keputusan Keuangan"
        )
        fig_beh.update_layout(template="plotly_white", xaxis_title="Skor (1–4)", yaxis_title="")
        st.plotly_chart(fig_beh, use_container_width=True)

        # ==================== INSIGHT OTOMATIS ====================
        top_aspect_b = avg_scores_b.iloc[0]["Aspek"]
        low_aspect_b = avg_scores_b.iloc[-1]["Aspek"]
        top_trans = translations_behavior.get(top_aspect_b, top_aspect_b)
        low_trans = translations_behavior.get(low_aspect_b, low_aspect_b)

        top_mean = avg_scores_b.iloc[0]["Rata-rata Skor"]
        low_mean = avg_scores_b.iloc[-1]["Rata-rata Skor"]

        st.markdown(f"""
        <div class='insight-box'>
            <h4>💡 Insight Utama</h4>
            <p><b>Aspek tertinggi:</b> {top_trans} (<b>{top_mean:.2f}</b>)</p>
            <p><b>Aspek terendah:</b> {low_trans} (<b>{low_mean:.2f}</b>)</p>
            <hr>
            <p><b>Interpretasi:</b> Aspek dengan skor tertinggi menunjukkan bahwa responden Gen Z memiliki perilaku keuangan positif, seperti disiplin menabung, berpikir matang sebelum membeli, dan sadar pentingnya perencanaan keuangan.</p>
            <p>Sementara itu, aspek terendah mengindikasikan adanya tantangan dalam keseimbangan antara keuangan dan kesejahteraan emosional — misalnya stres, impulsivitas, atau kekhawatiran berlebihan terkait uang.</p>
            <p>Secara umum, hasil ini menggambarkan bahwa <b>Gen Z cukup bijak dalam keputusan finansial, tetapi masih perlu memperkuat manajemen emosi dan refleksi jangka panjang</b> agar stabilitas finansial dapat beriringan dengan kesejahteraan hidup.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Kolom perilaku dan pengambilan keputusan keuangan tidak lengkap ditemukan dalam dataset.")

# ==================== TAB 4 : INTEGRASI & ANALISIS LANJUT ====================
with tab4:

    st.markdown('<div class="section-header"><h3>📊 Analisis Lanjutan & Integrasi Dataset</h3></div>', 
                unsafe_allow_html=True)

    # =========================================================
    # RENAME KOLOM DF_REGIONAL
    # =========================================================
    df_regional = df_regional.rename(columns={
        "Provinsi": "province",
        "PDRB (Ribu Rp)": "pdrb_thousand_rp",
        "Outstanding Pinjaman (Rp miliar)": "outstanding_billion",
        "Jumlah Penerima Pinjaman (akun)": "borrowers",
        "Jumlah Dana yang Diberikan (Rp miliar)": "loan_amount_billion",
        "Urbanisasi (%)": "urbanization_rate",
        "TWP 90%": "twp_90"
    })

    # =========================================================
    # RENAME KOLOM DF_LITERACY — FIX ERROR
    # =========================================================
    if "Province of Origin" in df_literacy.columns:
        df_literacy = df_literacy.rename(columns={"Province of Origin": "province"})

    # =========================================================
    # CLEANING NUMERIC COLUMNS (ANTI ERROR)
    # =========================================================
    def clean_numeric(series):
        if series is None:
            return None
        return (
            series.astype(str)
            .str.replace(r"[^0-9\.,-]", "", regex=True)
            .str.replace(r"\.(?=.*\.)", "", regex=True)
            .str.replace(",", ".", regex=False)
            .replace("", None)
            .astype(float)
        )

    numeric_cols_regional = [
        "pdrb_thousand_rp",
        "outstanding_billion",
        "borrowers",
        "urbanization_rate",
        "loan_amount_billion",
        "twp_90"
    ]

    for col in numeric_cols_regional:
        if col in df_regional.columns:
            df_regional[col] = clean_numeric(df_regional[col])

    if "avg_monthly_income" in df_profile.columns:
        df_profile["avg_monthly_income"] = clean_numeric(df_profile["avg_monthly_income"])

    # =========================================================
    # BUAT SKOR LITERASI (RATA-RATA SEMUA ITEM SKALA 1–4)
    # =========================================================
    literacy_columns = [
        col for col in df_literacy.columns
        if df_literacy[col].dtype != "object" and col not in ["Year of Birth"]
    ]

    if len(literacy_columns) > 0:
        df_literacy["literacy_score"] = df_literacy[literacy_columns].mean(axis=1)

    # =========================================================
    # 1. CLEAN UNTUK PLOT SCATTER
    # =========================================================
    df_regional_clean = df_regional.dropna(subset=[
        "pdrb_thousand_rp",
        "outstanding_billion",
        "borrowers",
        "urbanization_rate"
    ])

    # =========================================================
    # 1. PDRB vs Outstanding Pinjaman
    # =========================================================
    st.subheader("🔵 PDRB vs Outstanding Pinjaman")

    if not df_regional_clean.empty:
        fig1 = px.scatter(
            df_regional_clean,
            x="pdrb_thousand_rp",
            y="outstanding_billion",
            size="borrowers",
            color="urbanization_rate",
            hover_name="province",
            labels={
                "pdrb_thousand_rp": "PDRB (Ribu Rp)",
                "outstanding_billion": "Outstanding Pinjaman (Rp miliar)",
                "borrowers": "Jumlah Penerima Pinjaman",
                "urbanization_rate": "Urbanisasi (%)"
            }
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Data tidak cukup untuk menampilkan scatter plot.")

    # =========================================================
    # 2. Urbanisasi vs Jumlah Dana yang Diberikan
    # =========================================================
    st.subheader("🔵 Urbanisasi vs Dana yang Diberikan")

    df_clean2 = df_regional.dropna(subset=["urbanization_rate", "loan_amount_billion"])

    if not df_clean2.empty:
        fig2 = px.scatter(
            df_clean2,
            x="urbanization_rate",
            y="loan_amount_billion",
            trendline="ols",
            color="province",
            hover_name="province",
            labels={
                "urbanization_rate": "Urbanisasi (%)",
                "loan_amount_billion": "Dana Diberikan (Rp miliar)"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Data tidak cukup untuk menampilkan scatter plot Urbanisasi vs Dana.")

            # =========================================================
    # 3. Integrasi PDRB vs Pendapatan Gen Z (Grouped Bar Chart)
    # =========================================================
    st.subheader("📌 Integrasi: PDRB vs Pendapatan Rata-rata Gen Z (Bar Chart Gabungan)")

    df_merge_profile = df_regional.merge(df_profile, on="province", how="left")
    df_merge_profile = df_merge_profile.dropna(subset=["pdrb_thousand_rp", "avg_monthly_income"])

    if not df_merge_profile.empty:
        df_plot = df_merge_profile.sort_values("pdrb_thousand_rp", ascending=False)

        df_long = pd.melt(
            df_plot,
            id_vars="province",
            value_vars=["pdrb_thousand_rp", "avg_monthly_income"],
            var_name="indikator",
            value_name="nilai"
        )

        fig3 = px.bar(
            df_long,
            x="province",
            y="nilai",
            color="indikator",
            barmode="group",
            labels={
                "province": "Provinsi",
                "nilai": "Nilai",
                "indikator": "Indikator"
            }
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Data tidak cukup untuk menampilkan integrasi PDRB vs Pendapatan Gen Z.")

    # =========================================================
    # 4. Integrasi Literasi vs Risiko Kredit (BAR CHART HORIZONTAL)
    # =========================================================
    st.subheader("📌 Integrasi: Literacy vs Risiko Kredit (TWP 90%) — Bar Chart")

    df_merge_literacy = df_regional.merge(df_literacy, on="province", how="left")
    df_merge_literacy = df_merge_literacy.dropna(subset=["literacy_score", "twp_90"])

    # Urutkan berdasarkan skor literasi tertinggi → terendah
    df_plot4 = df_merge_literacy.sort_values("literacy_score", ascending=True)

    if not df_plot4.empty:
        fig4 = px.bar(
            df_plot4,
            x="literacy_score",
            y="province",
            orientation="h",
            color="twp_90",
            hover_data=["twp_90", "outstanding_billion"],
            labels={
                "literacy_score": "Skor Literasi (1–4)",
                "province": "Provinsi",
                "twp_90": "Risiko Kredit (TWP 90%)"
            },
            color_continuous_scale="RdYlGn_r"  # Hijau = risiko rendah, Merah = tinggi
        )

        fig4.update_layout(
            xaxis_title="Skor Literasi (1–4)",
            yaxis_title="Provinsi",
            coloraxis_colorbar=dict(title="TWP 90%")
        )

        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("Data tidak cukup untuk menampilkan integrasi Literacy vs Risiko Kredit.")