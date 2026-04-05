import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Kesin Çözüm", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            # Akdeniz transkriptinde genel GANO her zaman ilk sayfadadır
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if text:
                # Virgülleri noktaya çevir (3,17 -> 3.17)
                text = text.replace(',', '.')
                
                # 1. STRATEJİ: Doğrudan "Top.Krd/GANO" satırındaki merkezi değeri al
                # Örnek format: ": 150/3.17/83.4"
                merkezi_match = re.search(r"Top\.Krd/GANO/Yüzlük Not\s*:\s*\d+/([0-4]\.\d{1,2})/", text)
                if merkezi_match:
                    return float(merkezi_match.group(1))
                
                # 2. STRATEJİ: Eğer yukarıdaki yapı bozulmuşsa, belgenin sonundaki GANO etiketini al
                # Dönem ortalamalarını (DNO) elemek için negatif bakış (negative lookbehind) kullanıyoruz
                ganos = re.findall(r"(?<!D)GANO\s*[:\s]*([0-4]\.\d{1,2})", text, re.IGNORECASE)
                if ganos:
                    # En güncel GANO genellikle ya en üstteki özette ya da en sondadır
                    return float(ganos[0]) # Kimlik kısmındaki 3.17'ye öncelik ver
                    
    except Exception as e:
        return None
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi buraya yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort veriyi doğruluyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Sistem tarafından doğrulanan GANO: **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) 2.50 sınırının altında olduğu için kod oluşturulamadı.")
    else:
        st.error("GANO bilgisi tespit edilemedi. Lütfen e-devletten alınan orijinal PDF'i yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
