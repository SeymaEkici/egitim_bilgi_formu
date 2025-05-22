import pdfkit
import os
import traceback
from pathlib import Path

def generate_pdf():
    """
    Görünen HTML sayfasını alır ve PDF'ye çevirir.
    """
    try:
        print("PDF oluşturma işlemi başlatılıyor...")

        # HTML Çıktı Dosyasını Belirle
        html_path = Path("output") / "updated_egitim_cikti.html"

        print(f"📂 HTML dosya yolu: {html_path}")
        if not html_path.exists():
            print(f"❌ HATA: HTML dosyası bulunamadı: {html_path}")
            raise FileNotFoundError(f"HTML dosyası bulunamadı: {html_path}")

        # PDF Çıktı Dosyasını Belirle
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_output_path = output_dir / "egitim_bilgileri.pdf"

        print(f"📂 PDF çıktı yolu: {pdf_output_path}")

        # PDF Dönüştürme İşlemi
        try:
            pdfkit.from_file(str(html_path), str(pdf_output_path))
            print(f"✅ PDF başarıyla oluşturuldu: {pdf_output_path}")
        except Exception as pdf_error:
            print(f"🚨 PDF oluşturma hatası: {str(pdf_error)}")
            print("wkhtmltopdf kurulu mu kontrol ediliyor...")
            
            # Linux için alternatif yol dene
            try:
                config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
                pdfkit.from_file(str(html_path), str(pdf_output_path), configuration=config)
                print(f"✅ PDF alternatif yöntemle oluşturuldu: {pdf_output_path}")
            except Exception as alt_error:
                print(f"🚨 Alternatif PDF oluşturma hatası: {str(alt_error)}")
                print("⚠️ wkhtmltopdf kurulumu gerekiyor!")
                raise Exception("PDF oluşturulamadı, lütfen wkhtmltopdf kurulumunu kontrol edin.")

        return str(pdf_output_path)

    except Exception as e:
        error_message = f"🚨 PDF oluşturma hatası: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        raise Exception(error_message)