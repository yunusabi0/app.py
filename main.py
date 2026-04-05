import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# 300 KOD HAZIR HAVUZ
# ----------------------------
kod_havuzu = {
    "10": [f"ILZ{str(i).zfill(3)}10" for i in range(1,101)],
    "20": [f"ILZ{str(i).zfill(3)}20" for i in range(1,101)],
    "30": [f"ILZ{str(i).zfill(3)}30" for i in range(1,101)]
}

# ----------------------------
# KOD ALMA FONKSİYONU
# ----------------------------
def kod_al(yuzde):
    yuzde = str(yuzde)
    if yuzde not in st.session_state:
        st.session_state[yuzde] = kod_havuzu[yuzde].copy()
    if len(st.session_state[yuzde]) == 0:
        return None
    return st.session_state[yuzde].pop(0)

# ----------------------------
# GANO OKUMA FONKSİYONU (DOKUNMADIK)
# ----------------------------
def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            text=""
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            text = text.replace(",", ".")
            # Öncelikli: Top.Krd/GANO satırı
            for line in text.split("\n"):
                if "Top.Krd/GANO" in line:
                    match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)
                    if match:
                        gano = float(match.group(1))
                        if 0 <= gano <= 4:
                            return gano
            # Yedek: DNO olmayan ilk GANO
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
