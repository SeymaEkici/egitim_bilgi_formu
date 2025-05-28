from docx import Document
from io import BytesIO
import traceback
import re
import uuid

def read_docx(file):
    """DOCX dosyasını okur ve JSON formatında döndürür."""
    try:
        doc = Document(BytesIO(file))

        data = {
            "id": "",
            "egitim_adi": "",
            "egitmen_adi": "",
            "egitim_suresi": "",
            "hedef_kitle": "",
            "egitim_ozeti": "",
            "kaynak_dokumanlar": "",
            "gereksinimler": "",
            "kazanimlar": "",
            "amac": "",
            "kullanilan_programlar": "",
            "yardimci_kaynaklar": ""
        }

        # Word başlıklarını data anahtarlarıyla eşleştirme tablosu
        header_mapping = {
            "Eğitimin Adı (Versiyon bilgisi eklenebilir)": "egitim_adi",
            "Eğitmenin Adı-Soyadı": "egitmen_adi", 
            "Eğitim Kodu (Akademi Tarafından Doldurulacaktır)": "id", 
            "Tahmini Eğitim Süresi": "egitim_suresi",
            "Hedef Kitle-Eğitim Seviyesi (Ortaokul, Lise, Üniversite)": "hedef_kitle",
            "Hedef Kitle-İlgi Alanları": "hedef_kitle",
            "Eğitim Özeti": "egitim_ozeti",
            "Kaynak Dokümanlar": "kaynak_dokumanlar",
            "Eğitim Gereksinimleri (Ön Koşul Beceriler)": "gereksinimler",
            "Çıktılar (Eğitim Kazanımları)": "kazanimlar",
            "Eğitimin Amacı": "amac",
            "Kullanılacak programlar (versiyon bilgisi eklenmeli)": "kullanilan_programlar",
            "Tavsiye Edilen/Yardımcı Kaynaklar": "yardimci_kaynaklar"
        }

        print("\n🔍 DOCX Dosyası Okunuyor...")

        # Hedef kitle verilerini biriktirmek için
        hedef_kitle_parts = []

        # Tablo içeriğini oku
        for table in doc.tables:
            for row in table.rows:
                if len(row.cells) >= 2:
                    key_text = normalize_header(row.cells[0].text)
                    value_text = clean_value(row.cells[1].text)

                    if key_text and value_text:
                        # Tam eşleşme kontrolü
                        matched_key = find_exact_match(key_text, header_mapping)
                        if matched_key:
                            field_name = header_mapping[matched_key]
                            
                            # Hedef kitle alanları için özel işlem
                            if field_name == "hedef_kitle":
                                hedef_kitle_parts.append(value_text)
                                print(f"✅ HEDEF KİTLE EKLENDİ: '{key_text}' -> {value_text}")
                            else:
                                data[field_name] = value_text
                                print(f"✅ EŞLEŞTİ: '{key_text}' -> {field_name}")
                        else:
                            print(f"❌ EŞLEŞMEDİ: '{key_text}'")

        # Hedef kitle verilerini birleştir
        if hedef_kitle_parts:
            data["hedef_kitle"] = ", ".join(hedef_kitle_parts)

        # ID eksikse otomatik oluştur
        if not data["id"]:
            data["id"] = str(uuid.uuid4())[:8]

        print(f"\n📊 Toplam {sum(1 for v in data.values() if v)} alan dolduruldu")
        return data

    except Exception as e:
        error_message = f"DOCX işleme hatası: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        raise Exception(error_message)


def normalize_header(text):
    """Başlık metinlerini normalize eder - parantezleri korur."""
    if not text:
        return ""
    
    # Sadece fazla boşlukları temizle, parantezleri koru
    text = re.sub(r'\s+', ' ', text.strip())
    # Başlangıç/bitiş yıldızları temizle
    text = text.strip('*').strip()
    
    return text


def clean_value(text):
    """Değer metinlerini temizler."""
    if not text:
        return ""
    
    # Fazla boşlukları, satır sonlarını temizle
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text


def find_exact_match(search_text, mapping_dict):
    """Sadece tam eşleşme arar, yoksa None döndürür."""
    search_clean = search_text.lower().strip()
    
    for key in mapping_dict.keys():
        key_clean = key.lower().strip()
        if key_clean == search_clean:
            return key
    
    return None