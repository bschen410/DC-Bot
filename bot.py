# 導入Discord.py模組
import discord, asyncio, json
from discord.ext import commands
import motor


with open('config.json') as cf:
    config = json.load(cf)


# 使用 commands.Bot 並設置應用程式 ID
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="/", intents=intents, application_id=1299426191341518878
)


# 調用 event 函式庫
@bot.event
async def on_ready():
    # 同步應用指令
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"已同步 {len(slash)} 斜線指令")
    # 啟動檢查 Motor 資料的背景任務
    bot.loop.create_task(checkMotorData())


@bot.event
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == bot.user:
        return
    # 新訊息包含 Hello，回覆 Hello, world!
    if message.content.lower() == "hello":
        await message.channel.send("Hello, world!")
    # 檢查訊息是否提及了機器人
    if bot.user.mentioned_in(message):
        await message.channel.send("幹你娘賤種")

    # 確保斜線指令也可以正常運行
    await bot.process_commands(message)


async def checkMotorData():
    ori_result_1 = []
    ori_result_2 = []
    while True:
        result, location = await motor.getData(40, 41) # 板橋
        if result and result != ori_result_1:
            result = location + "\n" + "\n".join(result)
            await bot.get_channel(1299427050884694028).send(result)
            ori_result_1 = result.deepcopy()
        elif result == [] and result != ori_result_1:
            result = location + "\n的名額被搶光囉。"
            await bot.get_channel(1299427050884694028).send(result)
            ori_result_1 = []
        #
        result, location = await motor.getData(20, 25) # 基隆
        if result and result != ori_result_2:
            result = location + "\n" + "\n".join(result)
            await bot.get_channel(1299427050884694028).send(result)
            ori_result_2 = result.deepcopy()
        elif result == [] and result != ori_result_2:
            result = location + "\n的名額被搶光囉。"
            await bot.get_channel(1299427050884694028).send(result)
            ori_result_2 = []
        await asyncio.sleep(60)


# 定義斜線指令 /check_motor_data
@bot.tree.command(name="check_motor_data", description="檢查摩托車考照名額")
async def check_motor_data(interaction: discord.Interaction):
    """檢查 Motor 資料，並在頻道中回覆"""
    await interaction.response.defer()  # 告訴用戶請求正在處理
    result, location = await motor.getData(0, 46)  # 假設 motor 模組有一個 getData 函數
    if result:
        result = location + "\n" + "\n".join(result)
        await interaction.followup.send(result)
    else:
        await interaction.followup.send(
            location + "\n目前沒有可用的資料。"
        )

@bot.tree.command(name="hbd_urfy", description="彳亍")
async def hbd(interaction: discord.Interaction):
    user_id = 837032608897564723
    channel_id = 1290632541094674477
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(":x: :wind_blowing_face: :x: :wind_blowing_face: ")

# name指令顯示名稱，description指令顯示敘述
# name的名稱，中、英文皆可，但不能使用大寫英文
@bot.tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    # 回覆使用者的訊息
    await interaction.response.send_message("Hello, world!")


bot.run(config["DC_TOKEN"])
