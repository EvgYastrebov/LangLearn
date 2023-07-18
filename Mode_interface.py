import Kit
import Card
import random


class ModeStrategy():
    def __init__(self, kit: Kit):
        self._kit = kit
        self._sequence = []

    def create_sequence(self, mode: int) -> None:  # Создание последовательности
        self._sequence = self._kit.get_card_list()
        index_sequence = []
        for i in range (len(self._sequence)):
            index_sequence.append(i)
        self._sequence = list(zip(self._sequence, index_sequence))  # Присваиваем каждой карточке её индекс в наборе (kit)
        card_list = self._sequence
        random.shuffle(self._sequence)

        list_of_part_rates = [0.75, 0.5, 0.25]  # Добавляем в последователность слова до определенного рейтинга
        for elem in list_of_part_rates:
            self.__add_part_of_sequence(card_list, mode, elem)

        if len(self._sequence) > 2 * len(card_list):  # Обрезаем последовательность до размера 2n
            self._sequence = self._sequence[:2 * len(card_list)]

    def change_rate(self, mode: int, index: int, is_correct: bool) -> None:  # Изменение рейтинга слова
        if is_correct and self._kit.get_card_list()[index].get_word_rates()[mode] < 1:
            self._kit.get_card_list()[index].get_word_rates()[mode] += 0.1
        elif self._kit.get_card_list()[index].get_word_rates()[mode] > 0:
            self._kit.get_card_list()[index].get_word_rates()[mode] -= 0.1

    def change_word_translation(self) -> None:  # Слово и перевод меняются местами
        for i in range (len(self._sequence)):
            self._sequence[i][0].get_card_content()[0], self._sequence[i][0].get_card_content()[1] = self._sequence[i][0].get_card_content()[1], self._sequence[i][0].get_card_content()[0]

    def get_cards(self) -> list[Card]:
        return self._kit.get_card_list()

    def get_card(self, index: int) -> Card:
        return self._kit.get_card_list()[index]

    def get_sequence(self) -> list[[str, str], int]:
        return self._sequence

    def get_kit(self) -> Kit:
        return self._kit

    def __add_part_of_sequence(self, card_list: list, mode: int, limit_of_rate: float) -> None:  # Добавление частей последовательности
        if len(self._sequence) < 2 * len(card_list):
            for i in range (len(card_list)):
                if (card_list[i][0].get_word_rate(mode)) <= limit_of_rate:
                    self._sequence.append(card_list[i])

class ModeChoice(ModeStrategy):  # Режим выбора ответа
    def random_words(self, index: int) -> list[int, list[str, str, str, str]]:
        variants = [self._sequence[index][0]]
        other_words_sequence = self._kit.get_card_list()
        other_words_sequence = other_words_sequence[:self._sequence[index][1]] + other_words_sequence[self._sequence[index][1] + 1:]
        variants += random.sample(other_words_sequence, 3)  # list из элементов _sequence [правильный, рандом, рандом, рандом]
        true_index = random.randint(0, 3)  # По этому индексу будет лежать правильный ответ
        variants[0], variants[true_index] = variants[true_index], variants[0]
        return [true_index, variants]

    @staticmethod
    def check(answer: int, true_index: int) -> bool:  # Проверка ответа
        return answer - 1 == true_index


class ModeWrite(ModeStrategy):  # Режим ввода
    def check(self, answer: str, index: int) -> bool:  # Проверка введенного слова
        return answer == self._sequence[index][0].get_card_content()[1]


class ModeRotation(ModeStrategy):  # Режим карточек
    @staticmethod
    def rotation(current_word: str, current_pair: list[str, str]) -> str:
        return current_pair[1] if current_word == current_pair[0] else current_pair[1]

