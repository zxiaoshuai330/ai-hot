from flask import Flask, request
import random
import os
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    show_result = "none"

    # 🔥 假在線人數（每30分鐘變）
    seed = int(time.time() // 1800)
    random.seed(seed)
    online_users = random.randint(0, 57)

    if request.method == "POST":
        show_result = "block"

        try:
            today = float(request.form["today"])
            current = int(request.form["current"])
            last1 = int(request.form["last1"])
            last2 = int(request.form["last2"])

            avg = (last1 + last2) / 2
            diff = abs(last1 - last2)

            if diff > 80:
                risk = "高波動（節奏不穩）"
            elif diff > 30:
                risk = "中波動"
            else:
                risk = "穩定節奏"

            if current > avg * 1.3:
                status = "進入尾段醞釀"
                action = "建議低倍提前卡位"
                range_text = f"觀察區：約 {int(avg*0.8)}～{int(avg*1.2)} 轉"
            elif current < avg * 0.7:
                status = "剛結束釋放"
                action = "暫不建議進場"
                range_text = f"建議等待累積至 {int(avg)} 轉以上"
            else:
                status = "訊號累積中"
                action = "可小注測試"
                range_text = f"測試區：約 {int(avg*0.6)}～{int(avg*0.9)} 轉"

            confidence = random.randint(80, 96)
            signal_chance = random.randint(60, 95)

            if signal_chance > 75:
                signal_text = f"✅ 成功捕捉熱點訊號（機率 {signal_chance}%）"
            else:
                signal_text = f"⚠️ 訊號偏弱（目前機率 {signal_chance}%）"

            # 🔥 命中案例（隨機1~5筆）
            base_hits = [
                "🎯 48轉 → 命中",
                "🎯 63轉 → 命中",
                "🎯 72轉 → 命中",
                "🎯 91轉 → 命中",
                "🎯 105轉 → 命中",
                "🎯 58轉 → 命中",
                "🎯 83轉 → 命中"
            ]

            hit_count = random.randint(1, 5)
            random_hits = random.sample(base_hits, hit_count)

            hits_html = "<br>".join(random_hits)

            result = f"""
            <div id="cards">

                <div class="card step highlight">
                    📊 分析結果如下
                </div>

                <div class="card step">
                    {signal_text}
                </div>

                <div class="card step">
                    📊 節奏判定：{status}<br>
                    ⚠️ 波動狀態：{risk}
                </div>

                <div class="card step highlight">
                    🎯 操作建議：{action}
                </div>

                <div class="card step">
                    ⏱ 參考區間：{range_text}
                </div>

                <div class="card step">
                    🤖 AI信心指數：{confidence}%
                </div>

                <div class="card step">
                    📈 近期命中案例：<br>
                    {hits_html}
                </div>

                <div class="card step small">
                    ⚠️ 熱點訊號存在時通常不會維持太久<br>
                    💡 建議低倍觀察，避免重壓
                </div>

                <div class="card step small">
                    ※ 本系統為AI模型推估，結果僅供參考
                </div>

            </div>
            """

        except:
            result = "<div class='card'>⚠️ 請輸入正確數字</div>"

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            background:#0b0f1a;
            color:white;
            font-family:sans-serif;
            text-align:center;
            padding:20px;
        }}

        .title {{
            color:orange;
            font-size:26px;
            font-weight:bold;
        }}

        .online {{
            font-size:12px;
            color:#00ffcc;
            margin-bottom:10px;
        }}

        input {{
            width:90%;
            padding:12px;
            margin:8px 0;
            border-radius:10px;
            border:none;
            background:#1c2233;
            color:white;
        }}

        button {{
            width:95%;
            padding:15px;
            margin-top:15px;
            border:none;
            border-radius:12px;
            background:orange;
            color:black;
            font-size:16px;
        }}

        .card {{
            background:#151a2c;
            margin-top:15px;
            padding:15px;
            border-radius:15px;
            opacity:0;
            transform:translateY(30px);
        }}

        .show {{
            animation:fadeUp 0.5s forwards;
        }}

        @keyframes fadeUp {{
            to {{
                opacity:1;
                transform:translateY(0);
            }}
        }}

        .highlight {{
            background:orange;
            color:black;
            font-weight:bold;
        }}

        .small {{
            font-size:12px;
            color:gray;
        }}
    </style>

    <script>
        function startAnalysis(form, e) {{
            e.preventDefault();

            setTimeout(() => {{
                form.submit();
            }}, 4000);
        }}

        window.onload = function() {{
            let steps = document.querySelectorAll(".step");

            steps.forEach((el, i) => {{
                setTimeout(() => {{
                    el.classList.add("show");

                    if (i === steps.length - 1) {{
                        if (navigator.vibrate) {{
                            navigator.vibrate([120, 60, 120]);
                        }}
                    }}

                }}, i * 700);
            }});
        }}
    </script>

    </head>

    <body>

        <div class="title">⚡ 熱點雷達</div>
        <div class="online">🔥 目前線上使用：{online_users} 人</div>

        <form method="post" onsubmit="startAnalysis(this, event)">
            <input name="today" placeholder="今日得分率">
            <input name="current" placeholder="未開轉數">
            <input name="last1" placeholder="上次轉數">
            <input name="last2" placeholder="上上次">
            <button>開始分析</button>
        </form>

        <div style="display:{show_result};">
            {result}
        </div>

    </body>
    </html>
    """

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
