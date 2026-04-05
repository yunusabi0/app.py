import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Final Doğrulama", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    full_text = ""
    with pdfplumber.open(pdf_dosyasi) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                full_text += content + "\n"
    
    if not full_text:
        return None

    # Virgülleri noktaya çevir (Örn: 2,77 -> 2.77)
    full_text = full_text.replace(',', '.')
    
    # STRATEJİ: Metin içindeki TÜM "GANO: X.XX" kalıplarını bulur.
    # Akdeniz Üniversitesi transkriptinde güncel GANO her zaman en sonda yazar.
    # Bu yüzden regex ile tüm eşleşmeleri alıp listedeki SONUNCU elemanı seçeceğiz.
    
    # "GANO:" kelimesinden sonra gelen 0.00-4.00 arası sayıları yakalar
    gano_listesi = re.findall(r"GANO\s*[:\s]*([0-4][\.]\d{1,2})", full_text, re.IGNORECASE)
    
    if gano_listesi:
        # Listeyi sayıya çevir ve en sondaki (en güncel) değeri döndür
        return float(gano_listesi[-1])
        
    return None

def kod_uret(yuzde):
    # 8 haneli: 6 hane rastgele + 2 hane indirim yüzdesi
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort güncel ortalamanızı hesaplıyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Doğrulanan En Güncel GANO: **{gano}**")
        
        indirim = 0
        # Belirlediğin indirim aralıkları
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kodunuz hazır.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.error(f"GANO ({gano}) indirim sınırının (2.50) altında kalıyor.")
    else:
        st.error("GANO bilgisi tespit edilemedi. Lütfen dijital transkript yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
