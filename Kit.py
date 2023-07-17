import Card
import os
import time
import Mode_interface
import MenuTEST



class Kit():
    def __init__(self, name):
      self.__name = name
      self.__card_list = []
      self.__progress = 0.0

    def get_name_kit(self) -> str:
        return self.__name

    def get_card_list(self) -> list:
        return self.__card_list

    def change_name(self, new_name) -> bool:
        old_name = self.__name
        self.__name = new_name
        return self.__name != old_name

    def add_card(self, new_card: Card) -> None:
        self.__card_list.append(new_card)

    def remove_card(self, card_index) -> None:
        self.__card_list.pop(card_index)

    def __progress_counter(self) -> None:
        sum_rate = 0
        for elem in self.__card_list:
            rate_list = elem.get_word_rates()
            for now_rate in rate_list:
                sum_rate += now_rate
            self.__progress = (sum_rate / len(self.__card_list))

    def get_progress(self) -> float:
        return self.__progress

    def reset_counter(self) -> None:
        self.__progress = 0

    def StartModule(self, mode: int) -> None:  # Запуск режима
        if mode == 1:
            Mod = Mode_interface.ModeWrite(self)
            print("Режим 'Письмо'", '\n')
        elif mode == 2:
            Mod = Mode_interface.ModeChoice(self)
            print("Режим 'Тест'", '\n')
        elif mode == 3:
            Mod = Mode_interface.ModeRotation(self)
            print("Режим 'Карточки'", '\n')

        i = 0
        Mod.create_sequence(mode - 1)  # Создание последовательности слов
        while (i <= len(Mod.get_sequence())):
            print("Введите 'q' чтобы выйти из режима", '\n')
            current_card = Mod.get_sequence()[i][0]
            if mode == 1:
                print("Как переводится это слово:", current_card.get_card_content()[0], '\n')
                user_input = input("Введите перевод: ").strip()
            elif mode == 2:
                print("Слово:", current_card.get_card_content()[0], '\n')
                true_index, current_set = Mod.random_words(i)
                print(*[x.get_card_content()[1] for x in current_set[:4]])
                print("(введите цифру от 1 до 4)", '\n', "Выберите номер варианта: ", sep='', end='')
                user_input = input().strip()

                if not(user_input.isdigit()):  # Проверка на правильность ввода
                    while not(user_input.isdigit()) and not(user_input == 'q'):
                        print("Неверный ввод, повторите попытку")
                        user_input = input().strip()
            elif mode == 3:
                print("Слово:", current_card.get_card_content()[0], '\n', "Нажмите 'F', чтобы перевернуть карточку")
                user_input = input().strip()
                if (user_input == 'q'):
                    Mod.get_kit().__progress_counter()
                    break
                print(Mod.rotation(current_card.get_card_content()[0], current_card.get_card_content()))
                print("Угадали ли вы слово? ", '\n', "Введите 'Y', если да и 'N', если нет", sep='')
                user_input = input().strip()
            if (user_input == 'q'):
                Mod.get_kit().__progress_counter()
                break

            if mode == 1:  # Проверка ответа
                answer = Mod.check(user_input, i)
            elif mode == 2:
                answer = Mod.check(int(user_input), true_index)
            elif mode == 3:
                answer = True if (user_input == 'Y') or (user_input == 'y') else False
            if answer:
                print("Правильно!")
            else:
                print("Неправильно")
            Mod.change_rate(mode - 1, Mod.get_sequence()[i][1], answer)  # Изменение рейтинга слова
            i += 1
            time.sleep(2)
            if os.name == 'posix':  # Очистка экрана для Unix-подобных систем (Linux, macOS)
                os.system('clear')
            elif os.name == 'nt':  # Для Windows
                os.system('cls')
        Mod.get_kit().__progress_counter()  # Изменение прогресса набора
