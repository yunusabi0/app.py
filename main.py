import streamlit as st
import pdfplumber
import re
import requests
import base64

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# ARKA PLAN + PREMIUM UI
# ----------------------------
def set_bg():
    url = "https://images.pexels.com/photos/14433882/pexels-photo-14433882.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    
    response = requests.get(url)
    encoded = base64.b64encode(response.content).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* CAM KUTU - GÜNCELLENDİ */
        .block-container {{
            background: rgba(30, 35, 50, 0.72);
            padding: 2rem;
            border-radius: 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.08);
        }}

        /* YAZILAR */
        h1, h2, h3, p, label {{
            color: white !important;
        }}

        /* UPLOAD KUTUSU */
        [data-testid="stFileUploader"] {{
            background: rgba(255,255,255,0.08);
            padding: 10px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# ----------------------------
# 300 KOD HAZIR HAVUZ
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
            indirim = 10
        elif 3.00 <= gano < 3.50:
            indirim = 20
        elif 3.50 <= gano <= 4.00:
            indirim = 30

        if indirim > 0:
            kod = kod_al(indirim)
            if kod:
                st.balloons()
                st.success(f"%{indirim} indirim kazandınız!")
                st.code(kod)
            else:
                st.error("Kodlar tükenmiş.")
        else:
            st.warning("İndirim için GANO düşük.")

    else:
        st.error("GANO bulunamadı.")

st.divider()

st.markdown(
    "Bu site **Toplumsal Destek Projeleri** kapsamında [İLAZDO](https://ilazdo.com/) işbirliği sonucu hazırlanmıştır."
)
