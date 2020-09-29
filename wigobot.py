import discord
import pwread
from discord.ext import commands, buttons, tasks
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pymongo
from pymongo import MongoClient

# Switch to 8 if in GCM.
gcm_hour_adjustment = 0

cluster = MongoClient(pwread.dbcred())

# Database Name
db = cluster["discord"]

# MVP tracker Collection
mvp_tracker = db["mvp_tracker"]

# MVP Name Shortcut Collection
mvp_names = db["mvp_name_shortcuts"]

sched = AsyncIOScheduler()
sched.start()

bot = commands.Bot(command_prefix = "-")

class Reminder:
    def __init__(self, _min_minutes, min_time, min_time_msg, _max_minutes, max_time, max_time_msg, user, ctx):
        self._min_minutes = _min_minutes
        self.min_time = min_time
        self.min_time_msg = min_time_msg
        self._max_minutes = _max_minutes
        self.max_time = max_time
        self.max_time_msg = max_time_msg
        self.user = user
        self.ctx = ctx
        sched.add_job(self.send_reminder_min, 'date', run_date=self.min_time)
        sched.add_job(self.send_reminder_max, 'date', run_date=self.max_time)

    async def send_reminder_min(self):
        await Session(self._min_minutes, self.min_time, self.min_time_msg, self._max_minutes, self.max_time, self.max_time_msg, self.user, self.ctx).start(page=await self.user.send(self.min_time_msg), ctx=self.ctx)
        msg = "<@" + str(self.user.id) + "> " + self.min_time_msg
        await self.ctx.send(msg)

    async def send_reminder_max(self):
        await Session(self._min_minutes, self.min_time, self.min_time_msg, self._max_minutes, self.max_time, self.max_time_msg, self.user, self.ctx).start(page=await self.user.send(self.max_time_msg), ctx=self.ctx)
        msg = "<@" + str(self.user.id) + "> " + self.max_time_msg
        await self.ctx.send(msg)


class Session(buttons.Session):
    def __init__(self, _min_minutes, min_time, min_time_msg, _max_minutes, max_time, max_time_msg, user, ctx):
        self._min_minutes = _min_minutes
        self.min_time = min_time
        self.min_time_msg = min_time_msg
        self._max_minutes = _max_minutes
        self.max_time = max_time
        self.max_time_msg = max_time_msg
        self.user = user
        self.ctx = ctx
        super().__init__(timeout=None, try_remove=True)

    async def add_reminder(self):
        Reminder(self._min_minutes, self.min_time, self.min_time_msg, self._max_minutes, self.max_time, self.max_time_msg, self.user, self.ctx)
        await self.user.send('👍')

    @buttons.button('🔁', position=0)
    async def reschedule_reminder(self, ctx, member):
        current_time = datetime.now()
        self.min_time = current_time + timedelta(minutes = self._min_minutes, hours = gcm_hour_adjustment)
        self.max_time = current_time + timedelta(minutes = self._max_minutes, hours = gcm_hour_adjustment)
        await self.add_reminder()


class SendGuildLineup(buttons.Paginator):
    def __init__(self, message, gvg_dict, *args, **kwargs):
        self.message = message
        self.gvg_dict = gvg_dict
        super().__init__(*args, **kwargs)

    def checkAttendance(self, job, member):
        content = None
        char = "<@" + str(member.id) + ">"
        checkChar = [key for key, value in self.gvg_dict.items() if char in value]
        if checkChar != []:
            for charCount in checkChar:
                self.gvg_dict[charCount].remove(char)
 
        self.gvg_dict[job].append(char)
        content = "GvG Lineup:"
        for job_class in self.gvg_dict:
            if self.gvg_dict[job_class] != []:
                stringLineup = ', '.join(map(str, self.gvg_dict[job_class]))
                content += "\n" + job_class + ": " + stringLineup

        return(content)

    @buttons.button(emoji='🥵')
    async def olp(self, ctx, member):
        content = self.checkAttendance('OLP Professor', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🧬')
    async def ddcreo(self, ctx, member):
        content = self.checkAttendance('DD Creator', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🎭')
    async def ddstalker(self, ctx, member):
        content = self.checkAttendance('DD Stalker', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🧙')
    async def ddhw(self, ctx, member):
        content = self.checkAttendance('DD High Wizard', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🎻')
    async def clown(self, ctx, member):
        content = self.checkAttendance('Bragi Clown', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🥶')
    async def dlp(self, ctx, member):
        content = self.checkAttendance('DLP Professor', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🧚')
    async def fshw(self, ctx, member):
        content = self.checkAttendance('FS High Wizard', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🧪')
    async def sppcreo(self, ctx, member):
        content = self.checkAttendance('SPP Creator', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🏹')
    async def sniper(self, ctx, member):
        content = self.checkAttendance('Sniper', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🧽')
    async def devo(self, ctx, member):
        content = self.checkAttendance('Devo Paladin', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🤜')
    async def champ(self, ctx, member):
        content = self.checkAttendance('Champ', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🧖')
    async def gypsy(self, ctx, member):
        content = self.checkAttendance('Gypsy', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='⛪')
    async def highp(self, ctx, member):
        content = self.checkAttendance('High Priest', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🍭')
    async def linker(self, ctx, member):
        content = self.checkAttendance('Linker', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='🙈')
    async def otherclass(self, ctx, member):
        content = self.checkAttendance('Other Class', member)
        await self.message.edit(content=content)

    @buttons.button(emoji='💩')
    async def notgoing(self, ctx, member):
        content = self.checkAttendance('Not Going', member)
        await self.message.edit(content=content)


def mvp_query(ctx, mvp):
    results = None
    mvp_lower = mvp.lower()

    search_nick = mvp_names.find_one({"names": mvp_lower})
    if search_nick != None:
        mvp_id = search_nick["_id"]
        results = mvp_tracker.find_one({"_id": mvp_id})
    else:
        mvp = mvp.lower().title()
        results = mvp_tracker.find_one({"name": mvp})

    return(results)

@bot.command()
async def kill(ctx, *, mvp):
    results = mvp_query(ctx, mvp)
    user = ctx.message.author

    if results != None:
        current_time = datetime.now()
        str_current_time = (current_time + timedelta(hours = gcm_hour_adjustment)).strftime("%m/%d/%Y, %H:%M:%S")
        min_minutes = results["min_timer"]
        max_minutes = results["max_timer"]

        min_time = current_time + timedelta(minutes = min_minutes)
        max_time = current_time + timedelta(minutes = max_minutes)

        result_mvp = results["name"]
        reply_text = "Reminder set: " + result_mvp + " will spawn from " + (min_time + timedelta(hours = gcm_hour_adjustment)).strftime("%H:%M") + " to " + (max_time + timedelta(hours = gcm_hour_adjustment)).strftime("%H:%M")

        min_time_msg = results["name"] + " minimum spawn time at " + results["location"] + "."
        max_time_msg = results["name"] + " maximum spawn time at " + results["location"] + "."
        
        mvp_tracker.update_one({"name":results["name"]}, {"$set":{"time_killed":str_current_time}})

        Reminder(min_minutes, min_time, min_time_msg, max_minutes, max_time, max_time_msg, user, ctx)
        await ctx.send(reply_text)
    else:
        await ctx.send("No MVPs found with that name. Please try again.")

@bot.command()
async def check(ctx, *, mvp):
    results = mvp_query(ctx, mvp)
    if results != None:
        results = mvp_query(ctx, mvp)
        msg = "**MVP Name**: " + results["name"]
        msg += "\n**MVP Location**: " + results["location"]
        msg += "\n**Last Kill Time**: " + str(results["time_killed"])
        await ctx.send(msg)
    else:
        await ctx.send("No MVPs found with that name. Please try again.")

@bot.command()
async def spot(ctx, time, *, mvp):
    results = mvp_query(ctx, mvp)
    user = ctx.message.author
    
    if results != None:
        current_time = datetime.now()
        kill_time = datetime.strptime(time, '%H:%M').replace(year=current_time.year,month=current_time.month,day=current_time.day)

        if current_time.hour*60 + current_time.minute < results["min_timer"]:
            kill_time = kill_time - timedelta(days = 1)

        str_kill_time = kill_time.strftime("%m/%d/%Y, %H:%M:%S")
        min_minutes = results["min_timer"]
        max_minutes = results["max_timer"]
        min_time = kill_time + timedelta(minutes = min_minutes)
        max_time = kill_time + timedelta(minutes = max_minutes)

        min_time_msg = results["name"] + " minimum spawn time at " + results["location"] + "."
        max_time_msg = results["name"] + " maximum spawn time at " + results["location"] + "."
        
        mvp_tracker.update_one({"name":results["name"]}, {"$set":{"time_killed":str_kill_time}})
        result_mvp = results["name"]

        reply_text = "Reminder set: " + result_mvp + " will spawn from " + min_time.strftime("%H:%M") + " to " + max_time.strftime("%H:%M")
        
        min_time = min_time - timedelta(hours = gcm_hour_adjustment)
        max_time = max_time - timedelta(hours = gcm_hour_adjustment)

        Reminder(min_minutes, min_time, min_time_msg, max_minutes, max_time, max_time_msg, user, ctx)
        await ctx.send(reply_text)
    else:
        await ctx.send("No MVPs found with that name. Please try again.")

async def call_lineup(ctx):
    gvg_recruit_msg = 'Click  🥵  for OLP Professor'
    gvg_recruit_msg += '\nClick  🧬  for DD Creator'
    gvg_recruit_msg += '\nClick  🎭  for DD Stalker'
    gvg_recruit_msg += '\nClick  🧙  for DD High Wizard'
    gvg_recruit_msg += '\nClick  🎻  for Bragi Clown'
    gvg_recruit_msg += '\nClick  🥶  for DLP Professor'
    gvg_recruit_msg += '\nClick  🧚  for FS High Wizard'
    gvg_recruit_msg += '\nClick  🧪  for SPP Creator'
    gvg_recruit_msg += '\nClick  🏹  for Sniper'
    gvg_recruit_msg += '\nClick  🧽  for Devo Paladin'
    gvg_recruit_msg += '\nClick  🤜  for Champ'
    gvg_recruit_msg += '\nClick  🧖  for Gypsy'
    gvg_recruit_msg += '\nClick  ⛪  for High Priest'
    gvg_recruit_msg += '\nClick  🍭  for Linker'
    gvg_recruit_msg += '\nClick  🙈  for Other Class'
    gvg_recruit_msg += '\nClick  💩  for Not Going'

    gvg_dict = {"OLP Professor":[], "DD Creator":[], "DD Stalker":[], "DD High Wizard":[], 
                "Bragi Clown":[], "DLP Professor":[], "FS High Wizard":[], "SPP Creator":[],
                "Sniper":[], "Devo Paladin":[], "Champ":[], "Gypsy":[], 
                "High Priest":[], "Linker":[], "Other Class":[], "Not Going":[]}

    channel = bot.get_channel(742358330969686017) #guild-lineup channel ID
    message = await channel.send('GvG Lineup:')
    pagey = SendGuildLineup(message=message, gvg_dict=gvg_dict, title='Emoji List', colour=0xc67862, embed=True, timeout=14400, use_defaults=False,
                        entries=[gvg_recruit_msg,], length=1, format='**')
    await pagey.start(ctx)


@tasks.loop(seconds = 60)
async def send_mes():
    now = datetime.now()
    woe_discussion = bot.get_channel(719434806554787842) #woe-discussion channel ID
    if now.strftime("%H:%M") == "14:30" and now.strftime("%A") != 'Saturday':
        message = await woe_discussion.send('Tara KoE! Sino G?')
        ctx = await bot.get_context(message)
        await call_lineup(ctx)
    elif now.strftime("%H:%M") == "10:00" and now.strftime("%A") == 'Saturday':
        message = await woe_discussion.send('Tara WoE! Sino G?')
        ctx = await bot.get_context(message)
        await call_lineup(ctx)

@bot.event
async def on_ready():
    send_mes.start()
    print("Logged in!\n----------\n")
    print(f"Connected to {len(bot.guilds)} guilds...  {', '.join([e.name for e in bot.guilds])}") 

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Aww walang ganyang command mamser :pleading_face:")

bot.run(pwread.bot_token())
