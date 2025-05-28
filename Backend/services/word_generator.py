from pathlib import Path
from pdf2docx import Converter

def generate_word(pdf_path: str):
    """
    JSON verisini kullanarak bir Word (DOCX) dosyası oluşturur.
    """
    try:
#        doc = Document()
#
#        # Başlık ekle
#        doc.add_heading('Eğitim Bilgi Formu', level=1)
#
#        # Verileri belgeye ekle - Burası komple text olarak atıyor ve şablonu bozuyor
#        for key, value in data.items():
#            doc.add_paragraph(f"{key}: {value}")
#
#        # Word dosyasını kaydet
#        output_path = Path("output") / "egitim_bilgileri.docx"
#        output_path.parent.mkdir(parents=True, exist_ok=True)  # Klasör yoksa oluştur
#        doc.save(output_path)
#
#        print(f"✅ Word dosyası başarıyla oluşturuldu: {output_path}")
#        return output_path  # Artık Path objesi döndürüyorsun

        # PDF'den DOCX'e dönüştürülecek dosyanın yolunu belirle
        output_path = Path("output") / f"{Path(pdf_path).stem}.docx"
        output_path.parent.mkdir(parents=True, exist_ok=True)  # Klasör yoksa oluştur
        
        # PDF'den DOCX'e dönüştürme işlemi
        cv = Converter(pdf_path)
        cv.convert(str(output_path), start=0, end=None)
        cv.close()

        print(f"✅ PDF dosyası başarıyla DOCX formatına dönüştürüldü: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ PDF dosyası dönüştürülürken bir hata oluştu: {e}")
        raise Exception("PDF dönüştürme sırasında bir hata oluştu.")