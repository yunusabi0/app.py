import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Hassas Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    full_text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                full_text += content + "\n"
    
    # Virgülleri noktaya çevir (Örn: 2,77 -> 2.77)
    full_text = full_text.replace(',', '.')
    
    # AKDENİZ ÜNİVERSİTESİ ÖZEL AYIKLAMA MANTIĞI
    # 1. Öncelik: "Top.Krd/GANO" kalıbı (En üstteki genel özet kısmı)
    ozet_gano = re.search(r"GANO/Yüzlük Not\s*:\s*\d+/([0-4][\.]\d{1,2})", full_text)
    if ozet_gano:
        return float(ozet_gano.group(1))

    # 2. Öncelik: Metnin en sonunda, sadece "GANO:" yazan ve dönemsel olmayan değer
    # Dönem GANO'larını (DNO) elemek için kelime sınırlarına dikkat eder.
    temiz_gano = re.findall(r"(?<!D)GANO\s*[:\s]*([0-4][\.]\d{2})", full_text)
    if temiz_gano:
        # Genellikle genel ortalama ya en başta ya en sondadır. 
        # Akdeniz formatında en üstteki genel bilgiyi almak en sağlıklısıdır.
        return float(temiz_gano[0])
        
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Analiz ediliyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Doğrulanan Genel Ortalama (GANO): **{gano}**")
        
        indirim = 0
        # Belirlediğin aralıklar
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) indirim sınırının (2.50) altında.")
    else:
        st.error("GANO tespit edilemedi. Lütfen dijital bir transkript yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
