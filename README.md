# HACKATHON_LateCheck-

AgroScan IA - Detector de Enfermedades en Cultivos
AgroScan IA es una aplicación de escritorio desarrollada en Python que permite a productores agrícolas y técnicos de campo diagnosticar enfermedades en cultivos mediante el análisis de fotografías de hojas. El sistema utiliza la API de Gemini AI (Google) para procesar imágenes y devolver un diagnóstico detallado con síntomas, nivel de severidad y tratamiento recomendado.
La aplicación está pensada y contextualizada para el agro cruceño.

Cultivos soportados : 
  Soja
  Maiz
  Caña de Azucar 
  Girasol 

Arquitectura : 
El proyecto sigue el patrón de diseño MVC(MODELO-VISTA-CONTROLADOR), lo que permite una separación clara de responsabilidades. 
  
    AgroScan IA-sc/
  │
  ├── main.py                   # Punto de entrada de la aplicación
  │
  ├── control/
  │   ├── __init__.py
  │   └── controller.py         # Controlador MVC — coordina vista y modelo
  │
  ├── model/
  │   ├── __init__.py
  │   └── model.py              # Modelo — integración con Gemini AI
  │
  ├── view/
  │   ├── __init__.py
  │   └── view.py               # Vista — interfaz gráfica con Tkinter
  │
  ├── requirements.txt          # Dependencias del proyecto
  └── README.md

Tecnologias Utilizadas: 
Python 3.10
Tkinter 
Pillow
Google Gemini AI
Threading 
JSON/Regex

Imagen: 
<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/78313272-e6cb-45b8-81f0-d4cd5e822c09" />

Instrucción de Ejecución: 
  Haz clic en "Seleccionar Imagen del Cultivo" y elige una foto de una hoja (.jpg, .png, .bmp).
  Haz clic en "Analizar con Gemini AI".
  Espera unos segundos mientras se procesa la imagen.
  Lee el diagnóstico en el panel izquierdo: cultivo, enfermedad, severidad, síntomas y tratamiento.
  Opcionalmente, usa "Exportar Diagnóstico" para guardar el resultado.

Nombre de Equipo: Los Piratas
Integrantes: 
  Aro Challapa Omar
  Basilio Rodriguez Deimar Fernando
  Dias Bastos Andres Mario
  Laura Villegas Ernesto José
  Mamani Arancibia Fabricio Pablo
  Orellana Gutiérrez Diego 
   
  
