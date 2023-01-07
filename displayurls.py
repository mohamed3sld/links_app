from tkinter import *
from tkinter import messagebox
import sqlite3
import webbrowser
import re
from tkinter import ttk

con = sqlite3.connect('database_urls.db')
cur = con.cursor()


class DisplayU(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Display Links')
        self.iconbitmap("icons/display.ico")
        self.state('zoomed')

        self.regex2 = re.compile(r'^[a-zA-Z0-9].{1,50}')
    
        #Frames
        self.top = ttk.Frame(self, height=120)
        self.top.pack(fill=X)
        self.buttomFrame = ttk.Frame(self, height=500)
        self.buttomFrame.pack(fill=X)


        self.top_image = PhotoImage(file='icons/links.png')
        self.top_image_lbl = ttk.Label(self.top, image=self.top_image)
        self.top_image_lbl.place(x=120, y=10)
        self.heading = ttk.Label(self.top, text='Links Page', font='arial 25 bold')
        self.heading.place(x=260, y=40)


        #Scroll For ListBox
        self.sb = ttk.Scrollbar(self.buttomFrame, orient=VERTICAL)

        #List Box
        self.listBox = Listbox(self.buttomFrame, width=130, height=30, bg='white', font='arial 12 bold', bd=8)
        self.listBox.grid(row=0, column=0, padx=10)
        self.listBox.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.listBox.yview())
        self.sb.grid(row=0, column=1, sticky=S+N)


        #button
        self.updateicon = PhotoImage(file='icons/update.png')
        self.deleteicon = PhotoImage(file='icons/delete.png')
        self.go_to_link = PhotoImage(file='icons/go_to_link.png')
        self.copyicon = PhotoImage(file='icons/copyicon.png')
        self.btn_delete = ttk.Button(self.buttomFrame, text='  Delete Link  ', command=self.funcdelete, compound=LEFT, image=self.deleteicon, width=30).place(x=1260, y=20)
        self.btn_go = ttk.Button(self.buttomFrame, text='  Open Link  ', command=self.funcgoToLink, compound=LEFT, image=self.go_to_link, width=30).place(x=1260, y=75)
        self.btn_update = ttk.Button(self.buttomFrame, text=' Update Link ', command=self.update_1, compound=LEFT, image=self.updateicon, width=30).place(x=1260, y=130)
        self.btn_copyID = ttk.Button(self.buttomFrame, text='      Copy ID ', command=self.copy_func, compound=LEFT, image=self.copyicon, width=30)
        self.btn_copyID.place(x=1260, y=185)



        #search input
        global btn_reset
        self.icon_search = PhotoImage(file='icons/search.png')
        self.icon_reset = PhotoImage(file='icons/reset.png')
        self.search = ttk.Entry(self.top, font='arial 17 bold', width=30)
        self.search.place(relx=0.5, y=48, x=40)
        self.btn_search = ttk.Button(self.top, text='  Search  ', image=self.icon_search , command=self.funcsearch, width=12 , compound=LEFT).place(x=686, y=48)
        btn_reset = ttk.Button(self.top, text='  Reset  ', image=self.icon_reset, command=self.funcreset, width=12, compound=LEFT)
        btn_reset.place(x=580, y=48)

        self.n = StringVar()
        self.monthchoosen = ttk.Combobox(self.top, width=8, textvariable=self.n, font='arial 10 bold')
        self.monthchoosen.place(relx=0.7,x=135,y=53)

        self.mychoices = (' Group',' Website', ' Account',' App')
        self.monthchoosen['values'] = self.mychoices



        #keys keyboard
        self.search.bind('<Return>', self.funcsearch)
        self.monthchoosen.bind('<Return>', self.funcsearch)
        self.bind('<Delete>', self.funcdelete)
        self.bind("<Control-c>", self.copy_func)
        self.bind("<Control-C>", self.copy_func)





        links = cur.execute('SELECT * FROM links').fetchall()
        count = 0
        for link in links:
            self.listBox.insert(count, str(link[0])+'  --------  '+link[3]+' -'+link[1]+'  -------- >  '+link[2])
            count += 1

        #LABEL COUNT
        self.counter = Label(self.buttomFrame, text=f'{count}\nLINKS', font='times 40 bold', fg='gray')
        self.counter.place(x=1290, y=300)
        #___________



    def funcdelete(self, *args):
        try:
            selected_link = self.listBox.curselection()
            link = self.listBox.get(selected_link)
            id1 = int(link[:link.index(' ')])

            message = messagebox.askyesno('Warning', 'Are you sure you deleted the link?', icon='warning')

            if message:
                try:
                    cur.execute("DELETE FROM links WHERE id=?", (id1,))
                    con.commit()
                    self.listBox.delete(selected_link)
                except:
                    messagebox.showinfo('info', 'Link has no been deleted', icon='warning')

        except:
            messagebox.showerror('Error', 'Please select the link you want to delete!', icon='warning')






    def copy_func(self, *args):
        selected_link = self.listBox.curselection()
        link = self.listBox.get(selected_link)
        id1 = int(link[:link.index(' ')])
        self.clipboard_clear()
        self.clipboard_append(id1)
        messagebox.showinfo('Copied', "ID has been copied")



    def funcgoToLink(self):
        try:
            selected_link = self.listBox.curselection()
            link = self.listBox.get(selected_link)
            url = link[link.index('>')+3:]
            webbrowser.open_new_tab(url)
        except:
            messagebox.showerror('Error', 'Please select the link to access it!', icon='warning')

    


    def funcsearch(self, *args):
        search_text = self.search.get()# The text that was typed in the search input.
        self.listBox.delete(0, END)
        result = cur.execute("SELECT * FROM links").fetchall()



        for i in result:
            if search_text:
                if (search_text.lower() in i[1].lower()) or (search_text in str(i[0])):
                    self.listBox.insert(0, str(i[0])+'  --------  '+i[1]+'  -------- >  '+i[2])

            elif self.n.get() in i[3]:
                self.listBox.insert(0, str(i[0]) + '  --------  ' + i[1] + '  -------- >  ' + i[2])


        btn_reset.config(state='normal')
           



    def funcreset(self):
        self.listBox.delete(0, END)# Delete all items in ListBox.
        links = cur.execute('SELECT * FROM links').fetchall()# Select all items in the DataBase to add to the ListBox again.
        count1 = 0 
        for link in links:# Loop over elements that are called from the database.
            self.listBox.insert(count1, str(link[0])+'  --------  '+link[1]+'  -------- >  '+link[2])
            count1 += 1
 
        self.counter.configure(text=f'{count1}\nLINKS')
        btn_reset.config(state=DISABLED)



    def update_1(self):
        try:
            global link_id
            selected_link = self.listBox.curselection()
            link = self.listBox.get(selected_link)
            link_id = int(link[:link.index(' ')])
            update_link = Update_link()
        except:
            messagebox.showerror('Error', 'Please select the link to change your information!', icon='warning')



class Update_link(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry('700x300')
        self.resizable(False, False)
        self.title('Update Link')
        self.config(bg='#434242')
        self.iconbitmap("icons/app-development.ico")


        global link_id

        link = cur.execute('SELECT * FROM links WHERE id=?', (link_id,)).fetchall()
        url = link[0][2]
        name = link[0][1]


        self.icon_add = PhotoImage(file='icons/add.png')
        self.icon_url_add = PhotoImage(file='icons/urladd.png')
        self.icon_name = PhotoImage(file='icons/name.png')



        self.regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
       

        self.enturl = Label(self, text='Enter The Url:', fg='#22A39F', bg='#434242', font='times 15 bold').place(x=40, y=40)
        self.addurl = Entry(self, width=30, bg='#F3EFE0', fg='#222222', font='arial 15 bold')
        self.addurl.insert(0,url)
        self.addurl.place(x=240, y=40)
        self.urlimage = Label(self, image=self.icon_url_add, bg='#434242').place(x=590, y=40)

        self.entname = Label(self, text='Enter The Name:', fg='#22A39F', bg='#434242', font='times 15 bold').place(x=40, y=100)
        self.addname = Entry(self, width=30, bg='#F3EFE0', fg='#222222', font='arial 15 bold')
        self.addname.insert(0,name)
        self.addname.place(x=240, y=100)
        self.name = Label(self, image=self.icon_name, bg='#434242').place(x=590, y=100)



        #Button
        self.btn_add = Button(self, text='  Update the Link ', font='arial 15 bold', bg='#678983', fg='#181D31', command=self.funcupdate, image=self.icon_add, compound=LEFT).place(relx = 0.5, rely = 0.7, anchor = CENTER)
 
    
    def funcupdate(self):
        if re.findall(self.regex, self.addurl.get()):
            url = self.addurl.get()
            name = self.addname.get()

            message = messagebox.askyesno('Warning', 'Are You Sure?', icon='warning')
            if message == True:
                try:
                    query = "UPDATE links set url=?, name=? WHERE id=?"
                    cur.execute(query, (url, name, link_id))
                    con.commit()
                    messagebox.showinfo('Success', 'Link has been updated', icon='info')
                    self.destroy()
                    btn_reset.config(state='normal')



                except:
                    messagebox.showinfo('Warning', 'Link has not been updated', icon='warning')
        else:
            messagebox.showinfo('Warning', 'This Link is Wrong', icon='warning')