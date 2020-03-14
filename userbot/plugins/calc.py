# For UniBorg
# By Priyam Kalra
# Syntax (.calc <term1><operator><term2>)
# For eg .calc 02*02 or 99*99 (the zeros are important) (two terms and two digits max)
from telethon import events
from userbot.utils import admin_cmd
import asyncio
from telethon.tl import functions, types

#neccesary tg shit
@borg.on(admin_cmd(pattern="calc ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1) #get input
    exp = "Given expression is " + input #report back input
    #lazy workaround to add support for two digits
    final_input = tuple(input)
    term1part1 = final_input[0]
    term1part2 = final_input[1]
    term1 = str(term1part1) + str(term1part2)
    final_term1 = (int(term1))
    operator = str(final_input[2])
    term2part1 = final_input[3]
    term2part2 = final_input[4]
    term2 = str(term2part1) + str(term2part2)
    final_term2 = (int(term2))
    #actual calculations go here
    if input == "help":
        await event.edit("Syntax .calc <term1><operator><term2>\nFor eg .calc 02*02 or 99*99 (the zeros are important) (two terms and two digits max)")
    elif operator == "*":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 * final_term2))
    elif operator == "-":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 - final_term2))
    elif operator == "+":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 + final_term2))
    elif operator == "/":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 / final_term2))
    elif operator == "%":
        await event.edit("Solution -->\n" + exp + "\n" + str(final_term1 % final_term2))
    else:
        await event.edit("use .calc help")
