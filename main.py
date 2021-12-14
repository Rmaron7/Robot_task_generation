import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont

root = tk.Tk()
root[ 'bg' ] = '#ffffff'
root.geometry('1500x800')
root.title('генератор задач типа робот')
answer = []

all_Commands = [
                [ [ 0, -3 ], [ -2, 0 ] ],
                [ [ 0, -3 ], [ 2, 0 ] ],
                [ [ 0, -3 ], [ 2, 0 ], [ 0, 1 ] ],
                [ [ -1, 0 ], [ 0, -3 ], [ 2, 0 ] ],
                [ [ 0, -2 ], [ -2, 0 ], [ 0, 2 ] ]
              ]

new_Command = []

all_Commands_Len = len(all_Commands) # запоминаем длину первоначального списка

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
    global answer
    scale = int(25)
    size = int(entry_number_of_tasks.get())
    size *=1000
    img = Image.new('RGBA', (1000, size), 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', size=50)
    number_of_acceptable_commands = list()
    acceptable_commands = list()
    command = int()
    max_commands = int(entry_max_commands.get())
    min_commands = int(entry_min_commands.get())
    number_of_tasks = int(entry_number_of_tasks.get())
    for i in range(max_commands - min_commands):
        command = i + min_commands
        number_of_acceptable_commands.append(command)
    for i in range(len(all_Commands)):
        acceptable_commands.append(i)
    for i in range(number_of_tasks):
        currentX = int(500)
        currentY = int(500+i*1000)
        answer.clear()
        text_koords = int((i - 1) * 1000 + 100)
        stri = str(i)
        usertext = str('Задача ')
        usertext = usertext+stri
        draw.text((400, text_koords), usertext, font=font)
        number_commands = int(random.choice(number_of_acceptable_commands))

        for j in range(number_commands):
            random_command = int(random.choice(acceptable_commands))
            answer.append(random_command)

            for n in range(len(all_Commands[random_command])):

                currentX_koords = int(currentX)
                currentY_koords = int(currentY)
                nextX_koords = int(currentX_koords + scale*all_Commands[random_command][n][0])
                nextY_koords = int(currentY_koords - scale*all_Commands[random_command][n][1])
                currentX = nextX_koords
                currentY = nextY_koords
                draw.line(
                          (currentX_koords, currentY_koords, nextX_koords, nextY_koords),
                          fill='black',
                          width=3
                          )

        print(answer)

    img.save('TASK.png')

    root.destroy()


label_1 = tk.Label(root,
                   text='Минимум команд',
                   bg='white',
                   fg='black',
                   font=('Arial', 30, 'bold')
                   ).grid(row=0, column=0)
entry_min_commands = tk.Entry(root)
entry_min_commands.grid(row=0, column=1)

label_2 = tk.Label(root,
                   text='Максимум команд',
                   bg='white',
                   fg='black',
                   font=('Arial', 30, 'bold')
                   ).grid(row=1, column=0)
entry_max_commands = tk.Entry(root)
entry_max_commands.grid(row=1, column=1)

label_3 = tk.Label(root,
                   text='Набор команд',
                   bg='white',
                   fg='black',
                   font=('Arial', 30, 'bold')
                   ).grid(row=2, column=0)
entry_command_set = tk.Entry(root)
entry_command_set.grid(row=2, column=1)

label_4 = tk.Label(root,
                   text='Количество задач',
                   bg='white',
                   fg='black',
                   font=('Arial', 30, 'bold')
                   ).grid(row=3, column=0)
entry_number_of_tasks = tk.Entry(root)
entry_number_of_tasks.grid(row=3, column=1)

button_1 = tk.Button(root, text='Создать файл', command=finish).grid(row=4, column=0,
                                                                     columnspan=2,
                                                                     stick='we')

root.mainloop()
