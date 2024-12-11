
import cv2
import os
import imutils

class SaveImgs:


  def __init__(self, name,tipo="TMP"):
    self.name = name
    self.tipo = tipo
    self.pathMuestra = f"muestras/{self.name}/originales"
    self.imgFormat = f"muestras/{self.name}"
    self.pathVideo = f"muestras/{self.name}/video"

    if tipo != "TMP":
      if not os.path.exists(self.imgFormat):
        os.makedirs(self.imgFormat)
      if not os.path.exists(self.pathMuestra):
        print("Creando Directorio")
        os.makedirs(self.pathMuestra)


    if os.name == 'nt':
      self.pathTmp = f"C:\\Users\\traba\\AppData\\Local\\Temp\\"
    else:
      self.pathTmp = "/tmp/"

  def Verificacion(self,path)->bool:
    #Recordemos que esta comparacion solo se hace con uns dos fotos, una de muestra y otra que se ingresa,
    #Entonces el plan es tener mas de 1 foto de muestra pra comparar multiples veces, al mismo tiempo y

    img1 = cv2.imread(path,0)

    img2 = cv2.imread(f"{self.pathTmp}/{self.name}.jpg",0)

    orb = cv2.ORB_create()

    kpa, descriptorA = orb.detectAndCompute(img1, None)
    kpb, descriptorB = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(descriptorA, descriptorB)

    similares = [ i for i in matches if i.distance < 70 ]

    rango = 0

    if len(matches) == 0:
      rango = 0
    else:
      rango = len(similares)/len(matches)

    if rango >= 0.96:
      return True
    else:
      return False


  #Retorna donde se guardo la imagen
  def SaveFile(self,file,numero):
    if not os.path.exists(self.pathMuestra):

      os.makedirs(self.pathMuestra)
    #En esta parte puede ser posible, con un array
    print(self.pathMuestra)
    file.save(os.path.join(self.pathMuestra, f"muestra_{self.name+str(numero)}.jpg"))
    return os.path.join(self.pathMuestra, f"muestra_{self.name+str(numero)}.jpg")

  def SaveFileVideo(self,file):
    if not os.path.exists(self.pathVideo):
      os.makedirs(self.pathVideo)
    file.save(os.path.join(self.pathVideo, f"{self.name}.mp4"))
    return os.path.join(self.pathVideo, f"{self.name}.mp4")

  def ExtracImg(self,pathVideo:str):
    video = cv2.VideoCapture(pathVideo)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    while True:
      ret, frame = video.read()
      if ret == False: break
      frame = imutils.resize(frame, width=640)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      auxFrame = frame.copy()

      faces = faceCascade.detectMultiScale(gray, 1.3, 5)
      for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, +h),(0,255,0), 2)
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro,dsize=(150,150),interpolation=cv2.INTER_CUBIC)
        grays = cv2.cvtColor(rostro, cv2.COLOR_BGR2GRAY)
        if count % 15 == 0:
          cv2.imwrite(self.imgFormat + f"/{self.name}{count}.jpg", grays)
        count = count + 1
      if count == 300: break
    cv2.destroyAllWindows()
    video.release()
  def extract_faces_relevant_parts(self, pathVideo: str, num_faces: int = 100):
    video = cv2.VideoCapture(pathVideo)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Obtener información del video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Total frames: " + str(total_frames))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    duration = total_frames / fps
    # Dividir el video en tres partes
    part_frames = total_frames // 3
    count = 0
    saved_faces = 0
    interval = part_frames // (num_faces // 3)
    # Espacio entre las capturas dentro de cada parte
    while True:
      ret, frame = video.read()
      if not ret or saved_faces >= num_faces: break
      frame_pos = int(video.get(cv2.CAP_PROP_POS_FRAMES))
      if frame_pos % interval == 0: # Tomar una imagen en el intervalo definido
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces: cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rostro = auxFrame[y:y + h, x:x + w]
        rostro = cv2.resize(rostro, dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
        grays = cv2.cvtColor(rostro, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(self.imgFormat + f"/{self.name}{count}.jpg", grays)
        count += 1
        saved_faces += 1
    cv2.destroyAllWindows()
    video.release()


  def SaveFileTemp(self,file):
    print(self.pathTmp)
    file.save(os.path.join(self.pathTmp, f"{self.name}.jpg"))
    return os.path.join(self.pathTmp, f"{self.name}.jpg")


  def FormatImg(self,ruta:str,numero:int):
    image = cv2.imread(ruta)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Carga de modelo
    faceClasifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = faceClasifier.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
      cv2.rectangle(image, (x,y), (x+w, +h), (0,255,0), 2)
      rostro = gray[y:y+h, x:x+w]
      resizeImg = cv2.resize(rostro, dsize=(150,150), interpolation=cv2.INTER_CUBIC)
      if self.tipo == "TMP": #O LA NUEVA MUESTRA
        cv2.imwrite(self.pathTmp + f"{self.name}.jpg", resizeImg)
      else:
        print("Save in format TMP")
        print(self.imgFormat + f"/{self.name+str(numero)}.jpg", resizeImg)
        cv2.imwrite(self.imgFormat + f"/{self.name+str(numero)}.jpg", resizeImg)
    print("Formato Exitoso")

  def listarMuestras(self):
    nn = os.listdir(f"muestras/{self.name}")
    listaRutas = []
    nueva = []
    # Extensiones comunes de imágenes
    extensiones_imagen = {'.jpg', '.jpeg', '.png'}
    for item in nn:
      # Verificar si el archivo es una imagen y no es 'originales'
      if item != "originales" and os.path.splitext(item)[1].lower() in extensiones_imagen:
        nueva.append(item)
    print("Lista de imágenes")
    print(nueva)
    print("Lista de imágenes")
    path = os.path.dirname(os.path.abspath(__file__))
    for i in nueva:
      listaRutas.append(os.path.join(f"{path}/../muestras/{self.name}/{i}"))
    return listaRutas
  def listarMuestrasSinPath(self):
    nn = os.listdir(f"muestras/{self.name}")
    listaRutas = []
    nueva = []
    # Extensiones comunes de imágenes
    extensiones_imagen = {'.jpg', '.jpeg', '.png'}
    for item in nn:
      # Verificar si el archivo es una imagen y no es 'originales'
      if item != "originales" and os.path.splitext(item)[1].lower() in extensiones_imagen:
        nueva.append(item)
    return nueva


    '''
    print("listando")
    nn = os.listdir(f"muestras/{self.name}")
    listaRutas = []
    nueva  = []
    for item in nn:
      if item != "originales":
        nueva.append(item)
    for i in nueva:
      listaRutas.append(os.path.join(f"muestras/{self.name}/{i}"))
    return listaRutas
  '''

  #def SaveFileTemp(self,file):
