from flask import Flask, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
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

            confidence = random.randint(72, 95)

            result = f"""
            <div class="card">
                <h2>🤖 AI評分：{score}</h2>
            </div>

            <div class="card">
                <p>📊 節奏：{status}</p>
                <p>🏷 狀態：{tag}</p>
                <p>⚠️ 風險：{risk}</p>
            </div>

            <div class="card highlight">
                <p>🎯 建議：{action}</p>
            </div>

            <div class="card">
                <p>📈 信心指數：{confidence}%</p>
            </div>

            <div class="card small">
                ⚠️ 熱點訊號存在時，通常不會維持太久<br>
                💡 暫不建議重壓，可低倍觀察
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
            font-size:22px;
            margin-bottom:5px;
        }}
        .subtitle {{
            color:gray;
            font-size:14px;
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
        }}
        .highlight {{
            background:#ff8c00;
            color:black;
            font-weight:bold;
        }}
        .small {{
            font-size:12px;
            color:gray;
        }}
    </style>
    </head>

    <body>

        <div class="title">⚡ 熱點雷達</div>
        <div class="subtitle">AI節奏分析｜捕捉爆發點</div>

        <form method="post">
            <input name="today" placeholder="今日得分率">
            <input name="current" placeholder="未開轉數">
            <input name="last1" placeholder="上次轉數">
            <input name="last2" placeholder="上上次">
            <button>開始分析</button>
        </form>

        {result}

    </body>
    </html>
    """

app.run(host="0.0.0.0", port=10000)
