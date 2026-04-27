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

template_dir = r'c:\Users\brian\Desktop\網頁程式設計\project\static\templates'
for i in range(1, 18):
    img_name = f'E-WEB-Goal-{i:02d}.png'
    html_content = f"""{{% extends "base.html" %}}

{{% block head %}}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="{{{{ url_for('static', filename='css/網2.0.css') }}}}">
<style>
    .goal-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 50px 20px;
        text-align: center;
        background-color: #f9f9f9;
        min-height: 80vh;
    }}
    .goal-container img {{
        max-width: 300px;
        height: auto;
        margin-bottom: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .goal-container h1 {{
        color: #333;
        margin-bottom: 20px;
    }}
    .goal-container p {{
        font-size: 1.2rem;
        color: #555;
        max-width: 800px;
        line-height: 1.6;
    }}
    .back-btn {{
        margin-top: 40px;
        padding: 10px 20px;
        background-color: #333;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        transition: background-color 0.3s;
    }}
    .back-btn:hover {{
        background-color: #555;
    }}
</style>
{{% endblock %}}

{{% block content %}}
<div class="goal-container">
    <img src="{{{{ url_for('static', filename='image/{img_name}') }}}}" alt="目標 {i}">
    <h1>目標 {i}：{goals[i-1]}</h1>
    <p>{descs[i-1]}</p>
    <a href="{{{{ url_for('index') }}}}" class="back-btn">返回首頁</a>
</div>
{{% endblock %}}
"""
    with open(os.path.join(template_dir, f'goal_{i}.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

print("Generated 17 template files successfully.")
