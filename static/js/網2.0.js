
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

    // ==========================================
    // [AI 助手前端互動邏輯]
    // 負責從網頁取得使用者輸入的訊息，並傳送給後端的 Flask 伺服器
    // 交互檔案： 
    // - 後端 Python: main.py (負責在 /api/chat 處理這裡送出的資料，並呼叫 Gemini API)
    // - 介面 HTML: static/templates/index.html (包含 id="chat-submit", id="chat-input" 等畫面元素)
    // ==========================================
    const chatSubmit = document.getElementById('chat-submit');     // 綁定「送出」按鈕
    const chatInput = document.getElementById('chat-input');       // 綁定「文字輸入框」
    const chatMessages = document.getElementById('chat-messages'); // 綁定「對話顯示區」長方塊

    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return; // 防呆機制：如果發送空白文字就不往後執行

        // 1. 將使用者的文字包裝成一個氣泡元素，並顯示在畫面上
        const userDiv = document.createElement("div"); // 建立一個div元素做為對話氣泡
        userDiv.className = "chat-message user";       // 設定專屬樣式（在 CSS 中定義，靠右顯示）
        userDiv.innerText = text;                      // 將使用者輸入的文字塞進去
        chatMessages.appendChild(userDiv);             // 將這個氣泡加入到對話顯示區
        
        chatInput.value = ""; // 送出後清空輸入框
        chatMessages.scrollTop = chatMessages.scrollHeight; // 把畫面捲軸滾到最下面，方便看最新訊息

        // 2. 呼叫後端 API：透過 POST 請求將文字 JSON 化，發給 main.py 的 /api/chat 路由
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text }) // 打包成 JSON 格式發送，例如 {"message": "你好"}
        })
            .then(res => res.json()) // 接收從後端 main.py 回傳的執行結果，並解開 JSON
            .then(data => {
                // 3. 根據後端回傳回來的結果 (data.reply) 產生 AI 的對話氣泡
                const aiDiv = document.createElement("div");
                aiDiv.className = "chat-message ai"; // 設定 AI 專屬樣式（靠左顯示，底色不同）
                
                // 如果後端有發生錯誤，會把 "data.error" 丟回來，這裡如果沒有 reply 就顯示 error
                aiDiv.innerText = data.reply || data.error; 
                chatMessages.appendChild(aiDiv);
                
                // 再次將捲軸滾動到最底，確保使用者看到 AI 剛回覆的訊息
                chatMessages.scrollTop = chatMessages.scrollHeight; 
            })
            .catch(err => {
                // 4. 如果斷線、或其他原因導致完全連不到 Flask 伺服器，會在這裡顯示錯誤
                const errDiv = document.createElement("div");
                errDiv.className = "chat-message ai";
                errDiv.innerText = "網路連線失敗，請稍後再試！";
                chatMessages.appendChild(errDiv);
            });
    }

    // 當點擊「送出」按鈕時，觸發上面的 sendMessage 函式
    if (chatSubmit) chatSubmit.addEventListener('click', sendMessage);
    
    // 當專注在輸入框並且按下「Enter鍵」時，也一樣觸發 sendMessage 函式發出訊息
    if (chatInput) {
        chatInput.addEventListener('keypress', function (e) {
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
    { src: "static/image/quiz.png", name: '基本測驗', alt: "基本測驗", url: 'quiz.html' },
    { src: "static/image/浣熊施工中.png", name: '太空旅行', alt: "太空旅行", url: '' },
    { src: "static/image/浣熊施工中.png", name: '練PYTHON', alt: "練PYTHON", url: '' }
];

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
});

function detail_btn_click() {
    window.location.href = "https://www.youtube.com/watch?v=FxfEzHiIgQU";
}