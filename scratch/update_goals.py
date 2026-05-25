import os
import re

template_dir = r"c:\Users\brian\Desktop\網頁期末PROJECT\project\static\templates"
target_pattern = re.compile(
    r'<!-- 下方 Block：預留區塊 -->\s*<div class="block-bottom">.*?</div>',
    re.DOTALL
)

replacement = """<!-- 下方 Block：時事與新聞看板 -->
        <div class="block-bottom" style="display: flex; flex-direction: column; align-items: center; width: 100%; border: none; background: #ffffff; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-radius: 12px; box-sizing: border-box;">
            <h2 style="color: #2c3e50; font-size: 1.8rem; margin: 0 0 25px 0; font-weight: bold; border-bottom: 3px solid #e67e22; padding-bottom: 8px; width: fit-content; display: inline-block;">📰 SDGs 台灣與全球即時新聞 / 時事看板</h2>
            <div style="display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; width: 100%; margin-top: 15px; box-sizing: border-box;">
                {% for news in news_list %}
                    <a href="{{ news.link }}" target="_blank" style="text-decoration: none; flex: 1; min-width: 280px; max-width: 500px; display: flex; flex-direction: column; justify-content: space-between; background: #fcfdfe; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); transition: all 0.3s; box-sizing: border-box;" onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.08)'; this.style.borderColor='rgba(230, 126, 34, 0.4)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.02)'; this.style.borderColor='rgba(0,0,0,0.08)';">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <span style="background: rgba(230, 126, 34, 0.1); color: #e67e22; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; display: inline-block;">{{ news.source }}</span>
                                <span style="color: #999; font-size: 0.85rem;">📅 {{ news.date }}</span>
                            </div>
                            <h3 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 1.25rem; font-weight: 700; line-height: 1.4; text-align: left;">{{ news.title }}</h3>
                            <p style="margin: 0; color: #666; font-size: 0.95rem; line-height: 1.6; text-align: justify;">{{ news.summary }}</p>
                        </div>
                        <div style="margin-top: 20px; text-align: right; color: #e67e22; font-weight: bold; font-size: 0.95rem;">
                            閱讀新聞全文 ➔
                        </div>
                    </a>
                {% endfor %}
            </div>
        </div>"""

for file_name in os.listdir(template_dir):
    if file_name.startswith("goal_") and file_name.endswith(".html"):
        file_path = os.path.join(template_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 進行替換
        new_content, count = target_pattern.subn(replacement, content)
        if count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully updated {file_name}")
        else:
            # 有可能之前跑腳本已經修改過部分檔案，就不再重複印錯誤
            pass
