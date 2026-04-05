import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Kesin Çözüm", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            # Akdeniz Uni formatında güncel GANO her zaman ilk sayfadaki kimlik kısmındadır.
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if text:
                # Sayısal işlemler için virgülleri noktaya çevir (Örn: 2,77 -> 2.77) 
                text = text.replace(',', '.')
                
                # KRİTİK FİLTRE: Doğrudan resmi özet satırını hedef alıyoruz.
                # Bu satır Alp'te ": 150/2.77/75.4" ve Yunus'ta ": 150/3.17/83.4" şeklindedir.
                # Regex açıklaması: İki eğik çizgi (/) arasındaki 0-4 arası rakamı yakalar.
                ozel_kalip = re.search(r"Top\.Krd/GANO/Yüzlük Not\s*:\s*\d+/([0-4][\.]\d{1,2})/", text)
                
                if ozel_kalip:
                    return float(ozel_kalip.group(1))
                
                # EĞER YUKARIDAKİ BULUNAMAZSA (Farklı Versiyon): 
                # "GANO" kelimesini ara ama "DNO" (Dönem Notu) olanları ele.
                temiz_ganos = re.findall(r"(?<!D)GANO\s*[:\s]*([0-4][\.]\d{1,2})", text, re.IGNORECASE)
                if temiz_ganos:
                    # İlk sayfadaki ilk GANO genellikle en resmi olandır.
                    return float(temiz_ganos[0])
                    
    except Exception:
        return None
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkriptinizi (PDF) yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Doğrulama yapılıyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Resmi GANO Doğrulandı: **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kodunuz oluşturuldu.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.warning(f"GANO ({gano}) indirim alt sınırının (2.50) altında.")
    else:
        st.error("GANO bilgisi tespit edilemedi. Lütfen orijinal PDF yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
