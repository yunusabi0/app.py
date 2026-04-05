import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Kesin Onay", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            # Akdeniz Uni formatında resmi GANO her zaman ilk sayfadaki üst tabloda yer alır.
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if text:
                # Virgülleri noktaya çevirerek standart hale getir (2,77 -> 2.77)
                text = text.replace(',', '.')
                
                # KRİTİK FİLTRE: Doğrudan "Top.Krd/GANO/Yüzlük Not" satırını hedef alıyoruz.
                # Alp'te ": 150/2.77/75.4" ve Yunus'ta ": 150/3.17/83.4" olan merkezi veriyi çeker.
                # Regex: İki adet '/' işareti arasındaki 0-4 arası rakamı yakalar.
                resmi_satir = re.search(r"Top\.Krd/GANO/Yüzlük Not\s*:\s*\d+/([0-4][\.]\d{1,2})/", text)
                
                if resmi_satir:
                    return float(resmi_satir.group(1))
                
                # YEDEK PLAN: Eğer yukarıdaki spesifik yapı bulunamazsa (farklı PDF motoru),
                # Sadece "GANO" kelimesini ara ama "DNO" olanları (Dönem Notu) kesinlikle ele.
                # Negative Lookbehind (?<!D) kullanarak DNO kelimesine takılmasını engelliyoruz.
                temiz_liste = re.findall(r"(?<!D)GANO\s*[:\s]*([0-4][\.]\d{1,2})", text, re.IGNORECASE)
                if temiz_liste:
                    # İlk sayfadaki ilk GANO değeri her zaman resmi "Genel" ortalamadır.
                    return float(temiz_liste[0])
                    
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
    with st.spinner('Resmi veriler doğrulanıyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        # Doğru değerin çekildiğini kullanıcıya gösteriyoruz
        st.info(f"✅ Doğrulanan Resmi GANO: **{gano}**")
        
        indirim = 0
        if 2.50 <= gano < 3.00: indirim = 10
        elif 3.00 <= gano < 3.50: indirim = 20
        elif 3.50 <= gano <= 4.00: indirim = 30
        
        if indirim > 0:
            st.balloons()
            st.success(f"Tebrikler! GANO puanınıza göre %{indirim} indirim kazandınız.")
            st.code(kod_uret(indirim), language="text")
        else:
            st.warning(f"GANO ({gano}) indirim alt sınırının (2.50) altında.")
    else:
        st.error("GANO bilgisi tespit edilemedi. Lütfen e-devlet formatında PDF yükleyin.")

st.divider()
st.caption("GanoPort - Akdeniz Üniversitesi Toplumsal Destek Projesi © 2026")
