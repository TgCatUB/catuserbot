"""Get Poll Info on non supported clients
Syntax: .get_poll"""
from telethon import events
import asyncio
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="get_poll"))
async def _(event):
    reply_message = await event.get_reply_message()
    if reply_message.media is None:
        await event.edit("Please reply to a media_type == @gPoll to view the questions and answers")
    elif reply_message.media.poll is None:
        await event.edit("Please reply to a media_type == @gPoll to view the questions and answers")
    else:
        media = reply_message.media
        poll = media.poll
        closed_status = poll.closed
        answers = poll.answers
        question = poll.question
        edit_caption = """Poll is Closed: {}
Question: {}
Answers: \n""".format(closed_status, question)
        if closed_status:
            results = media.results
            i = 0
            for result in results.results:
                edit_caption += "{}> {}    {}\n".format(result.option, answers[i].text, result.voters)
                i += 1
            edit_caption += "Total Voters: {}".format(results.total_voters)
        else:
            for answer in answers:
                edit_caption += "{}> {}\n".format(answer.option, answer.text)
        await event.edit(edit_caption)
