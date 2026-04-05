import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Özel", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            # Akdeniz transkriptinde genel GANO her zaman ilk sayfadaki kimlik tablosundadır.
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if text:
                # Sayıları işlemek için virgülleri noktaya çevir (Örn: 2,77 -> 2.77)
                text = text.replace(',', '.')
                
                # NOKTA ATIŞI: "Ayrılış Tarihi/Öğrenim Durumu" satırının altındaki 
                # ": 150/3.17/83.4" benzeri yapıyı arar. 
                # Buradaki ortadaki sayı (3.17) gerçek genel ortalamadır.
                akdeniz_kalibi = re.search(r":\s*\d+/([0-4][\.]\d{1,2})/", text)
                
                if akdeniz_kalibi:
                    return float(akdeniz_kalibi.group(1))
                
                # Eğer yukarıdaki özel yapı bulunamazsa (farklı bir transkriptse), 
                # GANO kelimesini içeren satırları bul ve EN SONUNCUYU (en günceli) al.
                fallback_ganos = re.findall(r"GANO\s*[:\s]*([0-4][\.]\d{1,2})", text, re.IGNORECASE)
                if fallback_ganos:
                    # Genellikle transkriptin sonunda veya başında en güncel değer yer alır.
                    return float(fallback_ganos[0]) # Kimlik kısmındaki değere öncelik verir.
                    
    except Exception:
        return None
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")
st.write("Akdeniz Üniversitesi resmi formatı için optimize edildi.")

uploaded_file = st.file_uploader("Transkript PDF'inizi yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Veri doğrulanıyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Doğrulanan Genel Ortalama (GANO): **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) 2.50 sınırının altında olduğu için kod tanımlanamadı.")
    else:
        st.error("GANO tespit edilemedi. Lütfen orijinal, taranmamış bir PDF yüklediğinizden emin olun.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
