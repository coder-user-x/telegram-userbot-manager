import asyncio
import subprocess

async def run_bots():
    # Run bot.py
    bot_proc = await asyncio.create_subprocess_exec('python', 'bot/bot.py')
    # Run main.py
    userbot_proc = await asyncio.create_subprocess_exec('python', 'userbot_runner/main.py')

    await asyncio.gather(bot_proc.wait(), userbot_proc.wait())

if __name__ == "__main__":
    asyncio.run(run_bots())
