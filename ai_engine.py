import re

def analyze_message(text: str):

    if not text:
        return {"risk": 0, "type": "safe"}

    t = text.lower()
    risk = 0

    # 🚨 链接检测
    if re.search(r"http|t\.me|www", t):
        risk += 50

    # 🚨 推广关键词
    promo_words = ["赚钱", "兼职", "代理", "私聊", "福利", "进群", "点击"]
    if any(w in t for w in promo_words):
        risk += 30

    # 🚨 垃圾消息
    if len(t) <= 2:
        risk += 10

    # ===================
    # AI判断逻辑
    # ===================
    if risk >= 70:
        return {"risk": risk, "type": "ban"}
    elif risk >= 40:
        return {"risk": risk, "type": "mute"}
    elif risk >= 20:
        return {"risk": risk, "type": "warn"}

    return {"risk": risk, "type": "safe"}
