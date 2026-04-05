import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    full_text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                full_text += content + "\n"
    
    # Virgülleri noktaya çevir (3,17 -> 3.17)
    full_text = full_text.replace(',', '.')
    
    # AKDENİZ ÜNİVERSİTESİ ÖZEL FİLTRESİ:
    # Transkriptin başında "Top.Krd/GANO" kısmında yazan genel ortalamayı hedefler.
    genel_gano_match = re.search(r"Top\.Krd/GANO/Yüzlük Not\s*:\s*\d+/([0-4][\.]\d{1,2})", full_text)
    
    if genel_gano_match:
        return float(genel_gano_match.group(1))

    # Eğer yukarıdaki özel kalıp bulunamazsa, metindeki TÜM GANO etiketlerini bul
    # Akdeniz transkriptinde gerçek genel ortalama genellikle üstte veya en sondadır.
    all_ganos = re.findall(r"GANO\s*[:\s]*([0-4][\.]\d{1,2})", full_text, re.IGNORECASE)
    
    if all_ganos:
        # 3.17'yi bulmak için listedeki ilk veya son değerleri kontrol ederiz.
        # Senin transkriptinde genel toplam en üstte 3,17 olarak belirtilmiş.
        return float(all_ganos[0]) 
        
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort veriyi analiz ediyor...'):
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
            st.error(f"GANO ({gano}) indirim için yeterli değil (Min: 2.50).")
    else:
        st.error("GANO tespit edilemedi. Lütfen belgenin okunabilir olduğundan emin olun.")

st.divider()
st.caption("GanoPort - Akdeniz Üniversitesi Toplumsal Destek Projesi © 2026")
