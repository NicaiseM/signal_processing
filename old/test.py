# === Импорт необходимых модулей ===

import time
import pickle
import numpy as np
import pandas as pd
from sys import exit
from pathlib import Path
from zipfile import ZipFile
from metric import metric as mt
from matplotlib import pyplot as plt
from scipy.signal import find_peaks as fp


# === Классы ===

class Menu:

    def __init__(self):
        '''
        Инициализация меню

        Выводится строка приветствия, определяется словарь команд b
        переменные класса, хранящие значения выбранных прибора и файла.

        '''
        print('Вас приветствует программа обработки csv-файлов "Вторник-21"!')
        print('\n', r'|_|_/######\_|_'*4, '|\n', sep='')
        # print('\n', r'__/----\__'*6, '\n', sep='')
        self.commands = {}
        self.device = 'All'
        self.csv = 'All'

    def main(self):
        '''
        Главное меню

        Переменные класса прибора и файла возвращаются в исходное.
        Формируются список названий приборов согласно принятому
        формату таблицы и соответствующий ему словарь команд, где
        числовому ключу, совпадающему с номером в таблице, сопоставлен
        текст команды. Команды выбора прибора состоят из определения
        названия прибора в переменную и собственно команды построения
        списка csv-файлов. Функция devices_mark() используется
        для визуального представления того, файлы каких приборов
        имеются в наличии. Выравнивание столбцов в таблице происходит
        с использованием функции tabulate(), объединяющей заголовок и
        элементы столбца в один массив, в котором необходимое число \t
        Проставляется согласно максимальной длине строки-заголовка или
        строки-элемента. Нулевой индекс enumerate() не отображается,
        т.к. при i = 0 на экран выходит строка-заголовок, поэтому
        команды и записи начинаются с i = 1. Массивы ppc['devices'] и
        devices_mark(ppc['devices'], devices_with_csv / img) имеют
        меньшее количество элементов, т.к. не имеют заголовка.Также
        в конец списка (и в словарь команд) добавлены позиции all files
        и exit, позволяющие либо запустить цикл по полной обработке
        файлов, либо завершить работу программы соответственно.

        '''
        self.device = 'All'
        self.csv = 'All'
        csv_list = ['title'] + devices_mark(ppc['devices'], devices_with_csv)
        img_list = ['title'] + devices_mark(ppc['devices'], devices_with_img)
        print('Обнаружены изображения и файлы данных со следующих',
              'осциллографов:')
        head = ['Name', 'Images', 'csv-files']
        for i, (j, k) in enumerate(zip(['title'] + ppc['devices'],
                                   tabulate(head[0], ppc['devices']))):
            if i == 0:
                print('№', k[:-1], head[1], head[2], sep='\t')
            else:
                print(i, k[:-1], img_list[i], csv_list[i], sep='\t')
                self.commands[i] = ('self.device = \'' + j
                                    + '\'; self.device_csv_list()')
        self.commands[i + 1] = 'all_files()'  # НАПИСАТЬ!
        self.commands[i + 2] = 'exit()'
        print(i + 1, 'all files', sep='\t')
        print(i + 2, 'exit', sep='\t')
        self.select()

    def device_csv_list(self):
        '''
        Построение списка csv-файлов конкретного прибора

        Метод выводит список csv-файлов, соответствующих выбранному
        прибору, а также формируется список команд, определяющих
        выбранный файл в переменную класса и запускающих обработку
        одного файла. Также добавлены позиции all files и return в
        формируемую таблицу и соответствующие команды в список команд.
        Метод self.select() запускается с переключателем True, что
        требует показ списка установленных параметров перед обработкой.

        '''
        print(self.device.capitalize())
        print('Список csv-файлов, записанных данным прибором:')
        print('№\tcsv-file')
        for i, j in enumerate(csv_files[self.device]):
            self.commands[i + 1] = ('self.csv = \'' + j
                                    + '\'; csv_processing(menu.csv)')  # НАПИСАТЬ!
            print(i + 1, j, sep='\t')
        print(i + 2, 'all files', sep='\t')
        print(i + 3, 'return', sep='\t')
        self.commands[i + 2] = 'all_files()'  # НАПИСАТЬ!
        self.commands[i + 3] = 'self.main()'
        self.select(True)
# Здесь надо ИСПРАВИТЬ. Вызывает показ опций и подтверждение даже при
# возврате в предыдущее меню.

    def options(self):
        '''
        Вывод списка используемых параметров обработки

        Метод получает список параметров обработки из словаря ppc,
        который, в свою очередь, загружается из внешнего файла, выводит
        этот список и запрашивает подтверждение на исполнение через
        метод self.confirm(). Если подтверждение получено, то метод
        просто заканчивает свою работу, позволяя дальнейшую обработку
        посредством self.select(), иначе происходит возврат в последнее
        меню. При построении списка используется функция tabulate(),
        выравнивающая столбцы посредством табуляции.

        '''
        print('Установлены следующие параметры обработки:')
        print('Common')
        head = ['Параметр', 'Значение', 'Описание']
        for i, j, k in zip(
                tabulate(head[0], ppc['common'].keys()),
                tabulate(head[1], [i for i, j in ppc['common'].values()]),
                tabulate(head[2], [j for i, j in ppc['common'].values()])):
            print(i, j, k, sep='')
        print(self.device.capitalize())
        for i, j, k in zip(
                tabulate(head[0], ppc[self.device].keys()),
                tabulate(head[1], [i for i, j in ppc[self.device].values()]),
                tabulate(head[2], [j for i, j in ppc[self.device].values()])):
            print(i, j, k, sep='')
        if not self.confirm():
            if self.device != 'All':
                self.device_csv_list()
            else:
                self.main()

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

    def select(self, show_options=False):
        '''
        Выбор команды из словаря и ее выполнение

        Parameters
        ----------
        show_options: Управление отображением параметров. = False.

        Использует сформированный предстоящим пунктом меню словарь
        команд, соответствующих нумерации выведенного на экран списка.
        При вводе действительного ключа исполняет соответствующее ему
        строковое значение посредством функции exec(), иначе выводит
        сообщение о неверном вводе и приглашает ввести команду вновь.
        Если запрошен с истинным параметром show_options и командой
        [:-1] (т.е. не all() и не exit()), то должен выполнить метод
        self.options() перед продолжением.

        '''
        try:
            command = int(input('Выберите соответствующий номер: '))
        except ValueError:
            print('Неопознанная команда. Повторите ввод.\n')
            self.select()
        else:
            if command in self.commands:
                print()
                if show_options and command < len(self.commands) - 1:
                    self.options()
                exec(self.commands[command])
            else:
                print('Неопознанная команда. Повторите ввод.\n')
                self.select()


# === Функции ===

def tabulate(head, names):
    '''
    Создание выровненного списка-столбца для меню

    Parameters
    ----------
    head : Строка-заголовок.
    names : Список элементов меню.

    Returns
    -------
    column_with_tabs : Лист заголовка и элементов с табуляцией.

    Вычисляет наибольшую длину заголовка / элемента среди принятых,
    переводит длины в количество табуляций (\t = 4 знака), добавляет
    \t в необходимом для выравнивания количестве в конец заголовка и
    каждого из элементов.

    '''
    names_with_tabs = []
    head_with_tabs = head
    len_max = 0
    for i in names:
        if len_max < len(i):
            len_max = len(i)
    len_max = len_max//4 + 1
    len_head = len(head)//4 + 1
    if len_head > len_max:
        tabs_amount = len_head + 1
    else:
        tabs_amount = len_max + 1
    head_with_tabs = head + (tabs_amount - len_head)*'\t'
    for i in names:
        tabs_count = tabs_amount - (len(i)//4 + 1)
        names_with_tabs.append(i + tabs_count*'\t')
    column_with_tabs = [head_with_tabs] + names_with_tabs
    return column_with_tabs


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

    Строка под определением функции - строка документации. Именно она
    будет выводиться при использовании функции help. Функция открывает
    заданный файл, обрезает перенос строки и убирает комментарии, после
    чего помещает в словарь (либо в подсловарь, если встречает ключевое
    слово; запись в подсловарь прекращается при получении ключевого
    слова окончания, при этом подсловарь помещается в основной словарь)
    строки как ключ-значение, значение может быть списком, состоящим
    из собственно значения параметра и пояснения к нему.

    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        subdict_generation = False
        config_dict = {}
        while True:
            line = file.readline().strip('\n').strip('\r')
            if len(line) == 0:
                break
            if line.startswith('#'):
                continue
            if '#' in line:
                line = line.split('#')[0].strip()
            if line.startswith('|=begin=|'):
                subdict_generation = True
                subdict_name = line.split('=|=')[1].strip('=|')
                subdict = {}
                continue
            if line == '|=end=|':
                subdict_generation = False
                config_dict[subdict_name] = subdict
                continue
            if subdict_generation:
                key = line.split(': ')[0]
                subdict[key] = line.split(': ')[1]
                subdict[key] = [i for i in subdict[key].split(' - ')]
                subdict[key][0] = subdict[key][0].strip()
            else:
                config_dict[line.split(': ')[0]] = line.split(': ')[1]
    if 'devices' in config_dict:
        config_dict['devices'] = [i for i in config_dict['devices'].split('|')]
    return config_dict


def settings_declatation(settings_dict, device):
    '''
    Создание словаря настроек для обработки показаний прибора

    Parameters
    ----------
    settings_dict : Общий словарь параметров обработки данных.
    device : Название прибора.

    Returns
    -------
    settings : Словарь настроек обработки данных отдельного прибора.

    Принимая на вход общий словарь конфигурации обработки данных и
    название устройства, функция возвращает словарь, составленный из
    общих настроек и настроек, уникальных для данного прибора. Сделано
    это для удобства обращения к словарю настроек, которое заключается
    в использовании одинаковых ключей при обращении к схожим настройкам
    разных устройств, имеющих разные значения соответственно. Функция
    создает новый словарь, копирует в него общие настройки, после чего
    дополняет частными настройками прибора. Затем, по циклу, считанные
    из текстового файла строки преобразуются в элементы двоичной
    логики, значения метрических множителей приводятся в целочисленный
    вид, производится попытка преобразования подходящих строк в числа с
    плавающей запятой, после чего преобразованные значения записываются
    в чистовой словарь, который функция и возвращает.
    '''
    settings = {}
    settings_tmp = settings_dict['common'].copy()
    settings_tmp.update(settings_dict[device])
    for key, value in settings_tmp.items():
        if value[0] == 'True':
            value[0] = True
        elif value[0] == 'False':
            value[0] = False
        else:
            if key == 't_unit' or key == 'ch_unit':
                value[0] = int(value[0])
            try:
                value[0] = float(value[0])
            except ValueError:
                pass
        settings[key] = value[0]
    return settings


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

    Перебором по заданным значениям словаря конфигурации в работу
    принимаются только существующие каталоги, соответствующие ключу
    (предполагаются *_find, *_csv, *_img). Метод.glob выдает список
    файлов в каждом из каталогов, соответствующих критериям поиска.

    '''
    if Path(path).exists() and key.endswith(key_suffix):
        files = Path(path).glob(criteria)
        files = set(str(j) for j in files)
    else:
        files = set()
    return files


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

    Функция собирает имя zip-файла создаваемой резервной копии из
    названия родительского каталога (обычно являющего собой дату
    создания осциллограмм) и постфикса "-backup", названия и
    местоположения файлов функция получает на входе, местоположение
    создаваемого архива также задается. При записи файла в архив
    кортежем указывается адрес файла на ПК, а также адрес файла внутри
    архива. В объектах Path метод name выводит полное имя файла, stem -
    имя файла, suffix - его расширение, x.name == x.stem + x.suffix.

    '''
    bkp_name = str(Path.cwd().stem) + ' - backup.zip'
    bkp_path = str(Path(location).joinpath(bkp_name))
    with ZipFile(bkp_path, 'a') as bkp:
        for i in files:
            bkp.write(i, Path(i).name)


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

    Функция получает список файлов для переноса из списка, конечное
    положение файлов определяется файлом конфигурации. Создается
    каталог (если он уже не существует), выполняется перенос файлов по
    адресам, полученным путем объединения объектов WindowsPath - имени
    (из списка) и адреса (из файла конфигурации).

    '''
    for i in files:
        i = Path(i)
        name = Path(i.name)
        path = Path(location)
        if not path.exists():
            path.mkdir()
        i.rename(path.joinpath(name))


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

    Функция проверяет каждое название в списке на наличие среди
    элементов соответствующего массива использованных приборов. При его
    отсутствии название заменяется на None.

    '''
    devices_checked = devices[:]
    for i, j in enumerate(devices_checked):
        if j not in existing_devices:
            devices_checked[i] = None
    return devices_checked


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

    Использует функцию device_check() для проверки наличия файлов.
    Формирует список строк, где __1__ указывает на наличие файлов,
    созданных соответствующим прибором, __0__ - на их отсутствие.

    '''
    devices_checked = devices_check(devices, existing_devices)
    for i, j in enumerate(devices_checked):
        if j is not None:
            devices_checked[i] = '__1__'
        else:
            devices_checked[i] = '__0__'
    return devices_checked


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

    Формируется отсортированный список csv-файлов. Далее по этому
    списку с шагом в два проходит цикл, считывающий данные этих файлов
    в df Pandas. Путем ограничения количества столбцов проверяется, не
    являются ли файлы уже объединенными. Также конструкция обработки
    исключений останавливает работу цикла в случае нахождения в
    каталоге нечетного количества файлов(т.е. они уже объединены). В
    случае отсутствия создается каталог для размещения не объединенных
    файлов, после чего они переносятся в него. Далее происходит
    объединение df1 и df 2, результат которого записывается под именем
    первого файла.
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


def read(file):
    '''
    Чтение данных из csv-файла

    Parameters
    ----------
    file: Адрес обрабатываемого файла.

    Returns
    -------
    device : Название использованного прибора.
    time : Массив numpy, отображающий значения времени
    ch1 : Массив numpy, отображающий значения исследуемой величины №1.
    optional
    ch2 : Массив numpy, отображающий значения исследуемой величины №2.

    Первая и вторая строки каждого файла схраняются. Первая строка
    будет уникальной для каждого осциллографа, и, посредством сравнения
    строки, считанной из файла, с ее образцом, происходит определение
    прибора, сформировавшего обрабатываемый файл. Далее в зависимости
    от прибора происходит открытие текстового файла на чтение
    посредством функции with(), что позволяет быть уверенным в том, что
    файл будет закрыт независимо от результатов работы программы.
    После чего функция считывает данные из файла посредством команды
    read_csv модуля Pandas, при этом указывается запрет на
    автоматическую индексацию, столбцам присваиваются имена,
    пропускается определенное число строк в начале документа и импорту
    подвергаются только указанные строки. Также для осциллографа Rigol
    (new) требуются дополнительные параметры времени. Время в файлах
    данного формата представлено в виде значений шага и стартового
    времени, т.е. показания представлены в виде трио номер- ch1-ch2.
    Для получения начала и шага считываем вторую строку. После значения
    времени вычисляем в соответствии с этими параметрами. Далее столбцы
    таблицы Pandas по их именам присваиваются переменным. После
    присвоения переменные содержат массивы NumPy со считанными из файла
    значениями. Для Micsig из файла извлекается величина задержки,
    после чего подсчитывается настоящее время, т.к. Miqsig записывает
    время относительно опорной точки (см. руководство к осциллографу).

    '''
    with open(file, 'r') as file:
        line1 = file.readline()
        line2 = file.readline()
        device = None
        if line1[:5] == 'time\t' or line1[:4] == '0\t0.':
            device = 'globaltest'
        elif line1[:4] == '   ':
            device = 'gydropribor'
        elif line1[:-2] == 'ProID,Info,,time,Vol.':
            device = 'micsig1'
        elif line1[:-2] == ('ProID,Info,Unnamed: 2,time,Vol.,Unnamed: 5,'
                            + 'ProID,Info,Unnamed: 2,time,Vol.,Unnamed: '):
            device = 'micsig2'
        elif line1[:-2] == 'X,CH1,CH2,Start,Increment':
            device = 'rigol-new'
            params = line2.strip()
        elif line1[:-2] == 'Time,X(CH1),X(CH2)':
            device = 'rigol-old'
        elif line1[:-1] == 'Model,MSO46':
            device = 'tektronix'
        else:
            print('Wrong .csv file structure.')

        if device == 'globaltest':
            df = pd.read_csv(file, index_col=False, names=['t', 'ch1', 'ch2'],
                             sep='\t')
            time = df['t'].values
            ch1 = -df['ch1'].values
            ch2 = -df['ch2'].values
            time_step = (time[100] - time[0])/100
            for i in range(len(time) - 1):
                time[i + 1] = time[i] + time_step
            return device, time, ch1, ch2
        if device == 'gydropribor':
            df = pd.read_csv(file, index_col=False,
                             names=['t', 'ch'], sep='\s+')
            time = df['t'].values
            ch = df['ch'].values
            return device, time, ch, None
        if device == 'micsig1':
            df = pd.read_csv(file, index_col=False, names=['t', 'ch'],
                             skiprows=13, usecols=[3, 4])
            time, ch = df['t'].values, df['ch'].values
            delay = np.loadtxt(file, delimiter=',', dtype='str',
                               skiprows=5, max_rows=1, usecols=1)
            delay = float(np.ndarray.item(delay).split(' ')[0])
            time = time - ((time[-1] - time[0])/2 - delay)
            return device, time, ch, None
        if device == 'micsig2':
            df = pd.read_csv(file, index_col=False, names=['t', 'ch1', 'ch2'],
                             skiprows=13, usecols=[3, 4, 10])
            time = df['t'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
            delay = np.loadtxt(file, delimiter=',', dtype='str',
                               skiprows=5, max_rows=1, usecols=1)
            delay = float(np.ndarray.item(delay).split(' ')[0])
            time = time - ((time[-1] - time[0])/2 - delay)
            return device, time, ch1, ch2
        if device == 'rigol-new':
            params = file.readline().strip()
            x_start = float(params.split(',')[3])
            x_step = float(params.split(',')[4])
            df = pd.read_csv(file, index_col=False,
                             names=['i', 'ch1', 'ch2'], skiprows=2)
            time = x_start + x_step*df['i'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
            return device, time, ch1, ch2
        if device == 'rigol-old':
            df = pd.read_csv(file, index_col=False,
                             names=['t', 'ch1', 'ch2'], skiprows=2)
            time = df['t'].values
            ch1, ch2 = df['ch1'].values, df['ch2'].values
            return device, time, ch1, ch2
        if device == 'tektronix':
            df = pd.read_csv(file, index_col=False,
                             names=['t', 'ch1', 'ch2'], skiprows=12)
            time = df['t'].values
            ch1, ch2 = -df['ch1'].values, -df['ch2'].values
            return device, time, ch1, ch2


def time_shift_removal(time, zero_time):
    '''
    Ликвидация сдвига по времени

    Parameters
    ----------
    time : Массив numpy, содержащий временной ряд.
    zero_time : Значение времени, принимаемое за ноль.

    Returns
    -------
    time : Массив numpy, содержащий временной ряд, начинающийся с нуля.

    Функция определяет сдвиг по времени как поданное на ввод значение
    и для каждого элемента производит вычитание этого значения.

    '''
    time_shift = zero_time
    time = time - time_shift
    return time


def channel_shift_removal(ch, amount=1000):
    '''
    Ликвидация сдвига нуля исследуемой величины

    Parameters
    ----------
    ch : Лист массивов NumPy, содержащих значения исследуемой величины.
    amount : Количество проходов по определению сдвига.

    Returns
    -------
    ch: Список массивов numpy, содержащих исправленный сигнал.

    Функция определяет значение сдвига как среднее первых amount
    значений массива сигнала, после чего для каждого элемента
    производит вычитание этого значения.

    '''
    for num, i in enumerate(ch):
        i = i.copy()
        shift = 0
        for j in range(int(amount)):
            shift += i[j]
        shift = shift/(amount)
        i = i - shift
        ch[num] = i
    return ch


def time_limitation(time, time_start, time_end, ch):
    '''
    Применение ограничения по времени

    Parameters
    ----------
    time : Массив numpy, содержащий временной ряд.
    time_start : Установка начального времени
    time_end : Установка конечного времени
    ch : Лист массивов NumPy, содержащих значения исследуемой величины.

    Returns
    -------
    time : Обрезанный временной ряд.
    ch : лист массивов сигналов; значения, соответствущие обрезанному
    времени, удалены.

    Функция срезом отсекает значения времени больше максимального, по
    числу элементов полученной последовательности обрезает также каждый
    из каналов. После та же процедура повторяется и в отношении
    минимального времени.

    '''
    time = time.copy()
    time = time[time <= time_end]
    for num, i in enumerate(ch):
        i = i.copy()
        i = i[:len(time)]
        ch = np.resize(ch, (len(ch), len(i)))
        ch[num] = i
    time = time[time_start <= time]
    for num, i in enumerate(ch):
        i = i[len(i) - len(time):]
        ch = np.resize(ch, (len(ch), len(i)))
        ch[num] = i
    return time, ch


def smooth(ch, window=1000):
    '''
    Сглаживание методом скользящей средней

    Parameters
    ----------
    ch : Лист массивов NumPy с не сглаженными значениями величины.
    window : Ширина окна сглаживания.

    Returns
    -------
    ch : Список массивов numpy со сглаженными значениями величины.

    Функция находит среднее значение исследуемого сигнала на ширине
    окна и подставляет его вместо исходного. В процессе цикла функция
    проходит по всем точкам последовательности, не затрагивая только
    участки в начале и в конце массива. На вход подается лист массивов
    NumPy. Объекты ndarray, как и списки, не копируются при присвоении
    нового имени, т.е. при обработке исходных массивов выходной кортеж
    будет содержать ссылки на те же объекты, только уже обработанные.
    Для сохранения возможности доступа к исходным значениям кортеж
    преобразуется в список, т.к. далее будет следовать операция
    присваивания, в теле цикла создается копия каждого из элементов
    массива, которая затем обрабатывается. NB: В Python полный срез
    создает копию массива, и его изменение не затрагивает исходный
    массив. В NumPy изменения в срезе влияют на исходный массив, для
    создания копии используется метод array.copy().

    '''
    for num, i in enumerate(ch):
        i = i.copy()
        for j in range(window, i.size - window):
            window_sum = 0
            for k in range(-window, window + 1):
                window_sum += i[j + k]
            i[j] = (window_sum/(2*window + 1))
        ch[num] = i
    return ch


def find_peaks(time, ch, distance_rate=0.003, height_rate=0.1,
               prominence_rate=0.08):
    '''
    Поиск экстремумов сигнала

    Parameters
    ----------
    time : Массив NumPy, содержащий временной ряд.
    ch : Лист массивов NumPy, содержащих значения исследуемой величины.
    distance_rate : Ширина дистанции по времени между соседними пиками
        в долях от общей длительности файла. По умолчанию 0.003.
    height_rate : Абсолютная высота пика в долях от высоты наибольшего
        пика. По умолчанию 0.1.
    prominence_rate : Относительная высота пика в долях от высоты
        наибольшего пика. По умолчанию 0.08.

    Returns
    -------
    ch_peaks : Список экстремумов следующего вида:
        [[array([time]), array([channel])],  # Канал 1
         [array([time]), array([channel])]]  # Канал 2

    Функция определяет индексы и высоты пиков посредством использования
    функции find_peaks() модуля SciPy, при этом параметры поиска пиков
    задаются в отношении к уже известным величинам: дистанция между
    пиками вычисляется как доля от длины файла по времени, абсолютная и
    относительная высоты - как доля от высоты максимального значения
    массива. Значения времени вычисляются как показания шкалы времени
    с интексами, соответствующими индексам пиков. Полученные данные
    объединяются в массив и подаются на вывод.

    '''
    ch_peaks = None
    for num, i in enumerate(ch):
        peak_indexes, peak_heights = fp(i, distance=distance_rate*len(i),
                                        height=height_rate*np.max(i),
                                        prominence=prominence_rate*np.max(i))
        peak_times = np.array([time[i] for i in peak_indexes])
        peak_heights = peak_heights['peak_heights']
        if ch_peaks is None:
            ch_peaks = np.vstack((peak_times, peak_heights))
        else:
            ch_peaks = np.stack((ch_peaks,
                                 np.vstack((peak_times, peak_heights))))
    return ch_peaks


def find_secondary_peaks(time, peak_times, t_expand_left, t_expand_right, ch):
    '''
    Поиск основных и вторичных пиков

    Parameters
    ----------
    time : Массив NumPy, содержащий временной ряд.
    peak_times : Лист моментов времени основных пиков.
    t_expand_left : Левая граница времени поиска вторичных пиков.
    t_expand_right : Правая граница времени поиска вторичных пиков.
    ch : Лист массивов NumPy, содержащих значения исследуемой величины.

    Returns
    -------
    all_peaks : Список экстремумов следующего вида:
        [[[array([time]), array([channel])],    # Канал 1, пик 1
          [array([time]), array([channel])],    # Канал 1, пик 2
          ...                              ,]   # Канал 1, пик n
          [array([time]), array([channel])],    # Канал 2, пик 1
          [array([time]), array([channel])],    # Канал 2, пик 2
          ...                              ,]]  # Канал 2, пик n

    Помимо стандартных массивов времени и значений сигнала, функция
    принимает значения времени основных пиков и границы по времени от
    основного пика, в пределах которых будет производиться поиск
    вторичных пиков. Создается массив для всех искомых пиков, также
    создается подмассив для каждого канала. Определяются временные
    массивы времени и значений сигнала путем отсечения по заданным
    границам функцией time_limitation(), после чего происходит поиск
    пиков уже в пределах усеченных массивов. Излишние найденные пики
    убираются из рассмотрения функцией find_greatest_peaks(), которая
    возвращает лишь указанное число максимальных пиков среди поданных.
    Далее найденные значения объединяются в список.

    '''
    all_peaks = None
    for num, (i, j) in enumerate(zip(ch, peak_times)):
        channel_peaks = None
        for k in j:
            i = ch[num].copy()
            i = np.expand_dims(i, axis=0)
            t, ch_tmp = time_limitation(time, k - t_expand_left,
                                        k + t_expand_right, i)
            secondary_peaks = find_peaks(t, ch_tmp, 1/15, 1/10, 1/100)
            secondary_peaks = find_greatest_peaks(secondary_peaks[0],
                                                  secondary_peaks[1], 2)
            secondary_peaks = np.expand_dims(secondary_peaks, axis=0)
            if channel_peaks is None:
                channel_peaks = secondary_peaks
            else:
                channel_peaks = np.vstack((channel_peaks, secondary_peaks))
        channel_peaks = np.expand_dims(channel_peaks, axis=0)
        if all_peaks is None:
            all_peaks = channel_peaks
            # all_peaks = np.expand_dims(all_peaks, axis=0)
            # channel_peaks = np.expand_dims(channel_peaks, axis=0)
        else:
            all_peaks = np.vstack((all_peaks, channel_peaks))
    return all_peaks


def find_greatest_peaks(time, ch, num):
    '''
    Поиск наибольших n пиков в массиве

    Parameters
    ----------
    time : Массив NumPy, содержащий время пиков.
    ch : Массив NumPy, содержащий значения (высоты) пиков.
    num : Количество пиков, которое следует отобрать.

    Returns
    -------
    sorted_peaks : Список экстремумов следующего вида:
        [array([time]), array([channel])]

    Для указанного количества значимых пиков num функция определяет
    наибольший пик и помещает его значения времени и величины сигнала
    в массив, после чего соответствующие значения удаляются из исходных
    массивов. Упакованные значения максимального пика помещаются в
    массив выбранных пиков, после эти операции повторяются вплоть до
    достижения значения num. После возникает задача сортировки по
    времени выходного массива. Для этого создается список peak_times
    и в него помещаются значения времени пиков. Далее циклом по списку
    ведется поиск индекса минимального времени, значения пиков с этим
    индексом добавляются в список сортированных пиков и удаляются из
    временного списка выбранных пиков. Список сортированных пиков в
    последствии возвращается функцией.

    '''
    selected_peaks = None
    for i in range(num):
        peak_index = np.where(ch == np.max(ch))[0][0]
        peak = np.array([time[peak_index], ch[peak_index]])
        time = np.delete(time, peak_index)
        ch = np.delete(ch, peak_index)
        if selected_peaks is None:
            selected_peaks = peak.copy()
        else:
            selected_peaks = np.vstack((selected_peaks, peak))
    peak_times = np.array([])
    for i in range(len(selected_peaks)):
        peak_times = np.append(peak_times, selected_peaks[i][0])
    sorted_peaks_times = np.array([])
    sorted_peaks_ch = np.array([])
    for i in range(len(peak_times)):
        index = np.where(peak_times == np.min(peak_times))[0][0]
        sorted_peaks_times = np.append(sorted_peaks_times,
                                       selected_peaks[index][0])
        sorted_peaks_ch = np.append(sorted_peaks_ch, selected_peaks[index][1])
        peak_times[index] = np.max(peak_times) + 1
    sorted_peaks = np.vstack((sorted_peaks_times, sorted_peaks_ch))
    return sorted_peaks


# def find_peak_params(peaks):
#     peak_params = []
#     for channel in len(peaks):
#         for num, i in enumerate(peaks[channel]):
#             T0 = i[0][1] - i[0][0]
#             W = find_energy(T0)


def csv_processing(file):
    device, t, *ch = read(file)
    ch = np.array(ch)
    settings = settings_declatation(ppc, device)
    all_peaks = None
    if settings['time_shift']:
        t = time_shift_removal(t, t[0])
    if not settings['channel_shift']:
        ch = channel_shift_removal(ch, amount=settings['zero_amount'])
    if not settings['t_left']:
        settings['t_left'] = t[0]
    if not settings['t_right']:
        settings['t_right'] = t[-1]
    t, ch = time_limitation(t, settings['t_left'],  settings['t_right'], ch)
    if settings['smooth']:
        ch = smooth(ch, window=settings['smooth_window'])
    if settings['find_peaks']:
        ch_peaks = find_peaks(t, ch)
        all_peaks = find_secondary_peaks(t, ch_peaks[:, 0],
                                         settings['t_secondary'],
                                         settings['t_secondary'], ch)
    # with open('all_peaks.pickle', 'wb') as f:
    #     data = (settings, t, ch, all_peaks)
    #     pickle.dump(data, f)
    plotting(settings, t, ch, all_peaks)
    
    # Временные строки получения спектральной плотности
    import scipy
    from scipy.io import wavfile
    from scipy.fft import fft, fftfreq, ifft
    from scipy.fft import rfft, rfftfreq, irfft
    
    def plotting1(x, y=[], st=0):
        if st:
            plt.clf()
            if len(y):
                plt.plot(x, y)
            else:
                plt.plot(x)
            plt.grid(True)

    # def w(f):
    #     w = 2*np.pi*f
    #     return w
    # SAMPLE_RATE = 50
    # DURATION = 10
    # sigma = 1
    
    # time = np.linspace(-DURATION/2, DURATION/2, SAMPLE_RATE*DURATION)
    # signal = np.e**-(sigma*np.abs(time))
    # plotting1(time, signal, st=1)
    yf = rfft(ch[0])
    xf = rfftfreq(len(ch[0]), (max(t)/len(t))**-1)
    plotting1(xf, np.abs(yf), st=1)

# import pickle
# import numpy as np
# from matplotlib import pyplot as plt

# with open('all_peaks.pickle', 'rb') as f:
#     settings, t, ch, all_peaks = pickle.load(f)


def plotting(settings, t, ch, all_peaks):
    if settings['plt_primary']:
        for i in range(len(ch)):
            plt.clf()
            plt.plot(t/mt[settings['t_unit']][0], ch[i]/mt[settings['ch_unit']][0]*settings['conv_factor_' + str(i + 1)], 'g-', label='u(t)')
            plt.grid(True)
            plt.xlabel(settings['t_sign'].format(mt[settings['t_unit']][1]))
            plt.ylabel(settings['ch_sign'].format(mt[settings['ch_unit']][1]))
            # plt.ylim(bottom = 0) # Нижняя граница по у
            if settings['show_legend']:
                plt.legend(loc='best')
            if settings['show_title']:
                plt.title('Серия импульсов, канал №{0}'.format(i + 1))
            # plt.show()
            plt.savefig('./plot {0}.{1}'.format(i + 1, settings['fig_format']), format=settings['fig_format'], dpi=settings['fig_dpi'])
        plt.clf()
    if settings['plt_secondary']:
        for i in range(len(ch)):
            for num, j in enumerate(all_peaks[i]):
                plt.clf()
                plt.plot(t/mt[settings['t_unit']][0], ch[i]/mt[settings['ch_unit']][0]*settings['conv_factor_' + str(i + 1)], 'g-', label='u(t)')
                if settings['show_peaks']:
                    plt.plot(j[0]/mt[settings['t_unit']][0], j[1]/mt[settings['ch_unit']][0]*settings['conv_factor_' + str(i + 1)], 'bx')
                plt.grid(True)
                plt.xlabel(settings['t_sign'].format(mt[settings['t_unit']][1]))
                plt.ylabel(settings['ch_sign'].format(mt[settings['ch_unit']][1]))
                plt.xlim((j[0][0]-settings['t_expand_left'])/mt[settings['t_unit']][0], (j[0][0]+settings['t_expand_right'])/mt[settings['t_unit']][0])
                # plt.ylim(bottom=0) # Нижняя граница по у
                if settings['show_legend']:
                    plt.legend(loc='best')
                if settings['show_title']:
                    plt.title('Импульс №{0}, канал №{1}'.format(num + 1, i + 1))
                # plt.show()
                plt.savefig('./plot {0}-{1}.{2}'.format(i + 1, num + 1, settings['fig_format']), format=settings['fig_format'], dpi=settings['fig_dpi'])
        plt.clf()
    if settings['plt_united']:
        plt.clf()
        for i in range(len(ch)):
            for num, j in enumerate(all_peaks[i]):
                t_tmp = time_shift_removal(t, j[0][0])
                t_tmp, ch_tmp = time_limitation(t_tmp, -settings['t_expand_left'],  settings['t_expand_right'], [ch[i]])
                plt.plot(t_tmp/mt[settings['t_unit']][0], ch_tmp[0]/mt[settings['ch_unit']][0]*settings['conv_factor_' + str(i + 1)], 'g-', label='u(t)', alpha=0.1)
            plt.grid(True)
            plt.xlabel(settings['t_sign'].format(mt[settings['t_unit']][1]))
            plt.ylabel(settings['ch_sign'].format(mt[settings['ch_unit']][1]))
            if settings['show_title']:
                plt.title('Плотность распределения вероятности сигнала датчика давления,\nканал №{0}'.format(i + 1))
            # plt.show()
            plt.savefig('./plot united {0}.{1}'.format(i + 1, settings['fig_format']), format=settings['fig_format'], dpi=settings['fig_dpi'])
            plt.clf()
    return all_peaks


def all_files():
    print('You lost all files.')


# === Обработка файлов ===

start_time = time.time()
dsc = open_cfg('dsc.cfg')
ppc = open_cfg('ppc.cfg')
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

# menu = Menu()
# menu.main()

csv_processing('./globaltest/csv/14-57.txt')
print('Время выполнения программы составило {:.3f} с.'.format(time.time()
                                                              - start_time))

__version__ = '0.7'
# Исправления:
    # 71 - написание функции all() по обработке всех приборов
    # 95 - написание функции csv_processing()
    # 99 - написание функции all_files() по обработке всех файлов прибора
    # 102 - неправильное поведение при возврате в меню
# micsig_channel_unite - посмотреть возможность выполнить в np
# Переписать документацию под np начиная с time_shift_removal