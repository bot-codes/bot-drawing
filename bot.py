from PIL import Image as img
import colorsys
from pynput.mouse import Controller
import keyboard
import os.path
import uuid
import winsound
from PIL import ImageGrab
import colorsys
import pyautogui
import sys
import pyfiglet

# Essa parte afetárá completamente a qualidade
# Nessa configuração atual o desenho é feito em torno de 1 minuto
espacoPixels = 2.5
tipoConversao = 'P'
quantidadeCores = 32
tamanhoImagemX = 100
tamanhoImagemY = 100
pularBranco = True
pyautogui.PAUSE = 1/100

'''
#Para configuração de qualidade máximma utilize assim:
espacoPixels = 1 #Diminua tamanho do Pincel pra 1px neste caso (entre 1 e 10... ajuste conforme o tamanho do pincel)
tipoConversao = 'RGB' (I,F,P,RGB)
quantidadeCores = 256 (entre 0 e 16 milhões mas 256 costuma ser muito bom)
tamanhoImagemX = 250 (entre 20 e 350)
tamanhoImagemY = 250  (entre 20 e 350)
pularBranco = False
pyautogui.PAUSE = 1/1000

#Vai levar de 10 à 20 minutos a imagem nessa configuração, qualidade HD
'''



globalConfig = []



def beep(freq):
    return winsound.Beep(freq, 1000)

def restarApp():
    os.execl(sys.executable, sys.executable, *sys.argv)


def ler_file(file):
    with open(file) as f:
        return list(map(int,(str(f.read()).split(','))))


def write_file(name, array):
    f= open(name,"w");
    f.write(','.join((str(v) for v in array)));
    f.close();

def configurarBOT():
    global globalConfig
    (x,y) = Controller().position
    globalConfig.append(x)
    globalConfig.append(y)
    beep(500)
    if(len(globalConfig) == 2):
        print ("2: Posicione o cursor em cima do icone de PALETA e dê ALT+X")
    if(len(globalConfig) == 4):
        print ("3: Posicione o cursor no canto inferior esquerdo do seletor de CORES e dê ALT+X")
    if(len(globalConfig) == 6):
        print ("4: Posicione o cursor na parte inferior da BARRA da PALETA e dê ALT+X")
    if(len(globalConfig) == 8):
        write_file("configs.log", globalConfig)
        print ("Sucesso: Seu bot está pronto! Cso haja algum erro deleta o arquivo config.logs para refazer o procedimento!")
        print ("Lembre-se de não alterar o zoom do navegador ou diminuir o tamanho da tela!\n")
        return restarApp()
    return triggerAltX()


lastRGB = "255,255,255"
def pixelar(R,G,B, canvas, ax, ay):
    global lastRGB
    if lastRGB != ("{0},{1},{2}".format(R,G,B)):
        lastRGB =  ("{0},{1},{2}".format(R,G,B))
        Hue, Saturation, Value = colorsys.rgb_to_hsv(R,G,B)
        pyautogui.click(globalConfig[2],globalConfig[3])
        pyautogui.click(globalConfig[4] + (Hue*180), globalConfig[5] - (Saturation*100))
        pyautogui.click( globalConfig[6], globalConfig[7] - (Value/2.55))
    pyautogui.click(canvas[0]+(ax*espacoPixels),canvas[1]+(ay*espacoPixels))



def screenshot():
    im = ImageGrab.grabclipboard()
    try:
        im.thumbnail((tamanhoImagemX,tamanhoImagemY), img.ANTIALIAS)
    except:
        print("Erro na imagem copiada, tente copiar e dar CTRL + B novamente")
        restarApp()
    beep(1000)
    return im.convert(tipoConversao, palette=img.WEB, colors=quantidadeCores).convert('RGB')

def checkPixel(imageMapPixels, x,y, tox, toy):
    if "{0}_{1}".format(x+tox, y+toy) not in imageMapPixels or  "{0}_{1}".format(x, y) not in imageMapPixels:
        return False
    return imageMapPixels["{0}_{1}".format(x, y)] != imageMapPixels["{0}_{1}".format(x+tox, y+toy)]

def mapImageToDictionary(imagem):
    imageMapPixels = {};
    imageMapColor = {}
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            pixel = imagem.getpixel((x, y))
            rgb = "%d,%d,%d" % ((pixel[0]), (pixel[1]), (pixel[2]));
            pixel = "%d_%d" % (x,y);
            if rgb not in imageMapColor.keys():
                imageMapColor[rgb] = []
            imageMapColor[rgb].append([x,y])
            imageMapPixels[pixel] = rgb
    return [imageMapPixels, imageMapColor]

def receberImagem():
    print ('Carregando imagem ...')
    global globalConfig
    canvas = list(Controller().position)
    pyautogui.click(globalConfig[0], globalConfig[1])
    print ('Mapeando imagem ...')
    imagem = screenshot();
    (imageMapPixels, imageMapColor) = mapImageToDictionary(imagem)
    print("Result: ", len(imageMapColor), "\n\nTekan Enter untuk memulai kembali")
    winsound.Beep(1500, 100)
    for rgb in imageMapColor.keys():
        R, G, B = (map(int,(rgb.split(','))))
        if R > 200 and G > 200 and B > 200 and pularBranco:
            continue
        conta = -1
        while(conta < len(imageMapColor[rgb]) - 1):
            if keyboard.is_pressed("ctrl+i"):
                restarApp()
            conta += 1
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], -1, -1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 1, 1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], -1, 0):
                    continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 0, -1):
                    continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 1, 0):
                    continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 0, 1):
                    continue
            pixelar(R,G,B, canvas, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])
            del imageMapPixels["{0}_{1}" .format( imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])]

    for rgb in imageMapColor.keys():
        R, G, B = (map(int,(rgb.split(','))))
        if R > 200 and G > 200 and B > 200 and pularBranco:
            continue
        conta = -1
        while(conta < len(imageMapColor[rgb]) - 1):
            if keyboard.is_pressed("ctrl+i"):
                restarApp()
            conta += 1
            if  "{0}_{1}" .format( imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1]) not in imageMapPixels:
                continue
            pixelar(R,G,B, canvas, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])

    input('Program Sucess!!!')
    restarApp()


def triggerAltX():
    while not keyboard.is_pressed("alt+x"):
        pass
    configurarBOT()

def iniciarPrograma():
    global globalConfig
    if os.path.exists('configs.log'):
        globalConfig = ler_file('configs.log')
        beep(3000)

        print("=========================\n")
        print(pyfiglet.figlet_format("WirdProject"))
        print("Project By WirdGates\n\nJangan Ganti Copyright\n\n\n=========================\n\n1:Arahkan Cursor Pada layar yang ingin anda drawing\n2:O Lalu tekan CTRL+B")
        while not keyboard.is_pressed("ctrl+b") and not keyboard.is_pressed("ctrl+i"):
            pass
        if keyboard.is_pressed("ctrl+b"):
            receberImagem()
        if keyboard.is_pressed("ctrl+i"):
            restarApp()
    else:
        beep(500)
        print("\n\n\n=========== PRIMEIRA EXECUCAO DO BOT, VAMOS CONFIGURAR ELE===============\n")
        print ("1: Posicione o cursor em CIMA do ícone do LÁPIS e dê ALT+X")
        triggerAltX()

iniciarPrograma()
