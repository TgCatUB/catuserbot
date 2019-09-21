from config import default_flags

class flags:
	def __init__(self, disable_defaults=False, *, noall=None, crawler=None,
	lydia=None, adminreport=None, noerr=None, msgcount=None, ignore=None,
	flydia=None, afk=None):
		for flag in default_flags:
			self.__dict__[flag] = default_flags[flag]
		def iin(flag, rflag):
			if flag in default_flags and not disable_defaults:
				if rflag is not None:
					return rflag
				return default_flags[flag]
			return rflag
		self.noall = iin('noall', noall)
		self.crawler = iin('crawler', crawler)
		self.lydia = iin('lydia', lydia)
		self.adminreport = iin('adminreport', adminreport)
		self.noerr = iin('noerr', noerr)
		self.msgcount = iin('msgcount', msgcount)
		self.ignore = iin('ignore', ignore)
		self.flydia = iin('flydia', flydia)
		self.afk = iin('afk', afk)

	def __repr__(self):
		return "".join(
		(f'flags(noall={self.noall}, crawler={self.crawler}, ',
		f'lydia={self.lydia}, adminreport={self.adminreport}, ',
		f'noerr={self.noerr}, msgcount={self.msgcount}, ',
		f'ignore={self.ignore}, flydia={self.flydia},',
		f'afk={self.afk})')
		)

	def compare(self, to_be_compared):
		for flag in to_be_compared.__dict__.keys():
			if to_be_compared.__dict__[flag] == self.__dict__[flag] == True:
				if flag not in ('noerr',):
					return True
		for flag in to_be_compared.__dict__.keys():
			if to_be_compared.__dict__[flag]:
				if flag not in ('noerr',):
					return False
		return True

class identify:
	def __init__(self, int_id, name, session_path, trust=float('inf'), flags=flags(**default_flags)):
		self.int_id = int_id
		self.name = name
		self.session_path = session_path
		self.trust = trust
		self.flags = flags

	def __repr__(self):
		return "".join(
		(f'identify({self.int_id}, {self.name}, {self.session_path}, ',
		f'trust={self.trust}, flags={self.flags})')
		)

class internal_chat:
	def __init__(self, actual_chat, chat):
		self.actual_chat = actual_chat
		self.chat = chat

	def __eq__(self, chat):
		if self.chat == chat:
			return True
		if chat in set(self.chat):
			return True
		return False

	def __repr__(self):
		return f'internal_chat({self.actual_chat}, {self.chat})'

	def __iter__(self):
		return iter([self])

class follower:
	def __init__(self, identifier, client, me, enu):
		self.identifier = identifier
		self.client = client
		self.me = me
		self.enu = enu

		self.disconnect = client.disconnect

	def __eq__(self, int_id):
		return self.identifier.int_id == int_id

	def __iter__(self):
		return iter([self])

	async def online(self):
		return self.client.is_connected() and await self.client.is_user_authorized()
