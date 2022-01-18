import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import os
# ----------------------------------------------------------------------------------------------------------------------
# объявление основных данных
# ----------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
root['bg'] = '#ffffff'
root.geometry('1500x800')
root.title('генератор задач типа робот')
answer = []
answer_draw = []

all_Commands = [
    [[0, -3], [-2, 0]],
    [[0, -3], [2, 0]],
    [[0, -3], [2, 0], [0, 1]],
    [[-1, 0], [0, -3], [2, 0]],
    [[0, -2], [-2, 0], [0, 2]]
]

new_Command = []

all_Commands_Len = len(all_Commands)

f = open('Условия.txt', 'r', encoding='UTF8')
lines = f.read()
f.close()
print(lines)

for i in range(3):
    for j in range(all_Commands_Len):
        new_Command.clear()

        currentListIndex = i * all_Commands_Len + j

        for n in all_Commands[currentListIndex]:
            new_Command.append(n.copy())

        for n in new_Command:
            temp = n[0]
            n[0] = -n[1]
            n[1] = temp

        all_Commands.append(new_Command.copy())


def finish():
    if entry_min_diff.get().isdigit() and entry_max_diff.get().isdigit() and entry_number_of_tasks.get().isdigit() and entry_max_commands.get().isdigit() and entry_min_commands.get().isdigit():
        # --------------------------------------------------------------------------------------------------------------
        # подготовка всего для работы процедуры
        # --------------------------------------------------------------------------------------------------------------
        global answer
        global right
        global left
        global lower
        global upper
        global diff
        min_diff = int(entry_min_diff.get())
        max_diff = int(entry_max_diff.get())
        if min_diff > max_diff:
            min_diff = int(entry_max_diff.get())
            max_diff = int(entry_min_diff.get())
        if min_diff < 1:
            min_diff = 1
        if max_diff > 10:
            max_diff = 10
        diff = int()
        scale = int(25)
        size = int(entry_number_of_tasks.get())
        size *= 1000
        size_ans = int(entry_number_of_tasks.get())
        size_ans *= 75
        folder = str('Задачи от ' + str(dt.datetime.now()))
        folder = folder.replace(':', '.')
        os.mkdir(f'{folder}')
        imgansw = Image.new('RGBA', (1500, 1000 + size_ans), 'white')
        drawansw = ImageDraw.Draw(imgansw)
        font = ImageFont.truetype('arial.ttf', size=50)
        font_2 = ImageFont.truetype('arial.ttf', size=20)
        number_of_acceptable_commands = list()
        acceptable_commands = list()
        command = int()
        max_commands = int(entry_max_commands.get())
        min_commands = int(entry_min_commands.get())
        if min_commands > max_commands:
            max_commands = int(entry_min_commands.get())
            min_commands = int(entry_max_commands.get())
        if min_commands < 1:
            min_commands = 1
        if max_commands > 20:
            max_commands = 20
        number_of_tasks = int(entry_number_of_tasks.get())
        if int(entry_number_of_tasks.get())> 100:
            number_of_tasks = 100
        answer_str = str()

        for i in range(max_commands - min_commands+1):
            command = i + min_commands
            number_of_acceptable_commands.append(command)
        for i in range(len(all_Commands)):
            acceptable_commands.append(i)

            # ----------------------------------------------------------------------------------------------------------
            # генерация всех задач, проверка на подходимость
            # ----------------------------------------------------------------------------------------------------------
        ans_text_koords = int(750)
        i = 0
        for i in range(number_of_tasks):

            img= Image.new('RGBA', (1000, 1500), 'white')
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), str(i+1)+'. ', font=font, fill='black')
            for l in range(40):
                draw.line(
                    (l * scale, 500, l * scale, 1500),
                    fill='gray',
                    width=1
                )
            for l in range(40):
                draw.line(
                    (0, (l+20) * scale, 1000, (l+20) * scale),
                    fill='gray',
                    width=1
                )

            upper = int()
            lower = int()
            left = int()
            right = int()
            square = int()

            while not diff <= max_diff or not diff >= min_diff:
                diff = 0
                square = 0
                upper = 0
                lower = 0
                left = 0
                right = 0
                interm_coords = [0, 0]
                answer.clear()
                answer_str = ''

                currentX = int(500)
                currentY = int(1000)
                text_koords = int(500 + i * 50)
                number_commands = int(random.choice(number_of_acceptable_commands))
                draw.rectangle((currentX - 5, currentY - 5, currentX + 5, currentY + 5), fill='black')

                answer_str += f'{i+1}'
                answer_str += '. '

                for j in range(number_commands):
                    random_command = int(random.choice(acceptable_commands))
                    answer.append(random_command)

                    if random_command % 5 == 0:
                        answer_str += 'A '
                    elif random_command % 5 == 1:
                        answer_str += 'B '
                    elif random_command % 5 == 2:
                        answer_str += 'C '
                    elif random_command % 5 == 3:
                        answer_str += 'D '
                    elif random_command % 5 == 4:
                        answer_str += 'E '

                    for n in range(len(all_Commands[random_command])):

                        interm_coords[0] += all_Commands[random_command][n][0]
                        interm_coords[1] += all_Commands[random_command][n][1]
                        if interm_coords[0] > right:
                            right = interm_coords[0]
                        elif interm_coords[0] < left:
                            left = interm_coords[0]
                        if interm_coords[1] > lower:
                            lower = interm_coords[1]
                        elif interm_coords[1] < upper:
                            upper = interm_coords[1]

                square = (right - left) * (lower - upper)
                diff = int(number_commands * 50 / square)

                answer_draw = answer[:]
            diff = 0
            for j in range(5):

                text_koords = 225 + j * 175
                letter = ''
                letter += chr(65 + j)
                draw.text((text_koords, 525), letter, font=font, fill='black')

                currentX = 225 + j * 175
                currentY = 575
                draw.rectangle((currentX - 3, currentY - 3, currentX + 3, currentY + 3), fill='black')
                for n in range(len(all_Commands[j])):
                    currentX_koords = int(currentX)
                    currentY_koords = int(currentY)
                    nextX_koords = int(currentX_koords + scale * all_Commands[j][n][0])
                    nextY_koords = int(currentY_koords - scale * all_Commands[j][n][1])
                    currentX = nextX_koords
                    currentY = nextY_koords
                    draw.line(
                        (currentX_koords, currentY_koords, nextX_koords, nextY_koords),
                        fill='black',
                        width=5
                    )
            draw.multiline_text((30, 0), lines, font=font_2, fill='black')
            drawansw.multiline_text((30, 500), lines, font=font_2, fill='black')



            # ----------------------------------------------------------------------------------------------------------
            # отрисовка задач после удачной генерации
            # ----------------------------------------------------------------------------------------------------------

            currentX = 500
            currentY = 1000
            for j in range(number_commands):
                for n in range(len(all_Commands[answer_draw[j]])):
                    currentX_koords = int(currentX)
                    currentY_koords = int(currentY)
                    nextX_koords = int(currentX_koords + scale * all_Commands[answer_draw[j]][n][0])
                    nextY_koords = int(currentY_koords - scale * all_Commands[answer_draw[j]][n][1])
                    currentX = nextX_koords
                    currentY = nextY_koords
                    draw.line(
                        (currentX_koords, currentY_koords, nextX_koords, nextY_koords),
                        fill='black',
                        width=5
                    )
                drawansw.text((100, ans_text_koords), answer_str, font=font, fill='black')
            answer.clear()
            ans_text_koords += 75

            if i > 9:
                img.save(f'{folder}/TASK_{i+1}.png')
            else:
                img.save(f'{folder}/TASK_0{i+1}.png')

        # --------------------------------------------------------------------------------------------------------------
        # отрисовка команд на поле с ответами
        # --------------------------------------------------------------------------------------------------------------

        for i in range(5):

            text_koords = 250 + i * 300
            answer_str = ''
            answer_str += chr(65 + i)
            drawansw.text((text_koords, 25), answer_str, font=font, fill='black')

            currentX = 250 + i * 300
            currentY = 100
            drawansw.rectangle((currentX - 5, currentY - 5, currentX + 5, currentY + 5), fill='black')
            for n in range(len(all_Commands[i])):
                currentX_koords = int(currentX)
                currentY_koords = int(currentY)
                nextX_koords = int(currentX_koords + 75 * all_Commands[i][n][0])
                nextY_koords = int(currentY_koords - 75 * all_Commands[i][n][1])
                currentX = nextX_koords
                currentY = nextY_koords
                drawansw.line(
                    (currentX_koords, currentY_koords, nextX_koords, nextY_koords),
                    fill='black',
                    width=5
                )
        # --------------------------------------------------------------------------------------------------------------
        #   отрисовка команд на поле с условиями
        # --------------------------------------------------------------------------------------------------------------

        imgansw.save(f'{folder}/ANSWERS.png')
        root.destroy()

# ----------------------------------------------------------------------------------------------------------------------
# объявление всех полей ввода и кнопок
# ----------------------------------------------------------------------------------------------------------------------

label_1 = tk.Label(root,
                   text='Минимум команд',
                   bg='white',
                   fg='black',
                   font=('Arial', 30)
                   ).grid(row=0, column=0, stick='E')
entry_min_commands = tk.Entry(root)
entry_min_commands.grid(row=0, column=1)

label_2 = tk.Label(root,
                   text='Максимум команд',
                   bg='white',
                   fg='black',
                   font=('Arial', 30)
                   ).grid(row=1, column=0, stick='E')
entry_max_commands = tk.Entry(root)
entry_max_commands.grid(row=1, column=1)

label_3 = tk.Label(root,
                   text='Количество задач',
                   bg='white',
                   fg='black',
                   font=('Arial', 30)
                   ).grid(row=2, column=0, stick='E')
entry_number_of_tasks = tk.Entry(root)
entry_number_of_tasks.grid(row=2, column=1)

label_4 = tk.Label(root,
                   text='Минимальная сложность(по 10-балльной шкале)',
                   bg='white',
                   fg='black',
                   font=('Arial', 30)
                   ).grid(row=3, column=0, stick='E')
entry_min_diff = tk.Entry(root)
entry_min_diff.grid(row=3, column=1)

label_5 = tk.Label(root,
                   text='Максимальная сложность(по 10-балльной шкале)',
                   bg='white',
                   fg='black',
                   font=('Arial', 30)
                   ).grid(row=4, column=0, stick='E')
entry_max_diff = tk.Entry(root)
entry_max_diff.grid(row=4, column=1)

button_1 = tk.Button(root, text='Создать файл', command=finish).grid(row=5, column=0,
                                                                     columnspan=2,
                                                                     stick='we')

root.mainloop()
