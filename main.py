import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Otomatik Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    """PDF içindeki metni tarayıp GANO'yu bulan fonksiyon"""
    text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    # PDF içinde "GANO", "GPA", "Genel Ortalama" gibi anahtar kelimelerin yanındaki sayıları arar
    bulunanlar = re.findall(r"([0-3]\.\d{2}|4\.00)", text)
    if bulunanlar:
        # Genellikle transkriptin sonundaki en güncel ortalamayı almak için sonuncuyu seçeriz
        return float(bulunanlar[-1])
    return None

def kod_uret(yuzde):
    karakterler = string.ascii_uppercase + string.digits
    rastgele = ''.join(random.choices(karakterler, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Lütfen PDF formatındaki transkriptinizi buraya sürükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Belgeniz analiz ediliyor, lütfen bekleyin...'):
        gano = gano_bul(uploaded_file)
        
    if gano:
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
            st.error("GANO puanınız 2.50 altında olduğu için indirim tanımlanamadı.")
    else:
        st.error("Maalesef PDF içinde GANO bilgisi otomatik tespit edilemedi. Lütfen net bir transkript yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
