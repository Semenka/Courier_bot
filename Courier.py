import sys
import time
import telepot

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print 'Chat Message:', content_type, chat_type, chat_id

import sys
import time
import telepot

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print 'Chat Message:', content_type, chat_type, chat_id

def on_inline_query(msg):
    def compute_answer():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print 'Computing for: %s' % query_string

        articles = [{'type': 'article',
                         'id': 'abc', 'title': query_string, 'message_text': query_string}]

        return articles

    answerer.answer(msg, compute_answer)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print 'Chosen Inline Result:', result_id, from_id, query_string


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

bot.notifyOnMessage({'normal': on_chat_message,
                     'inline_query': on_inline_query,
                     'chosen_inline_result': on_chosen_inline_result})
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)