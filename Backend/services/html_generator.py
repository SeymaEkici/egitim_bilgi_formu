from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
import traceback

def generate_html_from_data(veri):
    """
    Verilen JSON verisini kullanarak HTML çıktısı oluşturur ve kaydeder.
    """
    try:
        # Mevcut çalışma dizini ve dosya yapısını kontrol et
        current_dir = os.getcwd()
        templates_dir = Path(current_dir) / "templates"
        template_file = templates_dir / "egitim_cikti.html"
        
        print(f"📂 Çalışma dizini: {current_dir}")
        print(f"📂 Templates dizini: {templates_dir}")
        print(f"📄 Şablon dosyası: {template_file}")
        
        # Templates klasörünün varlığını kontrol et
        if not templates_dir.exists():
            print(f"❌ HATA: Templates klasörü bulunamadı!")
            raise FileNotFoundError(f"Templates klasörü bulunamadı: {templates_dir}")
            
        # Şablon dosyasının varlığını kontrol et
        if not template_file.exists():
            print(f"❌ HATA: egitim_cikti.html şablonu bulunamadı!")
            raise FileNotFoundError(f"HTML şablonu bulunamadı: {template_file}")
        
        # Jinja2 ortamını ayarla
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("egitim_cikti.html")
        
        # HTML çıktısını oluştur
        html_output = template.render(**veri)

        # Dosyanın kaydedileceği yolu belirle
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)  # Eğer "output" klasörü yoksa oluştur

        output_path = output_dir / "updated_egitim_cikti.html"

        # HTML çıktısını kaydet
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)

        print(f"✅ HTML dosyası başarıyla oluşturuldu: {output_path}")
        return str(output_path)  # HTML dosyasının yolunu döndür

    except Exception as e:
        error_message = f"🚨 HTML oluşturma hatası: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        raise Exception(f"HTML oluşturma hatası: {str(e)}")