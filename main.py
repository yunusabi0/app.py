import streamlit as st
import pdfplumber
import re
import hashlib
import sqlite3

st.set_page_config(page_title="GanoPort", page_icon="🎓")

# ----------------------------

# VERİTABANI

# ----------------------------

conn = sqlite3.connect("gano.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS kullanilan_pdfler (hash TEXT PRIMARY KEY)")
c.execute("CREATE TABLE IF NOT EXISTS kodlar (kod TEXT PRIMARY KEY, kullanildi INTEGER DEFAULT 0)")
conn.commit()

# ----------------------------

# KODLARI EKLE

# ----------------------------

for i in range(1,101):
for tip in [20,30,40]:
kod = f"GNP{str(i).zfill(3)}{tip}"
try:
c.execute("INSERT INTO kodlar (kod) VALUES (?)", (kod,))
except:
pass
conn.commit()

# ----------------------------

# PDF HASH

# ----------------------------

def pdf_hash(file):
return hashlib.md5(file.getvalue()).hexdigest()

# ----------------------------

# KOD VER

# ----------------------------

def kod_al(indirim, pdf):
hash_degeri = pdf_hash(pdf)

```
c.execute("SELECT 1 FROM kullanilan_pdfler WHERE hash=?", (hash_degeri,))
if c.fetchone():
    return None

c.execute("SELECT kod FROM kodlar WHERE kullanildi=0 AND kod LIKE ? LIMIT 1", (f"%{indirim}",))
sonuc = c.fetchone()

if not sonuc:
    return None

kod = sonuc[0]

c.execute("UPDATE kodlar SET kullanildi=1 WHERE kod=?", (kod,))
c.execute("INSERT INTO kullanilan_pdfler (hash) VALUES (?)", (hash_degeri,))
conn.commit()

return kod
```

# ----------------------------

# GANO OKUMA

# ----------------------------

def gano_bul(pdf_dosyasi):
try:
with pdfplumber.open(pdf_dosyasi) as pdf:
text = ""
for page in pdf.pages:
t = page.extract_text()
if t:
text += t + "\n"

```
        text = text.replace(",", ".")

        for line in text.split("\n"):
            if "Top.Krd/GANO" in line:
                match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)
                if match:
                    return float(match.group(1))

        match = re.search(r"GANO\s*[: ]\s*([0-4]\.\d{1,2})", text, re.IGNORECASE)
        if match:
            return float(match.group(1))
except:
    return None
return None
```

# ----------------------------

# ARAYÜZ

# ----------------------------

st.title("🎓 GanoPort")
st.subheader("Otomatik Transkript Doğrulama Sistemi")

uploaded_file = st.file_uploader("Transkript PDF yükleyin", type="pdf")

if uploaded_file is not None:
with st.spinner("Analiz ediliyor..."):
gano = gano_bul(uploaded_file)

```
if gano is not None:
    st.success(f"GANO: {gano}")

    indirim = 0
    if 2.50 <= gano < 3.00:
        indirim = 20
    elif 3.00 <= gano < 3.50:
        indirim = 30
    elif 3.50 <= gano <= 4.00:
        indirim = 40

    if indirim > 0:
        kod = kod_al(indirim, uploaded_file)

        if kod:
            st.balloons()
            st.success(f"%{indirim} indirim kazandınız!")
            st.code(kod)
        else:
            st.error("Bu transkript için zaten kod alınmış veya kod kalmamış.")
    else:
        st.warning("İndirim için GANO yetersiz.")
else:
    st.error("GANO okunamadı.")
```
