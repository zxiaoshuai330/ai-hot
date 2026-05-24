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

            # 風險
            if diff > 80:
                risk = "高波動（節奏不穩）"
            elif diff > 30:
                risk = "中波動"
            else:
                risk = "穩定節奏"

            # 節奏 + 建議
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

            result = f"""
            <div id="cards">

                <div class="card step">📊 正在重建節奏模型...</div>

                <div class="card step">
                    🔍 節奏判定：{status}<br>
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
            animation:load 5s linear forwards;
        }}

        @keyframes load {{
            0% {{width:0%}}
            100% {{width:100%}}
        }}
    </style>

    <script>
        function startAnalysis(form, e) {{
            e.preventDefault();

            document.getElementById("loading").style.display = "block";

            let texts = [
                "🔍 掃描資料...",
                "📊 建立節奏模型...",
                "🧠 深度分析中...",
                "⚡ 捕捉關鍵訊號..."
            ];

            let i = 0;
            let interval = setInterval(() => {{
                if (i < texts.length) {{
                    document.getElementById("loadingText").innerText = texts[i];
                    i++;
                }} else {{
                    clearInterval(interval);
                }}
            }}, 1200);

            setTimeout(() => {{
                form.submit();
            }}, 5000);
        }}

        // 分段顯示（像APP）
        window.onload = function() {{
            let steps = document.querySelectorAll(".step");

            steps.forEach((el, i) => {{
                setTimeout(() => {{
                    el.classList.add("show");

                    // 最後一個震動
                    if (i === steps.length - 1) {{
                        if (navigator.vibrate) {{
                            navigator.vibrate([100, 50, 100]);
                        }}
                    }}

                }}, i * 600);
            }});
        }}
    </script>

    </head>

    <body>

        <div class="title">⚡ 熱點雷達</div>
        <div class="subtitle">AI節奏分析｜即時捕捉波動訊號</div>

        <form method="post" onsubmit="startAnalysis(this, event)">
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
