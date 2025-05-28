document.addEventListener("DOMContentLoaded", function () {
    console.log("📌 main.js DOMContentLoaded event çalıştı!");

    // 📌 Dosya yükleme sayfası (egitim_bilgi_formu.html için)
    if (document.getElementById("uploadForm")) {
        console.log("✅ Upload form sayfası tespit edildi!");
        // Bu sayfa için ayrı script kodu egitim_bilgi_formu.html içinde zaten var
        // Burada ek bir şey yapmaya gerek yok
    }

    // 📌 Çıktı sayfası kontrolü
    if (document.getElementById("outputContainer")) {
        console.log("✅ Çıktı sayfası tespit edildi!");
        
        let savedData = JSON.parse(localStorage.getItem("egitimData") || "{}");
        console.log("💾 Çıktı sayfası için localStorage verisi:", savedData);

        // Temel bilgileri doldur
        if (document.getElementById("displayEgitimAdi")) {
            document.getElementById("displayEgitimAdi").textContent = savedData.egitim_adi || "Bilinmiyor";
        }
        if (document.getElementById("displayEgitmenAdi")) {
            document.getElementById("displayEgitmenAdi").textContent = savedData.egitmen_adi || "Bilinmiyor";
        }
        if (document.getElementById("displayEgitimSuresi")) {
            document.getElementById("displayEgitimSuresi").textContent = savedData.egitim_suresi || "Bilinmiyor";
        }
        if (document.getElementById("displayEgitimID")) {
            document.getElementById("displayEgitimID").textContent = savedData.id || "Bilinmiyor";
        }
        if (document.getElementById("displayEgitimOzeti")) {
            document.getElementById("displayEgitimOzeti").innerText = savedData.egitim_ozeti || "Bilinmiyor";
        }
        if (document.getElementById("displayHedefKitle")) {
            document.getElementById("displayHedefKitle").innerText = savedData.hedef_kitle || "Bilinmiyor";
        }
        if (document.getElementById("displayKazanimlar")) {
            document.getElementById("displayKazanimlar").innerText = savedData.kazanimlar || "Bilinmiyor";
        }
        if (document.getElementById("displayAmac")) {
            document.getElementById("displayAmac").innerText = savedData.amac || "Bilinmiyor";
        }
        if (document.getElementById("displayKullanilanProgramlar")) {
            document.getElementById("displayKullanilanProgramlar").innerText = savedData.kullanilan_programlar || "Bilinmiyor";
        }

        // Link formatlaması ile özel alanlar
        // Gereksinimler formatlaması
        if (document.getElementById("displayGereksinimler")) {
            if (savedData.gereksinimler) {
                const inputText = savedData.gereksinimler;
                const formattedText = inputText.replace(/https?:\/\/[^\s]+/g, (url) => {
                    return `<a href="${url}" target="_blank" style="color:black; text-decoration:none;">${url}</a>`;
                }).replace(/\n/g, "<br>");
                document.getElementById("displayGereksinimler").innerHTML = formattedText;
            } else {
                document.getElementById("displayGereksinimler").innerHTML = "Bilinmiyor";
            }
        }

        // Kaynak Dokümanlar formatlaması
        if (document.getElementById("displayKaynakDokumanlar")) {
            if (savedData.kaynak_dokumanlar) {
                const inputText = savedData.kaynak_dokumanlar;
                const formattedText = inputText.replace(/https?:\/\/[^\s]+/g, (url) => {
                    return `<a href="${url}" target="_blank" style="color:black; text-decoration:none;">${url}</a>`;
                }).replace(/\n/g, "<br>");
                document.getElementById("displayKaynakDokumanlar").innerHTML = formattedText;
            } else {
                document.getElementById("displayKaynakDokumanlar").innerHTML = "Bilinmiyor";
            }
        }

        // Yardımcı Kaynaklar formatlaması
        if (document.getElementById("displayYardimciKaynaklar")) {
            if (savedData.yardimci_kaynaklar) {
                const inputText = savedData.yardimci_kaynaklar;
                const formattedText = inputText.replace(/https?:\/\/[^\s]+/g, (url) => {
                    return `<a href="${url}" target="_blank" style="color:black; text-decoration:none;">${url}</a>`;
                }).replace(/\n/g, "<br>");
                document.getElementById("displayYardimciKaynaklar").innerHTML = formattedText;
            } else {
                document.getElementById("displayYardimciKaynaklar").innerHTML = "Bilinmiyor";
            }
        }

        // 📌 Yazdırma sırasında butonları gizle
        window.onbeforeprint = function () {
            if (document.getElementById("printBtn")) {
                document.getElementById("printBtn").style.display = "none";
            }
            if (document.getElementById("wordConvertBtn")) {
                document.getElementById("wordConvertBtn").style.display = "none";
            }
        };

        window.onafterprint = function () {
            if (document.getElementById("printBtn")) {
                document.getElementById("printBtn").style.display = "block";
            }
            if (document.getElementById("wordConvertBtn")) {
                document.getElementById("wordConvertBtn").style.display = "block";
            }
        };
    }
});

// ✅ Yazdırma işlemi
function printPage() {
    window.print();
}

// ✅ Modal Aç
function openPdfModal() {
    if (document.getElementById("pdfModal")) {
        document.getElementById("pdfModal").style.display = "block";
    }
}

// ✅ Modal Kapat
function closePdfModal() {
    if (document.getElementById("pdfModal")) {
        document.getElementById("pdfModal").style.display = "none";
    }
}

// ✅ PDF'den Word'e çevir
function convertToWord() {
    let fileInput = document.getElementById("pdfFileInput");
    
    if (!fileInput || !fileInput.files[0]) {
        alert("Lütfen bir PDF dosyası seçin!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

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