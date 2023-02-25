import sys


CODEC = "cp1251"  # при иной кодировке используемых ниже файлов, заменить кодировку на нужную

MIN_ARGV = 3                 # минимальное число аргументов из командной строки
SUBSTRING_MIN_LEN = 0        # минимальная длина разбитых строк (нельзя указать меньше после -n)
DEFAULT_SUBSTRING_LEN = 200  # длина разбитых слов по умолчанию

OK = 0                            # возвращаемый код при правильном исполнении функции
ERR_NOT_ENOUGH_ARGV = -1          # коды ошибок: получено слишком мало
ERR_KEY_NOT_EXIST = -2            # не существует ключа
ERR_FILE_NOT_EXIST = -3           # открываемый файл не существует
ERR_WRONG_LEN_STRING = -4         # указана слишком короткая длина строки для разбиения
ERR_TOO_LONG_WORD = -5            # в файле есть слишком большое слово
ERR_TOO_LONG_STRING = -6          # в файле слишком длинная строка для разбития
ERR_OUTPUT_FILE_NO_REWRITE = -7   # файл не был перезаписан
ERR_NOT_EXIST_STR_AFTER_KEY = -8  # после ключа ожидался параметр


def find_argv_key(key: str) -> int:  # ищет необходимый ключ среди аргументов командной строки и возвращает его номер
    for it in range(len(sys.argv)):
        if sys.argv[it] == key:
            return it
    return ERR_KEY_NOT_EXIST


def check_argv_file_exist(argv_number_file: int) -> int:  # проверка существования файла с переданным именем
    try:
        input_file = open(sys.argv[argv_number_file])
        input_file.close()
    except FileNotFoundError:
        print("Ошибка: Файла с именем", sys.argv[argv_number_file], "не существует")
        return ERR_FILE_NOT_EXIST
    except IndexError:
        return ERR_NOT_EXIST_STR_AFTER_KEY
    return OK


def check_correct_argv() -> int:  # проверка корректности аргументов командной строки
    if len(sys.argv) < MIN_ARGV:  # проверка на существование минимума аргументов (-f и имя файла)
        print("Ошибка:", len(sys.argv) - 1, "- недостаточное количество аргументов, минимум 2 аргумента")
        return ERR_NOT_ENOUGH_ARGV

    args = find_argv_key("-f")  # проверка, существует ли -f
    if args == ERR_KEY_NOT_EXIST:
        print("Ошибка: -f - Не найден обязательный ключ")
        return ERR_KEY_NOT_EXIST

    args += 1
    err_code = check_argv_file_exist(args)  # проверка, существует ли файл ввода
    if err_code != OK:
        return err_code

    args = find_argv_key("-n")  # в случае существования аргумента -n, проверяем корректность
    if args != ERR_KEY_NOT_EXIST:
        args += 1
        try:
            if int(sys.argv[args]) < SUBSTRING_MIN_LEN:
                print("Ошибка: После ключа -n должно быть целое число большее", SUBSTRING_MIN_LEN, end="\0")
                print(", а не", (sys.argv[args]))
                return ERR_WRONG_LEN_STRING
        except ValueError:
            print("Ошибка: После ключа -n должно быть число")
            return ERR_WRONG_LEN_STRING
        except IndexError:
            print("Ошибка: После ключа -n должно стоять число")
            return ERR_NOT_EXIST_STR_AFTER_KEY

    args = find_argv_key("-r")
    if args != ERR_KEY_NOT_EXIST:
        args += 1
        try:
            sys.argv[args]
        except IndexError:
            print("Ошибка: После ключа -r должна быть команда")
            return ERR_NOT_EXIST_STR_AFTER_KEY

    args = find_argv_key("-n")  # дальше идет проверка на длину разбиения строк
    if args != ERR_KEY_NOT_EXIST:
        substrings_len = int(sys.argv[args + 1])
    else:
        substrings_len = DEFAULT_SUBSTRING_LEN

    input_file = open(sys.argv[find_argv_key("-f") + 1], mode='r', encoding=CODEC)
    input_list = input_file.read().split()
    input_file.close()
    str_tmp = ""
    for it in range(len(input_list)):  # проверка, нет ли слова большего, чем -n 'число'
        if input_list[it][0] == "@" or str_tmp != "":
            if str_tmp == "":
                str_tmp += input_list[it]
            else:
                str_tmp += " " + input_list[it]

            if len(str_tmp) > substrings_len:
                print("Ошибка: в файле есть тег больший, чем", substrings_len, end="")
                print(",невозможно разбить на строки:\n" + str_tmp)
                return ERR_TOO_LONG_WORD
            if str_tmp.find(":") != -1:
                str_tmp = ""
        if len(input_list[it]) > substrings_len:
            print("Ошибка: в файле есть слово большее, чем", substrings_len, end="")
            print(",невозможно разбить на строки:\n" + input_list[it])
            return ERR_TOO_LONG_WORD
    if find_argv_key("-l") != ERR_KEY_NOT_EXIST:  # проверка, нет ли строки со счетом пользователя большей -n 'число'
        input_file = open(sys.argv[find_argv_key("-f") + 1], mode='r', encoding=CODEC)
        input_list = input_file.read().split("\n")
        input_file.close()
        for it in range(len(input_list)):
            if input_list[it].find("score") != -1:
                if len(input_list[it]) > substrings_len:
                    print("Ошибка: в файле есть строка большая со счетом пользователя, чем", substrings_len, end="")
                    print(",невозможно разбить на строки:\n", it + 1, end="")
                    print(".", input_list[it])
                    return ERR_TOO_LONG_STRING

    return OK


def slice_file(substrings_len: int, file_name: str, key_l="") -> list[str]:  # нарезаем файл
    input_file = open(file_name, mode='r', encoding=CODEC)
    substrings = []  # тут хранятся правильно нарезанные строки

    if key_l == "":  # если нет ключа -l, то нарезаем по слову
        input_list = input_file.read().split("\n")
        str_tmp_tag_search = ""
        substr_tmp = ""
        for str_it in range(len(input_list)):
            if lambda_func[0] == "indiv":   # запрет на разбитие введенной строки
                if lambda_func[1](input_list[str_it]):  # ААААА, я не знаю как заранее сделать, что тут функция будет
                    if len(substr_tmp) + len(input_list[str_it]) > substrings_len:
                        substrings.append(substr_tmp)
                        substr_tmp = input_list[str_it] + "\n"
                    else:
                        substr_tmp += input_list[str_it] + "\n"
                    continue
            if input_list[str_it] == "":
                substr_tmp += "\n"
            list_tmp = input_list[str_it].split()
            for it in range(len(list_tmp)):
                if list_tmp[it][0] == "@" or str_tmp_tag_search != "":
                    if str_tmp_tag_search == "":
                        str_tmp_tag_search += list_tmp[it]
                    else:
                        str_tmp_tag_search += " " + list_tmp[it]

                    if str_tmp_tag_search.find(":") != -1:
                        if len(substr_tmp) + len(str_tmp_tag_search) > substrings_len:
                            substrings.append(substr_tmp)
                            substr_tmp = str_tmp_tag_search
                            str_tmp_tag_search = ""
                        else:
                            substr_tmp += " " + str_tmp_tag_search
                            str_tmp_tag_search = ""
                    continue
                if len(substr_tmp) + len(list_tmp[it]) > substrings_len:
                    substrings.append(substr_tmp)
                    substr_tmp = list_tmp[it]
                elif substr_tmp == "":
                    substr_tmp += list_tmp[it]
                else:
                    substr_tmp += " " + list_tmp[it]
                if it == (len(list_tmp) - 1) and substr_tmp != "":
                    substr_tmp += "\n"
            if str_it == (len(input_list) - 1) and substr_tmp != "":
                substrings.append(substr_tmp)
        for it in range(len(substrings)):  # удаляем лишние переносы строки в конце элементов списка
            if substrings[it][-1] == "\n":
                substrings[it] = substrings[it][:-1]
    elif key_l == "-l":
        list_tmp = input_file.read().split("\n")  # нарезаем на строки
        input_file.close()
        substr_tmp_slice = ""
        for it in range(len(list_tmp)):
            if list_tmp[it] == "":
                substr_tmp_slice += "\n"
                continue
            if list_tmp[it].find("score") != -1:  # строку со score резать нельзя
                if substr_tmp_slice != "":
                    if (len(substr_tmp_slice) + len(list_tmp[it])) > substrings_len:
                        substrings.append(substr_tmp_slice)
                        substr_tmp_slice = list_tmp[it]
                    else:
                        substr_tmp_slice += "\n" + list_tmp[it]
            else:  # обычную строку разбиваем на слова и делим на подстроки
                if list_tmp[it].find("score") == -1 and list_tmp[it - 1].find("score") != -1:
                    if (len(substr_tmp_slice) + len(list_tmp[it])) < substrings_len:
                        substr_tmp_slice += "\n"
                words_list_tmp = list_tmp[it].split()

                for word_it in range(len(words_list_tmp)):
                    if (len(substr_tmp_slice) + len(words_list_tmp[word_it])) > substrings_len:
                        substrings.append(substr_tmp_slice)
                        substr_tmp_slice = ""
                    if substr_tmp_slice == "":
                        substr_tmp_slice += words_list_tmp[word_it]
                    else:
                        substr_tmp_slice += " " + words_list_tmp[word_it]
                    if it == (len(list_tmp) - 1) and word_it == (len(words_list_tmp) - 1):
                        substrings.append(substr_tmp_slice)

    else:
        print("Ошибка: в функцию передан неправильный параметр, ожидался '-l' или ''")

    return substrings


def print_substrings(substrings: list[str]) -> None:
    for it in range(len(substrings)):
        print(f"Substring #{it}:\n{substrings[it]}", end="\n\n")


def write_list_in_file(input_list: list[str], file_name: str) -> int:
    err_code = ERR_FILE_NOT_EXIST
    try:
        file = open(file_name, 'r')
        file.close()
        err_code = OK
    except FileNotFoundError:
        pass
    if err_code == OK:
        print("Файл для выходных данных с именем " + file_name + " уже существует\nПерезаписать? Y|y - да")
        question = input()
        if question != "Y" and question != "y" and question != "да" and question != "Да":
            return ERR_OUTPUT_FILE_NO_REWRITE

    file = open(file_name, "w", encoding=CODEC)
    for it in range(len(input_list)):
        str_tmp = "Substring #" + str(it) + ":\n" + input_list[it] + "\n\n"
        file.write(str_tmp)
    file.close()
    return OK


lambda_func = ["type", "func"]
                                # Я не понял, что нужно в хардкоре. В условии написано, что вводится запрет на разбитие
                                # строки, в примере уже команда удаляет все строки, где имеется 'score'. Я подумал,
                                # подумал и все равно не понял. Сделал как понял - lambda line: 'score' in line -
                                # запрещает разбивать эту строку. будет работать только с line


def make_lambda_func(line: str) -> int:
    lambda_func[0] = "indiv"
    exec("lambda_func[1] = " + line)
    return 0


def main() -> int:
    err_code = check_correct_argv()
    if err_code != OK:
        return err_code

    args = find_argv_key("-n")
    if args != ERR_KEY_NOT_EXIST:
        substr_len = int(sys.argv[find_argv_key("-n") + 1])  # длина порезанной строки
    else:
        substr_len = DEFAULT_SUBSTRING_LEN

    args = find_argv_key("-r")
    if args != ERR_KEY_NOT_EXIST:
        make_lambda_func(sys.argv[args + 1])

    if find_argv_key("-l") != ERR_KEY_NOT_EXIST:
        substrings = slice_file(substr_len, sys.argv[find_argv_key("-f") + 1], "-l")
    else:
        substrings = slice_file(substr_len, sys.argv[find_argv_key("-f") + 1])

    args = find_argv_key("-d")
    if args != ERR_KEY_NOT_EXIST:
        write_list_in_file(substrings, sys.argv[args + 1])

    print_substrings(substrings)

    return 0


if __name__ == '__main__':
    sys.exit(main())
