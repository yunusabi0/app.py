import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Otomatik Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    full_text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                full_text += content + "\n"
    
    # Metni düzenle: Virgülleri noktaya çevir
    full_text = full_text.replace(',', '.')
    
    # STRATEJİ: "GENEL ORTALAMA", "GANO", "AGNO" kelimelerinden HEMEN SONRA gelen sayıyı ara
    # Bu yöntem alakasız kredileri veya dönem ortalamalarını eler.
    patterns = [
        r"(?:GENEL ORTALAMA|GANO|AGNO|GPA|CGPA)[:\s]+([0-4][\.]\d{1,2})",
        r"(?:GENEL AKADEMİK NOT ORTALAMASI)[:\s]+([0-4][\.]\d{1,2})"
    ]
    
    found_values = []
    for p in patterns:
        matches = re.findall(p, full_text, re.IGNORECASE)
        for m in matches:
            found_values.append(float(m))
            
    if found_values:
        # Transkriptin en sonunda yazan değer genellikle en güncel olandır.
        return found_values[-1]
        
    # Eğer yukarıdaki kelimelerle bulamazsa, metindeki tüm 0.00-4.00 arası sayıları bul 
    # ve içlerinden en mantıklı (genelde sonuncu) olanı seç.
    fallback = re.findall(r"\b([0-4][\.]\d{2})\b", full_text)
    if fallback:
        # 2.5 gibi kısa sayıları değil, 3.17 gibi tam formatlıları tercih et
        return float(fallback[-1])
        
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Lütfen PDF formatındaki transkriptinizi buraya sürükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort belgenizi analiz ediyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        # 3.17 gibi bir değerin doğru çekildiğinden emin oluyoruz
        st.info(f"✅ Sistem tarafından tespit edilen GANO: **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! GANO puanınıza göre %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) indirim sınırının (2.50) altında.")
    else:
        st.error("GANO verisi bulunamadı. Lütfen dijital bir transkript yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
