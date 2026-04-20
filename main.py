```python
import streamlit as st
import pdfplumber
import re
import requests
import base64

st.set_page_config(page_title="GanoPort", page_icon="🎓")

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
# KODLAR (SENİN VERDİKLERİN)
# ----------------------------
if "kodlar" not in st.session_state:
    st.session_state.kodlar = [
        "GNP00120","GNP00220","GNP00320","GNP00420","GNP00520","GNP00620","GNP00720","GNP00820","GNP00920","GNP01020",
        "GNP01120","GNP01220","GNP01320","GNP01420","GNP01520","GNP01620","GNP01720","GNP01820","GNP01920","GNP02020",
        "GNP02120","GNP02220","GNP02320","GNP02420","GNP02520","GNP02620","GNP02720","GNP02820","GNP02920","GNP03020",
        "GNP03120","GNP03220","GNP03320","GNP03420","GNP03520","GNP03620","GNP03720","GNP03820","GNP03920","GNP04020",
        "GNP04120","GNP04220","GNP04320","GNP04420","GNP04520","GNP04620","GNP04720","GNP04820","GNP04920","GNP05020",
        # ... (kısaltıldı ama sende TAM HALİ olacak)
    ]

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
```
