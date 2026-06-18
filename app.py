import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path
import subprocess
import sys
import math
from datetime import datetime, date
import uuid
import re


# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="PLTS Hybrid Maratua Dashboard",
    page_icon="⚡",
    layout="wide"
)


# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "maratua_hybrid.db"


# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown(
    """
    <style>
    /* =========================
       GLOBAL APP STYLE
    ========================= */
    .stApp {
        background-color: #F6F8FB;
    }

    .block-container {
    padding-top: 2.5rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
}

    section.main > div {
        padding-top: 0rem !important;
}

    /* =========================
       SIDEBAR STYLE
    ========================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061B33 0%, #06223D 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .sidebar-subtitle {
        font-size: 14px;
        color: #C9D7E8;
        line-height: 1.6;
        margin-bottom: 28px;
    }

    .sidebar-section {
        font-size: 14px;
        font-weight: 800;
        color: #A7B7C9;
        margin-top: 18px;
        margin-bottom: 12px;
        letter-spacing: 0.4px;
    }

    .sidebar-menu-item {
        padding: 10px 13px;
        border-radius: 12px;
        margin-bottom: 8px;
        color: #D8E7F7;
        font-weight: 700;
        line-height: 1.35;
    }

    .sidebar-menu-active {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        box-shadow: 0px 8px 18px rgba(37, 99, 235, 0.25);
    }

    .sidebar-menu-sub {
        font-size: 12px;
        color: #BBD0E6;
        margin-top: 3px;
        font-weight: 500;
    }

    .sidebar-info-box {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 12px;
        margin-top: 12px;
    }

    .sidebar-info-title {
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 8px;
        color: white;
    }

    .sidebar-info-text {
        font-size: 12px;
        line-height: 1.6;
        color: #D8E7F7;
    }

    /* =========================
       BUTTON STYLE
    ========================= */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 800 !important;
        box-shadow: 0px 8px 18px rgba(37, 99, 235, 0.25) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        color: white !important;
        border: none !important;
        transform: translateY(-1px);
    }

    /* =========================
       HEADER STYLE
    ========================= */
    .dashboard-title {
        font-size: 30px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 14px;
        color: #667085;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    /* =========================
       FILTER STYLE
    ========================= */
    div[data-baseweb="select"] > div {
        background-color: #EEF2F7 !important;
        border: 1px solid #D6E0EA !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    [data-testid="stTextInput"] input {
        background-color: #EEF2F7 !important;
        border: 1px solid #D6E0EA !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    label[data-testid="stWidgetLabel"] p {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #344054 !important;
    }

    /* =========================
       KPI CARD STYLE
    ========================= */
    .metric-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFF 100%);
        padding: 20px 22px;
        border-radius: 18px;
        border: 1px solid #DDE6F0;
        box-shadow: 0px 10px 25px rgba(16, 24, 40, 0.06);
        min-height: 140px;
}

    .metric-label {
        font-size: 12px;
        font-weight: 900;
        color: #344054;
        text-transform: uppercase;
        margin-bottom: 12px;
        letter-spacing: 0.2px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 900;
        color: #101828;
        margin-bottom: 8px;
    }

    .metric-caption {
        font-size: 13px;
        color: #667085;
    }

    .status-good {
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 800;
        margin-top: 10px;
    }

    .status-warning {
        display: inline-block;
        background-color: #FEF3C7;
        color: #92400E;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 800;
        margin-top: 10px;
    }

    .status-gap {
        display: inline-block;
        background-color: #E5E7EB;
        color: #374151;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 800;
        margin-top: 10px;
    }

    /* =========================
       SECTION STYLE
    ========================= */
    .section-title {
        font-size: 18px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 4px;
    }

    .section-caption {
        font-size: 13px;
        color: #667085;
        margin-bottom: 16px;
    }

    .dss-box {
        background: #EFF6FF;
        border: 1px solid #D7E8FF;
        border-radius: 16px;
        padding: 16px;
        min-height: 95px;
    }

    .dss-score {
        font-size: 32px;
        font-weight: 900;
        color: #111827;
    }

    .small-note {
        font-size: 13px;
        color: #667085;
        margin-top: 8px;
    }

    /* =========================
       STREAMLIT CONTAINER BORDER
    ========================= */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #DDE6F0 !important;
        border-radius: 18px !important;
        box-shadow: 0px 10px 25px rgba(16, 24, 40, 0.05) !important;
        padding: 18px !important;
    }

    /* =========================
       DATAFRAME STYLE
    ========================= */
    [data-testid="stDataFrame"] {
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    /* =========================
   HIDE STREAMLIT DEFAULT HEADER
    ========================= */
    header {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stStatusWidget"] {
        display: none !important;
    }

/*   =========================
    SIDEBAR RADIO MENU STYLE
    ========================= */
    [data-testid="stRadio"] label {
        color: #D8E7F7 !important;
        font-weight: 800 !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] > label {
        background: transparent;
        padding: 10px 12px;
        border-radius: 12px;
        margin-bottom: 6px;
    }

    [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.08);
    }

    [data-testid="stRadio"] input:checked + div {
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# DATABASE CHECK
# ======================================================
if not DB_PATH.exists():
    st.error("Database belum ditemukan. Jalankan dulu backend/create_database.py")
    st.stop()


# ======================================================
# BACKEND FUNCTIONS
# ======================================================
def run_etl_from_app():
    """
    Menjalankan script ETL dari Streamlit.
    Script ini membaca Excel dari folder raw_data,
    memproses KPI, lalu update database SQLite.
    """
    etl_path = BASE_DIR / "backend" / "run_etl.py"

    if not etl_path.exists():
        return False, "File backend/run_etl.py tidak ditemukan."

    try:
        result = subprocess.run(
            [sys.executable, str(etl_path)],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except Exception as e:
        return False, str(e)

# ======================================================
# DATA UPLOAD FUNCTIONS
# ======================================================
def get_raw_data_paths():
    raw_dir = BASE_DIR / "raw_data"

    folders = {
        "PLTS-BESS": raw_dir / "plts_bess",
        "PLTD": raw_dir / "pltd",
        "Laporan Sentral": raw_dir / "laporan_sentral"
    }

    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    return folders


def clear_existing_excel(folder_path):
    for file in folder_path.glob("*.xlsx"):
        file.unlink()


def save_uploaded_file(uploaded_file, folder_path, replace_existing=True):
    if uploaded_file is None:
        return None

    folder_path.mkdir(parents=True, exist_ok=True)

    if replace_existing:
        clear_existing_excel(folder_path)

    save_path = folder_path / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path


def folder_has_excel(folder_path):
    return len(list(folder_path.glob("*.xlsx"))) > 0


def get_existing_files_table():
    folders = get_raw_data_paths()
    rows = []

    for data_type, folder in folders.items():
        files = list(folder.glob("*.xlsx"))

        if files:
            for file in files:
                rows.append({
                    "Jenis Data": data_type,
                    "Nama File": file.name,
                    "Folder": str(folder.relative_to(BASE_DIR))
                })
        else:
            rows.append({
                "Jenis Data": data_type,
                "Nama File": "-",
                "Folder": str(folder.relative_to(BASE_DIR))
            })

    return pd.DataFrame(rows)


def render_placeholder_page(page_name):
    st.markdown(
        f"""
        <div class="dashboard-title">{page_name}</div>
        <div class="dashboard-subtitle">
            Halaman ini belum dikembangkan pada tahap saat ini.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Untuk prototype saat ini, halaman yang sudah aktif adalah "
        "Executive Overview dan Data Upload & Processing."
    )

# ======================================================
# DATA UPLOAD & DAILY INPUT FUNCTIONS
# ======================================================
def normalize_text(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def safe_numeric_series(series):
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(r"[^0-9.\-]", "", regex=True),
        errors="coerce"
    )


def period_from_date(value):
    value = pd.to_datetime(value, errors="coerce")
    if pd.isna(value):
        return None
    return value.strftime("%Y-%m")


def get_upload_folders():
    raw_dir = BASE_DIR / "raw_data"

    folders = {
        "PLTS-BESS Monthly": raw_dir / "plts_bess",
        "PLTD Monthly": raw_dir / "pltd",
        "Laporan Sentral": raw_dir / "laporan_sentral",
        "PLTS-BESS Daily": raw_dir / "plts_bess_daily",
        "PLTS-BESS Support": raw_dir / "plts_bess_support",
    }

    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    return folders


def clear_excel_files(folder_path):
    folder_path.mkdir(parents=True, exist_ok=True)
    for file in folder_path.glob("*.xlsx"):
        file.unlink()


def save_uploaded_file_generic(uploaded_file, folder_path, replace_existing=True):
    if uploaded_file is None:
        return None

    folder_path.mkdir(parents=True, exist_ok=True)

    if replace_existing:
        clear_excel_files(folder_path)

    save_path = folder_path / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path


def save_uploaded_file_keep_all(uploaded_file, folder_path):
    if uploaded_file is None:
        return None

    folder_path.mkdir(parents=True, exist_ok=True)

    save_path = folder_path / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path


def get_latest_excel(folder_path):
    files = list(folder_path.glob("*.xlsx"))
    if not files:
        return None
    return max(files, key=lambda file: file.stat().st_mtime)


def get_all_uploaded_files_table():
    folders = get_upload_folders()
    rows = []

    for data_type, folder in folders.items():
        files = list(folder.glob("*.xlsx"))

        if files:
            for file in files:
                rows.append({
                    "Jenis Data": data_type,
                    "Nama File": file.name,
                    "Folder": str(folder.relative_to(BASE_DIR))
                })
        else:
            rows.append({
                "Jenis Data": data_type,
                "Nama File": "-",
                "Folder": str(folder.relative_to(BASE_DIR))
            })

    return pd.DataFrame(rows)


# ======================================================
# MONTHLY EXCEL UPLOAD TAB
# ======================================================
def render_monthly_excel_upload_tab():
    folders = get_upload_folders()

    with st.container(border=True):
        st.markdown(
            '<div class="section-title">Monthly Excel Upload</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Upload file laporan bulanan PLTS-BESS dan PLTD untuk update Executive Overview.</div>',
            unsafe_allow_html=True
        )

        replace_existing = st.checkbox(
            "Replace existing monthly files",
            value=True,
            key="monthly_replace_existing"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            plts_monthly_file = st.file_uploader(
                "Upload file PLTS-BESS bulanan",
                type=["xlsx"],
                key="monthly_upload_plts_bess"
            )

        with col2:
            pltd_monthly_file = st.file_uploader(
                "Upload file PLTD bulanan",
                type=["xlsx"],
                key="monthly_upload_pltd"
            )

        with col3:
            laporan_sentral_file = st.file_uploader(
                "Upload Laporan Sentral",
                type=["xlsx"],
                key="monthly_upload_laporan_sentral"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Upload Monthly Files & Run ETL",
            type="primary",
            use_container_width=True,
            key="btn_monthly_upload_process"
        ):
            saved_files = []

            if plts_monthly_file is not None:
                saved_path = save_uploaded_file_generic(
                    plts_monthly_file,
                    folders["PLTS-BESS Monthly"],
                    replace_existing=replace_existing
                )
                saved_files.append(saved_path.name)

            if pltd_monthly_file is not None:
                saved_path = save_uploaded_file_generic(
                    pltd_monthly_file,
                    folders["PLTD Monthly"],
                    replace_existing=replace_existing
                )
                saved_files.append(saved_path.name)

            if laporan_sentral_file is not None:
                saved_path = save_uploaded_file_generic(
                    laporan_sentral_file,
                    folders["Laporan Sentral"],
                    replace_existing=replace_existing
                )
                saved_files.append(saved_path.name)

            if saved_files:
                st.success("File berhasil di-upload: " + ", ".join(saved_files))
            else:
                st.info("Tidak ada file baru yang di-upload. Sistem memakai file existing di raw_data.")

            if get_latest_excel(folders["PLTS-BESS Monthly"]) is None:
                st.error("File PLTS-BESS bulanan belum tersedia.")
                st.stop()

            if get_latest_excel(folders["PLTD Monthly"]) is None:
                st.error("File PLTD bulanan belum tersedia.")
                st.stop()

            with st.spinner("Menjalankan ETL bulanan..."):
                success, message = run_etl_from_app()

            if success:
                st.success("ETL bulanan berhasil. Dashboard sudah diperbarui.")
                with st.expander("Lihat log ETL"):
                    st.code(message)
            else:
                st.error("ETL bulanan gagal.")
                st.code(message)


# ======================================================
# PLTS-BESS DAILY EXPORT TAB
# ======================================================
def find_column(columns, include_keywords, exclude_keywords=None):
    exclude_keywords = exclude_keywords or []

    for col in columns:
        col_norm = normalize_text(col)

        include_match = any(keyword in col_norm for keyword in include_keywords)
        exclude_match = any(keyword in col_norm for keyword in exclude_keywords)

        if include_match and not exclude_match:
            return col

    return None


def parse_plts_bess_daily_excel(file_path, site="Maratua"):
    excel = pd.ExcelFile(file_path, engine="openpyxl")
    sheet_names = excel.sheet_names

    preferred_sheets = []

    for sheet in sheet_names:
        sheet_norm = normalize_text(sheet)
        if (
            "data harian" in sheet_norm
            or "plant" in sheet_norm
            or "report" in sheet_norm
            or "daily" in sheet_norm
        ):
            preferred_sheets.append(sheet)

    if not preferred_sheets:
        preferred_sheets = sheet_names

    last_error = None

    for sheet_name in preferred_sheets:
        try:
            raw = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=None,
                engine="openpyxl"
            )

            header_row = None

            for i in range(min(40, len(raw))):
                row_text = " ".join(normalize_text(x) for x in raw.iloc[i].tolist())

                if (
                    "statistical period" in row_text
                    or "epv" in row_text
                    or "pv yield" in row_text
                    or "daily yield" in row_text
                    or "production" in row_text
                    or "charge" in row_text
                    or "discharge" in row_text
                ):
                    header_row = i
                    break

            if header_row is None:
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    header=0,
                    engine="openpyxl"
                )
            else:
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    header=header_row,
                    engine="openpyxl"
                )

            df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]
            df.columns = [str(col).strip() for col in df.columns]

            date_col = find_column(
                df.columns,
                include_keywords=[
                    "statistical period",
                    "date",
                    "tanggal",
                    "time",
                    "period"
                ]
            )

            production_col = find_column(
                df.columns,
                include_keywords=[
                    "epv_out",
                    "epv out",
                    "epv",
                    "pv yield",
                    "daily yield",
                    "yield",
                    "production",
                    "generated energy"
                ],
                exclude_keywords=["specific", "total string"]
            )

            specific_col = find_column(
                df.columns,
                include_keywords=["specific energy", "specific yield", "specific"]
            )

            peak_power_col = find_column(
                df.columns,
                include_keywords=["peak power", "peak", "max power"]
            )

            charge_col = find_column(
                df.columns,
                include_keywords=["charge"],
                exclude_keywords=["discharge"]
            )

            discharge_col = find_column(
                df.columns,
                include_keywords=["discharge"]
            )

            soc_col = find_column(
                df.columns,
                include_keywords=["soc"]
            )

            if date_col is None:
                continue

            if production_col is None:
                continue

            result = pd.DataFrame()
            result["date"] = pd.to_datetime(df[date_col], errors="coerce")
            result["production_kwh"] = safe_numeric_series(df[production_col])

            result["specific_energy_kwh_per_kwp"] = (
                safe_numeric_series(df[specific_col])
                if specific_col is not None else None
            )

            result["peak_power_kw"] = (
                safe_numeric_series(df[peak_power_col])
                if peak_power_col is not None else None
            )

            result["bess_charge_kwh"] = (
                safe_numeric_series(df[charge_col])
                if charge_col is not None else 0
            )

            result["bess_discharge_kwh"] = (
                safe_numeric_series(df[discharge_col])
                if discharge_col is not None else 0
            )

            result["soc_avg_pct"] = (
                safe_numeric_series(df[soc_col])
                if soc_col is not None else None
            )

            result = result.dropna(subset=["date"])
            result = result[result["production_kwh"].notna()]

            if result.empty:
                continue

            result["period"] = result["date"].dt.strftime("%Y-%m")
            result["site"] = site

            result = result[
                [
                    "period",
                    "site",
                    "date",
                    "production_kwh",
                    "specific_energy_kwh_per_kwp",
                    "peak_power_kw",
                    "bess_charge_kwh",
                    "bess_discharge_kwh",
                    "soc_avg_pct"
                ]
            ]

            return result

        except Exception as e:
            last_error = e
            continue

    raise ValueError(
        f"File PLTS-BESS harian tidak berhasil diparse. "
        f"Pastikan file export memiliki kolom tanggal dan produksi PLTS. Error terakhir: {last_error}"
    )


def ensure_plts_bess_daily_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stg_plts_daily (
                period TEXT,
                site TEXT,
                date TEXT,
                production_kwh REAL,
                specific_energy_kwh_per_kwp REAL,
                peak_power_kw REAL,
                bess_charge_kwh REAL,
                bess_discharge_kwh REAL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS mart_plts_bess_daily_kpi (
                date TEXT,
                period TEXT,
                site TEXT,
                plts_production_kwh REAL,
                specific_energy_kwh_per_kwp REAL,
                peak_power_kw REAL,
                bess_charge_kwh REAL,
                bess_discharge_kwh REAL,
                soc_avg_pct REAL,
                source_file TEXT,
                updated_at TEXT
            )
        """)

        conn.commit()


def save_plts_bess_daily_to_database(daily_df, source_file):
    ensure_plts_bess_daily_tables()

    daily_df = daily_df.copy()
    daily_df["date"] = pd.to_datetime(daily_df["date"], errors="coerce")
    daily_df = daily_df.dropna(subset=["date"])
    daily_df["date"] = daily_df["date"].dt.strftime("%Y-%m-%d")

    periods = daily_df["period"].dropna().unique().tolist()
    site = daily_df["site"].iloc[0]

    stg_df = daily_df[
        [
            "period",
            "site",
            "date",
            "production_kwh",
            "specific_energy_kwh_per_kwp",
            "peak_power_kw",
            "bess_charge_kwh",
            "bess_discharge_kwh"
        ]
    ].copy()

    mart_df = daily_df.rename(columns={
        "production_kwh": "plts_production_kwh"
    }).copy()

    mart_df["source_file"] = source_file
    mart_df["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mart_df = mart_df[
        [
            "date",
            "period",
            "site",
            "plts_production_kwh",
            "specific_energy_kwh_per_kwp",
            "peak_power_kw",
            "bess_charge_kwh",
            "bess_discharge_kwh",
            "soc_avg_pct",
            "source_file",
            "updated_at"
        ]
    ]

    with sqlite3.connect(DB_PATH) as conn:
        for period in periods:
            conn.execute(
                """
                DELETE FROM stg_plts_daily
                WHERE period = ? AND site = ?
                """,
                (period, site)
            )

            conn.execute(
                """
                DELETE FROM mart_plts_bess_daily_kpi
                WHERE period = ? AND site = ?
                """,
                (period, site)
            )

        stg_df.to_sql(
            "stg_plts_daily",
            conn,
            if_exists="append",
            index=False
        )

        mart_df.to_sql(
            "mart_plts_bess_daily_kpi",
            conn,
            if_exists="append",
            index=False
        )

        conn.commit()


def load_saved_plts_bess_daily():
    ensure_plts_bess_daily_tables()

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """
            SELECT 
                date,
                site,
                plts_production_kwh,
                bess_charge_kwh,
                bess_discharge_kwh,
                peak_power_kw,
                source_file,
                updated_at
            FROM mart_plts_bess_daily_kpi
            ORDER BY date DESC
            LIMIT 30
            """,
            conn
        )

    return df


def render_plts_bess_daily_export_tab():
    folders = get_upload_folders()

    with st.container(border=True):
        st.markdown(
            '<div class="section-title">PLTS-BESS Daily Export</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Upload export FusionSolar untuk data harian PLTS-BESS. Data ini digunakan sebagai pengganti integrasi IoT/API langsung.</div>',
            unsafe_allow_html=True
        )

        replace_existing = st.checkbox(
            "Replace existing PLTS-BESS daily export",
            value=True,
            key="plts_daily_replace_existing"
        )

        col1, col2 = st.columns([1.2, 1])

        with col1:
            daily_export_file = st.file_uploader(
                "Upload FusionSolar Plant/Daily Report",
                type=["xlsx"],
                key="plts_bess_daily_export_file"
            )

        with col2:
            support_files = st.file_uploader(
                "Upload support files, optional: Inverter Report / Current Alarm / History Alarm",
                type=["xlsx"],
                accept_multiple_files=True,
                key="plts_bess_support_files"
            )

        st.info(
            "File support seperti Inverter Report dan Alarm akan disimpan sebagai dokumentasi data. "
            "Untuk saat ini yang diparse menjadi data harian adalah file Plant/Daily Report atau file PLTS-BESS yang memiliki kolom tanggal dan produksi."
        )

        if st.button(
            "Save PLTS-BESS Daily Export",
            type="primary",
            use_container_width=True,
            key="btn_save_plts_bess_daily_export"
        ):
            saved_support = []

            if support_files:
                for file in support_files:
                    saved_path = save_uploaded_file_keep_all(
                        file,
                        folders["PLTS-BESS Support"]
                    )
                    saved_support.append(saved_path.name)

            if daily_export_file is not None:
                saved_daily_path = save_uploaded_file_generic(
                    daily_export_file,
                    folders["PLTS-BESS Daily"],
                    replace_existing=replace_existing
                )
            else:
                saved_daily_path = get_latest_excel(folders["PLTS-BESS Daily"])

            if saved_daily_path is None:
                st.error("File PLTS-BESS daily export belum tersedia.")
                st.stop()

            try:
                daily_df = parse_plts_bess_daily_excel(
                    saved_daily_path,
                    site="Maratua"
                )

                save_plts_bess_daily_to_database(
                    daily_df,
                    source_file=saved_daily_path.name
                )

                total_plts = daily_df["production_kwh"].sum()
                total_charge = daily_df["bess_charge_kwh"].sum()
                total_discharge = daily_df["bess_discharge_kwh"].sum()

                st.success("Data harian PLTS-BESS berhasil disimpan ke database.")

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric("Jumlah Hari", f"{len(daily_df):,.0f}")

                with c2:
                    st.metric("Produksi PLTS", f"{total_plts:,.0f} kWh")

                with c3:
                    st.metric("BESS Charge", f"{total_charge:,.0f} kWh")

                with c4:
                    st.metric("BESS Discharge", f"{total_discharge:,.0f} kWh")

                if saved_support:
                    st.success("Support files tersimpan: " + ", ".join(saved_support))

                with st.expander("Preview data PLTS-BESS harian"):
                    st.dataframe(
                        daily_df,
                        use_container_width=True,
                        hide_index=True
                    )

            except Exception as e:
                st.error("Gagal memproses data PLTS-BESS harian.")
                st.code(str(e))

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<div class="section-title">Saved PLTS-BESS Daily Records</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Data harian PLTS-BESS yang sudah tersimpan di database.</div>',
            unsafe_allow_html=True
        )

        saved_df = load_saved_plts_bess_daily()

        if saved_df.empty:
            st.info("Belum ada data harian PLTS-BESS yang tersimpan.")
        else:
            st.dataframe(
                saved_df,
                use_container_width=True,
                hide_index=True
            )


# ======================================================
# PLTD DAILY LOG INPUT TAB
# ======================================================
def ensure_pltd_daily_log_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stg_pltd_log_header (
                log_id TEXT PRIMARY KEY,
                site TEXT,
                date TEXT,
                machine_no TEXT,
                machine_brand TEXT,
                operator_name TEXT,
                shift TEXT,
                uploaded_photo_path TEXT,
                created_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS stg_pltd_hourly_log (
                log_id TEXT,
                site TEXT,
                date TEXT,
                machine_no TEXT,
                hour TEXT,
                kwh_meter REAL,
                voltage_rs REAL,
                voltage_st REAL,
                voltage_rt REAL,
                current_r REAL,
                current_s REAL,
                current_t REAL,
                load_kw REAL,
                frequency_hz REAL,
                cos_phi REAL,
                rpm REAL,
                jkm REAL,
                temp_air REAL,
                temp_oil REAL,
                pressure_oil REAL,
                battery_voltage REAL,
                fuel_tank_liter REAL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS mart_pltd_daily_kpi (
                date TEXT,
                period TEXT,
                site TEXT,
                machine_no TEXT,
                production_kwh REAL,
                operating_hours REAL,
                avg_load_kw REAL,
                peak_load_kw REAL,
                avg_frequency_hz REAL,
                avg_voltage REAL,
                fuel_consumption_liter REAL,
                sfc_liter_per_kwh REAL,
                oil_added_liter REAL,
                status TEXT,
                notes TEXT,
                updated_at TEXT
            )
        """)

        conn.commit()


def create_default_pltd_hourly_df():
    hours = [f"{i:02d}.00" for i in range(1, 25)]

    return pd.DataFrame({
        "Jam": hours,
        "kWh Meter": [None] * 24,
        "Tegangan RS": [None] * 24,
        "Tegangan ST": [None] * 24,
        "Tegangan RT": [None] * 24,
        "Arus R": [None] * 24,
        "Arus S": [None] * 24,
        "Arus T": [None] * 24,
        "Beban kW": [None] * 24,
        "Frekuensi Hz": [None] * 24,
        "Cos Phi": [None] * 24,
        "RPM": [None] * 24,
        "JKM": [None] * 24,
        "Temperatur Air": [None] * 24,
        "Temperatur Oli": [None] * 24,
        "Tekanan Oli": [None] * 24,
        "Tegangan Accu": [None] * 24,
        "Stand BBM Tangki": [None] * 24
    })


def save_pltd_log_photo(uploaded_photo, log_id):
    if uploaded_photo is None:
        return None

    upload_dir = BASE_DIR / "uploaded_logs" / "pltd_daily"
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(uploaded_photo.name).suffix
    save_path = upload_dir / f"{log_id}{suffix}"

    with open(save_path, "wb") as f:
        f.write(uploaded_photo.getbuffer())

    return str(save_path.relative_to(BASE_DIR))


def hour_sort_value(hour_text):
    try:
        return float(str(hour_text).replace(".", "."))
    except Exception:
        return 999


def save_pltd_daily_log_to_database(
    operation_date,
    site,
    machine_no,
    machine_brand,
    operator_name,
    shift,
    hourly_df,
    bbm_awal,
    bbm_akhir,
    pengisian_bbm,
    oil_added,
    notes,
    uploaded_photo
):
    ensure_pltd_daily_log_tables()

    date_str = operation_date.strftime("%Y-%m-%d")
    period = operation_date.strftime("%Y-%m")
    machine_no = str(machine_no).strip()

    if not machine_no:
        raise ValueError("Machine No. wajib diisi.")

    df = hourly_df.copy()

    rename_map = {
        "Jam": "hour",
        "kWh Meter": "kwh_meter",
        "Tegangan RS": "voltage_rs",
        "Tegangan ST": "voltage_st",
        "Tegangan RT": "voltage_rt",
        "Arus R": "current_r",
        "Arus S": "current_s",
        "Arus T": "current_t",
        "Beban kW": "load_kw",
        "Frekuensi Hz": "frequency_hz",
        "Cos Phi": "cos_phi",
        "RPM": "rpm",
        "JKM": "jkm",
        "Temperatur Air": "temp_air",
        "Temperatur Oli": "temp_oil",
        "Tekanan Oli": "pressure_oil",
        "Tegangan Accu": "battery_voltage",
        "Stand BBM Tangki": "fuel_tank_liter"
    }

    df = df.rename(columns=rename_map)

    numeric_cols = [
        "kwh_meter",
        "voltage_rs",
        "voltage_st",
        "voltage_rt",
        "current_r",
        "current_s",
        "current_t",
        "load_kw",
        "frequency_hz",
        "cos_phi",
        "rpm",
        "jkm",
        "temp_air",
        "temp_oil",
        "pressure_oil",
        "battery_voltage",
        "fuel_tank_liter"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["sort_hour"] = df["hour"].apply(hour_sort_value)
    df = df.sort_values("sort_hour")

    valid_kwh = df[df["kwh_meter"].notna()].copy()

    if valid_kwh.empty:
        raise ValueError("Minimal satu baris kWh Meter harus diisi.")

    log_id = f"{site}_{date_str}_{machine_no}_{uuid.uuid4().hex[:8]}"
    uploaded_photo_path = save_pltd_log_photo(uploaded_photo, log_id)

    production_kwh = valid_kwh["kwh_meter"].iloc[-1] - valid_kwh["kwh_meter"].iloc[0]
    operating_hours = len(valid_kwh)

    avg_load_kw = df["load_kw"].mean()
    peak_load_kw = df["load_kw"].max()
    avg_frequency_hz = df["frequency_hz"].mean()

    voltage_values = df[["voltage_rs", "voltage_st", "voltage_rt"]].stack()
    avg_voltage = voltage_values.mean() if not voltage_values.empty else None

    fuel_consumption_liter = bbm_awal + pengisian_bbm - bbm_akhir

    if production_kwh and production_kwh > 0 and fuel_consumption_liter > 0:
        sfc = fuel_consumption_liter / production_kwh
    else:
        sfc = None

    if production_kwh <= 0 or sfc is None:
        status = "Need Validation"
    elif sfc <= 0.30:
        status = "Baik"
    else:
        status = "Perlu Dipantau"

    header_df = pd.DataFrame([{
        "log_id": log_id,
        "site": site,
        "date": date_str,
        "machine_no": machine_no,
        "machine_brand": machine_brand,
        "operator_name": operator_name,
        "shift": shift,
        "uploaded_photo_path": uploaded_photo_path,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    hourly_save_df = df[
        [
            "hour",
            "kwh_meter",
            "voltage_rs",
            "voltage_st",
            "voltage_rt",
            "current_r",
            "current_s",
            "current_t",
            "load_kw",
            "frequency_hz",
            "cos_phi",
            "rpm",
            "jkm",
            "temp_air",
            "temp_oil",
            "pressure_oil",
            "battery_voltage",
            "fuel_tank_liter"
        ]
    ].copy()

    hourly_save_df["log_id"] = log_id
    hourly_save_df["site"] = site
    hourly_save_df["date"] = date_str
    hourly_save_df["machine_no"] = machine_no

    hourly_save_df = hourly_save_df[
        [
            "log_id",
            "site",
            "date",
            "machine_no",
            "hour",
            "kwh_meter",
            "voltage_rs",
            "voltage_st",
            "voltage_rt",
            "current_r",
            "current_s",
            "current_t",
            "load_kw",
            "frequency_hz",
            "cos_phi",
            "rpm",
            "jkm",
            "temp_air",
            "temp_oil",
            "pressure_oil",
            "battery_voltage",
            "fuel_tank_liter"
        ]
    ]

    kpi_df = pd.DataFrame([{
        "date": date_str,
        "period": period,
        "site": site,
        "machine_no": machine_no,
        "production_kwh": production_kwh,
        "operating_hours": operating_hours,
        "avg_load_kw": avg_load_kw,
        "peak_load_kw": peak_load_kw,
        "avg_frequency_hz": avg_frequency_hz,
        "avg_voltage": avg_voltage,
        "fuel_consumption_liter": fuel_consumption_liter,
        "sfc_liter_per_kwh": sfc,
        "oil_added_liter": oil_added,
        "status": status,
        "notes": notes,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    with sqlite3.connect(DB_PATH) as conn:
        old_logs = pd.read_sql_query(
            """
            SELECT log_id
            FROM stg_pltd_log_header
            WHERE date = ? AND site = ? AND machine_no = ?
            """,
            conn,
            params=(date_str, site, machine_no)
        )

        for old_log_id in old_logs["log_id"].tolist():
            conn.execute(
                "DELETE FROM stg_pltd_hourly_log WHERE log_id = ?",
                (old_log_id,)
            )

        conn.execute(
            """
            DELETE FROM stg_pltd_log_header
            WHERE date = ? AND site = ? AND machine_no = ?
            """,
            (date_str, site, machine_no)
        )

        conn.execute(
            """
            DELETE FROM mart_pltd_daily_kpi
            WHERE date = ? AND site = ? AND machine_no = ?
            """,
            (date_str, site, machine_no)
        )

        header_df.to_sql(
            "stg_pltd_log_header",
            conn,
            if_exists="append",
            index=False
        )

        hourly_save_df.to_sql(
            "stg_pltd_hourly_log",
            conn,
            if_exists="append",
            index=False
        )

        kpi_df.to_sql(
            "mart_pltd_daily_kpi",
            conn,
            if_exists="append",
            index=False
        )

        conn.commit()

    return kpi_df, hourly_save_df


def load_saved_pltd_daily_logs():
    ensure_pltd_daily_log_tables()

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """
            SELECT 
                date,
                site,
                machine_no,
                production_kwh,
                operating_hours,
                fuel_consumption_liter,
                sfc_liter_per_kwh,
                status,
                updated_at
            FROM mart_pltd_daily_kpi
            ORDER BY date DESC, machine_no
            LIMIT 30
            """,
            conn
        )

    return df


def render_pltd_daily_log_input_tab():
    with st.container(border=True):
        st.markdown(
            '<div class="section-title">PLTD Daily Log Input</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Digitalisasi logsheet harian PLTD agar data operasi tersimpan langsung ke database tanpa rekap manual.</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            operation_date = st.date_input(
                "Tanggal operasi",
                value=date.today(),
                key="pltd_log_date"
            )

        with col2:
            site = st.text_input(
                "Site",
                value="Maratua",
                key="pltd_log_site"
            )

        with col3:
            machine_no = st.text_input(
                "Machine No.",
                key="pltd_log_machine_no"
            )

        with col4:
            machine_brand = st.text_input(
                "Merk Mesin",
                key="pltd_log_machine_brand"
            )

        col5, col6, col7 = st.columns([1, 1, 1.2])

        with col5:
            operator_name = st.text_input(
                "Operator / Petugas",
                key="pltd_log_operator"
            )

        with col6:
            shift = st.selectbox(
                "Shift",
                ["Shift Malam", "Shift Pagi", "Shift Sore", "Full Day", "Lainnya"],
                key="pltd_log_shift"
            )

        with col7:
            uploaded_photo = st.file_uploader(
                "Upload foto logsheet, opsional",
                type=["jpg", "jpeg", "png"],
                key="pltd_log_photo"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        default_df = create_default_pltd_hourly_df()

        edited_df = st.data_editor(
            default_df,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="pltd_hourly_data_editor"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        bbm_col1, bbm_col2, bbm_col3, oil_col = st.columns(4)

        with bbm_col1:
            bbm_awal = st.number_input(
                "BBM awal liter",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="pltd_bbm_awal"
            )

        with bbm_col2:
            bbm_akhir = st.number_input(
                "BBM akhir liter",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="pltd_bbm_akhir"
            )

        with bbm_col3:
            pengisian_bbm = st.number_input(
                "Pengisian BBM liter",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="pltd_pengisian_bbm"
            )

        with oil_col:
            oil_added = st.number_input(
                "Penambahan oli liter",
                min_value=0.0,
                value=0.0,
                step=0.5,
                key="pltd_oil_added"
            )

        notes = st.text_area(
            "Catatan operator",
            key="pltd_operator_notes"
        )

        if st.button(
            "Save PLTD Daily Log",
            type="primary",
            use_container_width=True,
            key="btn_save_pltd_daily_log"
        ):
            try:
                kpi_df, hourly_saved_df = save_pltd_daily_log_to_database(
                    operation_date=operation_date,
                    site=site,
                    machine_no=machine_no,
                    machine_brand=machine_brand,
                    operator_name=operator_name,
                    shift=shift,
                    hourly_df=edited_df,
                    bbm_awal=bbm_awal,
                    bbm_akhir=bbm_akhir,
                    pengisian_bbm=pengisian_bbm,
                    oil_added=oil_added,
                    notes=notes,
                    uploaded_photo=uploaded_photo
                )

                st.success("Logsheet harian PLTD berhasil disimpan ke database.")

                kpi = kpi_df.iloc[0]

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric("Produksi Harian", f"{kpi['production_kwh']:,.2f} kWh")

                with c2:
                    st.metric("Jam Operasi", f"{kpi['operating_hours']:,.0f} jam")

                with c3:
                    st.metric("Konsumsi BBM", f"{kpi['fuel_consumption_liter']:,.2f} liter")

                with c4:
                    sfc_value = kpi["sfc_liter_per_kwh"]
                    if pd.notna(sfc_value):
                        st.metric("SFC Harian", f"{sfc_value:.3f} L/kWh")
                    else:
                        st.metric("SFC Harian", "-")

                with st.expander("Preview hourly log yang tersimpan"):
                    st.dataframe(
                        hourly_saved_df,
                        use_container_width=True,
                        hide_index=True
                    )

            except Exception as e:
                st.error("Gagal menyimpan logsheet PLTD.")
                st.code(str(e))

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<div class="section-title">Saved PLTD Daily Logs</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Logsheet PLTD harian yang sudah tersimpan dan siap digunakan untuk Operational Dashboard.</div>',
            unsafe_allow_html=True
        )

        saved_logs = load_saved_pltd_daily_logs()

        if saved_logs.empty:
            st.info("Belum ada logsheet PLTD harian yang tersimpan.")
        else:
            st.dataframe(
                saved_logs,
                use_container_width=True,
                hide_index=True
            )


# ======================================================
# MAIN DATA UPLOAD & PROCESSING PAGE
# ======================================================
def render_data_upload_processing():
    st.markdown(
        """
        <div class="dashboard-title">Data Upload & Processing</div>
        <div class="dashboard-subtitle">
            Input dan pemrosesan data PLTS-BESS dan PLTD untuk memperbarui database dashboard.
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs([
        "Monthly Excel Upload",
        "PLTS-BESS Daily Export",
        "PLTD Daily Log Input"
    ])

    with tab1:
        render_monthly_excel_upload_tab()

    with tab2:
        render_plts_bess_daily_export_tab()

    with tab3:
        render_pltd_daily_log_input_tab()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<div class="section-title">Current Uploaded Files</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Daftar file yang saat ini tersimpan pada folder raw_data.</div>',
            unsafe_allow_html=True
        )

        files_df = get_all_uploaded_files_table()
        st.dataframe(
            files_df,
            use_container_width=True,
            hide_index=True
        )

def reset_database_for_testing():
    """
    Mengembalikan angka testing ke nilai awal mockup.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE mart_kpi_monthly
            SET 
                total_energy_kwh = 327940,
                plts_share_pct = 11.03,
                fuel_saving_liter = 11478
            WHERE period = '2026-04' AND site = 'Maratua'
        """)

        conn.commit()


def load_dashboard_data(period="2026-04", site="Maratua"):
    """
    Load data dari SQLite database.
    Cache sengaja tidak dipakai dulu supaya data langsung berubah saat testing.
    """
    with sqlite3.connect(DB_PATH) as conn:
        kpi_df = pd.read_sql_query(
            """
            SELECT *
            FROM mart_kpi_monthly
            WHERE period = ? AND site = ?
            """,
            conn,
            params=(period, site)
        )

        daily_plts_df = pd.read_sql_query(
            """
            SELECT date, production_kwh
            FROM stg_plts_daily
            WHERE period = ? AND site = ?
            ORDER BY date
            """,
            conn,
            params=(period, site)
        )

        kpi_attention_df = pd.read_sql_query(
            """
            SELECT KPI, Nilai, Satuan, Status, Catatan
            FROM mart_kpi_attention
            WHERE period = ? AND site = ?
            """,
            conn,
            params=(period, site)
        )

    if not daily_plts_df.empty:
        daily_plts_df["date"] = pd.to_datetime(daily_plts_df["date"])

    return kpi_df, daily_plts_df, kpi_attention_df

# ======================================================
# PERIOD HELPER FUNCTIONS
# ======================================================
def period_to_label(period):
    month_map = {
        "01": "Januari",
        "02": "Februari",
        "03": "Maret",
        "04": "April",
        "05": "Mei",
        "06": "Juni",
        "07": "Juli",
        "08": "Agustus",
        "09": "September",
        "10": "Oktober",
        "11": "November",
        "12": "Desember"
    }

    year, month = period.split("-")
    return f"{month_map.get(month, month)} {year}"


def get_available_periods(site="Maratua"):
    with sqlite3.connect(DB_PATH) as conn:
        period_df = pd.read_sql_query(
            """
            SELECT DISTINCT period
            FROM mart_kpi_monthly
            WHERE site = ?
            ORDER BY period DESC
            """,
            conn,
            params=(site,)
        )

    if period_df.empty:
        return {"April 2026": "2026-04"}

    period_map = {}

    for period in period_df["period"].tolist():
        label = period_to_label(period)
        period_map[label] = period

    return period_map

# ======================================================
# OPERATIONAL DASHBOARD - SLIDE 1 STYLE
# ======================================================

import math
from datetime import datetime, date

import pandas as pd
import plotly.graph_objects as go
import sqlite3
import streamlit as st


# ======================================================
# OPERATIONAL DASHBOARD STYLE
# ======================================================

st.markdown(
    """
    <style>
    .op-page-title {
        font-size: 30px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 2px;
    }

    .op-page-subtitle {
        font-size: 14px;
        color: #667085;
        margin-bottom: 18px;
    }

    .op-section-label {
        font-size: 13px;
        font-weight: 900;
        color: #111827;
        text-transform: uppercase;
        margin-bottom: 10px;
        letter-spacing: 0.2px;
    }

    .op-status-card {
        background: #FFFFFF;
        border: 1px solid #DDE6F0;
        border-radius: 14px;
        padding: 16px 16px;
        min-height: 112px;
        box-shadow: 0px 8px 20px rgba(16, 24, 40, 0.05);
    }

    .op-status-title {
        font-size: 12px;
        font-weight: 900;
        color: #344054;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .op-card-flex {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .op-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #EFF6FF;
        font-size: 24px;
        flex-shrink: 0;
    }

    .op-status-value {
        font-size: 22px;
        font-weight: 900;
        color: #111827;
        line-height: 1.1;
    }

    .op-status-value.green {
        color: #16A34A;
    }

    .op-status-value.blue {
        color: #2563EB;
    }

    .op-status-value.purple {
        color: #7C3AED;
    }

    .op-status-subtitle {
        font-size: 12px;
        color: #344054;
        margin-top: 8px;
        font-weight: 600;
    }

    .op-panel-title {
        font-size: 16px;
        font-weight: 900;
        color: #111827;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .op-flow-wrap {
        display: grid;
        grid-template-columns: 1.1fr 0.28fr 1.05fr 0.28fr 1.05fr;
        gap: 12px;
        align-items: center;
        min-height: 300px;
        padding: 10px 6px;
    }

    .op-flow-stack {
        display: flex;
        flex-direction: column;
        gap: 14px;
    }

    .op-flow-card {
        background: #FFFFFF;
        border: 1px solid #D7E3F0;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        box-shadow: 0px 6px 14px rgba(16, 24, 40, 0.04);
    }

    .op-flow-card.muted {
        background: #F8FAFC;
        opacity: 0.74;
    }

    .op-flow-label {
        font-size: 12px;
        color: #344054;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .op-flow-value {
        font-size: 22px;
        color: #2563EB;
        font-weight: 900;
    }

    .op-flow-value.green {
        color: #16A34A;
    }

    .op-flow-value.purple {
        color: #7C3AED;
    }

    .op-flow-value.gray {
        color: #98A2B3;
    }

    .op-flow-sub {
        font-size: 12px;
        font-weight: 700;
        color: #111827;
        margin-top: 6px;
    }

    .op-flow-arrow {
        font-size: 38px;
        font-weight: 900;
        color: #2563EB;
        text-align: center;
    }

    .op-mini-note {
        background: #EAF3FF;
        border-radius: 10px;
        padding: 8px 12px;
        font-size: 12px;
        color: #1E3A8A;
        font-weight: 700;
        margin-top: 8px;
    }

    .op-table-note {
        font-size: 12px;
        color: #667085;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# HELPER FUNCTIONS
# ======================================================

def op_to_float(value, default=0.0):
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def get_latest_operational_date(site="Maratua"):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(
                """
                SELECT MAX(date) AS latest_date
                FROM stg_plts_daily
                WHERE site = ?
                """,
                conn,
                params=(site,)
            )

        if df.empty or pd.isna(df.loc[0, "latest_date"]):
            return date.today()

        return pd.to_datetime(df.loc[0, "latest_date"]).date()

    except Exception:
        return date.today()


def get_operational_sites():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(
                """
                SELECT DISTINCT site
                FROM mart_kpi_monthly
                ORDER BY site
                """,
                conn
            )

        if df.empty:
            return ["Maratua"]

        return df["site"].dropna().astype(str).tolist()

    except Exception:
        return ["Maratua"]


def load_operational_slide1_data(selected_date, site="Maratua"):
    selected_period = selected_date.strftime("%Y-%m")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            kpi_df = pd.read_sql_query(
                """
                SELECT *
                FROM mart_kpi_monthly
                WHERE period = ? AND site = ?
                """,
                conn,
                params=(selected_period, site)
            )

            daily_df = pd.read_sql_query(
                """
                SELECT *
                FROM stg_plts_daily
                WHERE period = ? AND site = ?
                ORDER BY date
                """,
                conn,
                params=(selected_period, site)
            )

        if kpi_df.empty:
            with sqlite3.connect(DB_PATH) as conn:
                kpi_df = pd.read_sql_query(
                    """
                    SELECT *
                    FROM mart_kpi_monthly
                    WHERE site = ?
                    ORDER BY period DESC
                    LIMIT 1
                    """,
                    conn,
                    params=(site,)
                )

            if not kpi_df.empty:
                selected_period = str(kpi_df.iloc[0]["period"])

                with sqlite3.connect(DB_PATH) as conn:
                    daily_df = pd.read_sql_query(
                        """
                        SELECT *
                        FROM stg_plts_daily
                        WHERE period = ? AND site = ?
                        ORDER BY date
                        """,
                        conn,
                        params=(selected_period, site)
                    )

        if not daily_df.empty and "date" in daily_df.columns:
            daily_df["date"] = pd.to_datetime(daily_df["date"])

        return selected_period, kpi_df, daily_df

    except Exception:
        return selected_period, pd.DataFrame(), pd.DataFrame()


def build_hourly_operational_profile(selected_date, kpi_df, daily_df):
    if not kpi_df.empty:
        kpi_row = kpi_df.iloc[0]
        total_energy = op_to_float(kpi_row.get("total_energy_kwh"), 0)
        plts_monthly = op_to_float(kpi_row.get("plts_production_kwh"), 0)
    else:
        total_energy = 0
        plts_monthly = 0

    if not daily_df.empty:
        date_mask = daily_df["date"].dt.date == selected_date

        if date_mask.any():
            day_row = daily_df.loc[date_mask].iloc[0]
        else:
            day_row = daily_df.iloc[-1]

        day_plts_energy = op_to_float(day_row.get("production_kwh"), 0)
        peak_pv = op_to_float(day_row.get("peak_power_kw"), 0)
        day_bess_charge = op_to_float(day_row.get("bess_charge_kwh"), 0)
        day_bess_discharge = op_to_float(day_row.get("bess_discharge_kwh"), 0)
        available_days = max(len(daily_df), 1)

    else:
        day_plts_energy = plts_monthly / 30 if plts_monthly > 0 else 0
        peak_pv = 0
        day_bess_charge = 0
        day_bess_discharge = 0
        available_days = 30

    if peak_pv <= 0:
        peak_pv = max(day_plts_energy / 5.2, 512)

    avg_load = total_energy / max(available_days * 24, 1) if total_energy > 0 else 1600
    avg_load = max(avg_load, 1100)

    rows = []

    for h in range(24):
        sun_shape = max(0, math.sin((h - 5.8) / 12.7 * math.pi))
        pv_kw = peak_pv * (sun_shape ** 1.75)

        if 8 <= h <= 15:
            pv_kw *= 1.04

        if h in [11, 12, 13]:
            pv_kw *= 0.96

        morning_ramp = 120 * math.sin((h / 24) * 2 * math.pi)
        evening_bump = 260 * max(0, math.sin((h - 14) / 10 * math.pi))
        load_kw = avg_load + morning_ramp + evening_bump

        if 0 <= h <= 4:
            load_kw *= 0.78
        elif 5 <= h <= 7:
            load_kw *= 0.92
        elif 8 <= h <= 17:
            load_kw *= 1.05
        elif 18 <= h <= 22:
            load_kw *= 0.98
        else:
            load_kw *= 0.86

        if 7 <= h <= 17:
            charge_shape = max(0, math.sin((h - 7.2) / 10.0 * math.pi))
        else:
            charge_shape = 0

        discharge_shape = 0

        if 0 <= h <= 5:
            discharge_shape = max(0, math.sin((h + 1) / 7 * math.pi))
        elif 18 <= h <= 23:
            discharge_shape = max(0, math.sin((h - 17) / 7 * math.pi))

        bess_charge_kw = max(day_bess_charge / 5.5, 520) * charge_shape
        bess_discharge_kw = -max(day_bess_discharge / 5.0, 420) * discharge_shape
        bess_kw = bess_charge_kw + bess_discharge_kw

        pltd_kw = max(load_kw - pv_kw - bess_kw, 0)

        soc = 52 + 38 * max(0, math.sin((h - 4.5) / 16 * math.pi))

        if h >= 18:
            soc -= (h - 17) * 5.5

        soc = min(max(soc, 22), 96)

        rows.append({
            "hour": h,
            "time": f"{h:02d}:00",
            "pv_kw": round(pv_kw, 1),
            "load_kw": round(load_kw, 1),
            "bess_charge_kw": round(max(bess_kw, 0), 1),
            "bess_discharge_kw": round(min(bess_kw, 0), 1),
            "bess_kw": round(bess_kw, 1),
            "pltd_kw": round(pltd_kw, 1),
            "soc_pct": round(soc, 1),
        })

    return pd.DataFrame(rows)


# ======================================================
# RENDER COMPONENTS
# ======================================================

def render_operational_status_card(title, icon, value, subtitle, color_class=""):
    st.markdown(
        f"""
        <div class="op-status-card">
            <div class="op-status-title">{title}</div>
            <div class="op-card-flex">
                <div class="op-icon">{icon}</div>
                <div>
                    <div class="op-status-value {color_class}">{value}</div>
                    <div class="op-status-subtitle">{subtitle}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_flow_card(label, value, subtitle="", icon="", value_color="#2563EB"):
    card_html = (
        f'<div style="text-align:center; padding:10px 4px;">'
        f'<div style="font-size:28px; margin-bottom:8px;">{icon}</div>'
        f'<div style="font-size:12px; font-weight:900; color:#344054; margin-bottom:8px;">{label}</div>'
        f'<div style="font-size:24px; font-weight:900; color:{value_color}; margin-bottom:6px;">{value}</div>'
        f'<div style="font-size:12px; font-weight:700; color:#111827;">{subtitle}</div>'
        f'</div>'
    )

    with st.container(border=True):
        st.markdown(card_html, unsafe_allow_html=True)


def render_operational_flow(current):
    pv_kw = op_to_float(current.get("pv_kw"), 0)
    load_kw = op_to_float(current.get("load_kw"), 0)
    bess_kw = op_to_float(current.get("bess_kw"), 0)
    pltd_kw = op_to_float(current.get("pltd_kw"), 0)

    if bess_kw < 0:
        bess_sub = "Discharging"
        bess_value = f"{bess_kw:,.0f} kW"
        bess_color = "#7C3AED"
    elif bess_kw > 0:
        bess_sub = "Charging"
        bess_value = f"+{bess_kw:,.0f} kW"
        bess_color = "#7C3AED"
    else:
        bess_sub = "Idle"
        bess_value = "0 kW"
        bess_color = "#667085"

    source_col, arrow_col1, load_col, arrow_col2, grid_col = st.columns(
        [1.15, 0.22, 1.05, 0.22, 0.95]
    )

    with source_col:
        render_flow_card(
            label="PLTS (PV)",
            value=f"{pv_kw:,.0f} kW",
            subtitle="PV Output",
            icon="☀️",
            value_color="#2563EB"
        )

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        render_flow_card(
            label="BESS (Battery)",
            value=bess_value,
            subtitle=bess_sub,
            icon="🔋",
            value_color=bess_color
        )

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        render_flow_card(
            label="PLTD (Diesel)",
            value=f"{pltd_kw:,.0f} kW",
            subtitle="Diesel Output",
            icon="⚙️",
            value_color="#16A34A"
        )

    with arrow_col1:
        st.markdown(
            "<div style='height:315px; display:flex; align-items:center; justify-content:center; font-size:34px; font-weight:900; color:#2563EB;'>→</div>",
            unsafe_allow_html=True
        )

    with load_col:
        st.markdown("<div style='height:112px;'></div>", unsafe_allow_html=True)

        render_flow_card(
            label="LOAD (Beban)",
            value=f"{load_kw:,.0f} kW",
            subtitle="System Load",
            icon="🏭",
            value_color="#111827"
        )

    with arrow_col2:
        st.markdown(
            "<div style='height:315px; display:flex; align-items:center; justify-content:center; font-size:34px; font-weight:900; color:#2563EB;'>→</div>",
            unsafe_allow_html=True
        )

    with grid_col:
        st.markdown("<div style='height:112px;'></div>", unsafe_allow_html=True)

        render_flow_card(
            label="GRID / EXTERNAL",
            value="0 kW",
            subtitle="Not connected",
            icon="🗼",
            value_color="#98A2B3"
        )

    st.markdown(
        (
            "<div style='background:#EAF3FF; border-radius:10px; padding:9px 12px; "
            "font-size:12px; color:#1E3A8A; font-weight:700; margin-top:10px;'>"
            "Catatan: Nilai menunjukkan daya saat ini dalam kW. Untuk prototype, profil hourly dibentuk dari data harian/bulanan yang tersedia."
            "</div>"
        ),
        unsafe_allow_html=True
    )


def build_pltd_unit_table(current):
    pltd_kw = op_to_float(current.get("pltd_kw"), 0)

    allocation = [0.38, 0.34, 0.00, 0.28, 0.00]
    statuses = ["RUNNING", "RUNNING", "STANDBY", "RUNNING", "STANDBY"]
    hours = [8.4, 7.9, 0.0, 6.8, 0.0]

    rows = []

    for i in range(5):
        load_kw = round(pltd_kw * allocation[i])
        production = round(load_kw * hours[i])

        rows.append({
            "Unit Genset": f"Genset {i + 1}",
            "Status": statuses[i],
            "Jam Operasi (Jam)": hours[i],
            "Beban Saat Ini (kW)": load_kw,
            "Produksi Hari Ini (kWh)": production,
        })

    total = {
        "Unit Genset": "TOTAL",
        "Status": "",
        "Jam Operasi (Jam)": round(sum(hours), 1),
        "Beban Saat Ini (kW)": sum(row["Beban Saat Ini (kW)"] for row in rows),
        "Produksi Hari Ini (kWh)": sum(row["Produksi Hari Ini (kWh)"] for row in rows),
    }

    return pd.DataFrame(rows + [total])


def build_alarm_table(selected_date):
    base_date = selected_date.strftime("%d %b %Y")

    return pd.DataFrame([
        {
            "Waktu": f"{base_date} 09:42:15",
            "Level": "MAJOR",
            "Sumber": "Genset 2",
            "Deskripsi": "High Exhaust Temperature",
            "Status": "ACK",
        },
        {
            "Waktu": f"{base_date} 08:17:08",
            "Level": "MINOR",
            "Sumber": "PLTS Inverter 3",
            "Deskripsi": "DC Voltage Low",
            "Status": "ACK",
        },
        {
            "Waktu": f"{base_date} 07:55:31",
            "Level": "WARNING",
            "Sumber": "BESS",
            "Deskripsi": "SOC Below 30%",
            "Status": "CLEARED",
        },
        {
            "Waktu": f"{base_date} 06:21:44",
            "Level": "MINOR",
            "Sumber": "Genset 4",
            "Deskripsi": "Low Fuel Level",
            "Status": "ACK",
        },
        {
            "Waktu": f"{base_date} 05:10:02",
            "Level": "WARNING",
            "Sumber": "PLTS Combiner Box",
            "Deskripsi": "Communication Lost",
            "Status": "CLEARED",
        },
    ])


# ======================================================
# MAIN OPERATIONAL DASHBOARD
# ======================================================

def render_operational_dashboard():
    latest_date = get_latest_operational_date(site="Maratua")
    site_options = get_operational_sites()

    # ===============================
    # HEADER
    # ===============================

    header_left, header_right = st.columns([1.2, 2.2])

    with header_left:
        st.markdown(
            """
            <div class="op-page-title">Operational Dashboard</div>
            <div class="op-page-subtitle">
                Monitoring Operasional Harian - Team Leader Operasi
            </div>
            """,
            unsafe_allow_html=True
        )

    with header_right:
        f1, f2, f3, f4, f5 = st.columns([1.05, 0.9, 0.95, 1.15, 0.22])

        with f1:
            selected_date = st.date_input(
                "Periode",
                value=latest_date,
                key="op_slide1_date"
            )

        with f2:
            selected_site = st.selectbox(
                "Site",
                site_options,
                index=site_options.index("Maratua") if "Maratua" in site_options else 0,
                key="op_slide1_site"
            )

        with f3:
            selected_mode = st.selectbox(
                "Mode Tampilan",
                ["Real-time (Prototype)", "Near real-time", "Historical"],
                key="op_slide1_mode"
            )

        selected_period, kpi_df, daily_df = load_operational_slide1_data(
            selected_date=selected_date,
            site=selected_site
        )

        if not kpi_df.empty and "last_updated" in kpi_df.columns:
            last_updated = str(kpi_df.iloc[0]["last_updated"])
        else:
            last_updated = datetime.now().strftime("%d %b %Y %H:%M:%S WIB")

        with f4:
            st.text_input(
                "Last Updated",
                f"● {last_updated}",
                disabled=True,
                key="op_slide1_last_updated"
            )

        with f5:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

            if st.button("↻", key="op_slide1_refresh"):
                st.rerun()

    if kpi_df.empty:
        st.error("Data KPI operasional belum tersedia. Upload dan proses file Excel terlebih dahulu.")
        st.stop()

    hourly_df = build_hourly_operational_profile(
        selected_date=selected_date,
        kpi_df=kpi_df,
        daily_df=daily_df
    )

    if selected_date == date.today():
        current_hour = min(datetime.now().hour, 23)
    else:
        current_hour = 12

    current = hourly_df.loc[hourly_df["hour"] == current_hour].iloc[0]

    data_completeness = 96.2 if not daily_df.empty and not kpi_df.empty else 50.0

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # STATUS SISTEM
    # ===============================

    st.markdown(
        '<div class="op-section-label">Status Sistem</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        render_operational_status_card(
            "PLTD (Diesel)",
            "⚙️",
            "RUNNING",
            "4 Unit Beroperasi",
            "green"
        )

    with c2:
        render_operational_status_card(
            "PLTS (PV)",
            "☀️",
            "NORMAL",
            "Produksi Normal",
            "green"
        )

    with c3:
        render_operational_status_card(
            "BESS (Battery)",
            "🔋",
            "NORMAL",
            f"SOC: {op_to_float(current.get('soc_pct'), 72.4):.1f} %",
            "green"
        )

    with c4:
        render_operational_status_card(
            "Frekuensi Sistem",
            "〰️",
            "50.02 Hz",
            "Normal",
            ""
        )

    with c5:
        render_operational_status_card(
            "Tegangan Sistem",
            "⚡",
            "400.1 V",
            "Normal",
            ""
        )

    with c6:
        render_operational_status_card(
            "Data Completeness",
            "◔",
            f"{data_completeness:.1f} %",
            "Baik" if data_completeness >= 80 else "Perlu Dipantau",
            ""
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # ROW 1
    # ===============================

    row1_left, row1_right = st.columns([1.08, 1])

    with row1_left:
        with st.container(border=True):
            st.markdown(
                '<div class="op-panel-title">Diagram Aliran Energi (Real-time)</div>',
                unsafe_allow_html=True
            )

            render_operational_flow(current)

    with row1_right:
        with st.container(border=True):
            st.markdown(
                '<div class="op-panel-title">Trend Produksi PLTS Hari Ini</div>',
                unsafe_allow_html=True
            )

            fig_pv = go.Figure()

            fig_pv.add_trace(
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["pv_kw"],
                    mode="lines+markers",
                    name="PV Output (kW)",
                    line=dict(width=3, color="#2563EB"),
                    marker=dict(size=5, color="#2563EB")
                )
            )

            fig_pv.update_layout(
                height=280,
                margin=dict(l=20, r=20, t=10, b=20),
                yaxis=dict(title="kW", gridcolor="#E5E7EB"),
                xaxis=dict(title=""),
                legend=dict(orientation="h", y=-0.22, x=0.38),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig_pv, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # ROW 2
    # ===============================

    row2_left, row2_right = st.columns([1.08, 1])

    with row2_left:
        with st.container(border=True):
            st.markdown(
                '<div class="op-panel-title">Load Sistem (Hari Ini)</div>',
                unsafe_allow_html=True
            )

            fig_load = go.Figure()

            fig_load.add_trace(
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["load_kw"],
                    mode="lines+markers",
                    name="Load (kW)",
                    fill="tozeroy",
                    line=dict(width=3, color="#2563EB"),
                    marker=dict(size=5, color="#2563EB")
                )
            )

            fig_load.update_layout(
                height=260,
                margin=dict(l=20, r=20, t=10, b=20),
                yaxis=dict(title="kW", gridcolor="#E5E7EB"),
                xaxis=dict(title=""),
                legend=dict(orientation="h", y=-0.22, x=0.42),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig_load, use_container_width=True)

    with row2_right:
        with st.container(border=True):
            st.markdown(
                '<div class="op-panel-title">Trend BESS Charge / Discharge Hari Ini</div>',
                unsafe_allow_html=True
            )

            fig_bess = go.Figure()

            fig_bess.add_trace(
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["bess_charge_kw"],
                    mode="lines+markers",
                    name="Charge (kW)",
                    line=dict(width=3, color="#16A34A"),
                    marker=dict(size=5, color="#16A34A")
                )
            )

            fig_bess.add_trace(
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["bess_discharge_kw"],
                    mode="lines+markers",
                    name="Discharge (kW)",
                    line=dict(width=3, color="#7C3AED"),
                    marker=dict(size=5, color="#7C3AED")
                )
            )

            fig_bess.add_trace(
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["soc_pct"],
                    mode="lines",
                    name="SOC (%)",
                    yaxis="y2",
                    line=dict(width=2, dash="dash", color="#F97316")
                )
            )

            fig_bess.update_layout(
                height=260,
                margin=dict(l=20, r=20, t=10, b=20),
                yaxis=dict(title="kW", gridcolor="#E5E7EB"),
                yaxis2=dict(
                    title="SOC (%)",
                    overlaying="y",
                    side="right",
                    range=[0, 100]
                ),
                xaxis=dict(title=""),
                legend=dict(orientation="h", y=-0.22, x=0.20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig_bess, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # ROW 3
    # ===============================

    row3_left, row3_right = st.columns([1.08, 1])

    with row3_left:
        with st.container(border=True):
            st.markdown(
                '<div class="op-panel-title">Jam Operasi PLTD per Unit (Hari Ini)</div>',
                unsafe_allow_html=True
            )

            pltd_unit_df = build_pltd_unit_table(current)

            def style_unit_status(value):
                if value == "RUNNING":
                    return "background-color: #DCFCE7; color: #166534; font-weight: 800;"
                if value == "STANDBY":
                    return "background-color: #DBEAFE; color: #1D4ED8; font-weight: 800;"
                return ""

            st.dataframe(
                pltd_unit_df.style.map(style_unit_status, subset=["Status"]),
                use_container_width=True,
                hide_index=True
            )

    with row3_right:
        with st.container(border=True):
            title_col, button_col = st.columns([1, 0.25])

            with title_col:
                st.markdown(
                    '<div class="op-panel-title">Alarm & Gangguan Terakhir</div>',
                    unsafe_allow_html=True
                )

            with button_col:
                st.button("Lihat Semua", key="op_slide1_view_all_alarm")

            alarm_df = build_alarm_table(selected_date)

            def style_alarm_level(value):
                if value == "MAJOR":
                    return "background-color: #FDBA74; color: #9A3412; font-weight: 800;"
                if value == "MINOR":
                    return "background-color: #FDE68A; color: #92400E; font-weight: 800;"
                if value == "WARNING":
                    return "background-color: #DBEAFE; color: #1D4ED8; font-weight: 800;"
                return ""

            def style_alarm_status(value):
                if value == "ACK":
                    return "background-color: #DCFCE7; color: #166534; font-weight: 800;"
                if value == "CLEARED":
                    return "background-color: #E5E7EB; color: #374151; font-weight: 800;"
                return ""

            st.dataframe(
                alarm_df.style
                .map(style_alarm_level, subset=["Level"])
                .map(style_alarm_status, subset=["Status"]),
                use_container_width=True,
                hide_index=True
            )

    st.markdown(
        """
        <div class="op-table-note">
            Catatan: Data PLTS dan PLTD memakai hasil ETL yang tersedia.
            Load hourly, frekuensi, tegangan, SOC, dan alarm pada halaman ini
            masih berupa placeholder prototype sampai data real-time atau
            logsheet detail terintegrasi.
        </div>
        """,
        unsafe_allow_html=True
    )
        
# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">⚡ PLTS Hybrid Maratua</div>
        <div class="sidebar-subtitle">
            Monitoring & Decision Support<br>
            System
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Run ETL & Update Dashboard",
        type="primary",
        use_container_width=True,
        key="btn_run_etl_sidebar"
    ):
        with st.spinner("Memproses data Excel dan memperbarui database..."):
            success, message = run_etl_from_app()

        if success:
            st.success("ETL berhasil. Dashboard diperbarui.")
            st.rerun()
        else:
            st.error("ETL gagal dijalankan.")
            st.code(message)

    st.markdown('<div class="sidebar-section">MENU UTAMA</div>', unsafe_allow_html=True)

    selected_page = st.radio(
        "Pilih menu",
        [
            "Executive Overview",
            "Operational Dashboard",
            "Tactical Dashboard - Unit Layanan",
            "Tactical Dashboard - Unit Pelaksana",
            "Data Upload & Processing",
            "DSS Recommendation"
        ],
        index=0,
        label_visibility="collapsed",
        key="sidebar_page_selector"
    )

    st.markdown(
        """
        <div class="sidebar-info-box">
            <div class="sidebar-info-title">Tentang Sistem</div>
            <div class="sidebar-info-text">
                Dashboard ini menampilkan data integrasi PLTS-BESS dan PLTD 
                untuk monitoring, evaluasi, dan rekomendasi keputusan di 
                PLTS Hybrid Maratua.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ======================================================
# PAGE ROUTING
# ======================================================
# ======================================================
# PAGE ROUTING
# ======================================================
if selected_page == "Data Upload & Processing":
    render_data_upload_processing()
    st.stop()

elif selected_page == "Operational Dashboard":
    render_operational_dashboard()
    st.stop()

elif selected_page != "Executive Overview":
    render_placeholder_page(selected_page)
    st.stop()

# ======================================================
# HEADER FILTER
# ======================================================
header_left, header_right = st.columns([1.3, 1.7])

with header_left:
    st.markdown(
        """
        <div class="dashboard-title">Executive Overview Dashboard</div>
        <div class="dashboard-subtitle">
            Ringkasan performa sistem PLTS Hybrid Maratua
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1.25])

    with filter_col2:
        selected_site = st.selectbox(
            "Site",
            ["Maratua"],
            key="site_selector"
        )

    period_options = get_available_periods(site=selected_site)

    with filter_col1:
        selected_period_label = st.selectbox(
            "Periode",
            list(period_options.keys()),
            key="period_selector"
        )

    with filter_col3:
        last_updated_input = st.text_input(
            "Last Updated",
            "Mengikuti data terpilih",
            disabled=True,
            key="last_updated_input"
        )


selected_period = period_options[selected_period_label]


# ======================================================
# LOAD DATA
# ======================================================
kpi_df, daily_plts, kpi_attention = load_dashboard_data(
    period=selected_period,
    site=selected_site
)

if kpi_df.empty:
    st.error("Data KPI untuk periode dan site yang dipilih belum tersedia.")
    st.stop()

kpi_row = kpi_df.iloc[0]

kpi = {
    "total_energy_kwh": float(kpi_row["total_energy_kwh"]),
    "pltd_production_kwh": float(kpi_row["pltd_production_kwh"]),
    "plts_production_kwh": float(kpi_row["plts_production_kwh"]),
    "plts_share_pct": float(kpi_row["plts_share_pct"]),
    "sfc_pltd": float(kpi_row["sfc_pltd"]),
    "availability_pct": float(kpi_row["availability_pct"]),
    "fuel_saving_liter": float(kpi_row["fuel_saving_liter"]),
    "dss_score": int(kpi_row["dss_score"]),
    "priority": str(kpi_row["priority"]),
    "last_updated": str(kpi_row["last_updated"])
}

energy_source = pd.DataFrame({
    "source": ["PLTD Production", "PLTS Production"],
    "energy_kwh": [
        kpi["pltd_production_kwh"],
        kpi["plts_production_kwh"]
    ]
})


# ======================================================
# KPI CARDS
# ======================================================
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Energy Production</div>
            <div class="metric-value">{kpi["total_energy_kwh"]:,.0f} kWh</div>
            <div class="metric-caption">Total produksi hybrid</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">PLTS Share</div>
            <div class="metric-value">{kpi["plts_share_pct"]:.2f} %</div>
            <div class="metric-caption">Kontribusi PLTS</div>
            <span class="status-warning">Perlu Dipantau</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">SFC PLTD</div>
            <div class="metric-value">{kpi["sfc_pltd"]:.3f}</div>
            <div class="metric-caption">L/kWh - Spesifik konsumsi BBM</div>
            <span class="status-warning">Perlu Dipantau</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Availability Factor</div>
            <div class="metric-value">{kpi["availability_pct"]:.2f} %</div>
            <div class="metric-caption">Ketersediaan pembangkit</div>
            <span class="status-good">Baik</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Fuel Saving Estimate</div>
            <div class="metric-value">{kpi["fuel_saving_liter"]:,.0f} Liter</div>
            <div class="metric-caption">Estimasi BBM dihemat</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# ======================================================
# ROW 1: ENERGY MIX + DSS SUMMARY
# ======================================================
row1_left, row1_right = st.columns([1, 1.35])

with row1_left:
    with st.container(border=True):
        st.markdown(
            '<div class="section-title">Energy Mix (PLTS vs PLTD)</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Kontribusi energi PLTS dan PLTD terhadap total produksi hybrid</div>',
            unsafe_allow_html=True
        )

        fig_donut = px.pie(
            energy_source,
            names="source",
            values="energy_kwh",
            hole=0.55
        )

        fig_donut.update_traces(
            textinfo="percent",
            hovertemplate="%{label}<br>%{value:,.0f} kWh<extra></extra>"
        )

        fig_donut.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=0.85
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig_donut, use_container_width=True)

        st.info("Kontribusi PLTS terhadap total produksi hybrid masih perlu dioptimalkan.")

with row1_right:
    with st.container(border=True):
        st.markdown(
            '<div class="section-title">DSS Recommendation Summary</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Ringkasan evaluasi berbasis KPI sistem hybrid</div>',
            unsafe_allow_html=True
        )

        dss_col1, dss_col2 = st.columns(2)

        with dss_col1:
            st.markdown(
                f"""
                <div class="dss-box">
                    <div class="metric-label">DSS Score</div>
                    <span class="dss-score">{kpi["dss_score"]}</span> / 100
                </div>
                """,
                unsafe_allow_html=True
            )

        with dss_col2:
            st.markdown(
                f"""
                <div class="dss-box">
                    <div class="metric-label">Priority Level</div>
                    <span class="status-warning">{kpi["priority"]}</span>
                    <div class="small-note">Perlu perhatian</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        finding_col, rec_col = st.columns(2)

        with finding_col:
            st.markdown("**Main Findings**")
            st.markdown(
                """
                - Kontribusi PLTS terhadap beban masih rendah
                - SFC PLTD berada di atas target efisiensi
                - Potensi penghematan BBM masih dapat ditingkatkan
                - Beberapa data operasional belum lengkap
                """
            )

        with rec_col:
            st.markdown("**Recommendation**")
            st.markdown(
                """
                Evaluasi strategi dispatch PLTS-BESS dan efisiensi operasi PLTD.
                Optimalkan pemanfaatan energi surya dan pemeliharaan unit diesel.
                """
            )


st.markdown("<br>", unsafe_allow_html=True)


# ======================================================
# ROW 2: DAILY PLTS TREND
# ======================================================
with st.container(border=True):
    st.markdown(
        f'<div class="section-title">Tren Produksi PLTS Harian ({selected_period_label})</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="section-title">Produksi Energi per Sumber ({selected_period_label})</div>',
        unsafe_allow_html=True
    )

    fig_line = px.line(
        daily_plts,
        x="date",
        y="production_kwh",
        markers=True,
        labels={
            "date": "Tanggal",
            "production_kwh": "Produksi PLTS (kWh)"
        }
    )

    fig_line.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig_line.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(tickformat="%d %b"),
        yaxis=dict(title="kWh"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_line, use_container_width=True)


st.markdown("<br>", unsafe_allow_html=True)


# ======================================================
# ROW 3: ENERGY SOURCE + KPI ATTENTION
# ======================================================
bottom_left, bottom_right = st.columns([1, 1.35])

with bottom_left:
    with st.container(border=True):
        st.markdown(
            f'<div class="section-title">Tren Produksi PLTS Harian ({selected_period_label})</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="section-title">Produksi Energi per Sumber ({selected_period_label})</div>',
            unsafe_allow_html=True
        )

        fig_bar = px.bar(
            energy_source,
            x="source",
            y="energy_kwh",
            text="energy_kwh",
            labels={
                "source": "",
                "energy_kwh": "kWh"
            }
        )

        fig_bar.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside"
        )

        fig_bar.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="kWh"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

with bottom_right:
    with st.container(border=True):
        st.markdown(
            '<div class="section-title">KPI Requiring Attention</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-caption">Indikator yang perlu dipantau atau membutuhkan data tambahan</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            kpi_attention,
            use_container_width=True,
            hide_index=True
        )


# ======================================================
# FOOTER
# ======================================================
st.caption(
    "Catatan: Data diperoleh dari integrasi FusionSolar/Inspire, ComAp/logsheet PLTD, "
    "Form 12/13/14, Rekap EAF, dan BBM stock."
)