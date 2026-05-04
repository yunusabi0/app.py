import streamlit as st
import pdfplumber
import re
import hashlib
import os

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------
# TASARIM
# ----------------------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://tr.key.study/wp-content/uploads/2025/02/1-1.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.block-container {
    background: rgba(20, 25, 40, 0.85);
    padding: 2rem;
    border-radius: 18px;
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SABİT KODLAR (GÖMÜLÜ)
# ----------------------------
def kodlari_yukle():
    return [
"GNP00120","GNP00220","GNP00320","GNP00420","GNP00520","GNP00620","GNP00720","GNP00820","GNP00920","GNP01020",
"GNP01120","GNP01220","GNP01320","GNP01420","GNP01520","GNP01620","GNP01720","GNP01820","GNP01920","GNP02020",
"GNP02120","GNP02220","GNP02320","GNP02420","GNP02520","GNP02620","GNP02720","GNP02820","GNP02920","GNP03020",
"GNP03120","GNP03220","GNP03320","GNP03420","GNP03520","GNP03620","GNP03720","GNP03820","GNP03920","GNP04020",
"GNP04120","GNP04220","GNP04320","GNP04420","GNP04520","GNP04620","GNP04720","GNP04820","GNP04920","GNP05020",
"GNP05120","GNP05220","GNP05320","GNP05420","GNP05520","GNP05620","GNP05720","GNP05820","GNP05920","GNP06020",
"GNP06120","GNP06220","GNP06320","GNP06420","GNP06520","GNP06620","GNP06720","GNP06820","GNP06920","GNP07020",
"GNP07120","GNP07220","GNP07320","GNP07420","GNP07520","GNP07620","GNP07720","GNP07820","GNP07920","GNP08020",
"GNP08120","GNP08220","GNP08320","GNP08420","GNP08520","GNP08620","GNP08720","GNP08820","GNP08920","GNP09020",
"GNP09120","GNP09220","GNP09320","GNP09420","GNP09520","GNP09620","GNP09720","GNP09820","GNP09920","GNP10020",

"GNP00130","GNP00230","GNP00330","GNP00430","GNP00530","GNP00630","GNP00730","GNP00830","GNP00930","GNP01030",
"GNP01130","GNP01230","GNP01330","GNP01430","GNP01530","GNP01630","GNP01730","GNP01830","GNP01930","GNP02030",
"GNP02130","GNP02230","GNP02330","GNP02430","GNP02530","GNP02630","GNP02730","GNP02830","GNP02930","GNP03030",
"GNP03130","GNP03230","GNP03330","GNP03430","GNP03530","GNP03630","GNP03730","GNP03830","GNP03930","GNP04030",
"GNP04130","GNP04230","GNP04330","GNP04430","GNP04530","GNP04630","GNP04730","GNP04830","GNP04930","GNP05030",
"GNP05130","GNP05230","GNP05330","GNP05430","GNP05530","GNP05630","GNP05730","GNP05830","GNP05930","GNP06030",
"GNP06130","GNP06230","GNP06330","GNP06430","GNP06530","GNP06630","GNP06730","GNP06830","GNP06930","GNP07030",
"GNP07130","GNP07230","GNP07330","GNP07430","GNP07530","GNP07630","GNP07730","GNP07830","GNP07930","GNP08030",
"GNP08130","GNP08230","GNP08330","GNP08430","GNP08530","GNP08630","GNP08730","GNP08830","GNP08930","GNP09030",
"GNP09130","GNP09230","GNP09330","GNP09430","GNP09530","GNP09630","GNP09730","GNP09830","GNP09930","GNP10030",

"GNP00140","GNP00240","GNP00340","GNP00440","GNP00540","GNP00640","GNP00740","GNP00840","GNP00940","GNP01040",
"GNP01140","GNP01240","GNP01340","GNP01440","GNP01540","GNP01640","GNP01740","GNP01840","GNP01940","GNP02040",
"GNP02140","GNP02240","GNP02340","GNP02440","GNP02540","GNP02640","GNP02740","GNP02840","GNP02940","GNP03040",
"GNP03140","GNP03240","GNP03340","GNP03440","GNP03540","GNP03640","GNP03740","GNP03840","GNP03940","GNP04040",
"GNP04140","GNP04240","GNP04340","GNP04440","GNP04540","GNP04640","GNP04740","GNP04840","GNP04940","GNP05040",
"GNP05140","GNP05240","GNP05340","GNP05440","GNP05540","GNP05640","GNP05740","GNP05840","GNP05940","GNP06040",
"GNP06140","GNP06240","GNP06340","GNP06440","GNP06540","GNP06640","GNP06740","GNP06840","GNP06940","GNP07040",
"GNP07140","GNP07240","GNP07340","GNP07440","GNP07540","GNP07640","GNP07740","GNP07840","GNP07940","GNP08040",
"GNP08140","GNP08240","GNP08340","GNP08440","GNP08540","GNP08640","GNP08740","GNP08840","GNP08940","GNP09040",
"GNP09140","GNP09240","GNP09340","GNP09440","GNP09540","GNP09640","GNP09740","GNP09840","GNP09940","GNP10040"
    ]

# ----------------------------
# DOSYALAR (KALICI)
# ----------------------------
KULLANILAN_KOD_DOSYA = "kullanilan_kodlar.txt"
PDF_DOSYA = "kullanilan_pdfler.txt"

for d in [KULLANILAN_KOD_DOSYA, PDF_DOSYA]:
    if not os.path.exists(d):
        open(d, "w").close()

def kullanilan_kodlari_getir():
    with open(KULLANILAN_KOD_DOSYA) as f:
        return set(line.strip() for line in f)

def kod_kaydet(kod):
    with open(KULLANILAN_KOD_DOSYA, "a") as f:
        f.write(kod + "\n")

def kullanilan_pdfleri_getir():
    with open(PDF_DOSYA) as f:
        return set(line.strip() for line in f)

def pdf_kaydet(h):
    with open(PDF_DOSYA, "a") as f:
        f.write(h + "\n")

# ----------------------------
# PDF HASH
# ----------------------------
def pdf_hash(file):
    return hashlib.md5(file.getvalue()).hexdigest()

# ----------------------------
# KOD VER
# ----------------------------
def kod_al(indirim, pdf):
    h = pdf_hash(pdf)

    if h in kullanilan_pdfleri_getir():
        return None

    tum = kodlari_yukle()
    kullanilan = kullanilan_kodlari_getir()

    uygun = [k for k in tum if k.endswith(str(indirim)) and k not in kullanilan]

    if not uygun:
        return None

    kod = uygun[0]
    kod_kaydet(kod)
    pdf_kaydet(h)

    return kod

# ----------------------------
# GANO OKUMA
# ----------------------------
def gano_bul(pdf):
    try:
        with pdfplumber.open(pdf) as p:
            text = ""
            for page in p.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

        text = text.replace(",", ".")

        for line in text.split("\n"):
            if "Top.Krd/GANO" in line:
                m = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)
                if m:
                    return float(m.group(1))

        m = re.search(r"GANO\s*[: ]\s*([0-4]\.\d{1,2})", text, re.I)
        if m:
            return float(m.group(1))
    except:
        return None

# ----------------------------
# UI
# ----------------------------
st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

file = st.file_uploader("Transkript PDF yükleyin", type="pdf")

if file:
    with st.spinner("Analiz ediliyor..."):
        gano = gano_bul(file)

    if gano:
        st.success(f"GANO: {gano}")

        indirim = 0
        if 2.50 <= gano < 3.00:
            indirim = 20
        elif 3.00 <= gano < 3.50:
            indirim = 30
        elif 3.50 <= gano <= 4.00:
            indirim = 40

        if indirim:
            kod = kod_al(indirim, file)

            if kod:
                st.balloons()
                st.success(f"%{indirim} indirim kazandınız!")
                st.code(kod)
            else:
                st.error("Kod alınmış ya da kalmamış.")
        else:
            st.warning("GANO yetersiz.")
    else:
        st.error("GANO okunamadı.")
st.divider()

st.markdown(
    'Bu site **Toplumsal Destek Projeleri** dersi kapsamında '
    '[İLAZDO](https://www.instagram.com/ilazdo?igsh=MTk2NHE5aDBiYTBkMA==) işbirliği sonucu hazırlanmıştır.'

    'Destek:ganoport@gmail.com '
    'webmaster@ilazdo.com '
)
