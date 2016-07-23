
import time
import telepot
import json
import requests
import webbrowser


class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        command = msg['text'].strip().lower()
        if command == '/start':
            self.sendMessage(chat_id,'Start')
        elif command == '/help':
            self.sendMessage(chat_id,'Help')
        elif command == '/settings':
            self.sendMessage(chat_id,'Properties')
        elif command == '/pay':
            #open form incuding credit vard details
            url='https://semenka.github.io/Courier_bot/'
            webbrowser.open_new(url)
        print(msg['text'])

        #Request item information from yandex.market
        #self.market_search(msg['text'])

        print('Normal Message:', content_type, chat_type, chat_id)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)


        def compute_answer():
            # Compose your own answers
            articles = [{'type': 'article',
                            'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self._answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)

    def market_search(self,item):
        #url = 'https://api.content.market.yandex.ru/v1/model/10495456/info.json?geo_id=213&fields=ALL'
        #url='https://api.partner.market.yandex.ru/v2/models.json?query='+item+'&regionId=2'
        url='http://market.apisystem.ru/v1/search.json?geo_id=213&text='+item
        print (url)
        headers = {
            #'Host': 'api.content.market.yandex.ru',
            'Host': 'market.apisystem.ru',
            'Accept': '*/*',
            #'Authorization': 'KleokrEWUEkOrus7fTHTobW3LABBCD'
            'Authorization':'0580d082246836717e5ae100f7ed138d934889b5d9eb93677ba4'
        }
        r = requests.get(url, headers=headers)
        print(r.status_code)
        print(r.text)

    def ebay_search(self,item):
        url = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=AndreySe-Courierb-SBX-909b6b9a7-841db9d3&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&keywords=item&paginationInput.entriesPerPage=2'
        r = requests.get(url)
        print(r.status_code)
        print(r.text)

    def make_payment_stripe(self,stripeToken,amount):
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account/apikeys
        stripe.api_key = "sk_test_SKNAHPz5wdiuXodRn8I2OBwC"

        # Get the credit card details submitted by the form
        token = request.POST[stripeToken]

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=amount,  # amount in cents, again
                currency="usd",
                source=token,
                description="Example charge"
            )
        except stripe.error.CardError as e:
            # The card has been declined
            pass


def run():

    TOKEN = "169916765:AAHJwp1r_mIQ798eXj4fl2GbwwbNsTbI-h8"
    bot = YourBot(TOKEN)
    bot.notifyOnMessage()
    print('Listening ...')
    # Keep the program running.
    while 1:
        time.sleep(10)

if __name__ == '__main__':
    run()