import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ChatPermissions

from config import BOT_TOKEN, ADMIN_IDS
from ai_engine import analyze_message
from db import cursor, conn

# ❗ 防止BOT_TOKEN为空（Render必备）
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN 未设置，请检查 Render 环境变量")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ======================
# 初始化用户
# ======================
def init_user(uid):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (uid,))
    conn.commit()


# ======================
# 记录日志
# ======================
def log(uid, action, risk):
    cursor.execute(
        "INSERT INTO logs (user_id, action, risk) VALUES (?, ?, ?)",
        (uid, action, risk)
    )
    conn.commit()


# ======================
# 🚀 群消息入口
# ======================
@dp.message()
async def handler(msg: Message):

    print("📩 收到消息:", msg.text)

    uid = msg.from_user.id
    text = msg.text or ""
    chat_id = msg.chat.id

    # 管理员跳过
    if uid in ADMIN_IDS:
        return

    init_user(uid)

    # 更新消息数
    cursor.execute(
        "UPDATE users SET messages = messages + 1 WHERE user_id=?",
        (uid,)
    )
    conn.commit()

    # ======================
    # AI分析
    # ======================
    result = analyze_message(text)
    action = result["type"]
    risk = result["risk"]

    # ======================
    # SAFE
    # ======================
    if action == "safe":
        return

    # ======================
    # WARN
    # ======================
    if action == "warn":
        try:
            await msg.delete()
        except:
            pass
        await msg.answer("⚠️ 请遵守群规则")
        log(uid, "warn", risk)
        return

    # ======================
    # MUTE
    # ======================
    if action == "mute":
        try:
            await msg.delete()
        except:
            pass

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=uid,
            permissions=ChatPermissions(can_send_messages=False)
        )

        await msg.answer("🔇 已禁言")
        log(uid, "mute", risk)
        return

    # ======================
    # BAN
    # ======================
    if action == "ban":
        try:
            await msg.delete()
        except:
            pass

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=uid,
            permissions=ChatPermissions(can_send_messages=False)
        )

        await msg.answer("⛔ 已封禁")
        log(uid, "ban", risk)
        return


# ======================
# 📊 状态
# ======================
@dp.message(lambda m: m.text == "/stats")
async def stats(msg: Message):

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs")
    logs = cursor.fetchone()[0]

    await msg.answer(
        f"📊 群管系统\n用户: {users}\n日志: {logs}"
    )


# ======================
# 🚀 启动
# ======================
async def main():
    print("🤖 V3 PRO 云端启动中...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
