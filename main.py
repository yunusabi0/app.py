import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni %100 Fix", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            # Akdeniz Uni transkriptinde tek gerçek GANO ilk sayfadaki kimlik kısmındadır.
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if text:
                # Sayısal tutarlılık için virgülleri noktaya çevir (2,77 -> 2.77)
                text = text.replace(',', '.')
                
                # NOKTA ATIŞI FİLTRE:
                # Alp'in belgesindeki ": 150/2.77/75.4" satırını hedefler.
                # Regex: 'Top.Krd/GANO' ifadesinden sonra gelen '/' işaretleri arasındaki sayıyı alır.
                resmi_gano_match = re.search(r"Top\.Krd/GANO/Yüzlük Not\s*:\s*\d+/([0-4][\.]\d{1,2})/", text)
                
                if resmi_gano_match:
                    return float(resmi_gano_match.group(1))
                
                # YEDEK PLAN: Eğer üstteki yapı bulunamazsa, 
                # Dönem Notu (DNO) olmayan ilk GANO ifadesini al.
                temiz_liste = re.findall(r"(?<!D)GANO\s*[:\s]*([0-4][\.]\d{1,2})", text, re.IGNORECASE)
                if temiz_liste:
                    return float(temiz_liste[0])
                    
    except Exception:
        return None
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF'inizi buraya sürükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Resmi kayıtlar taranıyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Doğrulanan Resmi GANO: **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! %{indirim} indirim kodunuz oluşturuldu.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.warning(f"GANO ({gano}) indirim için alt sınırın (2.50) altında.")
    else:
        st.error("GANO tespit edilemedi. Lütfen orijinal transkript yükleyin.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
