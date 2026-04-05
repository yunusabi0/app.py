def gano_bul(pdf_dosyasi):

    try:
        with pdfplumber.open(pdf_dosyasi) as pdf:

            text = ""

            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

            text = text.replace(",", ".")

            # SATIR SATIR İNCELE
            for line in text.split("\n"):

                if "Top.Krd/GANO" in line:

                    # örnek: 150/2.77/75.4
                    match = re.search(r"\d+\s*/\s*([0-4]\.\d{1,2})\s*/", line)

                    if match:
                        return float(match.group(1))

            # YEDEK PLAN
            match = re.search(r"GANO\s*[: ]\s*([0-4]\.\d{1,2})", text, re.IGNORECASE)

            if match:
                return float(match.group(1))

    except Exception as e:
        print(e)

    return None
