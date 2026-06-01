
// 告訴程式：等網頁全部載入完畢後，再開始執行這裡面的程式碼
document.addEventListener("DOMContentLoaded", function () {

    // 1. 選取圖片物件
    const image = document.getElementById('raccoon1');
    const chatWindow = document.getElementById('chat-window');
    const closeBtn = document.getElementById('close-chat');

    // 系統優化：平滑置底滾動函式
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // 2. 如果成功抓到圖片，才幫它掛上「點擊事件」的監聽器
    if (image) {
        image.addEventListener('click', function () {
            chatWindow.classList.toggle('chat-hidden');
            if (!chatWindow.classList.contains('chat-hidden')) {
                // 開啟時自動捲動至最新對話，並將輸入框聚焦
                scrollToBottom();
                if (chatInput) chatInput.focus();
            }
        });
    }

    // 3. 「✖」按鈕的功能
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            chatWindow.classList.add('chat-hidden');
        });
    }

    // ==========================================
    // [AI 助手前端互動邏輯]
    // 負責從網頁取得使用者輸入的訊息，並傳送給後端的 Flask 伺服器
    // ==========================================
    const chatSubmit = document.getElementById('chat-submit');     // 綁定「送出」按鈕
    const chatInput = document.getElementById('chat-input');       // 綁定「文字輸入框」
    const chatMessages = document.getElementById('chat-messages'); // 綁定「對話顯示區」長方塊

    // 系統優化：聊天歷史 sessionStorage 持久化儲存
    function saveMessageToHistory(role, text) {
        try {
            let history = JSON.parse(sessionStorage.getItem('chat_history')) || [];
            history.push({ role: role, text: text });
            // 最多保留最近 15 條對話紀錄，避免佔用過多瀏覽器記憶體
            if (history.length > 15) history.shift();
            sessionStorage.setItem('chat_history', JSON.stringify(history));
        } catch (e) {
            console.error("無法寫入 sessionStorage 歷史對話:", e);
        }
    }

    // 系統優化：從 sessionStorage 載入歷史訊息
    function loadChatHistory() {
        if (!chatMessages) return;
        try {
            const history = JSON.parse(sessionStorage.getItem('chat_history'));
            if (history && history.length > 0) {
                chatMessages.innerHTML = ''; // 清空預設值
                history.forEach(msg => {
                    const msgDiv = document.createElement("div");
                    msgDiv.className = `chat-message ${msg.role}`;
                    msgDiv.innerText = msg.text;
                    chatMessages.appendChild(msgDiv);
                });
            } else {
                // 首次開啟或無歷史紀錄時，顯示小灰的專屬歡迎語氣泡
                chatMessages.innerHTML = '';
                const welcomeDiv = document.createElement("div");
                welcomeDiv.className = "chat-message ai";
                welcomeDiv.innerText = "🐾 浣熊小灰上線啦！有什麼關於 SDGs、ESG 或者是環保小遊戲的問題都可以問我喔！啾～🦝🐾";
                chatMessages.appendChild(welcomeDiv);
            }
            scrollToBottom();
        } catch (e) {
            console.error("載入歷史對話失敗:", e);
        }
    }

    // 載入執行
    loadChatHistory();

    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return; // 防呆機制：如果發送空白文字就不往後執行

        // 1. 將使用者的文字氣泡顯示在畫面上，並寫入歷史紀錄
        const userDiv = document.createElement("div");
        userDiv.className = "chat-message user";
        userDiv.innerText = text;
        chatMessages.appendChild(userDiv);
        saveMessageToHistory('user', text);
        
        chatInput.value = ""; // 送出後清空輸入框
        scrollToBottom();

        // 2. 呼叫後端 API
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
            .then(res => res.json())
            .then(data => {
                // 3. 產生 AI 對話氣泡，並寫入歷史紀錄
                const aiDiv = document.createElement("div");
                aiDiv.className = "chat-message ai";
                const replyText = data.reply || data.error;
                aiDiv.innerText = replyText;
                chatMessages.appendChild(aiDiv);
                saveMessageToHistory('ai', replyText);
                
                scrollToBottom();
            })
            .catch(err => {
                const errDiv = document.createElement("div");
                errDiv.className = "chat-message ai";
                errDiv.innerText = "網路連線失敗，請稍後再試！";
                chatMessages.appendChild(errDiv);
                scrollToBottom();
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

    // 選單切換功能
    const menuBtn = document.querySelector('.menu');
    const navUl = document.querySelector('header ul');
    if (menuBtn && navUl) {
        menuBtn.addEventListener('click', function () {
            navUl.classList.toggle('show');
        });
    }

    const quotes = [
        { text: "SDGs 的 17 個目標都有專屬顏色，但你知道嗎？這些顏色是經過精密設計的，目的是為了讓色盲人士也能輕鬆區分。此外，這些顏色組合在一起形成一個圓環（The SDG Wheel），象徵地球的完整與和諧。", author: "它是全世界最色彩繽紛的「密碼」" },
        { text: "大家都知道有 17 個目標（Goals），但其實底下還藏了 169 個細項目標（Targets）。", author: "它藏著 169 個「小任務」" },
        { text: "為了推廣這些目標，聯合國甚至找過知名音樂人製作歌曲，甚至連 《芝麻街》 的餅乾怪獸（Cookie Monster）和艾蒙（Elmo）都幫 SDGs 拍過宣傳片。這告訴我們：再嚴肅的議題，用「社群功能」和「視覺化」來推廣也是很重要的", author: "它用「可愛」攻佔人心" },
        { text: "在瑞典，資源回收做得太成功了，以至於他們每年都需要從鄰國（如挪威）「進口垃圾」來燃燒發電，否則垃圾發電廠會沒有燃料可用！這真的是『甜蜜的負擔』。", author: "瑞典的垃圾荒 🐾" },
        { text: "地球上所有的螞蟻加起來的總重量，大約和地球上所有人類的總重量差不多！這提醒我們：在自然界中，微小的生命也佔有舉足輕重的分量。", author: "微小但龐大的生命力 🐾" },
        { text: "世界上最古老的樹是一棵位於瑞典的歐洲雲杉，名叫『Old Tjikko』，它已經活了超過 9,550 年！它發芽時，人類甚至還沒有發明青銅器。", author: "見證人類文明的植物老祖宗 🐾" },
        { text: "海洋中最深的壕溝——馬里亞納海溝，深達 11,000 公尺。令人難過的是，科學家在如此深的海底，竟然發現了完好無損的『塑膠垃圾』。保護海洋，減少一次性塑膠真的刻不容緩！", author: "深海萬米下的塑膠悲劇 🐾" },
        { text: "在荷蘭，為了保護蜜蜂等傳粉昆蟲，政府將全國數百個『公車候車亭』的屋頂改造成綠地，種滿了野花與植物。這不僅美化了城市，還為蜜蜂提供了寶貴的庇護所！", author: "蜜蜂專屬的綠能公車站 🐾" },
        { text: "一棵成年樹木每年可以吸收大約 22 公斤的二氧化碳，並釋放出足夠 4 個人呼吸一整天的氧氣。這也是為什麼維護森林與植樹（SDG 15 陸地生態）是減緩地球暖化的關鍵！", author: "天然的綠色空氣清淨機 🐾" },
        { text: "據聯合國統計，全球每年浪費的食物高達 13 億噸，佔全球食物生產量的三分之一！如果把『浪費食物』當成一個國家，它的溫室氣體排放量將僅次於中國和美國，成為全球第三大碳排國。", author: "剩食竟然是隱形的碳排怪獸 🐾" },
        { text: "在哥斯大黎加，全國有超過 98% 的電力是來自再生能源（如水力、風力、地熱與太陽能）。他們甚至計劃在未來幾年內，成為全球第一個完全去碳化的國家！", author: "綠能發電的超級模範生 🐾" },
        { text: "網際網路其實也是有碳排放的！每當我們發送一封電子郵件、觀看線上影片或搜尋一次 Google，伺服器都在消耗電力。全球數據中心產生的碳排放量，已經跟全球航空業的碳排放量不相上下。", author: "點擊滑鼠也在產生碳足跡 🐾" },
        { text: "如果把地球的 46 億年歷史壓縮成『一天 24 小時』，那麼人類在最後的『1 分 15 秒』才出現，而我們工業革命以來的現代文明，只佔了最後的『0.002 秒』。但就在這短暫的瞬間，我們卻對地球造成了巨大的改變。", author: "壓縮成一天的地球歷史 🐾" }
    ];
    // 隨機選一則語錄
    const random = quotes[Math.floor(Math.random() * quotes.length)];
    const quoteEl = document.getElementById("quoteBlock");
    if (quoteEl) {
        quoteEl.innerHTML =
            `<h3>💡 ${random.author}</h3>
             <p class="quote-content">${random.text}</p>`;
    }




});

// 作品輯切換功能
let currentImageIndex = 0;
const images = [
    { 
        src: "static/image/quiz.png", 
        name: '基本測驗', 
        alt: "基本測驗", 
        url: 'quiz.html',
        desc: '最全面的 SDGs 知識檢索測驗！每次將從精心準備的 50 題豐富題庫中隨機抽取 20 題，來測試你的跨領域永續素養吧！🐾'
    },
    { 
        src: "static/images/clicking_earth/earth3.png", 
        name: 'Clicking Earth', 
        alt: "Clicking Earth", 
        url: 'clicking_earth.html',
        desc: '這是一款透過快速點擊和購置綠色能源（如風力、地熱與太陽能）來為地球累積環保分數、淨化生態環境的休閒永續放置型遊戲！🐾'
    },
    { 
        src: "static/image/浣熊施工中.png", 
        name: '敬請期待', 
        alt: "敬請期待", 
        url: '',
        desc: '小灰與開發團隊正在後台拼命籌備與編寫全新的神秘小遊戲！這將是一款將更多 SDGs 永續議題與趣味互動深度結合的精彩遊戲，敬請期待！🐾'
    }
];

// 更新顯示並綁定點擊連結
function updateProductDisplay() {
    const productImage = document.getElementById('productImage');
    const productName = document.getElementById('productName');
    const gameDescTitle = document.getElementById('gameDescTitle');
    const gameDescText = document.getElementById('gameDescText');
    const gamePlayBtn = document.getElementById('gamePlayBtn');
    if (!productImage || !productName) return;

    productImage.src = images[currentImageIndex].src;
    productImage.alt = images[currentImageIndex].alt;
    productName.textContent = images[currentImageIndex].name;

    // 動態更新卡片反面內容
    if (gameDescTitle) gameDescTitle.textContent = images[currentImageIndex].name;
    if (gameDescText) gameDescText.textContent = images[currentImageIndex].desc;
    
    // 動態綁定反面開始遊戲按鈕
    if (gamePlayBtn) {
        const url = images[currentImageIndex].url;
        if (url) {
            gamePlayBtn.textContent = "立即遊玩 🚀";
            gamePlayBtn.classList.remove('disabled');
            gamePlayBtn.onclick = () => window.open(url, '_blank');
        } else {
            gamePlayBtn.textContent = "施工中... 🦝";
            gamePlayBtn.classList.add('disabled');
            gamePlayBtn.onclick = null;
        }
    }

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
    window.location.href = "/games";
}