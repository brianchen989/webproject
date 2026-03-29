
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

    // 4. 對話功能
    const chatSubmit = document.getElementById('chat-submit');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // 加上使用者的話
        const userDiv = document.createElement("div");
        userDiv.className = "chat-message user";
        userDiv.innerText = text;
        chatMessages.appendChild(userDiv);
        chatInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // 呼叫後端 API
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            const aiDiv = document.createElement("div");
            aiDiv.className = "chat-message ai";
            aiDiv.innerText = data.reply || data.error;
            chatMessages.appendChild(aiDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(err => {
            const errDiv = document.createElement("div");
            errDiv.className = "chat-message ai";
            errDiv.innerText = "網路連線失敗，請稍後再試！";
            chatMessages.appendChild(errDiv);
        });
    }

    if (chatSubmit) chatSubmit.addEventListener('click', sendMessage);
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    const quotes = [
        { text: "SDGs 的 17 個目標都有專屬顏色，但你知道嗎？這些顏色是經過精密設計的，目的是為了讓色盲人士也能輕鬆區分。此外，這些顏色組合在一起形成一個圓環（The SDG Wheel），象徵地球的完整與和諧。", author: "它是全世界最色彩繽紛的「密碼」" },
        { text: "大家都知道有 17 個目標（Goals），但其實底下還藏了 169 個細項目標（Targets）。", author: "它藏著 169 個「小任務」" },
        { text: "為了推廣這些目標，聯合國甚至找過知名音樂人製作歌曲，甚至連 《芝麻街》 的餅乾怪獸（Cookie Monster）和艾蒙（Elmo）都幫 SDGs 拍過宣傳片。這告訴我們：再嚴肅的議題，用「社群功能」和「視覺化」來推廣也是很重要的", author: "它用「可愛」攻佔人心" }
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