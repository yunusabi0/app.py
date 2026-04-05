import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Kesin Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    full_text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        # Sadece ilk sayfayı tara çünkü genel GANO her zaman ilk sayfadaki kimlik kısmındadır
        first_page = pdf.pages[0]
        full_text = first_page.extract_text()
    
    if not full_text:
        return None

    # Metni standart hale getir: Virgülleri noktaya çevir
    full_text = full_text.replace(',', '.')
    
    # AKDENİZ ÜNİVERSİTESİ NOKTA ATIŞI FİLTRESİ
    # Bu kalıp doğrudan "Top.Krd/GANO/Yüzlük Not" satırını ve yanındaki değeri arar.
    # Örn: "150/3.17/83.4" içinden 3.17'yi çeker.
    ozel_kalip = re.search(r":\s*\d+/([0-4][\.]\d{1,2})/", full_text)
    
    if ozel_kalip:
        return float(ozel_kalip.group(1))

    # Alternatif: Eğer yukarıdaki bulunamazsa, GANO: yazısından hemen sonraki değeri al (DNO değil!)
    temiz_gano = re.findall(r"(?<!D)GANO\s*[:\s]*([0-4][\.]\d{2})", full_text)
    if temiz_gano:
        return float(temiz_gano[0])
        
    return None

def kod_uret(yuzde):
    # 8 haneli: 6 hane rastgele + 2 hane indirim yüzdesi
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort veriyi doğruluyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Doğrulanan Genel Ortalama (GANO): **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kodunuz oluşturuldu.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) indirim sınırının (2.50) altında.")
    else:
        st.error("GANO tespit edilemedi. Lütfen dijital bir transkript yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
