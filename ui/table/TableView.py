import tkinter
from tkinter import RIGHT, BOTTOM, ttk, X, Y, CENTER, NO


class TableView:
    def __init__(self, frame: tkinter.Frame):
        # scrollbar
        scroll = tkinter.Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)

        scroll = tkinter.Scrollbar(frame, orient='horizontal')
        scroll.pack(side=BOTTOM, fill=X)

        table = ttk.Treeview(frame, yscrollcommand=scroll.set, xscrollcommand=scroll.set)

        table.pack()

        scroll.config(command=table.yview)
        scroll.config(command=table.xview)

        # define our column

        table['columns'] = ('player_id', 'player_name', 'player_Rank', 'player_states', 'player_city')

        # format our column
        table.column("#0", width=0, stretch=NO)
        table.column("player_id", anchor=CENTER, width=80)
        table.column("player_name", anchor=CENTER, width=80)
        table.column("player_Rank", anchor=CENTER, width=80)
        table.column("player_states", anchor=CENTER, width=80)
        table.column("player_city", anchor=CENTER, width=80)

        # Create Headings
        table.heading("#0", text="", anchor=CENTER)
        table.heading("player_id", text="Id", anchor=CENTER)
        table.heading("player_name", text="Name", anchor=CENTER)
        table.heading("player_Rank", text="Rank", anchor=CENTER)
        table.heading("player_states", text="States", anchor=CENTER)
        table.heading("player_city", text="States", anchor=CENTER)

        table.insert(parent='', index='end', iid=0, text='',
                       values=('1', 'Ninja', '101', 'Oklahoma', 'Moore'))
        table.pack()