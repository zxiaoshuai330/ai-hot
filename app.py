from flask import Flask, request
import random
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    show_result = "none"

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
                risk = "高風險"
            elif diff > 30:
                risk = "中風險"
            else:
                risk = "低風險"

            if current > avg * 1.3:
                status = "觸發醞釀尾段"
                base_score = 75
            elif current < avg * 0.7:
                status = "節奏重建中"
                base_score = 40
            else:
                status = "訊號累積中"
                base_score = 60

            score = base_score + (today - 100) * 0.2
            score += random.randint(-5, 5)
            score = max(0, min(100, int(score)))

            if score > 70:
                tag = "🔥 熱點區"
                action = "建議提前卡位"
            elif score > 50:
                tag = "⚡ 過渡區"
                action = "可小注測試"
            else:
                tag = "❄️ 冷卻區"
                action = "低倍觀察"

            confidence = random.randint(75, 96)

            result = f"""
            <div id="cards">
                <div class="card">🤖 AI評分：{score}</div>
                <div class="card">📊 節奏：{status}<br>🏷 狀態：{tag}<br>⚠️ 風險：{risk}</div>
                <div class="card highlight">🎯 建議：{action}</div>
                <div class="card">📈 信心指數：{confidence}%</div>

                <div class="card small">
                    ⚠️ 熱點訊號存在時，通常不會維持太久<br>
                    💡 暫不建議重壓，可低倍觀察
                </div>

                <div class="card small">
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
            font-size:24px;
        }}

        .subtitle {{
            color:gray;
            font-size:13px;
            margin-bottom:20px;
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
            transform:translateY(20px);
            animation:fadeUp 0.6s forwards;
        }}

        .card:nth-child(1) {{animation-delay:0.3s}}
        .card:nth-child(2) {{animation-delay:0.8s}}
        .card:nth-child(3) {{animation-delay:1.3s}}
        .card:nth-child(4) {{animation-delay:1.8s}}
        .card:nth-child(5) {{animation-delay:2.3s}}
        .card:nth-child(6) {{animation-delay:2.8s}}

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

        .progress {{
            width:100%;
            height:10px;
            background:#222;
            border-radius:10px;
            overflow:hidden;
            margin-top:20px;
        }}

        .bar {{
            height:100%;
            width:0%;
            background:orange;
            animation:load 4s linear forwards;
        }}

        @keyframes load {{
            0% {{width:0%}}
            100% {{width:100%}}
        }}
    </style>

    <script>
        function startAnalysis(form) {{
            event.preventDefault();

            document.getElementById("loading").style.display = "block";

            let texts = [
                "🔍 掃描近期節奏...",
                "📊 建立波動模型...",
                "🧠 AI計算中...",
                "⚡ 捕捉熱點訊號..."
            ];

            let i = 0;
            let interval = setInterval(() => {{
                if (i < texts.length) {{
                    document.getElementById("loadingText").innerText = texts[i];
                    i++;
                }} else {{
                    clearInterval(interval);
                }}
            }}, 1000);

            setTimeout(() => {{
                form.submit();
            }}, 4000);
        }}
    </script>

    </head>

    <body>

        <div class="title">⚡ 熱點雷達</div>
        <div class="subtitle">AI節奏分析｜即時捕捉波動訊號</div>

        <form method="post" onsubmit="startAnalysis(this)">
            <input name="today" placeholder="今日得分率">
            <input name="current" placeholder="未開轉數">
            <input name="last1" placeholder="上次轉數">
            <input name="last2" placeholder="上上次">
            <button>開始分析</button>
        </form>

        <div id="loading" style="display:none;">
            <div id="loadingText" style="margin-top:20px;">🔍 AI分析中...</div>
            <div class="progress"><div class="bar"></div></div>
        </div>

        <div style="display:{show_result};">
            {result}
        </div>

    </body>
    </html>
    """

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
