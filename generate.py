from train import NGram
from train import save_model
from train import load_model
import os.path


while True:
    print("Если вы хотите обучить модель на новых данных, введите '1'\n"
          "Если вы хотите сгенерировать текст на предобученной модели, введите '2'")
    first = input(">>> ")
    if first == "1":
        while True:
            print("Какой длинны Вы хотите n-граммы в своей модели? 1/2")
            second_1 = input(">>> ")
            if second_1 == "1":
                n = 1
                break
            elif second_1 == "2":
                n = 2
                break
            else:
                print("Вы ввели неккоректное значение n, введите 1 или 2")
        while True:
            print("Введите название .txt файла(без расширения) с текстом для обучения")
            name_train_file = input(">>> ")
            if os.path.exists(f'{name_train_file}.txt'):
                break
            else:
                print(
                    "Вы ввели неккоректное имя файла,\n"
                    " или такого файла не существует,\n"
                    "обратите внимание, что файл должен быть в той же папке что и данная программа\n"
                    "Название файла должно быть на английском языке")
        n_gr = NGram(n=n)
        data = n_gr.get_data(f'{name_train_file}.txt')
        n_gr.fit(data)
        n_gr.convert_data()
        n_gr.train()
        while True:
            print("Хотите ли вы сохранить свою обученную модель? y/n ")
            second_2 = input(">>> ")
            if second_2 == "y" or second_2 == "yes":
                s = True
                break
            elif second_2 == "n" or second_2 == "no":
                s = False
                break
            else:
                print("Вы ввели неккоректное значение,введите y(yes) или n(no)")
        if s:
            print("Введите название, под которым хотите сохранить данную модель")
            model_name = input(">>> ")
            save_model(n_gr, f"{model_name}")
        files = os.listdir()
        print("Список доступных моделей:")
        for f in files:
            if "." in f:
                if f.split(".")[1] == "pkl":
                    print(f.split(".")[0])
        while True:
            print("Введите название модели, которую хотите использовать")
            second_3 = input(">>> ")
            if second_3 + ".pkl" in files:
                model = load_model(f"{second_3}")
                break
            else:
                print("Вы ввели не верное название модели\n"
                      "введите название модели без .pkl")
                print("Список доступных моделей:")
                for f in files:
                    if "." in f:
                        if f.split(".")[1] == "pkl":
                            print(f.split(".")[0])
        while True:
            print("Введите длинну текста, который хотите сгенерировать")
            second_4 = input(">>> ")
            try:
                l = int(second_4)
                break
            except:
                print("Неверный формат вводы, Вы должны ввест число")
        while True:
            print(
                "Введите слово, с которго нужно начать генерацию, \n"
                "если ввести 'no', то генерация начнется со случайного слова из текста")
            second_5 = input(">>> ")
            if second_5 == "no":
                break
            else:
                if model.predict(second_5) == 'I do not know the given word or phrase':
                    print("Вы ввели слово, которого нет в обучающей выборке")
                else:
                    break
        if second_5 == "no":
            print(model.generating_text(length=l))
            break
        else:
            print(model.generating_text(prefix=second_5, length=l))
            break
    elif first == "2":
        files = os.listdir()
        print("Список доступных моделей:")
        for f in files:
            if "." in f:
                if f.split(".")[1] == "pkl":
                    print(f.split(".")[0])
        while True:
            print("Введите название модели, которую хотите использовать")
            second_3 = input(">>> ")
            if second_3 + ".pkl" in files:
                model = load_model(f"{second_3}")
                break
            else:
                print("Вы ввели не верное название модели\n"
                      "введите название модели без .pkl")
                print("Список доступных моделей:")
                for f in files:
                    if "." in f:
                        if f.split(".")[1] == "pkl":
                            print(f.split(".")[0])
        while True:
            print("Введите длинну текста, который хотите сгенерировать")
            second_4 = input(">>> ")
            try:
                l = int(second_4)
                break
            except:
                print("Неверный формат вводы, Вы должны ввест число")
        while True:
            print(
                "Введите слово, с которго нужно начать генерацию, \n"
                "если ввести 'no', то генерация начнется со случайного слова из текста:  ")
            second_5 = input(">>> ")
            if second_5 == "no":
                break
            else:
                if model.predict(second_5) == 'I do not know the given word or phrase':
                    print("Вы ввели слово, которого нет в обучающей выборке")
                else:
                    break
        if second_5 == "no":
            print(model.generating_text(length=l))
            break
        else:
            text = model.generating_text(prefix=second_5, length=l)
            print(text)
            break
    else:
        print("Неверный формат ввода, Вы должны ввести число")
