from tkinter import *
from tkinter.messagebox import showinfo

import pyautogui

import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
import pyperclip as pc


import datetime
pytesseract.pytesseract.tesseract_cmd=r'C://Users//degal//AppData//Local//Tesseract-OCR//tesseract.exe'


class Application():

    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        self.path=''
        self.path1=''
        self.path2=''

        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")
        # abcd=self.pathfinder(root)



        # root.attributes("-transparent", "blue")
        # root.geometry('400x150+200+200')  # set new geometry
        # root.title('SnippingTool')
        # self.menu_frame = Frame(master, bg="blue")
        # self.menu_frame.pack(fill=BOTH, expand=YES)
        #
        # self.buttonBar = Frame(self.menu_frame,bg="")
        # self.buttonBar.pack(fill=BOTH,expand=YES)
        #
        # self.snipButton = Button(self.buttonBar,text="Take ScreenShot", width=15, command=self.createScreenCanvas, background="grey")
        # self.copyButton = Button(self.buttonBar,text="Copy from text",command=self.copypaste,background="grey")
        # self.copyButton.pack(expand=YES)
        # self.snipButton.pack(expand=YES)
        #
        #
        # self.master_screen = Toplevel(root)
        # self.master_screen.withdraw()
        # self.master_screen.attributes("-transparent", "blue")
        # self.picture_frame = Frame(self.master_screen, background = "blue")
        # self.picture_frame.pack(fill=BOTH, expand=YES)
        abcd = self.pathfinder(root)
        self.sniptool(root)
    def sniptool(self,root):
        root.attributes("-transparent", "blue")
        root.geometry('400x150+200+200')  # set new geometry
        root.title('SnippingTool')
        self.menu_frame = Frame(self.master, bg="blue")
        self.menu_frame.pack(fill=BOTH, expand=YES)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack(fill=BOTH, expand=YES)

        self.snipButton = Button(self.buttonBar, text="Take ScreenShot", width=15, command=self.createScreenCanvas,
                                 background="grey")
        self.copyButton = Button(self.buttonBar, text="Copy from text", command=self.copypaste, background="grey")
        self.copyButton.pack(expand=YES)
        self.snipButton.pack(expand=YES)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background="blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def pathfinder(self, root):
        root = tk.Tk()
        root.title('Tkinter File Dialog')
        root.resizable(False, False)
        root.geometry('400x400')

        def on_button_press1():
            self.path = fd.askdirectory(title='Select Folder')

            print(self.path)
            self.path1 = self.path + '/snippingData.txt'
            self.path2=self.path+'/ScreenShots/'
            a=os.path.isdir(self.path2)
            if not a:
                os.mkdir(self.path2)
            root.destroy()
        button = ttk.Button(root,text='Select Folder for Storing Data',command=on_button_press1)
        button.pack(expand=True)

    def copypaste(self):
        file_exists = os.path.exists(self.path1)

        text=pc.paste()
        if file_exists:
            try:
                fi = open(self.path1, 'a')
                fi.write('\n')
                fi.write('\n')
                fi.write(text)
            except:
                showinfo(
                    title='Selected Folder',
                    message='Please Select the Folder'
                )

        else:
            try:
                fi = open(self.path1, 'w+')

            except:
                showinfo(
                    title='Selected Folder',
                    message='Please Select the Folder'
                )





    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        # print(im.show())
        print(type(im))
        x = datetime.datetime.now()
        print(x)
        fileName = x.strftime("%f")
        print(fileName)
        im.save(self.path2 + fileName + ".png")
        img=Image.open(self.path2+fileName+".png")
        txt=pytesseract.image_to_string(img)

        print(txt)
        print(type(txt))

        im.save(self.path2 + fileName + ".png")
        a=os.path.exists(self.path1)
        print("path 1 is : ",self.path1)
        # if a:
        #     try:
        #         fi = open(self.path1, 'a')
        #         fi.write('\n')
        #         fi.write(txt)
        #         fi.close()
        #     except:
        #         print("please check ")
        # else:
        #     try:
        #         fi=open(self.path1,'w+')
        #         fi.write(txt)
        #
        #     except:
        #         showinfo(
        #             title='Selected Folder',
        #             message="Please Select the Folder"
        #         )
        fi = open(self.path1, 'a')
        fi.write('\n')
        fi.write(txt)
        fi.close()


        # fi = open("C://Users//degal//Desktop//SnipData.txt", 'a')
        # fi.write('\n')
        # fi.write(txt)
        # fi.close()

        self.exitScreenshotMode()

    def createScreenCanvas(self):
        print("abcdefghijklmno")
        if not os.path.isdir(self.path2):
            showinfo(
                title='Selected Folder',
                message="Please Select a Folder"
            )
            self.exitScreenshotMode()
        self.master_screen.deiconify()
        # root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.recPosition()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            print("right down")
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            print("left down")
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            print("right up")
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            print("left up")
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        print(event.x," ",event.y)
        return event

    def exitScreenshotMode(self):
        print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    # def exit_application(self):
    #     print("Application exit")
    #     root.quit()

    def on_button_press(self, event):
        # save mouse drag start position


        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)

if __name__ == '__main__':
    root = Tk()
    ac=Application(root)
    root.mainloop()
