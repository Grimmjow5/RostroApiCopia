
import cv2
import os

class SaveImgs:


  def __init__(self, name,tipo="TMP"):
    self.name = name
    self.tipo = tipo
    self.pathMuestra = f"muestras/{self.name}/originales"
    self.imgFormat = f"muestras/{self.name}"

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
    print("listando")
    nn = os.listdir(f"muestras/{self.name}")
    print(nn)
    listaRutas = []
    nueva = []
    # Extensiones comunes de imágenes
    extensiones_imagen = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    for item in nn:
      # Verificar si el archivo es una imagen y no es 'originales'
      if item != "originales" and os.path.splitext(item)[1].lower() in extensiones_imagen:
        nueva.append(item)

    path = os.path.dirname(os.path.abspath(__file__))
    for i in nueva:
      listaRutas.append(os.path.join(f"{path}/../muestras/{self.name}/{i}"))

    return listaRutas

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
