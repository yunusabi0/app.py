import streamlit as st
import pdfplumber
import re
import hashlib

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# TASARIM
# ----------------------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://tr.key.study/wp-content/uploads/2025/02/1-1.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    background: rgba(20, 25, 40, 0.85);
    padding: 2rem;
    border-radius: 18px;
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 300 KOD (20-30-40)
# ----------------------------
def tum_kodlar():
    return [
        f"GNP{str(i).zfill(3)}20" for i in range(1,101)
    ] + [
        f"GNP{str(i).zfill(3)}30" for i in range(1,101)
    ] + [
        f"GNP{str(i).zfill(3)}40" for i in range(1,101)
    ]

# ----------------------------
# SESSION BAŞLAT
# ----------------------------
if "kodlar" not in st.session_state:
    st.session_state.kodlar = tum_kodlar()

if "kullanilan_pdfler" not in st.session_state:
    st.session_state.kullanilan_pdfler = set()

# ----------------------------
# PDF HASH
# ----------------------------
def pdf_hash(file):
    return hashlib.md5(file.getvalue()).hexdigest()

# ----------------------------
# KOD VER
# ----------------------------
def kod_al(indirim, pdf):
    hash_degeri = pdf_hash(pdf)

    # aynı PDF tekrar kullanılamaz
    if hash_degeri in st.session_state.kullanilan_pdfler:
        return None

    uygun = [k for k in st.session_state.kodlar if k.endswith(str(indirim))]

    if not uygun:
        return None

    kod = uygun[0]

    st.session_state.kodlar.remove(kod)
    st.session_state.kullanilan_pdfler.add(hash_degeri)

    return kod

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

if uploaded_file is not None:
    with st.spinner("Analiz ediliyor..."):
        gano = gano_bul(uploaded_file)

    if gano is not None:
        st.success(f"GANO: {gano}")

        indirim = 0
        if 2.50 <= gano < 3.00:
            indirim = 20
        elif 3.00 <= gano < 3.50:
            indirim = 30
        elif 3.50 <= gano <= 4.00:
            indirim = 40

        if indirim > 0:
            kod = kod_al(indirim, uploaded_file)

            if kod:
                st.balloons()
                st.success(f"%{indirim} indirim kazandınız!")
                st.code(kod)
            else:
                st.error("Bu transkript için zaten kod alınmış veya kod kalmamış.")
        else:
            st.warning("İndirim için GANO yetersiz.")
    else:
        st.error("GANO okunamadı.")

st.divider()

st.markdown(
    'Bu site **Toplumsal Destek Projeleri** dersi kapsamında '
    '[İLAZDO](https://ilazdo.com/) işbirliği sonucu hazırlanmıştır.'
)
