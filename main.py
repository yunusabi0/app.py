```python
import streamlit as st
import pdfplumber
import re
import requests
import base64

st.set_page_config(page_title="GanoPort", page_icon="🎓")

DOSYA_YOLU = "gnp_indirim_kodlari.txt"

# ----------------------------
# ARKA PLAN
# ----------------------------
def set_bg():
    url = "https://images.pexels.com/photos/14433882/pexels-photo-14433882.jpeg"
    response = requests.get(url)
    encoded = base64.b64encode(response.content).decode()

    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
    }}

    .block-container {{
        background: rgba(30,35,50,0.72);
        padding: 2rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }}

    h1, h2, h3, p, label {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()

# ----------------------------
# TXT'DEN KOD OKU + SİL
# ----------------------------
def kod_al_ve_sil(indirim):
    try:
        with open(DOSYA_YOLU, "r") as f:
            kodlar = f.read().splitlines()

        uygun_kodlar = [k for k in kodlar if k.endswith(str(indirim))]

        if not uygun_kodlar:
            return None

        secilen = uygun_kodlar[0]

        kodlar.remove(secilen)

        with open(DOSYA_YOLU, "w") as f:
            f.write("\n".join(kodlar))

        return secilen

    except:
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
            kod = kod_al_ve_sil(indirim)

            if kod:
                st.balloons()
                st.success(f"%{indirim} indirim kazandınız!")
                st.code(kod)
            else:
                st.error("Bu indirim için kod kalmamış.")
        else:
            st.warning("İndirim için GANO düşük.")

    else:
        st.error("GANO bulunamadı.")

st.divider()

st.markdown("Bu sistem İLAZDO işbirliği ile geliştirilmiştir.")
```
