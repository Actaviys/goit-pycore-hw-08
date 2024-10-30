
'''
Команди:
        @1 - "hello" - Привітання з користувачем
        @2 - "add [ім'я]" - Створюю користувача
        -3- - "change [ім'я] [новий номер телефону]" - Замінив на команду `add-phone` (зберігає новий номер телефону 'phone' для контакту 'username', що вже існує в записнику.)
        @3 - "add-phone [ім'я] [номер телефону]" - Переробив команду `change`
        @4 - "phone [ім'я]" - Виводить номер телефону контакту
        @5 - "all" - Виводить всі контакти з номерами телефонів
        @6 - "exit" - Закрити програму
        @7 - "add-birthday [ім'я] [дата народження]" - Додаю до контакту день народження
        @8 - "show-birthday [ім'я]" - Показую день народження контакту
        @9 - "birthdays" - Повертає список користувачів, яких потрібно привітати по днях на наступному тижні
        @10 - "open-book [link to file]" - Команда для відкриття файлу в ручну
'''
""" 
Спростив клас Record і добавив функціонал до UserDict.
"""


from datetime import datetime
from collections import UserDict
import re
import pickle


class AddressBook(UserDict): #Клас для словника
    
    def add_record(self, data): #Метод для додавання словника до self.data
        super().update(data) #Додаю словник через super
    
    
    def find(self, fName): #Шукаю в словнику по імені
        return f"Find: {fName} {self.data.get(fName)}" #Повертаю результат
    
    
    def find_data_user(self, fdName, fdValue): #Метод для пошуку даних користувачів в UserDict 
        if self.data.get(fdName): #Роблю перевірку на співпадіння в поточному словнику користувачів UserDict
            userD = dict(self.data[fdName]) #Зберігаю словник користувача з UserDict якщо є співпадіння 
            return f"{fdName} - {fdValue} ->{userD[fdValue]}" #Повертаю результат пошуку 
    
    
    def find_birthday_users_for_week(self): #Метод пошуку користувачів на наступний тиждень
        try:
            today_time = datetime.today().date() #Зберігаю поточну дату
            dict_res = {} #Словник для результату пошуку
            
            for ur in self.data: #Проходжусь по словнику UserDict
                users_dicts = dict(self.data[ur]) #Зберігаю словник користувача
                
                if users_dicts.get("birthday"): #Роблю перевірку наявність дати народження
                    birtDT = datetime.strptime(users_dicts["birthday"], '%Y-%m-%d').date() #Перетворюю ДН з словника в об'єкт datetime
                    repYear = birtDT.replace(year=today_time.year) #Замінюю рік з ДН на поточний
                    
                    res_bird = int(( repYear - today_time ).days) #Віднімаю ДН від поточної дати і зберігаю як int
                    if res_bird <= 7 and res_bird >= 0: #Перевіряю чи на цьому тижні ДН
                        dict_res.update({ur: birtDT.isoformat()}) #Додаю до словника результатат перевірки 
                        
            return dict_res #Повертаю словник з результатом пошуку
        
        except: print("Wrong date in the dictionary") #Виводжу повідомлення якщо є помилкова дата народження в словнику
            

    def update_user(self, uUser, uDat=None): #Метод для оновлення даних користувача
        uDatKeys = "".join(dict(uDat).keys()) #Зберігаю ключ з вхідного словника
        if self.data.get(uUser): #Роблю перевірку на співпадіння в поточному словнику користувачів UserDict
            userD = dict(self.data[uUser]) #Зберігаю словник користувача з UserDict якщо є співпадіння    
            
            if userD.get(uDatKeys) == None: #Якщо немає спіпадінь в словнику користувача то додаю новий словник до користувача
                userD.update(uDat) #Добавляю до словника користувача <- вхідний словник
                super().update({uUser: userD}) #Оновлюю користувача в UserDict
                return print(f"'{uUser}' -> data has been updated")
            
            if userD.get(uDatKeys): #Якщо є ключ в користувача то оновлюю значення словника
                userD.update(uDat) #Добавляю до словника користувача <- вхідний словник
                super().update({uUser: userD}) #Оновлюю користувача в UserDict
                return print(f"'{uUser}' -> data has been updated")
            
        else: return print(f"User '{uUser}' -> is missing") #Якщо користувача не знайдено
    
    
    def delete(self, dName): #Метод для видалення запису з словника 
        return f"Delet - {dName} {self.data.pop(dName)}" #Повертаю результат і видаляю користувача




class Field(): #Базовий клас поля для контакту
    def __init__(self, fd_Name, fd_Phone=None) -> None:
        self.fd_Name = fd_Name
        self.fd_Phone = fd_Phone


class Name(Field): #Клас для імені ()
    def __init__(self, valName) -> None:
        self.valName = valName        
    
    def __str__(self) -> str:
        return self.valName


class Phone(Field): #Клас для телефону
    def __init__(self, valPhone) -> None:
        self.valPhone = valPhone
    
    def phone_validation(self): #Валідація номеру телефону
        if isinstance(self.valPhone, str) and len(self.valPhone) == 10: #Перевірка номера телефону
            return self.valPhone #Повертаю перевірений номер телефону
        else: return print("Wrong phone format") #Повертаю помилку невірного формату телефону


class Birthday(Field): #Клас для дати народження
    def __init__(self, valBirthday):
        self.valBirthday = valBirthday
    
    def birthday_validation(self): #Валідація дати народження
        try:
            validBirt = "".join(re.findall("\\d{2}\\.\\d{2}\\.\\d{4}", self.valBirthday)) #Додаю до рядка результат пошуку елементів врядку 
            self.lBirthday = datetime.strptime(validBirt, '%d.%m.%Y').date() #Пробую перетворити ДН з словника в об'єкт datetime
            return self.lBirthday.isoformat() #Повертаю об'єкт datetime з методом isoformat()
        
        except ValueError: 
            raise ValueError("Invalid date format. Use DD.MM.YYYY") #Виводжу помилку
        



class Record: #Клас для зберігання інформації про контакт
    def __init__(self, name):
        self.name = Name(name) #Зберігаю обєкт імені
        self.phones = None #Список для телефонів
        self.birthday = None #День народження
        self.dictREC = {} #Вихідний словник
    
    def dict_record(self): #Метод для створення словника
        self.dictREC = {self.name.valName: {
            "phone": self.phones,
            "birthday": self.birthday
            }}
        return self.dictREC #Вертаю словник




def add_user_book(addUser, User_book): #Функція додавання користувача до UserDict
    u = "".join(addUser) #Додаю ім'я зі списку до рядка
    if u: #Роблю перевірку на пусте значення
        rec = Record(u) #Створюю об'єкт класу Record
        User_book.add_record(rec.dict_record()) # І записую в UserDict
        print(f"Сontact '{u}' added")
    else: print("!Add a username!") #Виводжу попередження що ім'я не введене


def add_phone_to_user(args, User_book): #Функція додавання до користувача телефону ([name, phone], dict)
    n, p = args #Розбиваю список
    p = Phone(p).phone_validation() #Зберігаю завалідований номер телефону
    if p != None: #Роблю перевірку на відсутність валідації
        User_book.update_user(n, {"phone": p}) #Оновлюю телефон користувача


def add_birthday_to_user(args, User_book): #Функція додавання до користувача дня народження (['name', 'birthday'], dict)
    try:
        n, b = args #Пробую розбити на список
        b = Birthday(b).birthday_validation() #Перезаписую ДН з валідацією
        User_book.update_user(n, {"birthday": b}) #Оновлюю ДН користувача в словнику
        
    except: print("Enter the command correctly \n->add-birthday [name] [birthday]") #Повертаю помилку


##
def save_data(book, filename): #Функція збереження словника
    with open(filename, "wb") as f: #Відкриваю файл
        pickle.dump(book, f) #Створюю новий файл або переписую існуючий
        print("Book is saved")

##
def load_data(filename): #Функція зчитування словника
    try: 
        with open(filename, "rb") as f: #Пробую відкрити файл
            return pickle.load(f) #Декодую файл
    except FileNotFoundError: #Якщо файл відсутній то створюю новий словник
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено



def parse_input(user_input): #Функція для парсингу команд
    cmd, *args = user_input.split() #Розбиваю команду
    cmd = cmd.strip().lower() #Записую команду в окрему змінну
    return cmd, *args #Повертаю команду і аргументи


lincFile = "addressbook.pkl" #Посилання на файл

'''Переписав функцію main() на match/case'''
def main(): #Основна функція з циклом 
    book = AddressBook() #Екземпляр класу AddressBook
    
    book.add_record(load_data(lincFile)) #Записую до книги декодовані дані з файлу
    
    print("Welcome to the assistant bot!")
    while True: #Основний цикл для постійного запиту команд
        user_input = input("Enter a command: ") #Запитую команду
        
        try: #Якщо є команда то виконую перевірки
            command, *args = parse_input(user_input) #Зберігаю результат парсингу в змінні 
        
            match command:
                case "close": #Команда для закриття книги
                    save_data(book, lincFile) #Зберігаю в файл .pkl книгу з користувачами
                    print("Good bye!")
                    break
                
                case "hello": #Привітання
                    print("Hello! \nHow can I help you?")
                    
                case "all": #Виводжу всі контакти з AddressBook
                    print(book.data)
                    
                case "add": #Додаю користувача до AddressBook
                    add_user_book(args, book)
                
                case "add-phone": #Додаю телефон до користувача
                    add_phone_to_user(args, book)
                
                case "phone": #Виводжу телефон користувача
                    up = "".join(args) #Додаю ім'я зі списку до рядка
                    print(book.find_data_user(up, "phone")) #Шукаю телефон користувача в книзі
                
                case "add-birthday": #Додаю день народження до користувача
                    add_birthday_to_user(args, book)
                
                case "show-birthday": #Виводжу день народження користувача
                    ub = "".join(args) #Додаю ім'я зі списку до рядка
                    print(book.find_data_user(ub, "birthday")) #Шукаю день народження користувача в книзі
                
                case "birthdays": #Виводжу дні народження користувачів на найближчий тиждень
                    print("Dictionary with greetings for the week: ", book.find_birthday_users_for_week())
                
                case "open-book": #Команда для відкриття книги в ручну
                    lb = "".join(args) #Додаю посилання на файл зі списку до рядка
                    book.add_record(load_data(lb)) #Записую до книги AddressBook декодовані дані з файлу
                    print("Book has been updated")
                
                case _: #Якщо команда не роспізнана
                    print("Invalid command!!!")
                
        except: print("Enter command...") #Якщо команда відсутня
        



if __name__ == "__main__":
    main()
