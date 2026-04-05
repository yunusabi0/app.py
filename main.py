import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Fix", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    full_text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                full_text += content + "\n"
    
    if not full_text:
        return None

    # Virgülleri noktaya çevir (Örn: 2,77 -> 2.77) [cite: 6, 13]
    full_text = full_text.replace(',', '.')
    
    # STRATEJİ: Metindeki tüm GANO satırlarını bul.
    # Akdeniz formatında "GANO: 3.17" veya "GANO: 3.20" şeklinde yazar[cite: 8, 11, 13].
    # En güncel not her zaman belgenin en sonundaki GANO ibaresidir[cite: 13, 16].
    
    # regex: 'GANO' kelimesini bul, aradaki boşlukları/noktalamaları geç ve sayıyı al.
    matches = re.findall(r"GANO\s*[:\s]*([0-4][\.]\d{1,2})", full_text, re.IGNORECASE)
    
    if matches:
        # Listedeki en son eşleşme, transkriptin en altındaki güncel GANO'dur.
        return float(matches[-1])
        
    return None

def kod_uret(yuzde):
    # 8 haneli: 6 hane rastgele + 2 hane indirim yüzdesi
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort veriyi analiz ediyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Doğrulanan En Güncel GANO: **{gano}**")
        
        indirim = 0
        # GANO aralıklarına göre indirim oranları
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) 2.50 sınırının altında kaldığı için kod oluşturulamadı.")
    else:
        st.error("GANO bilgisi otomatik tespit edilemedi.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
