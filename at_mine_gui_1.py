# -*- coding: utf-8 -*-

#import time
#import numpy as np
from tqdm import tqdm
import requests as re
from bs4 import BeautifulSoup as bs
import tkinter as tk

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url_template = 'https://youdao.com/result?word={}&lang=en'

def get_word (word, retry = 5):
    url = url_template.format (word)
    i = True
    count = retry
    while i and count:
        print ('try {}'.format (word))
        i = False
        try:
            re0 = re.get (url, headers = headers)
        except:
            i = True
            count = count - 1
            print ('retry: {}'.format (word))
    if not count:
        print ('HTTP: {}'.format (word))
        return 'HTTP Error!'
    sp0 = bs (re0.text, 'lxml')
    sp1 = sp0.find ('body')
    sp2 = sp1.find ('div', {'class':'dict-book'})
    if sp2:
        sp_phonetic = sp1.find_all ('span', {'class' : 'phonetic'})
        sp_pos = sp2.find_all ('span', {'class':'pos'})
        sp_trans = sp2.find_all ('span', {'class':'trans'})
        phonetic = ' '.join (i.text for i in sp_phonetic)
        trans = '\n'.join ('{} {}'.format (pos.text, sp_trans [i].text) for i, pos in enumerate (sp_pos))
        trans_result = '\n'.join ([word, phonetic, trans, word])
        print ('Success: {}'.format (word))
    else:
        trans_result = 'Plz check! ({})'.format (word)
        print ('Check: {}'.format (word))
    return trans_result

def get_phrase (word, retry = 5):
    fixed_word = '%20'.join (word.split())
    url = url_template.format (fixed_word)
    success = False
    for count in range (retry):
        print ('try {}'.format (word))
        try:
            re0 = re.get (url, headers = headers)
            success = True
            break
        except:
            print ('retry: {}'.format (word))
    if not success:
        print ('HTTP: {}'.format (word))
        return 'HTTP Error!'
    sp0 = bs (re0.text, 'lxml')
    sp1 = sp0.find ('body')
    sp2 = sp1.find ('div', {'class':'dict-book'})
    if sp2:
        sp_trans = sp2.find_all ('span', {'class':'trans'})
        trans = '\n'.join (i.text for i in sp_trans)
        trans_result = '\n'.join ([word, trans, word])
        print ('Success: {}'.format (word))
    else:
        trans_result = 'Plz check! ({})'.format (word)
        print ('Check: {}'.format (word))
    return trans_result

def get_list (word_txt):
    trans_result = []
    #time.sleep (0.2 * np.random.random())
    for i in tqdm (word_txt.split ('\n')):
        if i:
            word = i.strip ()
            if word:
                trans_result.append (get_phrase (word) if ' ' in word else get_word (word))
    return '\n\n'.join (trans_result)

window = tk.Tk ()

wtxt1 = tk.Text (window)
wtxt2 = tk.Text (window)

img = tk.PhotoImage (file = 'youdao.png')
lab1 = tk.Label (window, image = img)

def but1_func ():
    wtxt2.delete (1.0, tk.END)
    word_txt = wtxt1.get ('1.0', tk.END)
    trans_txt = get_list (word_txt)
    wtxt2.insert('1.0', trans_txt)
    window.clipboard_clear ()
    window.clipboard_append (trans_txt)
    
but1 = tk.Button (window, text='翻译', command = but1_func)

def but2_func ():
    wtxt1.delete (1.0, tk.END)
    try:
        wtxt1.insert(tk.INSERT, window.clipboard_get())
    except tk.TclError:
        wtxt1.insert(tk.INSERT, '获取失败')
    but1_func ()
    
but2 = tk.Button (window, text='获取剪贴板并翻译', command = but2_func)

def but3_func ():
    wtxt1.delete (1.0, tk.END)
    wtxt2.delete (1.0, tk.END)
    
but3 = tk.Button (window, text='清空输入框', command = but3_func)

but_exit = tk.Button (window, text='退出', command = window.quit)

window.title ('AutoTranslator')
window.geometry ('960x540+60+20')
wtxt1.place (x = 10, y = 10, width = 350, height = 520)
wtxt2.place (x = 600, y = 10, width = 350, height = 520)
lab1.place (x = 365, y = 30, width = 220, height = 60)
but1.place (x = 370, y = 160, width = 210, height = 50)
but2.place (x = 370, y = 240, width = 210, height = 50)
but3.place (x = 370, y = 320, width = 210, height = 50)
but_exit.place (x = 370, y = 400, width = 210, height = 50)

window.mainloop ()
window.destroy ()
