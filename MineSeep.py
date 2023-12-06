import tkinter as tk
from random import sample
from tkinter.messagebox import showinfo, showerror

colors = {0: 'white',
          1: 'blue',
          2: 'green',
          3: '#c264ed',
          4: '#702a55',
          5: '#1f3057',
          6: '#36a891',
          7: '#b03a42',
          8: '#e3101e'}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Arial 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.count_bomb = 0
        self.in_mine = False
        self.is_open = False

    def __repr__(self):
        return f"My {self.x} {self.y} {self.in_mine} {self.number}"


class MineSweep:
    window = tk.Tk()
    ROW = 5
    COLUMNS = 5
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttuns = []

        for i in range(self.ROW + 2):
            tmp = []
            for j in range(self.COLUMNS + 2):
                btn = MyButton(self.window, x=i, y=j)
                btn.config(command=lambda buttom=btn: self.click(buttom))
                btn.bind("<Button-3>", self.right_click)
                tmp.append(btn)
            self.buttuns.append(tmp)

    def right_click(self, event):
        if self.IS_GAME_OVER:
            return
        curr_btn = event.widget
        if curr_btn['state'] == 'active':
            curr_btn['font'] = ('Arial', 20, 'bold')
            curr_btn['bg'] = 'white'
            curr_btn['state'] = 'disabled'
            curr_btn['text'] = "#"
        elif curr_btn['text'] == "#":
            curr_btn['text'] = ""
            curr_btn['state'] = 'active'
            curr_btn.configure(bg=curr_btn.master.cget('bg'))

    def click(self, clicked_button: MyButton):
        if self.IS_GAME_OVER:
            return

        if self.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_ceils()
            self.print_buttons()
            self.IS_FIRST_CLICK = False

        if clicked_button.in_mine:
            clicked_button.config(text="*", background="red", disabledforeground="black")
            clicked_button.is_open = True
            self.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли !')
            for i in range(1, self.ROW + 1):
                for j in range(1, self.COLUMNS + 1):
                    btn = self.buttuns[i][j]
                    # btn.grid(row=i, column=j)
                    if btn.in_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            # clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                # clicked_button.config(text='', disabledforeground=color)
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn):
        lst = [btn]

        while lst:
            cur_btn = lst.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue
                        next_but = self.buttuns[x + dx][y + dy]
                        if not next_but.is_open and 1 <= next_but.x <= self.ROW and \
                                1 <= next_but.y <= self.COLUMNS and next_but not in lst:
                            lst.append(next_but)

    def reload(self):
        # self.window.winfo_children()[0].destroy()
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_FIRST_CLICK = True
        self.IS_GAME_OVER = False

    def create_settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')

        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, self.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        min_entry = tk.Entry(win_settings)
        min_entry.insert(0, self.MINES)
        min_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_setting(row_entry, column_entry, min_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_setting(self, row: tk.Entry, column: tk.Entry, min: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(min.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение')
        self.ROW = int(row.get())
        self.COLUMNS = int(column.get())
        self.MINES = int(min.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings = tk.Menu(menubar, tearoff=0)
        settings.add_command(label='Играть', command=self.reload)
        settings.add_command(label='Настройки', command=self.create_settings_window)
        settings.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings)
        count = 1
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttuns[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='n,e,s,w')
                count += 1
                # print(self.buttuns[i][j])
        for i in range(1, self.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, self.ROW + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(self.ROW + 2):
            for j in range(self.COLUMNS + 2):
                btn = self.buttuns[i][j]
                if btn.in_mine:
                    btn.config(text="*", background="red", disabledforeground="black")
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)
                # btn.config(state='disabled')

    def start(self):
        self.create_widgets()
        # # self.open_all_buttons()
        self.window.mainloop()

    def print_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttuns[i][j]
                if btn.in_mine:
                    print('B', end=" ")
                else:
                    print(btn.count_bomb, end=" ")
            print()

    def get_mine(self, ex_number: int):
        ind = set(sample(range(1, self.ROW * self.COLUMNS + 1), self.MINES))
        if ex_number in ind:
            ind.remove(ex_number)
        return ind

    def insert_mines(self, number: int):
        ind = self.get_mine(number)
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttuns[i][j]
                if btn.number in ind:
                    btn.in_mine = True

    def count_mines_in_ceils(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttuns[i][j]
                count_bomb = 0
                if not btn.in_mine:
                    for rox_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttuns[i + rox_dx][j + col_dx]
                            if neighbour.in_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb


game = MineSweep()
game.start()
