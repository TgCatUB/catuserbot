# Default flags to use
# Flags:
# noall (excludes the follower from being chosen when using all followers)
# crawler
# lydia (enable lydia on this follower?)
# adminreport (receives admin reports and sends it to log_chat)
# noerr
#   if used on follower, follower's errors will be sent to log chat
#   if used on handler, handler's errors will be sent to log chat
# msgcount (counts all the messages you have and show it in 'follow info')
# ignore (if a user is ignored, ignore that user on this follower)
# flydia (have lydia talk to flydia'd (lydia in groups) users?)
# afk (afk responses from this follower?)
default_flags = {'lydia': True, 'adminreport': True, 'msgcount': True, 'ignore': True, 'flydia': True, 'afk': True}
# Chat used for logs
log_chat = -1001172135061
# Send help text as file?
help_as_file = True
# Try to use windows newlines everywhere?
windows_newlines = False
# Lydia API Key (set as None if you don't want it)
# To get one, send `#activateapi` to https://t.me/IntellivoidDev
lydia_api = None

from classes import identify, internal_chat, flags
# Tuple of followers to use (and authorize)
# internal id, internal name, session path, trust (defaults to infinity), flags (see default flags)
followers = (
#identify(0, 'example-follower', 'followers/0-example-follower.session'),
#identify(1, 'controlled-by-someone-else', 'followers/1-cbse.session', 5),
#identify(2, 'crawler', 'followers/2-crawler.session', flags=flags(crawler=True)),
#identify(3, 'no-default-example', 'followers/3-nde.session', flags=flags(True, noall=True))
)

# Internal chat names used
# chat username/id, internal chat name (str or list)
internal_chat_names = (
#internal_chat('userbottestingspam', 'ubs'),
#internal_chat('userbottesting', 'ub'),
#internal_chat(-1001338615562, 'bge'),
#internal_chat('owlybird', ('owl', 'owls', 'owl\'s'))
)
