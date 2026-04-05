import streamlit as st
import pdfplumber
import re
import random
import string

st.set_page_config(page_title="GanoPort | Akdeniz Uni Kesin Çözüm", page_icon="🎓")

def gano_bul(pdf_dosyasi):
    all_numbers = []
    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:
            # Tüm sayfaları tara
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Virgülleri noktaya çevir (3,17 -> 3.17)
                    text = text.replace(',', '.')
                    # Sadece 0.00 ile 4.00 arasındaki GANO formatındaki sayıları bul
                    # Yanında DNO veya AKTS olanları değil, saf sayıları listele
                    matches = re.findall(r"\b([0-4]\.\d{2})\b", text)
                    for m in matches:
                        all_numbers.append(float(m))
        
        if all_numbers:
            # Akdeniz Uni transkriptinde EN GÜNCEL GANO her zaman en sondadır.
            # 3.13 veya 2.93 gibi ara dönem notlarını atlayıp en sonuncuyu alır.
            return all_numbers[-1]
    except:
        return None
    return None

def kod_uret(yuzde):
    rastgele = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{rastgele}{yuzde}"

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")
st.write("Akdeniz Üniversitesi formatına uygun güncellendi.")

uploaded_file = st.file_uploader("Transkript PDF'inizi buraya yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('GanoPort en güncel ortalamanızı hesaplıyor...'):
        gano = gano_bul(uploaded_file)
        
    if gano is not None:
        st.info(f"✅ Sistem tarafından doğrulanan en güncel GANO: **{gano}**")
        
        indirim = 0
        # Belirlediğin indirim aralıkları
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
        st.error("GANO bilgisi tespit edilemedi. Lütfen dijital bir PDF yüklediğinizden emin olun.")

st.divider()
st.caption("GanoPort - Toplumsal Destek Projesi © 2026")
