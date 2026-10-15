import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="E-Commerce Public Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Brazil States Full Name Mapping
BRAZIL_STATES = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
}

# Path fallback: works both from project root and from inside dashboard/
@st.cache_data
def load_data():
    paths = ["main_data.csv", os.path.join("dashboard", "main_data.csv")]
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
            return df
    raise FileNotFoundError("main_data.csv tidak ditemukan.")

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# Sidebar: Filters
st.sidebar.title("Filter Data")

min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()
start_default = pd.to_datetime("2017-01-01").date() if pd.to_datetime("2017-01-01").date() >= min_date else min_date

# Date filter: dua kolom berdampingan ke samping (Dari & Sampai)
st.sidebar.markdown("**Rentang Waktu Transaksi**")
col_d1, col_d2 = st.sidebar.columns(2)
with col_d1:
    start_date = st.date_input(
        "Dari",
        min_value=min_date,
        max_value=max_date,
        value=start_default,
        key="start_date_picker"
    )
with col_d2:
    end_date = st.date_input(
        "Sampai",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        key="end_date_picker"
    )

if start_date > end_date:
    st.sidebar.error("Tanggal 'Dari' tidak boleh melebihi tanggal 'Sampai'.")
    st.stop()

# State filter: with full state name labels
all_states = sorted(df["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Pilih Negara Bagian (State)",
    options=all_states,
    default=[],
    format_func=lambda x: f"{x} - {BRAZIL_STATES.get(x, x)}"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Analyst:** Farrel Farica Firjaturazza")
st.sidebar.markdown("**Dataset:** Brazilian E-Commerce (Olist)")

# Apply filters
filtered_df = df[
    (df["order_purchase_timestamp"].dt.date >= start_date) &
    (df["order_purchase_timestamp"].dt.date <= end_date)
]

if selected_states:
    filtered_df = filtered_df[filtered_df["customer_state"].isin(selected_states)]

if filtered_df.empty:
    st.warning("Tidak ada transaksi untuk filter yang dipilih. Silakan sesuaikan rentang tanggal atau wilayah.")
    st.stop()

# Header
st.title("🛒 E-Commerce Public Analytics Dashboard")
st.markdown("Visualisasi performa penjualan, metrik pelanggan (RFM), dan sebaran demografi e-commerce Brazil.")

# Key Performance Indicators (KPIs)
unique_orders_df = filtered_df.drop_duplicates(subset=["order_id"])
total_orders = unique_orders_df["order_id"].nunique()
total_revenue = unique_orders_df["total_payment"].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_customers = unique_orders_df["customer_unique_id"].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Pesanan", value=f"{total_orders:,}")
with col2:
    st.metric(label="Total Pendapatan", value=f"R$ {total_revenue:,.0f}")
with col3:
    st.metric(label="Rata-rata Pesanan (AOV)", value=f"R$ {avg_order_value:.2f}")
with col4:
    st.metric(label="Pelanggan Unik", value=f"{total_customers:,}")

st.markdown("---")

# Section 1: Monthly Trends (Pertanyaan 1) with Callout Badges
st.subheader("📈 Tren Pertumbuhan Pendapatan dan Pesanan Bulanan")

monthly_df = unique_orders_df.copy()
monthly_df["year_month"] = monthly_df["order_purchase_timestamp"].dt.to_period("M").astype(str)

monthly_summary = monthly_df.groupby("year_month").agg(
    order_count=("order_id", "nunique"),
    revenue=("total_payment", "sum")
).reset_index()

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(13, 8), sharex=True)

# 1. Revenue Line Chart
ax[0].plot(
    monthly_summary["year_month"],
    monthly_summary["revenue"],
    marker="o",
    markersize=5.5,
    markerfacecolor="white",
    markeredgewidth=2,
    markeredgecolor="#1f77b4",
    color="#1f77b4",
    linewidth=2.2
)
ax[0].fill_between(monthly_summary["year_month"], monthly_summary["revenue"], color="#1f77b4", alpha=0.10)
ax[0].set_title("Tren Pertumbuhan Total Pendapatan Bulanan E-Commerce", fontsize=12, fontweight="bold", pad=12)
ax[0].set_ylabel("Total Pendapatan (BRL)", fontsize=10, fontweight="semibold")
ax[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"R$ {x*1e-3:.0f}K"))
ax[0].grid(True, linestyle="--", alpha=0.45)

# Callout Badge Peak Revenue (Identik dengan Notebook)
if not monthly_summary.empty:
    peak_rev = monthly_summary.loc[monthly_summary["revenue"].idxmax()]
    ax[0].set_ylim(0, peak_rev["revenue"] * 1.25)
    ax[0].annotate(
        f"Puncak Tertinggi ({peak_rev['year_month']})\nR$ {peak_rev['revenue']:,.0f}",
        xy=(peak_rev["year_month"], peak_rev["revenue"]),
        xytext=(0, 26),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="#d62728", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.45", fc="#fff2f0", ec="#d62728", lw=1.2),
        ha="center", fontsize=9.5, fontweight="bold", color="#d62728"
    )

# 2. Orders Line Chart
ax[1].plot(
    monthly_summary["year_month"],
    monthly_summary["order_count"],
    marker="s",
    markersize=5.5,
    markerfacecolor="white",
    markeredgewidth=2,
    markeredgecolor="#2ca02c",
    color="#2ca02c",
    linewidth=2.2
)
ax[1].fill_between(monthly_summary["year_month"], monthly_summary["order_count"], color="#2ca02c", alpha=0.10)
ax[1].set_title("Tren Pertumbuhan Volume Pesanan Bulanan E-Commerce", fontsize=12, fontweight="bold", pad=12)
ax[1].set_ylabel("Jumlah Pesanan (Orders)", fontsize=10, fontweight="semibold")
ax[1].set_xlabel("Bulan Transaksi", fontsize=10, fontweight="semibold")
ax[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
ax[1].grid(True, linestyle="--", alpha=0.45)

# Callout Badge Peak Orders (Identik dengan Notebook)
if not monthly_summary.empty:
    peak_ord = monthly_summary.loc[monthly_summary["order_count"].idxmax()]
    ax[1].set_ylim(0, peak_ord["order_count"] * 1.25)
    ax[1].annotate(
        f"Puncak Pesanan ({peak_ord['year_month']})\n{peak_ord['order_count']:,} Orders",
        xy=(peak_ord["year_month"], peak_ord["order_count"]),
        xytext=(0, 26),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="#d62728", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.45", fc="#fff2f0", ec="#d62728", lw=1.2),
        ha="center", fontsize=9.5, fontweight="bold", color="#d62728"
    )

plt.xticks(rotation=40, ha="right", fontsize=9)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# Section 2 & 3: Columns layout for RFM and State Distribution
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("👥 Karakteristik Pelanggan Terbaik (RFM)")
    
    # Calculate RFM based on filtered slice
    snapshot_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm_df = unique_orders_df.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("total_payment", "sum")
    ).reset_index()

    rfm_tab1, rfm_tab2, rfm_tab3 = st.tabs(["Recency (Hari)", "Frequency (Order)", "Monetary (Belanja)"])
    colors = ["#1f77b4", "#aec7e8", "#aec7e8", "#aec7e8", "#aec7e8"]

    with rfm_tab1:
        top_r = rfm_df.sort_values(by="recency", ascending=True).head(5).copy()
        top_r["cid_short"] = top_r["customer_unique_id"].apply(lambda x: x[:8] + "...")
        fig_r, ax_r = plt.subplots(figsize=(6, 3.8))
        sns.barplot(data=top_r, x="recency", y="cid_short", order=top_r["cid_short"], palette=colors, ax=ax_r)
        ax_r.set_xlabel("Hari Terakhir Belanja")
        ax_r.set_ylabel(None)
        ax_r.set_xlim(0, max(top_r["recency"].max() * 1.3, 2))
        for p in ax_r.patches:
            val = p.get_width()
            ax_r.annotate(f"{int(val)} hari", (val + 0.08, p.get_y() + p.get_height()/2), va="center", fontsize=8.5, fontweight="semibold")
        st.pyplot(fig_r)
        plt.close()

    with rfm_tab2:
        top_f = rfm_df.sort_values(by="frequency", ascending=False).head(5).copy()
        top_f["cid_short"] = top_f["customer_unique_id"].apply(lambda x: x[:8] + "...")
        fig_f, ax_f = plt.subplots(figsize=(6, 3.8))
        sns.barplot(data=top_f, x="frequency", y="cid_short", order=top_f["cid_short"], palette=colors, ax=ax_f)
        ax_f.set_xlabel("Total Pesanan (Orders)")
        ax_f.set_ylabel(None)
        ax_f.set_xlim(0, top_f["frequency"].max() * 1.3)
        for p in ax_f.patches:
            val = p.get_width()
            ax_f.annotate(f"{int(val)} order", (val + 0.3, p.get_y() + p.get_height()/2), va="center", fontsize=8.5, fontweight="semibold")
        st.pyplot(fig_f)
        plt.close()

    with rfm_tab3:
        top_m = rfm_df.sort_values(by="monetary", ascending=False).head(5).copy()
        top_m["cid_short"] = top_m["customer_unique_id"].apply(lambda x: x[:8] + "...")
        fig_m, ax_m = plt.subplots(figsize=(6, 3.8))
        sns.barplot(data=top_m, x="monetary", y="cid_short", order=top_m["cid_short"], palette=colors, ax=ax_m)
        ax_m.set_xlabel("Total Pengeluaran (BRL)")
        ax_m.set_ylabel(None)
        ax_m.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"R$ {x*1e-3:.0f}K"))
        ax_m.set_xlim(0, top_m["monetary"].max() * 1.3)
        for p in ax_m.patches:
            val = p.get_width()
            ax_m.annotate(f"R$ {val:,.0f}", (val + 300, p.get_y() + p.get_height()/2), va="center", fontsize=8.5, fontweight="semibold")
        st.pyplot(fig_m)
        plt.close()

with col_right:
    st.subheader("📍 Persebaran Pelanggan (Top 10 State)")
    state_df = unique_orders_df.groupby("customer_state").agg(
        customer_count=("customer_unique_id", "nunique"),
        order_count=("order_id", "nunique")
    ).sort_values(by="customer_count", ascending=False).head(10).reset_index()

    # Full State Name Label
    state_df["state_label"] = state_df["customer_state"].apply(lambda x: f"{x} - {BRAZIL_STATES.get(x, x)}")
    total_cust_filtered = unique_orders_df["customer_unique_id"].nunique()

    fig_s, ax_s = plt.subplots(figsize=(6, 3.8))
    sns.barplot(data=state_df, x="customer_count", y="state_label", palette="crest", ax=ax_s)
    ax_s.set_xlabel("Jumlah Pelanggan Unik")
    ax_s.set_ylabel(None)
    ax_s.set_xlim(0, state_df["customer_count"].max() * 1.35)
    for p in ax_s.patches:
        val = p.get_width()
        pct = (val / total_cust_filtered * 100) if total_cust_filtered > 0 else 0
        ax_s.annotate(f"{int(val):,} ({pct:.1f}%)", (val + 100, p.get_y() + p.get_height()/2), va="center", fontsize=8)
    st.pyplot(fig_s)
    plt.close()

st.markdown("---")

# Section 4: Top 10 Product Categories
st.subheader("📦 Top 10 Kategori Produk Berdasarkan Nilai Transaksi")
cat_df = filtered_df.groupby("product_category_name_english").agg(
    total_revenue=("price", "sum"),
    order_count=("order_id", "nunique")
).sort_values(by="total_revenue", ascending=False).head(10).reset_index()

fig_c, ax_c = plt.subplots(figsize=(10, 4))
sns.barplot(data=cat_df, x="total_revenue", y="product_category_name_english", palette="Blues_r", ax=ax_c)
ax_c.set_xlabel("Total Penjualan Produk (BRL)")
ax_c.set_ylabel(None)
ax_c.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"R$ {x*1e-3:.0f}K"))
ax_c.set_xlim(0, cat_df["total_revenue"].max() * 1.25)
for p in ax_c.patches:
    ax_c.annotate(f"R$ {p.get_width():,.0f}", (p.get_width() + 10000, p.get_y() + p.get_height()/2), va="center", fontsize=9)
plt.tight_layout()
st.pyplot(fig_c)
plt.close()

# Footer
st.caption("Copyright © 2026 Farrel Farica Firjaturazza - Dicoding Belajar Analisis Data dengan Python")
