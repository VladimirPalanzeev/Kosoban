from tkinter import *
from time import sleep

# * ** ** ** ** ** ** ** ** ** *
# ===== Функции и методы
# * ** ** ** ** ** ** ** ** ** *

# При нажатии на кнопку "Продолжить"
def nextLevelSet(btnNext: Button):
    global level
    level += 1

    # Устанавливаем "фокус внимания" на Canvas для того, чтобы работали кнопки
    cnv.focus_set()

    # Удаляем кнопку продолжить
    btnNext.destroy()
    # Возвращаем в область видимости Button
    #btnCheat.place(x=10, y=590)
    btnReset.place(x=10, y=550)
    # Очищаем Canvas
    cnv.delete(ALL)
    reset()

# Переключение на следующий уровень в случае победы
def nextLevel():
    print("Метод nextLevel()")
    # Удаляем ВСЕ объекты с Canvas
    cnv.delete(ALL)
    # Останавливаем таймер
    stopTimer()

    # Убираем из зоны видимости кнопки, чтобы пользователь не мог их нажимать
   # btnCheat.place(x=-100, y=-100)
    btnReset.place(x=-100, y=-100)

    # Создаем кнопку "Продолжить". Удалять её, освобождая память будем каждый раз после нажатия в методе nextLevelSet
    btnNext = Button(text="Продолжить", font="Verdana, 19", width=45)
    btnNext.place(x=300, y=550)
    btnNext.focus_set()
    btnNext["command"] = lambda b=btnNext : nextLevelSet(b)

    # По умолчанию центр координат находится в центре надписи
    cnv.create_text(WIDTH * SQUARE_SIZE // 2, 200, fill="#aaffcc",
                    text=f"Победа! Вы собрали головоломку за {getMinSec(second)}! Поздравляем!",
                    font="Verdana, 25")



# Останавливаем таймер: прекращаем отсчёт времени
def stopTimer():
    global timeRun
    if timeRun != None:
        root.after_cancel(timeRun)

        # Убираем маркер работы таймера
        timeRun = None

# Возвращаем строку в виде ММ:СС
def getMinSec(s):
    # Находим минуты
    intMin = s // 60
    # Находим секунды
    intSec = s % 60
    textSecond = str(intSec)

    # Сбрасываем минуты, если прошло больше 59 (чтобы не вводить часы)
    if intMin > 59:
        intMin % 60

    # Добавляем лидирующий 0 если секунд меньше 10
    if intSec < 10:
        textSecond = "0" + textSecond

    if intMin == 0:
        return f"{textSecond} сек."
    else:
        textMin = str(intMin)
        if intMin < 10:
            textMin = "0" + textMin
        return f"{textMin} мин. {textSecond} сек."


# Обновляем полоску с текстом вверху
def updateText():
    global textTime, second, timeRun

    # Увеличиваем количество секунд
    second += 1
    # Удаляем предыдущую надпись
    cnv.delete(textTime)

    # формируем строку для вывода
    txt =  f"Уровень: {level}   Прошло времени: {getMinSec(second)}"

    # Создаем переменную для таймера
    textTime = cnv.create_text(10, 10, fill="#ffcaab", anchor="nw", text=txt, font="Verlana, 15")

    # Вешаем на timeRun вызов метода каждую секунду
    timeRun = root.after(1000, updateText)

# Читерская кнопка "Установить ящики"
def goCheat():
    global moving
    print("Метод goCheat()")
    moving = True
    # Просто устанавливаем все ящики на нужные места и перерисовываем изображения
    for i in range(len(boxes)):
        boxes[i][0] = finish[i][0]
        boxes[i][1] = finish[i][1]
        cnv.coords(boxes[i][2], SQUARE_SIZE // 2 + boxes[i][1] * SQUARE_SIZE,
                   SQUARE_SIZE // 2 + boxes[i][0] * SQUARE_SIZE)
    cnv.update()

    # Поставил паузу в 2 сек
    sleep(2)

    # Запускаем метод проверки все ли ящики находятся на своих местах
    checkBoxInFinish()

# Проверка "находятся ли ящики на своих местах"
def checkBoxInFinish():
    global finish, win
    print("Метод checkBoxInFinish()")

    # Сначала сбрасываем параметр в списке мест для сбора отвечающий на вопрос "Ящик на месте?"
    for fin in finish:
        fin[3] = False

    # Предполагаем сто пользователь собрал ящики и пытаемся доказать обратное
    win = True
    fin = 0
    while fin < len(finish) and win:
        box = 0
        while box < len(boxes):
            if finish[fin][0:2] == boxes[box][0:2]:
                finish[fin][3] = True
                box = len(boxes)
            box += 1
        win = win and finish[fin][3]
        fin += 1

    # Если всё же победа, то...
    if win:
        nextLevel()



# Перемещение коробки и игрока
def movePlayerBoxTo(x, y, count, numberBox):
    global moving
    count -= 1
    # .move перемещает объект Canvas на заданные значения x и y в пикселях
    cnv.move(player[2], x, y)
    cnv.move(boxes[numberBox][2], x, y)

    if count > 0:
        moving = True
        # Задаем анимацию с интервалом в 20 миллисекунд
        root.after(20, lambda x=x, y=y, c=count, n=numberBox: movePlayerBoxTo(x, y, c, n))
    else:
        print("Метод movePlayerBoxTo() выполнился")

        # Перемещение закончилось, можно "активировать" реакцию программы на нажатие клавиш клавиатуры
        moving = False

        # Обязательно проверяем: собраны ли ящики
        checkBoxInFinish()



# Перемещение игрока
def movePlayerTo(x, y, count):
    global moving
    count -= 1
    # Перемещение игрок БЕЗ ящика
    cnv.move(player[2], x, y)
    # Продолжаем пока не переместим на нужное расстояние
    if count > 0:
        moving = True
        # Задаем анимацию с интервалом в 20 миллисекунд
        root.after(20, lambda x=x, y=y, c=count: movePlayerTo(x, y, c))
    else:
        print("Метод movePlayerTo() выполнился")
        # Перемещение закончилось, можно "активировать" реакцию программы на нажатие клавиш клавиатуры
        moving = False



# Получаем номер ящика, расположенного по координатам x, y
def getBox(x, y):
    print("Метод getBox()")
    for i in range(len(boxes)):
        if boxes[i][0] == x and boxes[i][1] == y:
            return i
    return None


# Получаем номер объекта, расположенного в позиции x, y. Это либо ящик (2), либо стена (1) или пустое место(0)
def getNumber(x, y):
    print("Метод getNumber()")
    for box in boxes:
        if box[0] == x and box[1] == y:
            return 2
    if dataLevel[x][y] <= 1:
        return dataLevel[x][y]



# Рассчитываем перемещение погрузчика, метод вызывается при нажатии на стрелки
def move (v):
    print("Метод move()")
    # Если выполняется анимация, то прерывать метод
    if moving:
        return 0
    # Удаляем изображение игрока
    cnv.delete(player[2])
    # ... и тут же создаем его повернутым ч сторону v
    player[2] = cnv.create_image(SQUARE_SIZE // 2 + player[1] * SQUARE_SIZE,
                                 SQUARE_SIZE // 2 + player[0] * SQUARE_SIZE,
                                 image=img[3][v])
    # Забираем координаты в x, y для удобства написания кода
    x = player[0]
    y = player[1]

    # Вверх
    if v == UPKEY:
        # Получаем номер объекта сверху
        check = getNumber(x - 1, y)
        # Если это пусто место или место сбора ящиков, то двигаемся
        if check == 0:
            movePlayerTo(0, - 8, 8)
            # Обязательно изменяем координаты игрока
            player[0] -= 1
        # Если впереди ящик,...
        elif check == 2:
            # ... то получаем номер клетки, в которую нужно передвинуть ящик и ...
            nextCheck = getNumber(x - 2, y)
            # ... если клетка пустая, то перемещаем ящик и погрузчик
            if nextCheck == 0:
                numberBox = getBox(x - 1, y)
                # Отправляем координаты смещения и номер ящика
                movePlayerBoxTo(0, - 8, 8, numberBox)
                # Обязательно изменяем координаты игрока
                player[0] -= 1
                # и ящика
                boxes[numberBox][0] -= 1


    # ВНИЗ
    elif v == DOWNKEY:
        check = getNumber(x + 1, y)
        if check == 0:
            movePlayerTo(0, 8, 8)
            player[0] += 1
        elif check == 2:
            nextCheck = getNumber(x + 2, y)
            if nextCheck == 0:
                numberBox =getBox(x + 1, y)
                movePlayerBoxTo(0, 8, 8, numberBox)
                player[0] += 1
                boxes[numberBox][0] += 1

    # ВЛЕВО
    elif v == LEFTKEY:
        check = getNumber(x, y - 1)
        if check == 0:
            movePlayerTo(-8, 0, 8)
            player[1] -= 1
        elif check == 2:
            nextCheck = getNumber(x, y - 2)
            if nextCheck == 0:
                numberBox = getBox(x, y - 1)
                movePlayerBoxTo(-8, 0, 8, numberBox)
                player[1] -= 1
                boxes[numberBox][1] -= 1

    # ВПРАВО
    elif v == RIGHTKEY:
        check = getNumber(x, y + 1)
        if check == 0:
            movePlayerTo(8, 0, 8)
            player[1] += 1
        elif check == 2:
            nextCheck = getNumber(x, y + 2)
            if nextCheck == 0:
                numberBox = getBox(x, y + 1)
                movePlayerBoxTo(8, 0, 8, numberBox)
                player[1] += 1
                boxes[numberBox][1] += 1


# Создание объектов Canvas: формируем изображение позиции
def createLevel():
    print("Метод createLevel()")
    global player, boxes, finish
    player = []
    boxes = []
    finish = []

    # Рисуем нижний слой кирпичные стены и места для сбора
    for i in range(len(dataLevel)):
        for j in range(len(dataLevel[i])):
            if dataLevel[i][j] == 1:
                cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                 SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                 image=img[0])
            elif dataLevel[i][j] == 3:
                dataLevel[i][j] = 0
                finish.append([i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                                      SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                                      image=img[2]),
                               False])

    # Данные списка finish[a, b, c, d]:
    # a - координата по x относительно математической модели 20x10
    # b - координата по y -||-
    # c - объект image на Canvas (изображение зеленой точки)
    # d - признак True - есть ящик на этой клетке, False - нет

    # Рисуем верхний слой: ящики и игрока
    for i in range(len(dataLevel)):
        for j in range(len(dataLevel[i])):
            if dataLevel[i][j] == 2:
                dataLevel[i][j] = 0
                boxes.append([i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                                      SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                                      image=img[1])])
            # Данные списка boxes[a, b, c]:
            # a - координата по x относительно математической модели 20x10
            # b - координата по y -||-
            # c - объект image на Canvas (изображение ящика)

            elif dataLevel[i][j] == 4:
                dataLevel[i][j] = 0
                player = [i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                                      SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                                      image=img[3][1])]
            # Данные списка player[a, b, c]:
            # a - координата по x относительно математической модели 20x10
            # b - координата по y -||-
            # c - объект image на Canvas (изображение погрузчика)


# Загрузка данных уровня
def getLevel(lvl):
    global dataLevel
    print("Метод getLevel")
    dataLevel = []
    tmp = []

    # Формируем индекс к имени файла
    idx = str(lvl)
    if lvl < 10:
        idx = f"0{lvl}"

    try:
        f = open(f"levels/level{idx}.dat", "r", encoding="utf-8")
        for i in f.readlines():
            tmp.append(i.replace("\n", ""))
        f.close()
        # Перегоняем в двумерный список с числами
        for i in range(len(tmp)):
            dataLevel.append([])
            for j in tmp[i]:
                dataLevel[i].append(int(j))
    except:
        print("Не найден файл с данными.")
        quit(0)



# Замостить изображением grass.png всю область окна. Метод нужно вызывать самым первым при формировании изображения
# окна, чтобы "трава" легла нижним слоем
def clear_setGrass():
    print("Метод clear_setGrass()")
    cnv.delete(ALL)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            cnv.create_image(SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                             SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                             image=backGround)


# Сброс и пересоздание уровня
def reset():
    global moving, second, timeRun
    print("Метод reset()")
    moving = False
    second = -1

    # Останавливаем таймер
    stopTimer()

    # Загружаем данные
    getLevel(level)

    # Очищаем экран устанавливая фон
    clear_setGrass()

    # Создаём уровень
    createLevel()

    # Запускаем таймер
    updateText()




# * ** ** ** ** ** ** ** ** ** *
# ===== Основной блок
# * ** ** ** ** ** ** ** ** ** *

# Создание окна
root = Tk()
root.resizable(False, False)
root.title("Кособан")
root.iconbitmap("icon/icon.ico")

# Количество плиток по ширине и высоте
WIDTH = 20
HEIGHT = 10

# Размер одной плитки
SQUARE_SIZE = 64

# Установка геометрии окна
POS_X = root.winfo_screenwidth() // 2 - (WIDTH * SQUARE_SIZE) // 2
POS_Y = root.winfo_screenheight() // 2 - (HEIGHT * SQUARE_SIZE) // 2
root.geometry(f"{WIDTH * SQUARE_SIZE + 0}x{HEIGHT * SQUARE_SIZE + 0}+{POS_X}+{POS_Y}")

# Константы-коды для направления движения
UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

# КАНВАС
cnv = Canvas(root, width=WIDTH * SQUARE_SIZE, height=HEIGHT * SQUARE_SIZE, bg="#373737")
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

# Назначаем клавиши управления курсором
cnv.bind("<Up>", lambda e, x=UPKEY: move(x))
cnv.bind("<Down>", lambda e, x=DOWNKEY: move(x))
cnv.bind("<Left>", lambda e, x=LEFTKEY: move(x))
cnv.bind("<Right>", lambda e, x=RIGHTKEY: move(x))

# Выполняется ли анимация? Если True, то метод move(x) выполняться не будет
moving = True

# Текстура "травы", фона
backGround = PhotoImage(file="image/grass.png")

# Список для хранения изображений
img = []
img.append(PhotoImage(file="image/wall.png"))        # Стена
img.append(PhotoImage(file="image/box.png"))         # Ящик
img.append(PhotoImage(file="image/finish.png"))      # Место сбора
img.append([])
img[3].append(PhotoImage(file="image/kosoban_up.png"))        # Погрузчик вверх
img[3].append(PhotoImage(file="image/kosoban_down.png"))      # Погрузчик вниз
img[3].append(PhotoImage(file="image/kosoban_left.png"))      # Погрузчик вправо
img[3].append(PhotoImage(file="image/kosoban_right.png"))     # Погрузчик влево

# Объект(список) игрок
player = None
# Ящики (список)
boxes = None
# Места для ящиков (список)
finish = None
# Победа?
win = False

# Восстановление игрового поля на начальную стадию
btnReset = Button(text="Сбросить поле".upper(),
                  font=("Consolas", "15"),
                  width=20)
btnReset.place(x=10, y=550)

# Просто вызываем пересоздание уровня
btnReset["command"] = reset

# Кнопка-чит
#btnCheat = Button(text="Установить ящики".upper(), font=("Consolas", "15"),width=20)
#btnCheat.place(x=10, y=590)
#btnCheat["command"] = goCheat

# Текстовая строка, показывающая время
textTime = None
# Прошедшее время
second = None

# Уровень
level = 1
# Данные об игровом поле загружаются из файла
dataLevel = []

# Переменная для таймера. Необходима, чтобы останавливать работу root.after()
timeRun = None

# Создаем уровень
reset()

root.mainloop()
