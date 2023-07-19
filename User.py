import Kit
import Card


class User:
    def __init__(self, user: str):
        self.__kits = []
        self.__username = user

    def get_username(self) -> str:
        return self.__username

    def get_count_kits(self) -> int:
        return len(self.__kits)

    def get_kit_by_index(self, inedex: int) -> Kit:
        return self.__kits[inedex]

    def add_kit(self, kit: Kit) -> None:
        self.__kits.append(kit)

    def remove_kit(self, index: int):
        self.__kits.pop(index)

    def show_kits(self) -> None:
        if not(self.__kits):
            print("Список наборов пуст!")
        for i in range(len(self.__kits)):
            print(i, self.__kits[i].get_name_kit())

    def show_kit(self, index: int) -> None:
        print(index, self.__kits[index].get_name_kit())

    def show_element_of_kit(self, index: int) -> None:  # Вывод слово - перевод
        card_list = self.__kits[index].get_card_list()
        if not(card_list):
            print("Набор пуст!")
        for j in range(len(card_list)):
            print(j, card_list[j].get_card_content()[0], card_list[j].get_card_content()[1])

    def show_progress(self, index: int) -> None:
        print(self.__kits[index].get_progress())
