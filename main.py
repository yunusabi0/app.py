import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# GANO OKUMA FONKSİYONU
# ----------------------------

def gano_bul(pdf_dosyasi):

    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:

            text = ""

            # tüm sayfaları oku
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

            # virgül sorununu çöz
            text = text.replace(",", ".")

            # satır satır kontrol
            for line in text.split("\n"):

                if "Top.Krd/GANO" in line:

                    # örnek satır: 150/2.77/75.4
                    match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)

                    if match:
                        gano = float(match.group(1))

                        if 0 <= gano <= 4:
                            return gano

            # yedek plan
            match = re.search(r"GANO\s*[: ]\s*([0-4]\.\d{1,2})", text, re.IGNORECASE)

            if match:
                gano = float(match.group(1))

                if 0 <= gano <= 4:
                    return gano

    except Exception as e:
        print(e)

    return None


# ----------------------------
# İNDİRİM KODU OLUŞTURMA
# ----------------------------

def kod_uret(yuzde):

    # 6 rastgele karakter
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # son 2 hane indirim
    kod = f"{rastgele}{str(yuzde).zfill(2)}"

    return kod


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

            kod = kod_uret(indirim)

            st.balloons()

            st.success(f"Tebrikler! %{indirim} indirim kazandınız.")

            st.code(kod, language="text")

        else:

            st.warning(f"GANO ({gano}) indirim için alt sınır olan 2.50'nin altında.")

    else:

        st.error("GANO tespit edilemedi. Lütfen orijinal transkript yükleyin.")


st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
