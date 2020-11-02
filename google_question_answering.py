from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk

import sys
from urllib import parse
import time
import argparse
import os
from functools import wraps


driver = webdriver.Chrome('./chromedriver')


class OptionsPopupWindow(Tk):
    def __init__(self, options=[]):
        super().__init__()
        self.value = None
        self.buttons = [
            Button(self,text=options[i],command=self.generate_submit_function(i))
            for i in range(0, len(options))
        ]
        for button in self.buttons:
            button.pack()
        if self.buttons:
            self.buttons[0].focus()
            self.buttons[0].bind('<Return>', self.generate_submit_function(0))
        
        self.e=Entry(self)
        self.e.pack()
        self.submit_button = Button(self, text="Done", command=self.submit)
        self.submit_button.pack()
        
    def generate_submit_function(self, i):
        def f(event=None):
            self.value=self.buttons[i]["text"]
            self.destroy()
        return f
        
    def submit(self):
        self.value=self.e.get()
        self.destroy()

def prompt_options(options):
    app = OptionsPopupWindow(options=options)
    app.mainloop()
    return app.value


class ProblemPopupWindow(Tk):
    def __init__(self, message):
        super().__init__()
        self.value = None
        self.label = Label(self, width=120, height=10,
            text=f"A problem occured: {message}\nPlease solve it and click resume or skip")
        self.label.pack()
        self.resume_button = Button(self,text="Resume",command=self.resume)
        self.resume_button.pack()
        self.skip_button = Button(self,text="Skip",command=self.skip)
        self.skip_button.pack()
        
    def resume(self):
        self.value="resume"
        self.destroy()
        
    def skip(self):
        self.value="skip"
        self.destroy()


def prompt_problem(message):
    app = ProblemPopupWindow(message)
    app.mainloop()
    return app.value

def fix_problem(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resume_or_skip = "resume"
        try: 
            func(*args, **kwargs)
        except Exception as e:
            print(e)
            resume_or_skip = prompt_problem(f"Problem in {func.__name__}: {str(e)}")
        return resume_or_skip
    return wrapper

def validate_options(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return prompt_options(res)
    return wrapper

def get_answers_from_page():
    html_doc = driver.page_source
    #open("out.txt", "w").write(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    answers = soup.findAll("div", {"data-tts" : "answers"})
    answers = [answer["data-tts-text"] for answer in answers]
    assert len(answers) >= 1, "No answer for the question returned by google"
    return answers

@fix_problem
def hit_search(question):
    driver.get('https://google.com')
    time.sleep(1)
    search_input = driver.find_element(By.NAME, "q")
    search_input.send_keys(question + "\n")
    time.sleep(1)
    _ = get_answers_from_page()

@validate_options
def ask_google(question):
    skip_or_resume = hit_search(question)
    if skip_or_resume == "skip":
        return []
    elif skip_or_resume == "resume":
        return get_answers_from_page()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get response from Google Question Answering with human visual validation')
    parser.add_argument('--question', help='Question to ask',
        nargs='*', dest='questions')

    args = parser.parse_args()
    print(args.questions)
    for question in args.questions:
        print(f"found response {ask_google(question)} for question {question}")



