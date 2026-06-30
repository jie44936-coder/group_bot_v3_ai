import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatPermissions

from config import BOT_TOKEN, ADMIN_IDS
from ai_engine import analyze_message

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# 📩 消息入口（核心）
# =========================
@dp.message()
async def handler(msg: Message):

    print("📩 收到消息:", msg.text)

    uid = msg.from_user.id
    text = msg.text or ""
    chat_id = msg.chat.id

    # 忽略管理员
    if uid in ADMIN_IDS:
        return

    # =========================
    # 🧠 AI分析
    # =========================
    result = analyze_message(text)
    action = result["type"]
    risk = result["risk"]

    # =========================
    # 🚫 SAFE（正常消息不处理）
    # =========================
    if action == "safe":
        return

    # =========================
    # ⚠️ WARN（警告）
    # =========================
    if action == "warn":

        try:
            await msg.delete()
        except:
            pass

        await msg.answer("⚠️ 请遵守群规则")
        return

    # =========================
    # 🔇 MUTE（禁言）
    # =========================
    if action == "mute":

        try:
            await msg.delete()
        except:
            pass

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=uid,
            permissions=ChatPermissions(
                can_send_messages=False
            )
        )

        await msg.answer("🔇 你已被禁言")
        return

    # =========================
    # ⛔ BAN（封禁）
    # =========================
    if action == "ban":

        try:
            await msg.delete()
        except:
            pass

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=uid,
            permissions=ChatPermissions(
                can_send_messages=False
            )
        )

        await msg.answer("⛔ 你已被封禁")
        return


# =========================
# 📊 群统计
# =========================
@dp.message(F.text == "/stats")
async def stats(msg: Message):

    await msg.answer("📊 群管系统运行正常")


# =========================
# 🚀 启动
# =========================
async def main():
    print("🤖 V3 PRO 群管已启动")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())