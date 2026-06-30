import re

def analyze_message(text: str):

    if not text:
        return {"risk": 0, "type": "safe"}

    risk = 0
    t = text.lower()

    # 🚨 广告/推广
    if re.search(r"http|t\.me|www", t):
        risk += 50

    promo_words = ["赚钱", "兼职", "代理", "私聊", "进群", "福利", "点击"]
    if any(w in t for w in promo_words):
        risk += 30

    # 🚨 刷屏/垃圾
    if len(t) <= 2:
        risk += 15

    # 🚨 复杂规则
    if any(c.isdigit() for c in t) and len(t) < 6:
        risk += 20

    # ======================
    # AI判定
    # ======================
    if risk >= 70:
        return {"risk": risk, "type": "ban"}
    elif risk >= 40:
        return {"risk": risk, "type": "mute"}
    elif risk >= 20:
        return {"risk": risk, "type": "warn"}

    return {"risk": risk, "type": "safe"}