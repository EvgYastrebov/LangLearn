class Card:
    def __init__(self) -> None:
        self.__card = ['', '']
        self.__word_rates = [0, 0, 0]

    def get_card_content(self) -> list:
        return self.__card

    def get_word_rates(self) -> list:
        return self.__word_rates

    def get_word_rate(self, index: int) -> float:
        return self.__word_rates[index]

    def edit_card(self, word:str, translation:str) -> None:
        self.__card[0] = word
        self.__card[1] = translation
        self.__word_rates = [0, 0, 0]

