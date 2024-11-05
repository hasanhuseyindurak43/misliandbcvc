var sidebarBtn = document.getElementById('sidebarBtn')
var sidebarContainer = document.getElementById('sidebarContainer')


sidebarBtn.onclick = function selam() {
    if (sidebarContainer.style.marginLeft == "-100%") {
        sidebarContainer.style.marginLeft = "0%"
    }else{
        sidebarContainer.style.marginLeft = "-100%"
    }
}

var ids = "istek";
setInterval(function () {
    // istek id değiştirme
    // Karakter setimizi burada tanımlıyoruz.
    var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var str = "";
    // Rastgele karakter seçimi
    for (let i = 0; i < 5; i++) {
        str += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    // Rastgele karakter seçimi
    document.getElementById(`${ids}`).id = str;
    ids = str;

    // alert("Burası Captcha Bölümü");
    }, 5000); // 5 Saniye sonra yenileyecek.