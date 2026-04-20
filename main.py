import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# ARKA PLAN + TASARIM
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://tr.key.study/wp-content/uploads/2025/02/1-1.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .block-container {
        background-color: rgba(240,242,246,0.9);
        padding: 2rem;
        border-radius: 15px;
    }

    /* FILE UPLOADER (SİYAH KISMI DÜZELTİR) */
    section[data-testid="stFileUploader"] > div {
        background-color: #2c2f36 !important;  /* koyu gri */
        border: 1px solid #3a3f47 !important;
        border-radius: 12px !important;
    }

    section[data-testid="stFileUploader"] label {
        color: #e0e0e0 !important;
    }

    /* Upload butonu */
    section[data-testid="stFileUploader"] button {
        background-color: #1f2a44 !important; /* lacivert */
        color: white !important;
        border-radius: 8px !important;
    }

    /* Yazılar */
    section[data-testid="stFileUploader"] small {
        color: #b0b3b8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# 300 KOD HAVUZU
# ----------------------------
kod_havuzu = {
    "10": [f"ILZ{str(i).zfill(3)}10" for i in range(1,101)],
    "20": [f"ILZ{str(i).zfill(3)}20" for i in range(1,101)],
    "30": [f"ILZ{str(i).zfill(3)}30" for i in range(1,101)]
}

def kod_al(yuzde):
    yuzde = str(yuzde)
    if yuzde not in st.session_state:
        st.session_state[yuzde] = kod_havuzu[yuzde].copy()
    if len(st.session_state[yuzde]) == 0:
        return None
    return st.session_state[yuzde].pop(0)

def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            text=""
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            text = text.replace(",", ".")
            
            for line in text.split("\n"):
                if "Top.Krd/GANO" in line:
                    match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)
                    if match:
                        gano = float(match.group(1))
                        if 0 <= gano <= 4:
                            return gano
            
            match = re.search(r"GANO\s*[: ]\s*([0-4]\.\d{1,2})", text, re.IGNORECASE)
            if match:
                gano = float(match.group(1))
                if 0 <= gano <= 4:
                    return gano
    except Exception:
        return None
    return None

# ----------------------------
# ARAYÜZ
# ----------------------------
st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner("Transkript analiz ediliyor..."):
        gano = gano_bul(uploaded_file)

    if gano is not None:
        st.success(f"Doğrulanan GANO: **{gano}**")
        indirim = 0

        if 2.50 <= gano < 3.00:
            indirim = 10
        elif 3.00 <= gano < 3.50:
            indirim = 20
        elif 3.50 <= gano <= 4.00:
            indirim = 30

        if indirim > 0:
            kod = kod_al(indirim)
            if kod is None:
                st.error("Bu indirim kategorisindeki kodlar tükenmiştir.")
            else:
                st.balloons()
                st.success(f"Tebrikler! %{indirim} indirim kazandınız.")
                st.code(kod)
        else:
            st.warning(f"GANO ({gano}) indirim için alt sınır olan 2.50'nin altında.")
    else:
        st.error("GANO tespit edilemedi. Lütfen orijinal transkript yükleyin.")

st.divider()

st.markdown(
    'Bu site **Toplumsal Destek Projeleri** dersi kapsamında '
    '[İLAZDO](https://ilazdo.com/) işbirliği sonucu hazırlanmıştır.'
)
