import MenuTEST
import User
import Menues
import Kit
import Card
import time
import os
import random
import Mode_interface

m = MenuTEST.Menu()
u = User.User(input("Добро пожаловать, введите ваш юзернейм: ").strip())
m.display_menu()
m.handle_input(u)