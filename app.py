import threading
import tkinter as tk
from client import Client
from functools import partial
from tkinter import Button, font as tkfont


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.reg = False
        self.username = None
        self.send_user = "No one"
        self.client = Client()
        self.current_messages = 0
        self.shared_data = {"Balance": tk.IntVar()}
        self.user_data = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in [UserNamePage, UserPage]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.current_frame = None

        self.show_frame("UserNamePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if self.current_frame:
            self.current_frame.forget()
        self.current_frame = self.frames[page_name]
        self.current_frame.update_widgets(self.username)
        self.current_frame.tkraise()


class UserNamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#3d3d5c")
        self.controller = controller

        self.controller.title("P2P Chat")
        w, h = self.controller.winfo_screenwidth(), self.controller.winfo_screenheight()
        # w, h = 800, 600
        self.controller.geometry("%dx%d+0+0" % (w, h))

        heading_label = tk.Label(self,
                                 text="P2P Chat App",
                                 font=('helvetica', 45, "bold"),
                                 foreground='white',
                                 background="#3d3d5c"
                                 )
        heading_label.pack(pady=25)

        # label only for space
        space_label = tk.Label(self, height=4, bg="#3d3d5c")
        space_label.pack()

        username_label = tk.Label(self,
                                  text="Enter a username",
                                  font=("helvetica", 13),
                                  bg="#3d3d5c",
                                  fg="white")
        username_label.pack(pady=5)

        username = tk.StringVar()
        username_entry_box = tk.Entry(self,
                                      textvariable=username,
                                      width=42)

        username_entry_box.focus_set()
        username_entry_box.pack(pady=5)

        def enter_username():
            self.controller.username = username.get()
            controller.client.set_username(username.get())
            self.controller.reg = True
            username.set("")
            username_taken_label["text"] = ""
            t = threading.Thread(target=controller.client.receive)
            t.start()
            self.controller.show_frame("UserPage")

        enter_button = tk.Button(self,
                                 text="Enter",
                                 command=enter_username,
                                 relief="raised",
                                 borderwidth=3,
                                 width=40,
                                 height=3
                                 )
        enter_button.pack(pady=5)

        username_taken_label = tk.Label(self,
                                        text='',
                                        font=('helvetica', 13),
                                        fg='white',
                                        bg='#33334d',
                                        anchor='n')

        username_taken_label.pack(fill="both", expand=True)

    def update_widgets(self, x) -> None:
        pass


class UserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#3d3d5c")
        self.controller = controller
        self.controller.title("P2P Chat")
        self.username = None
        w, h = self.controller.winfo_screenwidth(), self.controller.winfo_screenheight()
        # w, h = 800, 600
        self.controller.geometry("%dx%d+0+0" % (w, h))

        def create_user_buttons():
            users = self.controller.user_data.keys()
            users = [x for x in users if x != self.controller.username]
            for i, user in enumerate(users):
                button = tk.Button(button_frame,
                                   command=partial(connect, user),
                                   text=user,
                                   relief="raised",
                                   borderwidth=3,
                                   width=20,
                                   height=2,
                                   anchor='n'
                                   )
                button.grid(row=i, column=0, pady=0)

        def update_list_box(messages):
            if len(messages) != self.controller.current_messages:
                lstbox.insert(0,messages[-1])
                self.controller.current_messages += 1
        
        def connect(username):
            self.controller.send_user = username
            self.controller.client.connect(
                int(self.controller.user_data[username]))
            self.current_user_label["text"] = f"{self.username} You are connected to {self.controller.send_user}"

        def send_message():
            # t = threading.Thread(target=self.controller.client.send_message,args=(message.get(),))
            # t.start()
            self.controller.client.send_message(message.get())
            message.set("")

        heading_label = tk.Label(self,
                                 text="P2P Chat App",
                                 font=('helvetica', 45, "bold"),
                                 foreground='white',
                                 background="#3d3d5c"
                                 )
        heading_label.pack(pady=25)

        select_user_label = tk.Label(self,
                                     text="Select User to talk",
                                     font=('helvetica', 13),
                                     fg='white',
                                     bg='#3d3d5c',
                                     anchor='w')
        select_user_label.pack(fill='x')

        ########################################
        chat_frame = tk.Frame(self, bg='#33334d')
        chat_frame.pack(fill='both', expand=True)

        button_frame = tk.Frame(chat_frame, bg='#33334d', width=200)
        button_frame.grid(row=0, column=0, padx=20)

        #########################################
        message_frame = tk.Frame(chat_frame, bg='#33334d')
        message_frame.grid(row=0, column=1, columnspan=3)

        self.current_user_label = tk.Label(message_frame,
                                      text=f"{self.username} You are connected to {self.controller.send_user}",
                                      font=('helvetica', 13),
                                      fg='white',
                                      bg='#3d3d5c',
                                      anchor='w')
        self.current_user_label.grid(row=0, column=1, pady=5)

        message_display_label = tk.Label(message_frame,
                                         text="Messages displayed here",
                                         font=('helvetica', 13),
                                         fg='white',
                                         bg='#3d3d5c',
                                         anchor='w')
        message_display_label.grid(row=1, column=1, pady=5)

        lstbox = tk.Listbox(message_frame, height=20, width=43)
        lstbox.grid(row=2, column=1, pady=5)

        write_message_label = tk.Label(message_frame,
                                       text="Write message here",
                                       font=('helvetica', 13),
                                       fg='white',
                                       bg='#3d3d5c',
                                       anchor='w')
        write_message_label.grid(row=3, column=1, pady=5)

        message = tk.StringVar()
        messagebox = tk.Entry(message_frame, textvariable=message, font=(
            'Helvetica', 10), border=2, width=32)
        messagebox.grid(row=4, column=1, pady=5)

        sendmessagebutton = tk.Button(
            message_frame, text="send", command=send_message, borderwidth=0)
        sendmessagebutton.grid(row=5, column=1, pady=5)

        def update_user_list():
            if self.controller.reg:
                user_list = self.controller.client.get_user_list_from_manager()
                all_user = user_list.split(',')
                for user in all_user:
                    username, port = user.split(':')
                    self.controller.user_data[username] = port
            create_user_buttons()
            all_messages = self.controller.client.all_messages
            update_list_box(all_messages)
            update_label.after(2000, update_user_list)

        update_label = tk.Label(self, height=0, width=0)
        update_label.pack()

        update_user_list()

    def update_widgets(self, username) -> None:
        self.username = self.controller.username
        self.current_user_label["text"] = f"{self.username} You are connected to {self.controller.send_user}"



if __name__ == '__main__':
    app = App()
    app.mainloop()
