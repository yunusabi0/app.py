import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# ARKA PLAN
# ----------------------------
def set_bg():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1e2332, #2b5876);
    }

    .block-container {
        background: rgba(30,35,50,0.72);
        padding: 2rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }

    h1, h2, h3, p, label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

set_bg()

# ----------------------------
# TÜM KODLARI OTOMATİK OLUŞTUR
# ----------------------------
def tum_kodlari_olustur():
    kodlar = []

    for indirim in [20, 30, 40]:
        for i in range(1, 101):
            kod = f"GNP{str(i).zfill(3)}{indirim}"
            kodlar.append(kod)

    return kodlar

if "kodlar" not in st.session_state:
    st.session_state.kodlar = tum_kodlari_olustur()

# ----------------------------
# KOD SEÇ
# ----------------------------
def kod_al(indirim):
    for k in st.session_state.kodlar:
        if k.endswith(str(indirim)):
            st.session_state.kodlar.remove(k)
            return k
    return None

# ----------------------------
# GANO OKUMA
# ----------------------------
def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            text = ""
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

            text = text.replace(",", ".")

            for line in text.split("\n"):
                if "Top.Krd/GANO" in line:
                    match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)
                    if match:
                        return float(match.group(1))

            match = re.search(r"GANO\s*[: ]\s*([0-4]\.\d{1,2})", text, re.IGNORECASE)
            if match:
                return float(match.group(1))
    except:
        return None

    return None

# ----------------------------
# ARAYÜZ
# ----------------------------
st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF yükleyin", type="pdf")

if uploaded_file:
    with st.spinner("Analiz ediliyor..."):
        gano = gano_bul(uploaded_file)

    if gano is not None:
        st.success(f"GANO: **{gano}**")

        indirim = 0
        if 2.50 <= gano < 3.00:
            indirim = 20
        elif 3.00 <= gano < 3.50:
            indirim = 30
        elif 3.50 <= gano <= 4.00:
            indirim = 40

        if indirim > 0:
            kod = kod_al(indirim)

            if kod:
                st.balloons()
                st.success(f"%{indirim} indirim kazandınız!")
                st.code(kod)
            else:
                st.error("Kod kalmamış.")
        else:
            st.warning("İndirim için GANO düşük.")

    else:
        st.error("GANO bulunamadı.")

st.divider()
st.markdown("Bu sistem İLAZDO işbirliği ile geliştirilmiştir.")
