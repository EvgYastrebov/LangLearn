import Card
import Kit
import User
import subprocess
import Menues
import os
import time
import Mode_interface

class Menu:
    def clear_terminal(self):
        if os.name == 'posix':  # Для Unix-подобных систем (Linux, macOS)
            os.system('clear')
        elif os.name == 'nt':  # Для Windows
            os.system('cls')

    def display_menu(self):
        print()
        print("Меню:")
        for key, item in Menues.menu_items.items():
            print(f"{key}. {item['name']}")
        print()
        print("Выберите пункт меню по номеру или введите 'q' для выхода")

    def display_kits_menu(self):
        print()
        print("Меню:")
        for key, item in Menues.kit_show_items.items():
            print(f"{key}. {item['name']}")
        print()
        print("Выберите пункт меню по номеру или введите 'q' для выхода")

    def display_cards_menu(self):
        print()
        print("Меню:")
        for key, item in Menues.card_show_items.items():
            print(f"{key}. {item['name']}")
        print()
        print("Выберите пункт меню по номеру или введите 'q' для выхода")

    def display_mode_menu(self):
        print()
        print("Меню:")
        for key, item in Menues.menu_show_items.items():
            print(f"{key}. {item['name']}")
        print()
        print("Выберите пункт меню по номеру или введите 'q' для выхода")

    def handle_input(self, user):
        u = user
        while True:
            user_input = input("Введите номер пункта меню: ").strip()
            if user_input == 'q':
                break# Выход из программы
            elif user_input in Menues.menu_items.keys():
                selected_item = Menues.menu_items[user_input]
                print(f"Выбран пункт меню: {selected_item['name']}")
                command = selected_item['command']
                self.execute_command(command, u)
            else:
                print("Некорректный ввод. Попробуйте снова.")

    def execute_command(self, command, user):
        u = user
        if command == 'main_menu_command_1':
            self.clear_terminal()
            kit = Kit.Kit(input("Введите название набора: ").strip())
            if kit.get_name_kit() == 'q':
                self.display_menu()
                return
            u.add_kit(kit)
            print("Набор добавлен!")
            self.display_menu()
        elif command == 'main_menu_command_2':
            while True:
                while True:
                    u.show_kits()
                    print()
                    kit_number_input = input("Введите номер желаемого набора для взаимодействия с ним: ").strip()
                    if (kit_number_input.isdigit()) and (not(u.get_count_kits() - 1 < int(kit_number_input))) or (kit_number_input == 'q'):
                        break
                    else:
                        self.clear_terminal()
                        print("Некорректный ввод. Попробуйте снова.")

                if kit_number_input == 'q':
                    self.display_menu()
                    return

                kit_number_input = int(kit_number_input)
                u.show_element_of_kit(kit_number_input)
                print()
                self.display_kits_menu()
                while True:
                    user_input = input("Введите номер пункта меню: ").strip()
                    if user_input == 'q' or kit_number_input == -1:
                        self.clear_terminal()
                        self.display_menu()
                        break # Выход из программы
                    elif user_input in Menues.kit_show_items.keys():
                        selected_item = Menues.kit_show_items[user_input]
                        print(f"Выбран пункт меню: {selected_item['name']}")
                        command = selected_item['command']
                        self.execute_command_kit(command, kit_number_input, u)
                    else:
                        print("Некорректный ввод. Попробуйте снова.")

    def execute_command_kit(self, command, kit_number_input, user):
        u = user
        def kit_and_menu():
            print("Текущий набор:", end='')
            u.show_kit(kit_number_input)
            print()
            self.display_kits_menu()
            print()
        if command == 'kit_menu_command_1':
            self.clear_terminal()
            cardi = Card.Card()
            cardi_edit_input = input("Введите слово и его перевод: ").strip().split()
            if (len(cardi_edit_input) == 1) and (cardi_edit_input[0] == 'q'):
                kit_and_menu()
                return
            elif len(cardi_edit_input) < 2:
                print("Неправильный ввод!")
                time.sleep(2)
                self.execute_command_kit('kit_menu_command_1', kit_number_input, u)
                return
            cardi.add_card(cardi_edit_input[0],cardi_edit_input[1])
            u.get_kit_by_index(kit_number_input).add_card(cardi)
            self.clear_terminal()
            kit_and_menu()
            return True
        elif command == 'kit_menu_command_2': # ------------------- меню карточек
            while True:
                while True:
                    print("Введите 'q', чтобы вернуться назад")
                    print("Слова, содержащиеся в этом наборе:")
                    u.show_element_of_kit(kit_number_input)
                    print()
                    card_number_input = input("Выберете карточку, с которой хотите взаимодейсвтовать:").strip()
                    if (card_number_input.isdigit()) and not(len(u.get_kit_by_index(kit_number_input).get_card_list()) - 1) < (int(card_number_input)) or card_number_input == 'q':
                        break
                    else:
                        self.clear_terminal()
                        print("Некорректный ввод. Попробуйте снова.")

                if card_number_input == 'q' :
                    self.clear_terminal()
                    self.display_kits_menu()
                    return True

                card_number_input = int(card_number_input)
                self.display_cards_menu()
                while True:
                    user_input = input("Введите номер пункта меню: ").strip()
                    if user_input == 'q':
                        self.clear_terminal()
                        u.show_element_of_kit(kit_number_input)
                        break # Выход из программы
                    elif user_input in Menues.card_show_items.keys():
                        selected_item = Menues.card_show_items[user_input]
                        print(f"Выбран пункт меню: {selected_item['name']}")
                        command = selected_item['command']
                        if self.execute_command_card(command, kit_number_input, card_number_input, u):
                            break
                    else:
                        print("Некорректный ввод. Попробуйте снова.")
        elif command == 'kit_menu_command_3':
            self.clear_terminal()
            print("Ваш текущий прогресс по данному набору:", "{:.2f}%".format(u.get_kit_by_index(kit_number_input).get_progress()*100))
            print()
            kit_and_menu()
            return True
        elif command == 'kit_menu_command_4':
            self.clear_terminal()
            u.get_kit_by_index(kit_number_input).reset_counter()
            print("Ваш прогрес по данному набору сброшен!")
            print()
            kit_and_menu()
            return True
        elif command == 'kit_menu_command_5':
            u.remove_kit(kit_number_input)
            self.clear_terminal()
            print("Набор удален")
            return False
        elif command == 'kit_menu_command_6': #вызов режима ----------------------
            self.clear_terminal()
            self.display_mode_menu()
            while True:
                user_input = input("Введите номер пункта меню: ").strip()
                if user_input == 'q':
                    self.display_kits_menu()
                    return True # Выход из программы
                elif user_input in Menues.menu_show_items.keys():
                    selected_item = Menues.menu_show_items[user_input]
                    print(f"Выбран пункт меню: {selected_item['name']}")
                    command = selected_item['command']
                    self.execute_command_mode(command, kit_number_input, u)
                else:
                    print("Некорректный ввод. Попробуйте снова.")

    def execute_command_mode(self, command, kit_number_input, user):
        u = user
        if command == 'mode_menu_command_1':
            self.clear_terminal()
            u.get_kit_by_index(kit_number_input).start_module(1)
            self.display_mode_menu()
        elif command == 'mode_menu_command_2':
            self.clear_terminal()
            if len(u.get_kit_by_inedx(kit_number_input).get_card_list()) < 4:
                print("Ошибка! Требуется хотя бы 4 карточки в наборе!")
                self.display_mode_menu()
                return
            u.get_kit_by_index(kit_number_input).start_module(2)
            self.display_mode_menu()
        elif command == 'mode_menu_command_3':
            self.clear_terminal()
            u.get_kit_by_index(kit_number_input).start_module(3)
            self.display_mode_menu()

    def execute_command_card(self, command, kit_number_input, card_number_input, user):
        u = user
        if command == 'card_menu_command_1':
            self.clear_terminal()
            edit_input = input("Введите измененное слово и его перевод: ").strip().split()
            if edit_input == ['q']:
                self.clear_terminal()
                self.display_cards_menu()
                return False
            u.get_kit_by_index(kit_number_input).get_card_list()[card_number_input].edit_card(edit_input[0],edit_input[1])
            print("Карточка успешно изменена!")
        elif command == 'card_menu_command_2':
            self.clear_terminal()
            u.get_kit_by_index(kit_number_input).remove_card(card_number_input)
            print("Карточка успешно удалена!")
            print()
        return True