# === Импорт необходимых модулей ===


import numpy as np
import pandas as pd
from sys import exit
from pathlib import Path
from zipfile import ZipFile
from matplotlib import pyplot as plt
from scipy.signal import find_peaks, peak_prominences

# Надо будет тоже куда-нибудь в файл вывести?
devices = ['gydropribor', 'micsig', 'rigol-new', 'rigol-old', 'tektronix']

# === Классы ===


class Menu:

    def __init__(self):
        '''
        Инициализация меню

        Выводится строка приветствия и определяется словарь команд.

        '''
        print('Вас приветствует программа обработки csv-файлов "Вторник-21"!')
        print('\n', r'|_|_/######\_|_'*4, '|\n', sep='')
        # print('\n', r'__/----\__'*6, '\n', sep='')
        self.commands = {}

    def main(self):
        '''
        Главное меню

        Формируются список названий приборов согласно принятому
        формату таблицы и соответствующий ему словарь команд, где
        числовому ключу, совпадающему с номером в таблице, сопоставлен
        текст команды. Функция devices_mark() используется для
        для визуального представления того, файлы каких приборов
        имеются в наличии. Для выравнивания записей используется
        табуляция, добавляемая в потребном количестве в зависимости
        от длины названия прибора. Также в конец списка (и в словарь)
        команд) добавлены позиции all files и exit, позволяющие либо
        запустить цикл по полной обработке файлов, либо завершить
        работу программы соответственно.

        '''
        print('Обнаружены изображения и файлы данных со следующих',
              'осциллографов:')
        print('№', 'Name\t', 'Images', 'csv-files', sep='\t')
        devices_with_tabs = []
        for i, j in enumerate(devices):
            if len(j) <= 4:
                tabs = '\t\t'
            elif len(j) <= 8:
                tabs = '\t'
            else:
                tabs = ''
            devices_with_tabs.append(j + tabs)
            self.commands[i + 1] = 'self.device_csv_list(\'' + j + '\')'
        self.commands[i + 2] = 'all_files()'
        self.commands[i + 3] = 'exit()'
        csv_list = devices_mark(devices, devices_with_csv)
        img_list = devices_mark(devices, devices_with_img)
        for i, j in enumerate(devices_with_tabs):
            print(i + 1, j, img_list[i], csv_list[i], sep='\t')
        print(i + 2, 'all files', sep='\t')
        print(i + 3, 'exit', sep='\t')
        self.select()

    def device_csv_list(self, device):
        '''
        Построение списка csv-файлов конкретного прибора

        Parameters
        ----------
        device : Название прибора - ключ словаря, содержащего csv-файлы

        Получая на вход ключ словаря, метод выводит список csv-файлов,
        хранящийся в соответствующем его значении. В то же время
        формируется список команд, позволяющих запустить обработку
        одного файла. Также добавлены позиции all files и return в
        формируемую таблицу и соответствующие команды в список команд.

        '''
        print(device.capitalize())
        print('Список csv-файлов, записанных данным прибором:')
        print('№\tcsv-file')
        for i, j in enumerate(csv_files[device]):
            self.commands[i + 1] = 'csv_processing(\'' + j + '\')'  # Написать
            print(i + 1, j, sep='\t')
        print(i + 2, 'all files', sep='\t')
        print(i + 3, 'return', sep='\t')
        self.commands[i + 2] = 'all_files()'
        self.commands[i + 3] = 'self.main()'
        self.select()

    def confirm(self):
        '''
        Запрос подтверждения

        Returns
        -------
        bool
            Да (yes) = 1, нет (no) = 0.

        Метод возвращает 1 или 0 при вводе различных вариантов да/нет.

        '''
        tmp = input('Подтвердить выбор, д/н: ')
        if tmp in 'YesyesДада':
            return True
        if tmp in 'NonoНетнет':
            return False
        else:
            print('Неопознанная команда. Повторите ввод.')
            self.confirm()

    def select(self):
        '''
        Выбор команды из словаря и ее выполнение

        Использует сформированный предстоящим пунктом меню словарь
        команд, соответствующих нумерации выведенного на экран списка.
        При вводе действительного ключа исполняет соответствующее ему
        строковое значение посредством функции exec(), иначе выводит
        сообщение о неверном вводе и приглашает ввести команду вновь.

        '''
        try:
            command = int(input('Выберите соответствующий номер: '))
        except ValueError:
            print('Неопознанная команда. Повторите ввод.')
            self.select()
        else:
            if command in self.commands:
                print()
                exec(self.commands[command])
            else:
                print('Неопознанная команда. Повторите ввод.')
                self.select()


# === Функции ===


def open_cfg(file_name):
    '''
    Импорт данных файла конфигурации

    Parameters
    ----------
    file_name : Имя файла конфигурации
        (должен находиться в текущей директории).

    Returns
    -------
    config_dict : Словарь вида {'x_img':'./x/img', 'x.csv':'./x/csv'}.

    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        config_dict = {}
        while True:
            line = file.readline().strip('\n')
            if len(line) == 0:
                break
            if not line.startswith('#'):
                config_dict[line.split(' : ')[0]] = line.split(' : ')[1]
        return config_dict

# Функция импорта файла структуры файловой системы
#
# Строка под определением функции - строка документации. Именно она
# будет выводиться при использовании функции help.
# Функция открывает заданный файл, обрезает перенос строки и помещает
# в словарь не отмеченные # строки как ключ-значение.


def files_search(path, key, key_suffix, criteria):
    '''
    Функция построения отфильтрованного множества файлов

    Parameters
    ----------
    path : Путь, в котором осуществляется поиск файлов. Должен
        соответствовать значениям словаря конфигурации.
    key : Соответствующий ключ файла конфигурации.
    key_suffix : Окончание ключа. В конфигурационном файле опреледяет
        назначение каталога (find, img, csv, backup etc.)
    criteria : Критерий сортировки файлов методом glob.

    Returns
    -------
    files : Множество адресов файлов, соответствующих критерию. При
        отсутствии найденных файлов возвращается пустое множество.

    '''
    if Path(path).exists() and key.endswith(key_suffix):
        files = Path(path).glob(criteria)
        files = set(str(j) for j in files)
    else:
        files = set()
    return files

# Функция поиска файлов и создания множества их адресов
#
# Перебором по заданным значениям словаря конфигурации в работу
# принимаются только существующие каталоги, соответствующие ключу
# (предполагаются *_find, *_csv, *_img). Метод .glob выдает список
# файлов в каждом из каталогов, соответствующих критериям поиска.


def backup(files, location):
    '''
    Создание резервной копии файлов

    Parameters
    ----------
    files : Cписок подлежащих копированию файлов.
    location : Ключ для получения расположения создаваемого архива.

    Returns
    -------
    None.

    '''
    bkp_name = str(Path.cwd().stem) + ' - backup.zip'
    bkp_path = str(Path(location).joinpath(bkp_name))
    with ZipFile(bkp_path, 'a') as bkp:
        for i in files:
            bkp.write(i, Path(i).name)

# Функция создания резервной копии файлов
#
# Функция собирает имя zip-файла создаваемой резервной копии из
# названия родительского каталога (обычно являющего собой дату создания
# осциллограмм) и постфикса "-backup", названия и местоположения файлов
# функция получает на входе, местоположение создаваемого архива также
# задается. При записи файла в архив кортежем указывается адрес файла
# на ПК, а также адрес файла внутри архива. В объектах Path метод name
# выводит полное имя файла, stem - имя файла, suffix - его расширение,
# т.о. x.name == x.stem + x.suffix.


def transfer(files, location):
    '''
    Перенос файлов в местоположение, определенное файлом конфигурации.

    Parameters
    ----------
    files : Cписок подлежащих перемещению файлов.
    location : Ключ для получения необходимого нового расположения.

    Returns
    -------
    None.

    '''
    for i in files:
        i = Path(i)
        name = Path(i.name)
        path = Path(location)
        if not path.exists():
            path.mkdir()
        i.rename(path.joinpath(name))

# Функция переноса файлов
#
# Функция получает список файлов для переноса из списка, конечное
# положение файлов определяется файлом конфигурации. Создается каталог
# (если он уже не существует), выполняется перенос файлов по адресам,
# полученным путем объединения объектов WindowsPath - имени (из списка)
# и адреса (из файла конфигурации).


def devices_check(devices, existing_devices):
    '''
    Получение списка приборов, файлы которых имеются в наличии

    Parameters
    ----------
    devices : Массив названий приборов.
    existing_devices : Массив названий приборов, созданные которыми файлы
        присутствуют в рабочем каталоге (подкаталогах).

    Returns
    -------
    devices_checked : Расположенный в заданном порядке список названий
        приборов. При отсутствии файлов прибора вместо названия
        значится None.

    '''
    devices_checked = devices[:]
    for i, j in enumerate(devices_checked):
        if j not in existing_devices:
            devices_checked[i] = None
    return devices_checked

# Функция получения упорядоченного списка использованных приборов
#
# Функция проверяет каждое название в списке на наличие среди элементов
# соответствующего массива использованных приборов. При его отсутствии
# название заменяется на None.


def devices_mark(devices, existing_devices):
    '''
    Получения списка обозначений наличия и отсутствия файлов приборов

    Parameters
    ----------
    devices : Массив названий приборов.
    existing_devices : Массив названий приборов, созданные которыми файлы
        присутствуют в рабочем каталоге (подкаталогах).

    Returns
    -------
    devices_checked : Cписок строк, где __1__ указывает на наличие
    файлов, созданных соответствующим прибором, __0__ - на отсутствие.

    '''
    devices_checked = devices_check(devices, existing_devices)
    for i, j in enumerate(devices_checked):
        if j is not None:
            devices_checked[i] = '__1__'
        else:
            devices_checked[i] = '__0__'
    return devices_checked

# Функция маркировки наличия и отсутствия файлов приборов
#
# Использует функцию device_check() для проверки наличия файлов.
# Формирует список строк, где __1__ указывает на наличие файлов,
# созданных соответствующим прибором, __0__ - на их отсутствие.


def micsig_channel_unite(micsig_csv, micsig_one_channel_csv):
    '''
    Объединение csv-файлов двух каналов Micsig в один файл

    Parameters
    ----------
    micsig_csv : Расположение каталога с подлежащими объединению
        файлами.
    micsig_one_channel_csv : Расположение каталога, предназначенного
        для хранения csv-файлов в том виде, в котором они пребывали
        до объединения.

    Returns
    -------
    None.

    '''
    tmp = Path(dsc[micsig_csv]).glob('*.csv')
    csv_list = sorted([str(i) for i in tmp])
    for i in range(0, len(csv_list), 2):
        df1 = pd.read_csv(csv_list[i], index_col=False)
        try:
            df2 = pd.read_csv(csv_list[i + 1], index_col=False)
        except IndexError:
            break
        if len(df1.columns) < 7 and len(df1.columns) < 7:
            path = Path(dsc[micsig_one_channel_csv])
            if not path.exists():
                path.mkdir()
            path_1, path_2 = Path(csv_list[i]), Path(csv_list[i + 1])
            path_1.rename(path.joinpath(path_1.name))
            path_2.rename(path.joinpath(path_2.name))
            df = pd.concat([df1, df2], axis=1)
            df.to_csv(csv_list[i], index=False)

# Функция объединения csv-файлов двух каналов Micsig в один файл
#
# Формируется отсортированный список csv-файлов. Далее по этому списку
# с шагом в два проходит цикл, считывающий данные этих файлов в df
# Pandas. Путем ограничения количества столбцов проверяется, не
# являются ли файлы уже объединенными. Также конструкция обработки
# исключений останавливает работу цикла в случае нахождения в каталоге
# нечетного количества файлов(т.е. они уже объединены). В случае
# отсутствия создается каталог для размещения не объединенных файлов,
# после чего они переносятся в него. Далее происходит объединение df1 и
# df 2, результат которого записывается под именем первого файла.


def read_gydropribor(file):
    '''
    Чтение данных из csv-файла, сформированного прибором Gydropribor

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    time : Массив numpy, отображающий значения времени
    ch : Массив numpy, отображающий значения исследуемой величины.

    '''
    with open(file, 'r', encoding='utf-8') as file:
        test_string = '   '
        if file.readline()[:4] != test_string:
            print('Wrong .csv file structure.')
        else:
            df = pd.read_csv(file, index_col=False,
                             names=['t', 'ch'], skiprows=12, sep='\s+')
            time = df['t'].values
            ch = df['ch'].values
    return time, ch

# Чтение данных Gydropribor
#
# Данные в csv-файле представлены без использования специальных средств
# облегчения жизни, поэтому представляется возможным прямое чтение.


def read_micsig(file):
    '''
    Чтение данных из csv-файла, сформированного прибором Micsig

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    time : Массив numpy, отображающий значения времени
    ch : Массив numpy, отображающий значения исследуемой величины.

    '''
    with open(file, 'r', encoding='utf-8') as file:
        test_string = ('ProID,Info,Unnamed: 2,time,Vol.,Unnamed: 5,ProID,'
                       + 'Info,Unnamed: 2,time,Vol.,Unnamed: ')
        if file.readline()[:-2] != test_string:
            print('Wrong .csv file structure.')
        else:
            df = pd.read_csv(file, index_col=False, names=['t', 'ch'],
                             skiprows=13, usecols=[3, 4])
            time, ch = df['t'].values, df['ch'].values
            delay = np.loadtxt(file, delimiter=',', dtype='str',
                               skiprows=5, max_rows=1, usecols=1)
            delay = float(np.ndarray.item(delay).split(' ')[0])
            time = time - ((time[-1] - time[0])/2 - delay)
    return time, ch

# Чтение данных Micsig
#
# Происходит открытие текстового файла на чтение посредством функции
# with(), что позволяет быть уверенным в том, что файл будет закрыт
# независимо от результатов работы программы. Задается тестовая строка,
# уникальная для каждого осциллографа, и, посредством сравнения строки,
# считанной из файла, с ее образцом, происходит проверка правильности
# обрабатываемого файла во избежание дальнейших возможных ошибок.
# Функция считывает данные из файла посредством команды read_csv модуля
# Pandas, при этом указывается запрет на автоматическую индексацию,
# столбцам присваиваются имена, пропускается определенное число строк
# в начале документа и импорту подвергаются только указанные строки.
# Далее столбцы таблицы Pandas по их именам присваиваются переменным.
# После присвоения переменные содержат массивы NumPy со считанными из
# файла значениями. Из файла извлекается величина задержки, после чего
# подсчитывается действительное время, т.к. Miqsig записывает время
# относительно опорной точки (см. руководство к осциллографу).


def read_micsig_united(file):
    '''
    Чтение данных из csv-файла, сформированного прибором Micsig

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    time : Массив numpy, отображающий значения времени
    ch1 : Массив numpy, отображающий значения исследуемой величины №1.
    ch1 : Массив numpy, отображающий значения исследуемой величины №2.

    '''
    with open(file, 'r', encoding='utf-8') as file:
        test_string = ('ProID,Info,Unnamed: 2,time,Vol.,Unnamed: 5,ProID,'
                       + 'Info,Unnamed: 2,time,Vol.,Unnamed: ')
        if file.readline()[:-2] != test_string:
            print('Wrong .csv file structure.')
        else:
            df = pd.read_csv(file, index_col=False, names=['t', 'ch1', 'ch2'],
                             skiprows=13, usecols=[3, 4, 10])
            time = df['t'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
            delay = np.loadtxt(file, delimiter=',', dtype='str',
                               skiprows=5, max_rows=1, usecols=1)
            delay = float(np.ndarray.item(delay).split(' ')[0])
            time = time - ((time[-1] - time[0])/2 - delay)
    return time, ch1, ch2

# Чтение данных Micsig
#
# Отличия от предыдущей функции заключаются в том, что импортируются
# оба канала из объединенных заранее файлов (по умолчанию у Micsig
# раздельные файлы на каждый из каналов).


def read_rigol_new(file):
    '''
    Чтение данных из csv-файла, сформированного прибором Rigol (new)

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    time : Массив numpy, отображающий значения времени
    ch1 : Массив numpy, отображающий значения исследуемой величины №1.
    ch1 : Массив numpy, отображающий значения исследуемой величины №2.

    '''
    with open(file, 'r', encoding='utf-8') as file:
        test_string = 'X,CH1,CH2,Start,Increment'
        if file.readline()[:-2] != test_string:
            print('Wrong .csv file structure.')
        else:
            params = file.readline().strip()
            x_start = float(params.split(',')[3])
            x_step = float(params.split(',')[4])
            df = pd.read_csv(file, index_col=False,
                             names=['i', 'ch1', 'ch2'], skiprows=2)
            time = x_start + x_step*df['i'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
    return (time, ch1, ch2)

# Чтение данных Rigol (new)
#
# Время в файлах данного формата представлено в виде значений шага
# и стартового времени, т.е. показания представлены в виде трио номер-
# ch1-ch2. Для получения начала и шага считываем вторую строку. После
# значения времени вычисляем в соответствии с этими параметрами.


def read_rigol_old(file):
    '''
    Чтение данных из csv-файла, сформированного прибором Rigol (old)

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    time : Массив numpy, отображающий значения времени
    ch1 : Массив numpy, отображающий значения исследуемой величины №1.
    ch1 : Массив numpy, отображающий значения исследуемой величины №2.

    '''
    with open(file, 'r', encoding='utf-8') as file:
        test_string = 'Time,X(CH1),X(CH2)'
        if file.readline()[:-2] != test_string:
            print('Wrong .csv file structure.')
        else:
            df = pd.read_csv(file, index_col=False,
                             names=['t', 'ch1', 'ch2'], skiprows=2)
            time = df['t'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
    return (time, ch1, ch2)

# Чтение данных Rigol (old)
#
# Данные в csv-файле представлены без использования специальных средств
# облегчения жизни, поэтому представляется возможным прямое чтение.


def read_tektronix(file):
    '''
    Чтение данных из csv-файла, сформированного прибором Tektronix

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    time : Массив numpy, отображающий значения времени
    ch1 : Массив numpy, отображающий значения исследуемой величины №1.
    ch1 : Массив numpy, отображающий значения исследуемой величины №2.

    '''
    with open(file, 'r', encoding='utf-8') as file:
        test_string = 'Model,MSO46'
        if file.readline()[:-1] != test_string:
            print('Wrong .csv file structure.')
        else:
            df = pd.read_csv(file, index_col=False,
                             names=['t', 'ch1', 'ch2'], skiprows=12)
            time = df['t'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
    return (time, ch1, ch2)

# Чтение данных Tektronix
#
# Данные в csv-файле представлены без использования специальных средств
# облегчения жизни, поэтому представляется возможным прямое чтение.


def smooth(ch, window):
    '''
    Сглаживание методом скользящей средней

    Parameters
    ----------
    ch : Массив numpy с не сглаженными значениями величины.
    window : Ширина окна сглаживания.

    Returns
    -------
    ch : Массив numpy со сглаженными значениями величины.

    '''
    for i in range(window, ch.size - window):
        window_sum = 0
        for j in range(-window, window + 1):
            window_sum += ch[i + j]
        ch[i] = window_sum/(2*window + 1)
    return ch

# Функция сглаживания методом скользящей средней
#
# Функция находит среднее значение исследуемого сигнала на ширине окна
# и подставляет его вместо исходного. В процессе цикла функция проходит
# по всем точкам последовательности, не затрагивая только ограниченные
# участки в начале и в конце массива.


def time_shift_removal(time):
    '''
    Ликвидация сдвига по времени

    Parameters
    ----------
    time : Массив numpy, содержащий временной ряд.

    Returns
    -------
    time : Массив numpy, содержащий временной ряд, начинающийся с нуля.

    '''
    time_shift = time[0]
    time = time - time_shift
    return time

# Ликвидация смещения нуля по времени
#
# Функция определяет сдвиг по времени как значение первого элемента
# ряда и для каждого элемента производит вычитание этого значения.


def channel_shift_removal(ch, number):
    '''
    Ликвидация сдвига нуля исследуемой величины

    Parameters
    ----------
    ch : Массив numpy, содержащий значения исследуемой величины.
    number : Количество проходов по определению сдвига.

    Returns
    -------
    ch : Массив numpy, содержащий исправленный сигнал.

    '''
    shift = 0
    for i in range(number):
        # shift = (shift + ch[i])/2  # Старый вариант
        shift += ch[i]
    shift = shift/(number + 1)
    ch = ch - shift
    return ch

# Ликвидация сдвига нуля исследуемой величины
#
# Функция определяет значение сдвига как среднее первых number значений
# массива сигнала, после чего для каждого элемента производит вычитание
# этого значения.


def all_files():
    print('You lost all files.')

# === Обработка файлов ===


dsc = open_cfg('dsc.txt')
devices_with_csv, devices_with_img = set(), set()
for i, j in dsc.items():
    csv_files = files_search(j, i, 'find', '*.[tcb][xsi][tvn]')
    if csv_files:
        backup(csv_files, dsc[i.split('_')[0] + '_back'])
        transfer(csv_files, dsc[i.split('_')[0] + '_csv'])
    img_files = files_search(j, i, 'find', '*.[pjb][npm][ggp]')
    if img_files:
        backup(img_files, dsc[i.split('_')[0] + '_back'])
        transfer(img_files, dsc[i.split('_')[0] + '_img'])
micsig_channel_unite('micsig_csv', 'micsig_one_channel_csv')
csv_files, img_files = {}, {}
for i, j in dsc.items():
    if i.split('_')[0] not in csv_files.keys():
        csv_files[i.split('_')[0]] = set()
    csv_files[i.split('_')[0]] |= files_search(j, i, 'csv',  # txt, csv, bin
                                               '*.[tcb][xsi][tvn]')
    if csv_files[i.split('_')[0]]:
        devices_with_csv.add(i.split('_')[0])
    if i.split('_')[0] not in img_files.keys():
        img_files[i.split('_')[0]] = set()
    img_files[i.split('_')[0]] |= files_search(j, i, 'img',  # png, jpg, bmp
                                               '*.[pjb][npm][ggp]')
    if img_files[i.split('_')[0]]:
        devices_with_img.add(i.split('_')[0])
# devices_with_csv = sorted([i for i in devices_with_csv])
# devices_with_img = sorted([i for i in devices_with_img])

# В программу вносится словарь, определяющий структуру файловой
# системы. Определяются множества, в которые будут собираться названия
# приборов, файлы данных которых присутствуют в соответствующих
# подкаталогах. Множества необходимы для того, чтобы отсечь
# повторяющиеся названия. Функция files_searsh() выдает список файлов,
# соответствующих критериям поиска, при этом поиск производится в
# каталогах, определенных словарем конфигурации. По полученному
# множеству строк-адресов проводятся операции резервного копирования и
# переноса файлов. Навигация по ключам словаря структуры файловой
# системы производится путем получения имени прибора отсечением
# постфикса (dsc[i.split('_')[0]) и добавлением нового.
# Эти операции производятся для csv и img файлов. Также производится
# объединение файлов каналов осциллографа Micsig. После происходит
# повторный поиск файлов уже в тех каталогах, куда они должны были
# быть пересены, их адреса собираются в словари, в которых ключом
# является название прибора, значением - множество файлов.

menu = Menu()
menu.main()




__version__ = '0.6'
