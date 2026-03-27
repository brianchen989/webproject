
// 告訴程式：等網頁全部載入完畢後，再開始執行這裡面的程式碼
document.addEventListener("DOMContentLoaded", function () {

    // 1. 選取圖片物件
    const image = document.getElementById('raccoon1');
    const chatWindow = document.getElementById('chat-window');
    const closeBtn = document.getElementById('close-chat');

    // 2. 如果成功抓到圖片，才幫它掛上「點擊事件」的監聽器
    if (image) {
        image.addEventListener('click', function () {
            // toggle 的意思是：如果原本藏著就顯示，顯示著就藏起來
            chatWindow.classList.toggle('chat-hidden');
        });
    }

    // 3. 「✖」按鈕的功能
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            // 強制加上隱藏的 class
            chatWindow.classList.add('chat-hidden');
        });
    }

    const quotes = [
        { text: "在這個世界上，有兩種力量，一是劍，二是筆。<br>最後，劍會被筆所征服。", author: "佐藤長治" },
        { text: "成功不是終點，失敗也不是終結，最重要的是勇於前行。", author: "丘吉爾" },
        { text: "相信自己，你就能創造奇蹟。", author: "匿名" },
        { text: "行動是治療恐懼的良藥。", author: "匿名" },
        { text: "不怕慢，只怕站。", author: "中國諺語" }
    ];
    // 隨機選一則語錄
    const random = quotes[Math.floor(Math.random() * quotes.length)];
    document.getElementById("quoteBlock").innerHTML =
        `<p>${random.text}</p><p>— ${random.author}</p>`;




});

// 作品輯切換功能
let currentImageIndex = 0;
const images = [
    { src: "static/image/浣熊施工中.png", name: 'pygame', alt: "pygame", url: '' },
    { src: "static/image/浣熊施工中.png", name: '太空旅行', alt: "太空旅行", url: '' },
    { src: "static/image/浣熊施工中.png", name: '練PYTHON', alt: "練PYTHON", url: '' }
];
images.style.width = "100px";
images.style.height = "100px";

// 更新顯示並綁定點擊連結
function updateProductDisplay() {
    const productImage = document.getElementById('productImage');
    const productName = document.getElementById('productName');
    if (!productImage || !productName) return;

    productImage.src = images[currentImageIndex].src;
    productImage.alt = images[currentImageIndex].alt;
    productName.textContent = images[currentImageIndex].name;

    // 點圖片跳轉（在新分頁開啟）
    productImage.style.cursor = 'pointer';
    productImage.onclick = () => {
        const url = images[currentImageIndex].url;
        if (url) window.open(url, '_blank');
    };
}
// 切到上一張
function left_btn_click() {
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
    updateProductDisplay();
}
// 切到下一張
function right_btn_click() {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    updateProductDisplay();
}

// 初始化（載入時設定第一張）
document.addEventListener("DOMContentLoaded", function () {
    // ...existing DOMContentLoaded code...
    updateProductDisplay();
    updateAchievementDisplay();
});

function detail_btn_click() {
    window.location.href = "https://www.youtube.com/watch?v=FxfEzHiIgQU";
}