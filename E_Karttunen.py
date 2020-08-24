#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import json
import re

with open('karttunen.json', 'r') as k:
    karttunen = json.load(k)

print('Nr. entries in Karttunen:', len(karttunen), '\n==============================')

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("E-Karttunen")
        self.master.geometry('1000x700')
       # self.pack()
       # self.grid(sticky='nsew')
        self.place()

        self.create_widgets()


    def create_widgets(self):
        self.first = tk.Label(self.master, 
                                width=115, 
                                height=40, 
                                bg='black')
        self.first.place(relx=.5, rely=.5, anchor='c')


        ###################
        ##
        ##   TOP BAR
        ##
        ###################
        self.top_bar = tk.Label(self.first, 
                                height=3,
                                width=105,
                                bg='grey', 
                              #  text='TOP BAR',
                                anchor='n')
        self.top_bar.place(relx=.5, rely=.01, anchor='n')

        self.search_lab = tk.Label(self.top_bar,
                                height=1,
                                width=39,
                                bg='grey',
                                text='Search String:',
                                padx=1,
                                anchor='c')
        self.search_lab.place(relx=.195, rely=.1, anchor='n')

        self.search_entry = tk.Entry(self.top_bar,
                                width=39)
                                #bg='pink')
        self.search_entry.place(relx=.195, rely=.5, anchor='n')

        self.search = tk.Button(self.top_bar,
                                width=13,
                                text="Search",
                                command=self.init_search)
        self.search.place(relx=.485, rely=.35, anchor='n')

        self.clear = tk.Button(self.top_bar,
                                width=13,
                                text="Clear Search",
                                command=self.clear_search)
        self.clear.place(relx=.65, rely=.35, anchor='n')
    
        self.search_target = tk.StringVar()
        self.search_in = ttk.Combobox(self.top_bar,
                                width=13,
                                textvariable=self.search_target)
        self.search_in["values"] = ('Nahuatl', 'English', 'Spanish')
        self.search_in.current(0)
        self.search_in.place(relx=.92, rely=.1, anchor='n')

        self.search_in_lab = tk.Label(self.top_bar,
                                text="Searching in:",
                                bg='grey')
        self.search_in_lab.place(relx=.795, rely=.1, anchor='n')

        self.search_type = tk.StringVar()
        self.search_like = ttk.Combobox(self.top_bar,
                                width=13,
                                textvariable=self.search_type)
        self.search_like["values"] = ('Substring','Exact Match')
        self.search_like.current(0)
        self.search_like.place(relx=.92, rely=.5, anchor='n')

        self.search_like_lab = tk.Label(self.top_bar,
                                text="Search type:",
                                bg='grey')
        self.search_like_lab.place(relx=.796, rely=.5, anchor='n')

        ###################
        ##
        ##   LEFT COLUMN
        ##
        ###################
        self.left_col = tk.Label(self.first,
                                width=40,
                                height=35,
                                bg='#282828')
        self.left_col.place(relx=.217, rely=.1, anchor='n')

        self.result_hws = tk.Listbox(self.left_col,
                            #    width=39,
                            #    height=33,
                                bg='grey')
        self.result_hws.place(relheight=1, relwidth=1)#relx=.5, rely=.5, anchor='c')
        self.result_hws.bind('<<ListboxSelect>>', self.show_hw_res)

        self.L_scrollbar = tk.Scrollbar(self.result_hws, 
                                orient='vertical')
        self.L_scrollbar.place(relx=.97, relheight=1)

        ###################
        ##
        ##   RIGHT COLUMN
        ##
        ###################        
        self.right_col = tk.Canvas(self.first,
                                width=500,#62,
                                height=596,#35,
                               # bg='yellow',
                                bg='#282828') #,
  #                              text='RIGHT COL')
        self.right_col.place(relx=.687, rely=.1, anchor='n')

        self.hw_details = tk.Canvas(self.right_col,
                            #    width=39,
                            #    height=20,
                                bg='grey')
        self.hw_details.place(relheight=1, relwidth=1)#.975)

       # self.R_scrollbar = tk.Scrollbar(self.right_col,
       #                         orient='vertical')
       # self.R_scrollbar.place(relx=.975, relheight=1)
        

        ###################
        ##
        ##   FUNCTIONS
        ##
        ###################        

    def init_search(self):
        self.search_term = self.search_entry.get().lower()
        self.result_hws.delete(0,'end')
        if len(self.search_term) > 0 :
            print('You searched for:', self.search_term)

            # IF NAHUATL
            self.search_target = self.search_in.get()
            self.search_in.current(self.search_in['values'].index(self.search_target))            
            if self.search_target == 'Nahuatl':            
                self.search_type = self.search_like.get()
                self.search_like.current(self.search_like['values'].index(self.search_type))
                print("Searching in: Nahuatl")

                print('Search Type:', self.search_type)
                self.L_scrollbar.config(command=self.result_hws.yview)
                self.result_hws.config(yscrollcommand=self.L_scrollbar.set)

                if self.search_type == 'Substring':
                    self.regex_term = re.compile('.*(%s).*'%self.search_term).match
                    self.sub_dict = {k:v for k,v in karttunen.items() if self.regex_term(k)}
                    print('Hits:', len(self.sub_dict))
                    for k,v in self.sub_dict.items():
                        self.result_hws.insert('end', k)

                if self.search_type == 'Exact Match':
                    if self.search_term in karttunen:
                        self.result_hws.insert('end', self.search_term)
                    mb.showinfo(title="Search Tip", message="Karttunen's headwords are sometimes broken by hyphens to indicate morphology (e.g., and esp. absolutive endings on nouns) and parentheses to indicate optional / variation in phonemes. If these 'special characters' are not included in the search, but appear in the entry, there will be no hit.")
            else:
                mb.showerror(title='Error', message="English and Spanish don't work yet. Search in Nahuatl.")
        else:
            print('Oi! Enter a search term, mate.')
            mb.showerror(title="Hold up!", message="Lookie here mang... \nYou need to enter a search term if you expect to find anything.")

    def show_hw_res(self, evt):
        self.selected_hw = self.result_hws.get(self.result_hws.curselection())
        print(karttunen[self.selected_hw])

        slaves = self.hw_details.pack_slaves()
        for slave in slaves:
            slave.destroy()

     #   self.R_scrollbar.config(command=self.hw_details.yview)
      #  self.hw_details.config(yscrollcommand=self.R_scrollbar.set)

        self.hw_self = tk.Label(self.hw_details,
                            text=self.selected_hw,
                            bg='grey',
                            pady=10,
                            font=('times', 24))
        self.hw_self.pack()

        
        if 'Grammar' in karttunen[self.selected_hw]:
            self.hw_grammar_lab = tk.Label(self.hw_details,
                                    text = "Grammar information:",
                                    height=2,
                                    padx=10, pady=5,
                                    anchor='sw',
                                    bg='grey',
                                    font=('times', 10))
            self.hw_grammar_lab.pack(fill='x')
            self.hw_grammar = tk.Label(self.hw_details,
                                    text = karttunen[self.selected_hw]['Grammar'],
                                    padx=10,
                                    anchor='w',
                                    wraplength=475, justify='left',
                                    bg='grey',
                                    font=('times', 14))
            self.hw_grammar.pack(fill='x')


        if 'English' in karttunen[self.selected_hw]:
            self.hw_english_lab = tk.Label(self.hw_details,
                                    text = "English:",
                                    height=2,
                                    padx=10, pady=5,
                                    anchor='sw',
                                    bg='grey',
                                    font=('times', 10))
            self.hw_english_lab.pack(fill='x')
            self.hw_english = tk.Label(self.hw_details,
                                    text = karttunen[self.selected_hw]['English'],
                                    padx=10,
                                    anchor='w',
                                    wraplength=475, justify='left',
                                    bg='grey',
                                    font=('times', 14))
            self.hw_english.pack(fill='x')
 
        if 'Spanish' in karttunen[self.selected_hw]:
            self.hw_spanish_lab = tk.Label(self.hw_details,
                                    text = "Spanish:",
                                    height=2,
                                    padx=10, pady=5,
                                    anchor='sw',
                                    bg='grey',
                                    font=('times', 10))
            self.hw_spanish_lab.pack(fill='x')
            self.hw_spanish = tk.Label(self.hw_details,
                                    text = karttunen[self.selected_hw]['Spanish'],
                                    padx=10,
                                    anchor='w',
                                    wraplength=475, justify='left',
                                    bg='grey',
                                    font=('times', 14))
            self.hw_spanish.pack(fill='x')

    
        if 'Comment' in karttunen[self.selected_hw]:
            self.hw_comment_lab = tk.Label(self.hw_details,
                                    text = "Comment:",
                                    height=2,
                                    padx=10, pady=5,
                                    anchor='sw',
                                    bg='grey',
                                    font=('times', 10))
            self.hw_comment_lab.pack(fill='x')
            self.hw_comment = tk.Label(self.hw_details,
                                    text = karttunen[self.selected_hw]['Comment'],
                                    padx=10,
                                    anchor='w',
                                    wraplength=475, justify='left',
                                    bg='grey',
                                    font=('times', 14))
            self.hw_comment.pack(fill='x')


        if 'Lexical Reference' in karttunen[self.selected_hw]:
            self.hw_lexref_lab = tk.Label(self.hw_details,
                                    text = "See also:",
                                    height=2,
                                    padx=10, pady=5,
                                    anchor='sw',
                                    bg='grey',
                                    font=('times', 10))
            self.hw_lexref_lab.pack(fill='x')
            self.hw_lexref = tk.Label(self.hw_details,
                                    text = karttunen[self.selected_hw]['Lexical Reference'],
                                    padx=10,
                                    anchor='w',
                                    wraplength=475, justify='left',
                                    bg='grey',
                                    font=('times', 14))
            self.hw_lexref.pack(fill='x')

        if "Source" in karttunen[self.selected_hw]:
            self.hw_src_lab = tk.Label(self.hw_details,
                                    text = "Karttunen's source:",
                                    height=2,
                                    padx=10, pady=5,
                                    anchor='sw',
                                    bg='grey',
                                    font=('times', 10))
            self.hw_src_lab.pack(fill='x')
            self.hw_src = tk.Label(self.hw_details,
                                    text = karttunen[self.selected_hw]['Source'],
                                    padx=10,
                                    anchor='w',
                                    wraplength=475, justify='left',
                                    bg='grey',
                                    font=('times', 14))
            self.hw_src.pack(fill='x')


    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.result_hws.delete(0,'end')
        self.search_like.current(self.search_like['values'].index(self.search_type))
        slaves = self.hw_details.pack_slaves()
        for slave in slaves:
            slave.destroy()




def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
	main()
