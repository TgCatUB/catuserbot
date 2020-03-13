import threading



from sqlalchemy import Column, UnicodeText, Integer

from userbot.plugins.sql_helper import SESSION, BASE







class RSS(BASE):

    __tablename__ = "rss_feed"

    id = Column(Integer, primary_key=True)

    chat_id = Column(UnicodeText, nullable=False)

    feed_link = Column(UnicodeText)

    old_entry_link = Column(UnicodeText)



    def __init__(self, chat_id, feed_link, old_entry_link):

        self.chat_id = chat_id

        self.feed_link = feed_link

        self.old_entry_link = old_entry_link



    def __repr__(self):

        return "<RSS for chatID {} at feed_link {} with old_entry_link {}>".format(self.chat_id,

                                                                                   self.feed_link,

                                                                                   self.old_entry_link)





RSS.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()





def check_url_availability(tg_chat_id, tg_feed_link):

    try:

        return SESSION.query(RSS).filter(RSS.feed_link == tg_feed_link,

                                         RSS.chat_id == tg_chat_id).all()

    finally:

        SESSION.close()





def add_url(tg_chat_id, tg_feed_link, tg_old_entry_link):

    with INSERTION_LOCK:

        action = RSS(tg_chat_id, tg_feed_link, tg_old_entry_link)



        SESSION.add(action)

        SESSION.commit()





def remove_url(tg_chat_id, tg_feed_link):

    with INSERTION_LOCK:

        # this loops to delete any possible duplicates for the same TG User ID, TG Chat ID and link

        for row in check_url_availability(tg_chat_id, tg_feed_link):

            # add the action to the DB query

            SESSION.delete(row)



        SESSION.commit()





def get_urls(tg_chat_id):

    try:

        return SESSION.query(RSS).filter(RSS.chat_id == tg_chat_id).all()

    finally:

        SESSION.close()





def get_all():

    try:

        return SESSION.query(RSS).all()

    finally:

        SESSION.close()





def update_url(row_id, new_entry_links):

    with INSERTION_LOCK:

        row = SESSION.query(RSS).get(row_id)



        # set the new old_entry_link with the latest update from the RSS Feed

        row.old_entry_link = new_entry_links[0]



        # commit the changes to the DB

        SESSION.commit()
