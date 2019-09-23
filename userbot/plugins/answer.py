from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="answer ?(.*)", outgoing=True))
async def answer:
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.answer(message="Nom Nom NOM! Files deleted.\nLast Words were: {}".format(input_str))
