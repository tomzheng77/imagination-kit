class ImkGpt:
    """
    Class for quickly creating basic chatbots from arbitrary content
    Create a chatbot using the HTML files in the directory
    bot = s100.py.gpt.ii("test/htmls").c()
    bot.a("what is the square root of 2") => "1.4142"
    """
    def __init__(self, s100):
        self.s100 = s100
