import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Otomatik Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            extract = page.extract_text()
            if extract:
                text += extract
    
    # PDF metnini temizle (boşlukları ve satır başlarını kontrol et)
    text = text.replace(',', '.') # Virgüllü notları noktaya çevirir (Örn: 3,50 -> 3.50)
    
    # Çok daha geniş kapsamlı bir arama: "GANO", "GPA", "Genel", "Ortalama", "AGNO" kelimelerini ara
    # Ve peşinden gelen 0.00-4.00 arası sayıları yakala
    desenler = [
        r"(?:GANO|GPA|ORTALAMA|AGNO|Genel)\D*([0-4][\.,]\d{2})",
        r"([0-4][\.,]\d{2})" # Eğer kelime bulamazsa doğrudan sayıları ara
    ]
    
    bulunan_sayilar = []
    for desen in desenler:
        sonuclar = re.findall(desen, text, re.IGNORECASE)
        for s in sonuclar:
            bulunan_sayilar.append(float(s.replace(',', '.')))

    if bulunan_sayilar:
        # Transkriptlerde güncel GANO genelde en sonda yazar
        return bulunan_sayilar[-1]
    return None

def kod_uret(yuzde):
    karakterler = string.ascii_uppercase + string.digits
    rastgele = ''.join(random.choices(karakterler, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Lütfen PDF formatındaki transkriptinizi buraya sürükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Belgeniz analiz ediliyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano and 0.0 <= gano <= 4.0:
        st.info(f"✅ Sistem tarafından tespit edilen GANO: **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) 2.50 altında olduğu için indirim tanımlanamadı.")
    else:
        st.error("GANO bilgisi otomatik tespit edilemedi. Lütfen PDF'in taranmış bir resim (fotoğraf) değil, okunabilir bir dijital PDF olduğundan emin olun.")
        # Debug için: Eğer hata alıyorsan alttaki satırı aktif edip PDF'ten ne okunduğunu görebilirsin
        # st.text(text) 

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
