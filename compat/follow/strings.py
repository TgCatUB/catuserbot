source = 'https://gitlab.com/blankX/follow'

ids_seperator = ' >> '
all_followers = '>><<'
here_chat = '<<>>'
traverse_seperator = '.'

follow_who = '404: Follower {} not found'
cmd_notes_failed = '404: Cannot find note {}'
cmd_execnotes_failed = '404: Cannot find execnote {}'
no_lydia = 'Lydia is not enabled!'
user_required = '404: No user found'
speedtest_disabled = 'Speedtest is not enabled!'
newer_db = 'The database\'s version ({}) is newer than expected ({})'

cmd_help_text = r'^follow help(?: (.+))?$'
cmd_help_text_help = '''
<code>follow help</code>
<code>follow help [optional follower name/id]</code>
	What are you reading?
'''

cmd_followers = r'^follow followers$'
cmd_followers_respond = '''Followers:
<code>{}</code>'''
cmd_followers_sub = '{num} / {name} / {trust}\n'
cmd_followers_help = '''
<code>follow followers</code>
	Shows the list of followers
'''

cmd_deactivate = r'^follow deactivate$'
cmd_deactivate_respond = '200: Operation deactivate complete'
cmd_deactivate_help = '''
<code>follow deactivate</code>
	Turns off the userbot
'''

cmd_send = r'^follow s(?:end|ay)(?: (.+))?\n(.+)\n([\s\S]+)$'
cmd_send_help = '''
<code>follow send [optional follower name/id]
[chat]
[text]</code>
	Sends <code>[text]</code> to <code>[chat]</code>
'''

cmd_join = r'^follow join(?: (.+))?\n(?:(?:https?://)?(?:t\.me|telegram\.(?:org|me|dog))/joinchat/)?(.+)$'
cmd_join_respond = '200: Operation join complete.'
cmd_join_help = '''
<code>follow join [optional follower name/id]
[username/invite]</code>
	Joins <code>[username/invite]</code>
'''

cmd_leave = r'^follow leave(?: (.+))?\n(?:(?:https?://)?(?:t\.me|telegram\.(?:org|me|dog))/joinchat/)?(.+)$'
cmd_leave_respond = '200: Operation leave complete.'
cmd_leave_help = '''
<code>follow leave [optional follower name/id]
[username/invite/id]</code>
	Leaves <code>[username/invite/id]</code>
'''

cmd_speedtest = r'^follow speedtest$'
cmd_speedtest_processing = 'Operation Speedtest:\nTesting Download\n'
cmd_speedtest_upload = 'Testing Upload'
cmd_speedtest_respond = '<a href="{1}">{0}</a>200: Operation speedtest complete'
cmd_speedtest_help = '''
<code>follow speedtest</code>
	Does a speedtest (blocking calls are made)
'''

cmd_cli = r'^follow cli (.+)$'
cmd_cli_respond = '200: Executed'
cmd_cli_help = '''
<code>follow cli [cli command]</code>
	Runs <code>[cli command]</code> (for shell)
'''

cmd_notes_add = r'^follow n(?:otes?)? (?:add|save) (.+)\n([\s\S]+)$'
cmd_notes_add_respond = '200: Operation add note complete'
cmd_notes_add_help = '''
<code>follow notes add [name]
[content]</code>
	Adds a note named <code>[name]</code> with <code>[content]</code>
'''

cmd_notes_remove = r'^follow n(?:otes?)? remove (.+)$'
cmd_notes_remove_respond = '200: Operation remove note complete'
cmd_notes_remove_help = '''
<code>follow notes remove [name]</code>
	Removes the note <code>[name]</code>
'''

cmd_notes = r'^follow n(?:otes?)? ((?!add)(?!remove)(?!save).+)$'
cmd_notes_help = '''
<code>follow notes [name]</code>
	Gets the note <code>[name]</code>
'''

cmd_notes_list = r'^follow n(?:otes?)?$'
cmd_notes_list_respond = '''Notes:
<code>{}</code>'''
cmd_notes_list_help = '''
<code>follow notes</code>
	Lists your notes
'''

cmd_execnotes_add = r'^follow e(?:xec)?n(?:otes?)? (?:add|save) (.+)\n([\s\S]+)$'
cmd_execnotes_add_respond = '200: Operation add execnote complete'
cmd_execnotes_add_help = '''
<code>follow execnotes add [name]
[code]</code>
	Adds an execnote named <code>[name]</code> that runs <code>[code]</code>
'''

cmd_execnotes_remove = r'^follow e(?:xec)?n(?:otes?)? remove (.+)$'
cmd_execnotes_remove_respond = '200: Operation remove execnote complete'
cmd_execnotes_remove_help = '''
<code>follow execnotes remove [name]</code>
	Removes the execnote <code>[name]</code>
'''

cmd_execnotes = r'^follow e(?:xec)?n(?:otes?)? ((?!add)(?!remove)(?!show)(?!save).+)$'
cmd_execnotes_help = '''
<code>follow execnotes [name]</code>
	Runs the execnote <code>[name]</code>
'''

cmd_execnotes_show = r'^follow e(?:xec)?n(?:otes?)? show (.+)$'
cmd_execnotes_show_help = '''
<code>follow execnotes show [name]</code>
	Shows the code for the execnote <code>[name]</code>
'''

cmd_execnotes_list = r'^follow e(?:xec)?n(?:otes?)?$'
cmd_execnotes_list_respond = '''Execnotes:
<code>{}</code>'''
cmd_execnotes_list_help = '''
<code>follow execnotes</code>
	Lists your execnotes
'''

cmd_exec_py = r'^follow exec[ \n]([\s\S]+)$'
cmd_exec_py_processing = 'Executing...'
cmd_exec_py_respond = '200: Executed'
cmd_exec_py_returned = '''200: Executed, code returned:
<code>{}</code>'''
cmd_exec_py_help = '''
<code>follow exec
[python code]</code>
	Executes <code>[python code]</code> (for python)
'''

cmd_execnotes_processing = cmd_exec_py_processing
cmd_execnotes_respond = cmd_exec_py_respond
cmd_execnotes_returned = cmd_exec_py_returned

cmd_restart = r'^follow (q(?:uick[\-_]?)?)?re(?:start|boot)$'
cmd_restart_respond = 'Restarting...'
cmd_restart_restarted = '200: Restarted'
cmd_restart_help = '''
<code>follow restart</code>
<code>follow qrestart</code>
	Restarts the userbot
	Quickly restart the userbot
'''

cmd_insult = r'^follow insult (.+)$'
cmd_insult_help = '''
<code>follow insult [name]</code>
	Insults <code>[name]</code>
'''

cmd_dcinfo = r'^follow dcinfo(?: (.+))?$'
cmd_dcinfo_help = '''
<code>follow dcinfo [optional follower id/name]</code>
	Gets the country, nearest DC and current DC
'''

cmd_cas = r'^follow cas (\d+)$'
cmd_cas_processing = 'Processing...'
cmd_cas_respond = '''<a href="https://combot.org/cas/query?user_id={user_id}">Record found!</a>
Offenses: {offenses}

<a href="https://combot.org/cas">Powered by CAS</a>'''
cmd_cas_help = '''
<code>follow cas [user id]</code>
	Checks if <code>[user id]</code> is CAS banned
	Uses <a href="https://combot.org/cas">CAS</a>
'''

cmd_afk = r'^follow afk (.+)$'
cmd_afk_respond = '200: AFK Status Set'
im_afk = """I'm currently AFK. Why?
{}"""
cmd_afk_help = '''
<code>follow afk [reason]</code>
	Sets your AFK status
'''

cmd_unafk = r'^follow unafk$'
cmd_unafk_respond = '200: AFK Status Set'
cmd_unafk_help = '''
<code>follow unafk</code>
	Unsets your AFK status
'''

crawler_joined = '''Joined <code>{invite}</code>

From: <a href="tg://user?id={user.id}">{user.id}</a>
<a href="t.me/c/{sanitised_cid}/{e.id}">Message Link</a>'''
crawler_failed = 'Cannot join chat <code>{invite}</code>'

cmd_json = r'^follow json(?: (.+))?$'
cmd_json_help = '''
<code>follow json [optional traverse path]</code>
	Shows the json of the replied/sent message
'''

cmd_info = r'^follow(?: (?:i(?:nfo)?|stat(?:us|s)?|about))?$'
cmd_info_respond = '''Userbot online.

<code>Followers: {fwlr_count}
Current Follower: {fwlr.identifier.name}
Message Count: {message_count}
Source Code:</code> {source}'''
cmd_info_help = '''
<code>follow</code>
	Gives userbot info
'''

cmd_lydia_enable = r'^follow lydia (?:enable|[Tt]rue)(?: (.+))?$'
cmd_lydia_enable_respond = 'Lydia enabled!'
cmd_lydia_enable_already = 'Lydia is already enabled!'
cmd_lydia_enable_help = '''
<code>follow lydia enable [user]</code>
<code>follow lydia enable</code> <i>(as reply)</i>
	Enable lydia for <code>[user]</code>
'''

cmd_lydia_disable = r'^follow lydia (?:disable|[Ff]alse)(?: (.+))?$'
cmd_lydia_disable_respond = 'Lydia disabled!'
cmd_lydia_disable_already = 'Lydia is already disabled!'
cmd_lydia_disable_help = '''
<code>follow lydia disable [user]</code>
<code>follow lydia disable</code> <i>(as reply)</i>
	Disable lydia for <code>[user]</code>
'''

cmd_admin_report = r'@admins?|^[/\.!#](?:report|admins?)(?:$|\W)'
admin_report = '''Admin report!

<a href='{link}'>Chat</a>: <code>{chat.id}</code>
<a href='tg://user?id={reporter.id}'>Reporter</a>: <code>{reporter.id}</code>
<a href='tg://user?id={reportee.id}'>Reportee</a>: <code>{reportee.id}</code>
Remark: <code>{remark}</code>
Reported Message: <code>{reported_message}</code>'''
admin_report_no_reportee = '''Admin report!

<a href='{link}'>Chat</a>: <code>{chat.id}</code>
<a href='tg://user?id={reporter.id}'>Reporter</a>: <code>{reporter.id}</code>
Remark: <code>{remark}</code>'''

cmd_brief = r'^follow brief(?: (.+))?\n([\s\S]+)$'
cmd_brief_help = '''
<code>follow brief [seconds]
[text]</code>
	Sends <code>[text]</code> and delete it after <code>[seconds]</code>
'''

cmd_ignore_enable = r'^follow ignore (?:enable|[Tt]rue)(?: (.+))?$'
cmd_ignore_enable_respond = 'User ignored!'
cmd_ignore_enable_already = 'User is already ignored!'
cmd_ignore_enable_help = '''
<code>follow ignore enable [user]</code>
<code>follow ignore enable</code> <i>(as reply)</i>
	Ignores <code>[user]</code>
'''

cmd_ignore_disable = r'^follow ignore (?:disable|[Ff]alse)(?: (.+))?$'
cmd_ignore_disable_respond = 'User un-ignored!'
cmd_ignore_disable_already = 'User is already un-ignored!'
cmd_ignore_disable_help = '''
<code>follow ignore disable [user]</code>
<code>follow ignore disable</code> <i>(as reply)</i>
	Un-ignores <code>[user]</code>
'''

cmd_flydia_enable = r'^follow f(?:orce)?lydia (?:enable|[Tt]rue)(?: (.+))?$'
cmd_flydia_enable_respond = 'Lydia enabled in groups!'
cmd_flydia_enable_already = 'Lydia is already enabled in groups!'
cmd_flydia_enable_help = '''
<code>follow flydia enable [user]</code>
<code>follow flydia enable</code> <i>(as reply)</i>
	Enable lydia for <code>[user]</code> in groups
'''

cmd_flydia_disable = r'^follow f(?:orce)?lydia (?:disable|[Ff]alse)(?: (.+))?$'
cmd_flydia_disable_respond = 'Lydia disabled in groups!'
cmd_flydia_disable_already = 'Lydia is already disabled in groups!'
cmd_flydia_disable_help = '''
<code>follow flydia disable [user]</code>
<code>follow flydia disable</code> <i>(as reply)</i>
	Disable lydia for <code>[user]</code> in groups
'''

cmd_read = r'^follow (?:(q)(?:uick)?[\-_]?)?read(?: (.+))?\n(.+)$'
cmd_read_respond = '200: Operation read complete'
cmd_read_help = '''
<code>follow read [optional follower id/name]
[chat]</code>
<code>follow qread [optional follower id/name]
[chat]</code>
	Reads <code>[chat]</code> as <code>[optional follower id/name]</code>
	Quickly reads <code>[chat]</code> as <code>[optional follower id/name]</code>
'''
