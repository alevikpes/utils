import bot


class TestBot:

    def setup(self):
        self.bot = bot.SomeNameBot()

    def test_bot_url(self):
        testdata = 'https://api.telegram.org/bot/'
        assert testdata == self.bot._bot_url()
