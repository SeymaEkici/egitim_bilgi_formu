document.addEventListener("DOMContentLoaded", function () {

    console.log("📌 DOMContentLoaded event çalıştı!");

    // 📌 Dosya yükleme sayfası
    if (document.getElementById("uploadForm")) {
        document.getElementById("uploadForm").addEventListener("submit", async function (event) {
            event.preventDefault();
            let fileInput = document.getElementById("fileInput").files[0];

            if (!fileInput) {
                alert("Lütfen bir .docx dosyası seçin!");
                return;
            }

            let formData = new FormData();
            formData.append("file", fileInput);

            try {
                console.log("📤 Dosya backend’e gönderiliyor...");
                let response = await fetch("http://127.0.0.1:8001/docx/read", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("Dosya yükleme başarısız! HTTP Hata: " + response.status);
                }

                let result = await response.json();
                console.log("✅ Backend JSON Yanıtı:", result);

                if (result.parsed_data) {
                    console.log("📂 Kaydedilecek Veri:", result.parsed_data); // ✅ Konsola backend verisini bas
                    localStorage.setItem("egitimData", JSON.stringify(result.parsed_data));

                    // 🌟 localStorage’a kaydedilen veriyi kontrol et
                    console.log("💾 localStorage Verisi:", localStorage.getItem("egitimData"));

                    window.location.href = "eksik_veri_formu.html";
                } else {
                    alert("Hata: Backend JSON verisi boş geldi!");
                }

            } catch (error) {
                console.error("Hata:", error);
                alert("Dosya yükleme başarısız! Hata: " + error.message);
            }
        });
    }

    // 📌 Eksik veri formu sayfası
    document.addEventListener("DOMContentLoaded", function () {

        console.log("📌 DOMContentLoaded event çalıştı!");
    
        if (document.getElementById("missingDataForm")) {
            console.log("✅ missingDataForm bulundu!");
            
            let savedData = JSON.parse(localStorage.getItem("egitimData") || "{}");
            console.log("💾 localStorage'tan alınan veri:", savedData);
    
            document.getElementById("id").value = savedData.id || "";
            document.getElementById("egitimAdi").value = savedData.egitim_adi || "";
            document.getElementById("egitmenAdi").value = savedData.egitmen_adi || "";
            document.getElementById("egitimSuresi").value = savedData.egitim_suresi || "";
            document.getElementById("egitimOzeti").value = savedData.egitim_ozeti || "";
            document.getElementById("hedefKitle").value = savedData.hedef_kitle || "";
            document.getElementById("kaynakDokumanlar").value = savedData.kaynak_dokumanlar || "";
            document.getElementById("kazanimlar").value = savedData.kazanimlar || "";
            document.getElementById("amac").value = savedData.amac || "";
            document.getElementById("gereksinimler").value = savedData.gereksinimler || "";
            document.getElementById("kullanilacak_programlar").value = savedData.kullanilacak_programlar || "";
            document.getElementById("yardimciKaynaklar").value = savedData.yardimciKaynaklar || "";
    
            document.getElementById("missingDataForm").addEventListener("submit", function (event) {
                event.preventDefault();
                submitForm();
            });
    
        } else {
            console.error("⛔ Hata: missingDataForm bulunamadı! HTML içinde eksik olabilir.");
        }
    });

    // 📌 Çıktı sayfasında mıyız?
    if (document.getElementById("outputContainer")) {
        let savedData = JSON.parse(localStorage.getItem("egitimData") || "{}");

        document.getElementById("displayEgitimAdi").innerText = savedData.egitim_adi || "Bilinmiyor";
        document.getElementById("displayEgitmenAdi").innerText = savedData.egitmen_adi || "Bilinmiyor";
        document.getElementById("displayEgitimSuresi").innerText = savedData.egitim_suresi || "Bilinmiyor";
        document.getElementById("displayEgitimOzeti").innerText = savedData.egitim_ozeti || "Bilinmiyor";
        document.getElementById("displayHedefKitle").innerText = savedData.hedef_kitle || "Bilinmiyor";
        document.getElementById("displayKaynakDokumanlar").innerText = savedData.kaynak_dokumanlar || "Bilinmiyor";
        document.getElementById("displayGereksinimler").innerText = savedData.gereksinimler || "Bilinmiyor";
        document.getElementById("displayKazanimlar").innerText = savedData.kazanimlar || "Bilinmiyor";
        document.getElementById("displayAmac").innerText = savedData.amac || "Bilinmiyor";
        document.getElementById("displayKullanilacakProgramlar").innerText = savedData.kullanilacak_programlar || "Bilinmiyor";
        document.getElementById("displayYardimciKaynaklar").innerText = savedData.yardimciKaynaklar || "Bilinmiyor";

        // Yazdırma sırasında butonları gizle
        window.onbeforeprint = function () {
            document.getElementById("printBtn").style.display = "none";
            document.getElementById("wordDownloadBtn").style.display = "none";
        };

        window.onafterprint = function () {
            document.getElementById("printBtn").style.display = "block";
            document.getElementById("wordDownloadBtn").style.display = "block";
        };
    }
});

// ✅ Eksik verileri kaydetme fonksiyonu
function submitForm() {

    let formData = {
        id: document.getElementById("id").value,
        egitim_adi: document.getElementById("egitimAdi").value,
        egitmen_adi: document.getElementById("egitmenAdi").value,
        egitim_suresi: document.getElementById("egitimSuresi").value,
        egitim_ozeti: document.getElementById("egitimOzeti").value,
        hedef_kitle: document.getElementById("hedefKitle").value,
        kaynak_dokumanlar: document.getElementById("kaynakDokumanlar").value,
        kazanimlar: document.getElementById("kazanimlar").value,
        amac: document.getElementById("amac").value,
        gereksinimler: document.getElementById("gereksinimler").value,
        kullanilacak_programlar: document.getElementById("kullanilacak_programlar").value,
        yardimciKaynaklar: document.getElementById("yardimciKaynaklar").value,
    };

    localStorage.setItem("egitimData", JSON.stringify(formData));
    window.location.href = "egitim_cikti.html";
}

// ✅ Yazdırma işlemi
function printPage() {
    window.print();
}

// ✅ Word dosyası dönüştürme işlemi (masaüstünden dosya seçilecek)
function convertToWord() {
    let fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".pdf";
    fileInput.style.display = "none";

    fileInput.addEventListener("change", function () {
        let file = fileInput.files[0];

        if (file) {
            let formData = new FormData();
            formData.append("pdf_path", file);

            fetch("http://127.0.0.1:8001/word/generate", {
                method: "POST",
                body: formData
            })
                .then(response => response.blob())
                .then(blob => {
                    let link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = "egitim_bilgileri.docx";
                    link.click();
                })
                .catch(error => console.error("Hata:", error));
        }
    });

    fileInput.click();
}
document.addEventListener("DOMContentLoaded", function () {

    // 📌 Çıktı sayfasında mıyız?
    if (document.getElementById("outputContainer")) {
        let savedData = JSON.parse(localStorage.getItem("egitimData") || "{}");

        document.getElementById("displayEgitimAdi").textContent = savedData.egitim_adi || "Bilinmiyor";
        document.getElementById("displayEgitmenAdi").textContent = savedData.egitmen_adi || "Bilinmiyor";
        document.getElementById("displayEgitimSuresi").textContent = savedData.egitim_suresi || "Bilinmiyor";
        document.getElementById("displayEgitimOzeti").innerText = savedData.egitim_ozeti || "Bilinmiyor";
        document.getElementById("displayHedefKitle").innerText = savedData.hedef_kitle || "Bilinmiyor";
        document.getElementById("displayKaynakDokumanlar").innerText = savedData.kaynak_dokumanlar || "Bilinmiyor";
        document.getElementById("displayEgitimID").textContent = savedData.id || "Bilinmiyor";
        document.getElementById("displayGereksinimler").innerText = savedData.gereksinimler || "Bilinmiyor";
        document.getElementById("displayKazanimlar").innerText = savedData.kazanimlar || "Bilinmiyor";
        document.getElementById("displayAmac").innerText = savedData.amac || "Bilinmiyor";
        document.getElementById("displayKullanilacakProgramlar").innerText = savedData.kullanilacak_programlar || "Bilinmiyor";
        document.getElementById("displayYardimciKaynaklar").innerText = savedData.yardimciKaynaklar || "Bilinmiyor";

        // 📌 Yazdırma sırasında butonları gizle
        window.onbeforeprint = function () {
            document.getElementById("printBtn").style.display = "none";
            document.getElementById("wordConvertBtn").style.display = "none";
        };

        window.onafterprint = function () {
            document.getElementById("printBtn").style.display = "block";
            document.getElementById("wordConvertBtn").style.display = "block";
        };
    }
});

// ✅ Modal Aç
function openPdfModal() {
    document.getElementById("pdfModal").style.display = "block";
}

// ✅ Modal Kapat
function closePdfModal() {
    document.getElementById("pdfModal").style.display = "none";
}

// ✅ PDF'den Word'e çevir
function convertToWord() {
    let fileInput = document.getElementById("pdfFileInput").files[0];

    if (!fileInput) {
        alert("Lütfen bir PDF dosyası seçin!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("http://127.0.0.1:8001/word/convert", {
        method: "POST",
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            let link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "egitim_bilgileri.docx";
            link.click();
        })
        .catch(error => console.error("Hata:", error));

    // ✅ Modal'ı kapat
    closePdfModal();
}