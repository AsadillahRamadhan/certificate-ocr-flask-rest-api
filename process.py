import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

elements = ['nomor', 'nama', 'instansi', 'tanggal', 'event']
instansi = ['universitas', 'institut', 'politeknik']
nama_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
event = ['peserta', 'event', 'acara']

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def validationNomor(word):
  for i in range(len(word)):
    if word[i].isdigit():
      return True
  return False

def cariNomor(i, j):
  if '/'.lower() in sentences[i].lower() and '.' in sentences[i].lower() and validationNomor(sentences[i].lower()):
        if(validation[j] == False):
          contents[elements[j]] = sentences[i]
          validation[j] = True
  if 'nomor' in contents:
    if(' ' in contents['nomor']):
      contents['nomor'] = contents['nomor'].split(' ')
      for k in range(len(contents['nomor'])):
        if '/' in contents['nomor'][k]:
          contents['nomor'] = contents['nomor'][k]
          break

def cariNama(i, j):
  if 'kepada'.lower() in sentences[i].lower():
    if(validation[j] == False):
          for k in range(1, 10):
            if(sentences[i+k] != ' '):
              contents[elements[j]] = sentences[i+k]
              validation[j] = True
              break

def cariInstansi(i, j):
  if(validation[j] == False):
    for l in range(len(instansi)):
      if instansi[l].lower() in sentences[i].lower():
        contents[elements[j]] = sentences[i]
        validation[j] = True
        jenis_instansi = instansi[l]
        break

    if 'instansi' in contents:
      nama_instansi = []
      contents['instansi'] = contents['instansi'].split(' ')
      for i in range(len(contents['instansi'])):
        if(jenis_instansi.lower() in contents['instansi'][i].lower()):
          start_point = i
          break
      for i in range(start_point, len(contents['instansi'])):
        if(contents['instansi'][i].istitle() or contents['instansi'][i].isupper()):
            nama_instansi.append(contents['instansi'][i])
        else:
          break
      contents['instansi'] = ' '.join(nama_instansi)

def cariTanggal(i, j):
  if(validation[j] == False):
    for m in range(len(nama_bulan)):
        if nama_bulan[m].lower() in sentences[i].lower():
          contents[elements[j]] = sentences[i]
          validation[j] = True
          break

    if 'tanggal' in contents:
      tanggal_temp = []
      contents['tanggal'] = contents['tanggal'].split(' ')
      for i in range(len(contents['tanggal'])):
        for j in range(len(nama_bulan)):
          if nama_bulan[j] in contents['tanggal'][i]:
            index = i
      tanggal_temp.append(contents['tanggal'][index-1])
      tanggal_temp.append(contents['tanggal'][index])
      tanggal_temp.append(contents['tanggal'][index+1])
      contents['tanggal'] = ' '.join(tanggal_temp)

def cariEvent(i, j):
  if(validation[j] == False):
    for k in range(len(event)):
      if event[k].lower() in sentences[i].lower():
        contents[elements[j]] = sentences[i]
        validation[j] = True
        break

    if 'event' in contents:
      event_temp = []
      contents['event'] = contents['event'].split(' ')
      for i in range(len(contents['event'])):
        for j in range(len(event)):
          if event[j].lower() in contents['event'][i].lower():
            start = i
      for i in range(start + 1, len(contents['event'])):
        if contents['event'][i].istitle() or contents['event'][i].isdigit() or contents['event'][i].isupper():
          event_temp.append(contents['event'][i])
        else:
          break
      contents['event'] = ' '.join(event_temp)

def predict(file):
    global contents
    contents = {}
    global validation
    validation = [False] * len(elements)

    src = cv2.imread(file)
    image_processed = cv2.adaptiveThreshold(cv2.GaussianBlur(get_grayscale(src.copy()), (3,3), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)

    custom_config = r'-l ind --oem 3 --psm 6'
    history = pytesseract.image_to_string(image_processed, config=custom_config)
    global sentences
    sentences = history.split('\n')

    for i in range(len(sentences)):
        for j in range(len(elements)):
            if(j == 0):
                cariNomor(i, j)
            elif(j == 1):
                cariNama(i, j)
            elif(j == 2):
                cariInstansi(i, j)
            elif(j == 3):
                cariTanggal(i, j)
            elif(j == 4):
                cariEvent(i, j)

    return contents

