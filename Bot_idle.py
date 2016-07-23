import sys
import asyncio
import telepot
import telepot.async
import paypalrestsdk
import logging

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AbSZYKQdrgaY7i4Q7CkLZADpPe-EPhdyPhzJx8yi2otgg6gC_8ILBWLPgOJQJQjsnbBwYGRZnLaubNKm",
  "client_secret": "EC1zXPSTZ4LFs0nNLE7avwrW4foDHOUY3K20QeOVrWF3MgRIt3iOsE4nYuDjTarTuAVqBa_Kb9RSBy0j" })


payment = paypalrestsdk.Payment({
  "intent": "sale",
  "payer": {
    "payment_method": "credit_card",
    "funding_instruments": [{
      "credit_card": {
        "type": "visa",
        "number": "4648420020326773",
        "expire_month": "07",
        "expire_year": "2017",
        "cvv2": "798",
        "first_name": "Andrey",
        "last_name": "Semenov" }}]},
  "transactions": [{
    "item_list": {
      "items": [{
        "name": "item",
        "sku": "item",
        "price": "0.01",
        "currency": "USD",
        "quantity": 1 }]},
    "amount": {
      "total": "0.01",
      "currency": "USD" },
    "description": "This is the payment transaction description." }]})


class YourBot(telepot.async.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.async.helper.Answerer(self)

    @asyncio.coroutine
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        command = msg['text'].strip().lower()
        if command == '/start':
            yield from self.sendMessage(chat_id,'Start')
        elif command == '/help':
            yield from self.sendMessage(chat_id,'Help')
        elif command == '/settings':
            yield from self.sendMessage(chat_id,'Properties')
        elif command == '/pay':
            if payment.create():
                print("Payment created successfully")
            else:
                print(payment.error)
    
        show_keyboard = {'keyboard':[['Yes','No'], ['','']]}
        hide_keyboard = {'hide_keyboard': True}
        yield from self.sendMessage(chat_id,'Order?', reply_markup=show_keyboard)
        print('Normal Message:', content_type, chat_type, chat_id,command)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        def compute_answer():
            articles = [{'type': 'article',
                            'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self._answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)



TOKEN ="169916765:AAHJwp1r_mIQ798eXj4fl2GbwwbNsTbI-h8"

bot = YourBot(TOKEN)
loop = asyncio.get_event_loop()


loop.create_task(bot.messageLoop())
print('Listening ...')
loop.run_forever()
