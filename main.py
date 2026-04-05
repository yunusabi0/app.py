import streamlit as st
import random
import string

# Sayfa Ayarları
st.set_page_config(page_title="GanoPort | İndirim Portalı", page_icon="🎓")

# Tasarım ve Başlık
st.title("🎓 GanoPort")
st.subheader("Başarıyı Ödüllendiren Destek Platformu")
st.write("Toplumsal Destek Projeleri kapsamında, akademik başarınızı yurt dışı hayallerinize dönüştürüyoruz.")

st.divider()

# Kullanıcı Bilgileri
st.info("Lütfen güncel transkriptinizi PDF formatında yükleyin ve GANO bilginizi girin.")

uploaded_file = st.file_uploader("Transkriptinizi Yükleyin (PDF)", type=["pdf"])
gano = st.number_input("GANO (Genel Akademik Not Ortalaması):", 
                       min_value=0.0, max_value=4.0, step=0.01, format="%.2f")

# İndirim Kodu Üretici
def kod_uret(yuzde):
    # İlk 6 hane rastgele büyük harf ve rakam
    karakterler = string.ascii_uppercase + string.digits
    rastgele_kisim = ''.join(random.choices(karakterler, k=6))
    # Toplam 8 hane: 6 hane rastgele + 2 hane indirim yüzdesi
    return f"{rastgele_kisim}{yuzde}"

# Hesaplama ve Sonuç
if st.button("İndirim Kodumu Oluştur"):
    if uploaded_file is not None:
        indirim_orani = 0
        
        # Senin belirttiğin kriterler:
        if 2.50 <= gano < 3.00:
            indirim_orani = 10
        elif 3.00 <= gano < 3.50:
            indirim_orani = 20
        elif 3.50 <= gano <= 4.00:
            indirim_orani = 30
        
        if indirim_orani > 0:
            ozel_kod = kod_uret(indirim_orani)
            st.balloons() # Tebrik efekti
            st.success(f"Tebrikler! GANO puanınıza göre %{indirim_orani} indirim kazandınız.")
            
            # Kodun büyük ve kopyalanabilir görünmesi için kutu içine alıyoruz
            st.code(ozel_kod, language="text")
            
            st.write(f"**Kod Detayları:**")
            st.write(f"* İndirim Oranı: %{indirim_orani}")
            st.write(f"* Kullanım Alanı: İşbirlikçi Yurt Dışı Danışmanlık Firması")
            st.caption("Not: Kodun son iki hanesi indirim yüzdenizi temsil etmektedir.")
        else:
            st.error("Üzgünüz, indirim koduna hak kazanmak için GANO'nun en az 2.50 olması gerekmektedir.")
    else:
        st.warning("Lütfen geçerli bir transkript dosyası yüklediğinizden emin olun.")

st.divider()
st.caption("© 2026 GanoPort - Toplumsal Destek Projeleri")
