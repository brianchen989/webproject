import os

goals = [
    '終結貧窮', '消除飢餓', '健康與福祉', '優質教育', '性別平權', '淨水及衛生',
    '可負擔的潔淨能源', '合適的工作及經濟成長', '工業化、創新及基礎建設', '減少不平等',
    '永續城鄉', '責任消費及生產', '氣候行動', '保育海洋生態', '保育陸域生態',
    '和平、正義及健全制度', '多元夥伴關係'
]
descs = [
    '消除各地一切形式的貧窮。',
    '確保糧食安全，消除飢餓，促進永續農業。',
    '確保及促進各年齡層健康生活與福祉。',
    '確保有教無類、公平以及高品質的教育，及提倡終身學習。',
    '實現性別平權，並賦予婦女權力。',
    '確保所有人都能享有水、衛生及其永續管理。',
    '確保所有的人都可取得負擔得起、可靠、永續及現代的能源。',
    '促進包容且永續的經濟成長，讓每個人都有一份好工作。',
    '建立具有韌性的基礎建設，促進包容且永續的工業，並加速創新。',
    '減少國內及國家間的不平等。',
    '建構具包容、安全、韌性及永續特質的城市與鄉村。',
    '促進綠色經濟，確保永續消費及生產模式。',
    '完備減緩調適行動，以因應氣候變遷及其影響。',
    '保育及永續利用海洋生態系，以確保生物多樣性並防止海洋環境劣化。',
    '保育及永續利用陸域生態系，確保生物多樣性並防止土地劣化。',
    '促進和平多元的社會，確保司法平等，建立具公信力且廣納民意的體系。',
    '建立多元夥伴關係，協力促進永續願景。'
]

details = [
    '貧窮不僅是缺乏收入，還包括飢餓、營養不良、受教育與基本醫療服務的機會受限。此目標致力於推行社會保護系統，幫助弱勢群體抵禦經濟與災害衝擊，從根源消滅貧困。',
    '旨在確保每個人，特別是孩童和弱勢群體，都能獲得足夠且營養的食物。同時強調推動永續農業發展、改善土地質量，並支持在地小農以確保糧食系統的穩定。',
    '關注降低孕產婦與新生兒死亡率，終結傳染病流行，並預防非傳染性疾病。同時倡導心理健康及擴大醫療保健的普及率，讓所有人都能享有健康的生活品質。',
    '教育是改善生活與推動永續發展的核心。此目標確保無論性別、貧富或城鄉，所有人都能享有免費且高品質的小學及中學教育，並推廣終身學習的機會。',
    '消除一切對女性的歧視與暴力，確保女性在政治、經濟與公共生活中享有平等的參與及決策權。賦權女性不僅是基本人權，更是促進全球經濟成長的關鍵。',
    '水資源短缺與水質污染嚴重影響人類生存。此目標強調提供安全且可負擔的飲用水，改善衛生設施，並推動水資源的永續管理與保護生態系統。',
    '能源是現代社會運作的基礎。此目標推廣增加再生能源在能源結構中的比例，提升能源效率，並確保所有人都能取得負擔得起、可靠且現代化的能源。',
    '旨在創造全民充分且具生產力的就業機會，確保工作環境的安全，並消除強迫勞動與童工。同時推動包容性與永續的經濟成長，提升全球資源使用效率。',
    '穩固的基礎建設與具包容性的工業化是經濟發展的基石。此目標鼓勵技術創新與升級，提升基礎建設的韌性，並促進中小型企業的發展。',
    '關注國家內部與國家之間的貧富差距。透過推動普惠的社會、經濟與政治制度，保障弱勢群體的權利，並確保平等的機會以消弭歧視。',
    '隨著全球城市化加速，此目標致力於提供安全的住房與公共運輸，改善貧民窟，並保護自然及文化遺產，讓城市與鄉村兼具包容、安全與永續性。',
    '推廣綠色經濟，強調資源的高效利用。透過減少食物浪費、推動廢棄物回收與再利用，鼓勵企業採用永續做法，從根本改變我們生產與消費的方式。',
    '氣候變遷是全球面臨的最大威脅之一。此目標呼籲各國將氣候變遷對策納入國家政策，加強對氣候相關災害的抵禦能力，並推廣氣候教育與意識。',
    '海洋覆蓋了地球大部分表面，是生命的搖籃。此目標專注於減少海洋污染、保護海洋及沿海生態系統，並有效管理漁業以防止過度捕撈。',
    '森林覆蓋與生物多樣性對於維持地球生態平衡至關重要。此目標致力於阻止森林砍伐、恢復退化的土地、對抗沙漠化，並保護瀕危物種。',
    '沒有和平與正義，永續發展就無法實現。此目標旨在大幅減少一切形式的暴力，建立透明、負責的機構，並確保所有人都能平等地訴諸司法。',
    '永續發展需要政府、企業與民間社會的共同努力。此目標強調加強全球資源動員，促進技術共享與能力建構，攜手建立強大且包容的全球夥伴關係。'
]

template_dir = r'c:\Users\brian\Desktop\網頁程式設計\project\static\templates'
for i in range(1, 18):
    img_name = f'E-WEB-Goal-{i:02d}.png'
    html_content = f"""{{% extends "base.html" %}}

{{% block head %}}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="{{{{ url_for('static', filename='css/網2.0.css') }}}}">
<style>
    /* 新版專屬 Header 樣式 */
    .goal-header {{
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        position: sticky;
        top: 0;
        z-index: 1000;
        padding: 15px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }}
    .goal-header-logo {{
        font-size: 1.6rem;
        font-weight: 800;
        color: #2c3e50;
        text-decoration: none;
        letter-spacing: 1px;
    }}
    .goal-header-logo span {{
        color: #4a7c59;
    }}
    .goal-nav {{
        display: flex;
        gap: 30px;
    }}
    .goal-nav a {{
        text-decoration: none;
        color: #555;
        font-weight: 600;
        font-size: 1.1rem;
        transition: color 0.3s;
        padding: 5px 10px;
        border-radius: 5px;
    }}
    .goal-nav a:hover {{
        color: #4a7c59;
        background-color: rgba(74, 124, 89, 0.1);
    }}

    /* 新版專屬 Footer 樣式 */
    .goal-footer {{
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 50px 20px;
        text-align: center;
        margin-top: 50px;
    }}
    .goal-footer h4 {{
        margin: 0 0 15px 0;
        font-size: 1.6rem;
        letter-spacing: 1.5px;
        color: #ffffff;
    }}
    .goal-footer p {{
        margin: 0;
        font-size: 1.1rem;
        color: #bdc3c7;
    }}

    /* 版面配置樣式 */
    .goal-page {{
        display: flex;
        flex-direction: column;
        gap: 30px;
        padding: 20px 40px;
        max-width: 1200px;
        margin: 0 auto;
        min-height: 70vh;
    }}
    
    .block-top {{
        display: flex;
        flex-wrap: wrap;
        gap: 40px;
        align-items: flex-start;
        background: #ffffff;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }}
    
    .block-top-left {{
        flex: 1;
        min-width: 280px;
        display: flex;
        justify-content: center;
    }}
    
    .block-top-left img {{
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }}
    
    .block-top-left img:hover {{
        transform: translateY(-5px);
    }}
    
    .block-top-right {{
        flex: 2;
        min-width: 320px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }}
    
    .block-top-right h1 {{
        color: #2c3e50;
        margin: 0;
        font-size: 2.2rem;
        border-bottom: 3px solid #4a7c59;
        padding-bottom: 10px;
        display: inline-block;
        width: fit-content;
    }}
    
    .block-top-right h3 {{
        color: #e67e22;
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
        background-color: rgba(230, 126, 34, 0.1);
        padding: 10px 15px;
        border-left: 5px solid #e67e22;
        border-radius: 4px;
    }}
    
    .block-top-right p {{
        font-size: 1.15rem;
        color: #444;
        line-height: 1.8;
        margin: 10px 0 0 0;
        text-align: justify;
    }}
    
    .block-middle {{
        background: linear-gradient(135deg, #f0f7fa 0%, #eef5ff 100%);
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px dashed #a0c4ff;
        box-shadow: inset 0 0 10px rgba(160, 196, 255, 0.2);
    }}
    
    .block-middle h2 {{
        color: #34495e;
        margin-bottom: 15px;
        font-size: 1.8rem;
    }}
    
    .block-bottom {{
        background: #fdfdfd;
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        min-height: 200px;
        border: 2px dashed #ddd;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .back-btn {{
        display: inline-block;
        margin-top: 10px;
        padding: 15px 35px;
        background-color: #4a7c59;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: bold;
        letter-spacing: 1px;
        transition: all 0.3s;
        text-align: center;
        align-self: center;
        width: fit-content;
        box-shadow: 0 4px 10px rgba(74, 124, 89, 0.3);
    }}
    
    .back-btn:hover {{
        background-color: #3b6347;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(74, 124, 89, 0.4);
    }}
</style>
{{% endblock %}}

{{% block content %}}
<!-- 全新設計的專屬 Header -->
<header class="goal-header">
    <a href="{{{{ url_for('index') }}}}" class="goal-header-logo">SDGs <span>永續發展目標</span></a>
    <nav class="goal-nav">
        <a href="{{{{ url_for('index') }}}}">回到首頁</a>
        <a href="{{{{ url_for('index') }}}}#17goals">探索所有目標</a>
    </nav>
</header>

<main>
    <div class="goal-page">
        <!-- 上方 Block：圖片與介紹 -->
        <div class="block-top">
            <div class="block-top-left">
                <img src="{{{{ url_for('static', filename='image/{img_name}') }}}}" alt="目標 {i}">
            </div>
            <div class="block-top-right">
                <h1>目標 {i}：{goals[i-1]}</h1>
                <h3>簡介：{descs[i-1]}</h3>
                <p>{details[i-1]}</p>
            </div>
        </div>
        
        <!-- 中間 Block：遊戲區塊 -->
        <div class="block-middle">
            <h2>🎮 與此目標相關的小遊戲</h2>
            <p style="color: #666; font-size: 1.1rem;">（此處為目標 {i} 相關小遊戲的預留空間）</p>
        </div>
        
        <!-- 下方 Block：預留區塊 -->
        <div class="block-bottom">
            <p style="color: #999; font-size: 1.1rem;">（下方區塊：未來可以新增更多與此目標相關的內容或資訊）</p>
        </div>
        
        <a href="{{{{ url_for('index') }}}}" class="back-btn">返回首頁</a>
    </div>
</main>

<!-- 全新設計的專屬 Footer -->
<footer class="goal-footer">
    <h4>共同致力於改變我們的世界</h4>
    <p>2030年永續發展議程 (The 2030 Agenda for Sustainable Development)</p>
</footer>
{{% endblock %}}
"""
    with open(os.path.join(template_dir, f'goal_{i}.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

print("Regenerated 17 template files with NEW header and footer designs successfully.")
