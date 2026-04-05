import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort", page_icon="🎓")

def gano_bul(pdf_dosyasi):

    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:

            text = ""

            # ilk 2 sayfayı oku (bazı transkriptlerde ilk sayfada olmuyor)
            for page in pdf.pages[:2]:
                t = page.extract_text()
                if t:
                    text += t + "\n"

            text = text.replace(",", ".")  # 3,25 -> 3.25

            # 1. yöntem : Top.Krd/GANO formatı
            match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", text)

            if match:
                gano = float(match.group(1))
                if 0 <= gano <= 4:
                    return gano

            # 2. yöntem : GANO : 3.25
            match = re.search(r"GANO\s*[:\s]\s*([0-4]\.\d{1,2})", text, re.IGNORECASE)

            if match:
                gano = float(match.group(1))
                if 0 <= gano <= 4:
                    return gano

            # 3. yöntem : Genel ortalama
            match = re.search(r"Genel.*?([0-4]\.\d{1,2})", text, re.IGNORECASE)

            if match:
                gano = float(match.group(1))
                if 0 <= gano <= 4:
                    return gano

    except Exception:
        return None

    return None


def kod_uret(yuzde):

    # 6 rastgele karakter + 2 indirim
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return f"{rastgele}{str(yuzde).zfill(2)}"


st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF yükleyin", type="pdf")

if uploaded_file is not None:

    with st.spinner("Transkript analiz ediliyor..."):

        gano = gano_bul(uploaded_file)

    if gano:

        st.success(f"Doğrulanan GANO : **{gano}**")

        indirim = 0

        if 2.50 <= gano < 3.00:
            indirim = 10

        elif 3.00 <= gano < 3.50:
            indirim = 20

        elif 3.50 <= gano <= 4.00:
            indirim = 30


        if indirim > 0:

            kod = kod_uret(indirim)

            st.balloons()

            st.success(f"%{indirim} indirim kazandınız!")

            st.code(kod)

        else:

            st.warning("İndirim için minimum GANO 2.50")

    else:

        st.error("GANO okunamadı. Lütfen farklı PDF deneyin.")


st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
