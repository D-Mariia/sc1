from collections import Counter
import math

def clean ():
    try:
        with open("harry.txt", "r", encoding="utf-8") as file:
            text = file.read()
        lower_text = text.lower()

        lower_text = lower_text.replace('ё', 'е').replace('ъ', 'ь')

        cleaned_text = ""
        for letter in lower_text:
            if 'а' <= letter <= 'я':
                cleaned_text += letter
            else:
                cleaned_text += " "

        cleaned_text = " ".join(cleaned_text.split())

        with open("potter.txt", "w", encoding="utf-8") as file:
            file.write(cleaned_text)

        print("Файл очищено та збережено як  'potter.txt'")
    except FileNotFoundError:
        print("Помилка: файл 'harry.txt' не знайдено")

clean()

def count_frequencies():
    try:
        with open("potter.txt", "r", encoding="utf-8") as file:
            text = file.read()

        l_f = Counter(letter for letter in text if 'а' <= letter <= 'я' or letter == ' ')
        sorted_l_f = sorted(l_f.items(), key=lambda x: x[1], reverse=True)

        b_f = Counter ([(text[i], text[i+1]) for i in range(len(text) - 1)
                   if 'а' <= text[i] <= 'я' or text[i] == ' ' and 'а' <= text[i+1] <= 'я' or text[i+1] == ' '])
        unique_l = sorted(set(letter for letter in text if 'а' <= letter <= 'я' or letter == ' '))

        b_f_1 = Counter ([(text[i], text[i+2]) for i in range(len(text) - 2)
                   if 'а' <= text[i] <= 'я' or text[i] == ' ' and 'а' <= text[i+2] <= 'я' or text[i+2] == ' '])
        unique_l_1 = sorted(set(letter for letter in text if 'а' <= letter <= 'я' or letter == ' '))


        with open("results.txt", "w", encoding="utf-8") as output_file:
            output_file.write("Частоти літер:\n")
            for letter, freq in sorted_l_f:
                output_file.write(f"{letter}: {freq}\n")

            output_file.write("\nЧастоти біграм (пари букв, що перетинаються):\n")

            output_file.write("     " + "     ".join(unique_l) + "\n")

            for letter in unique_l:
                row = f"{letter} "
                for second_letter in unique_l:
                    row += f"{b_f.get((letter, second_letter), 0):5} "
                output_file.write(row + "\n")

            output_file.write("\nЧастоти біграм (пари букв, що не перетинаються):\n")

            output_file.write("     " + "     ".join(unique_l_1) + "\n")

            for letter in unique_l_1:
                row = f"{letter} "
                for second_letter in unique_l_1:
                    row += f"{b_f_1.get((letter, second_letter), 0):5} "
                output_file.write(row + "\n")


        print("Частоти літер і біграм  збережено в 'results.txt'")
        return l_f, b_f, b_f_1
    except FileNotFoundError:
        print("Помилка: файл 'potter.txt' не знайдено")
        return None, None, None


def entropy(frequencies):
    total_count = sum(frequencies.values())
    probabilities = [freq / total_count for freq in frequencies.values()]
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def count_entropy():
    l_f, b_f, b_f_1 = count_frequencies ()

    if l_f is not None:

        l_e = entropy(l_f)
        b_e = entropy(b_f) / 2
        b_e_1 = entropy(b_f_1) / 2

        with open("results.txt", "a", encoding="utf-8") as output_file:
            output_file.write("\nЗ пробілами:\n")
            output_file.write(f"\nЕнтропія літер: {l_e:.4f}\n")
            output_file.write(f"Ентропія біграм (пари букв, що перетинаються) : {b_e:.4f}\n")
            output_file.write(f"Ентропія біграм (пари букв, що не перетинаються) : {b_e_1:.4f}\n")

        print("Ентропії літер і біграм збережено в 'results.txt'.")

count_entropy()

def count_entropy_without_spaces():
    try:
        with open("potter.txt", "r", encoding="utf-8") as file:
            text = file.read()

        text_no_spaces = text.replace(" ", "")

        l_f = Counter(letter for letter in text_no_spaces if 'а' <= letter <= 'я')
        b_f = Counter([(text_no_spaces[i], text_no_spaces[i+1]) for i in range(len(text_no_spaces) - 1)
                       if 'а' <= text_no_spaces[i] <= 'я' and 'а' <= text_no_spaces[i+1] <= 'я'])
        b_f_1 = Counter([(text_no_spaces[i], text_no_spaces[i+2]) for i in range(len(text_no_spaces) - 2)
                         if 'а' <= text_no_spaces[i] <= 'я' and 'а' <= text_no_spaces[i+2] <= 'я'])

        l_e = entropy(l_f)
        b_e = entropy(b_f) / 2
        b_e_1 = entropy(b_f_1) / 2

        with open("results.txt", "a", encoding="utf-8") as output_file:
            output_file.write("\nБез пробілів:\n")
            output_file.write(f"\nЕнтропія літер : {l_e:.4f}\n")
            output_file.write(f"Ентропія біграм (пари букв, що перетинаються): {b_e:.4f}\n")
            output_file.write(f"Ентропія біграм (пари букв, що не перетинаються): {b_e_1:.4f}\n")

        print("Ентропії літер і біграм без пробілів збережено в 'results.txt'.")

    except FileNotFoundError:
        print("Помилка: файл 'potter.txt' не знайдено.")

count_entropy_without_spaces()