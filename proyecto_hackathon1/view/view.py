import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import os
import webbrowser

class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.current_image_path = None
        self.photo = None
        
        self.root = tk.Tk()
        self.root.title("🌾 AgroDetect SC - Detector de Enfermedades en Cultivos")
        self.root.geometry("950x800")
        self.root.configure(bg='#e8f5e9')  # Verde claro boliviano
        
        self.setup_ui()
    
    def setup_ui(self):
        # Colores temáticos
        color_verde_bolivia = '#1b5e20'
        color_celeste = '#0288d1'
        color_fondo = '#e8f5e9'
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg=color_fondo)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título con bandera de Bolivia
        title_frame = tk.Frame(main_frame, bg=color_fondo)
        title_frame.pack(pady=(0, 5))
        
        # Banner de colores bolivianos
        banner = tk.Frame(title_frame, bg='#ff0000', height=3)
        banner.pack(fill=tk.X, pady=(0, 10))
        banner2 = tk.Frame(title_frame, bg='#ffff00', height=3)
        banner2.pack(fill=tk.X, pady=(0, 2))
        banner3 = tk.Frame(title_frame, bg='#008000', height=3)
        banner3.pack(fill=tk.X, pady=(0, 10))
        
        title = tk.Label(title_frame, 
                        text="🌾 AgroDetect SC - Santa Cruz 🌿", 
                        font=('Arial', 20, 'bold'), 
                        bg=color_fondo, 
                        fg=color_verde_bolivia)
        title.pack()
        
        subtitle = tk.Label(title_frame, 
                           text="Detección temprana de enfermedades en cultivos con IA",
                           font=('Arial', 11), 
                           bg=color_fondo, 
                           fg='#555555')
        subtitle.pack()
        
        subtitle2 = tk.Label(title_frame, 
                            text="Producto boliviano - Desarrollado para el agro cruceño",
                            font=('Arial', 9, 'italic'), 
                            bg=color_fondo, 
                            fg='#888888')
        subtitle2.pack(pady=(5, 0))
        
        # Contenedor horizontal: diagnóstico a la izquierda, imagen a la derecha
        content_frame = tk.Frame(main_frame, bg=color_fondo)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Columna de diagnóstico
        left_frame = tk.Frame(content_frame, bg=color_fondo)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna de imagen
        right_frame = tk.Frame(content_frame, bg=color_fondo)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))
        
        # Área de imagen
        image_frame = tk.Frame(right_frame, bg='#ffffff', relief=tk.RIDGE, bd=2, width=420, height=240)
        image_frame.pack(fill=tk.BOTH, expand=False)
        image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(image_frame, 
                                    text="📸 Arrastra una imagen del cultivo\n\n o haz clic en 'Seleccionar Imagen'\n\n---\n🌽 Soja  |  🌽 Maíz  |  🍚 Arroz  |  🌻 Girasol  |  🎋 Caña",
                                    bg='#ffffff', 
                                    fg='#999999', 
                                    font=('Arial', 11),
                                    justify=tk.CENTER)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de la columna de imagen
        button_frame = tk.Frame(right_frame, bg=color_fondo)
        button_frame.pack(pady=15, fill=tk.X)
        
        self.btn_select = tk.Button(button_frame, 
                                    text="📁 Seleccionar Imagen del Cultivo", 
                                    command=self.on_select_image,
                                    bg=color_celeste, 
                                    fg='white', 
                                    font=('Arial', 11, 'bold'),
                                    padx=20, 
                                    pady=8)
        self.btn_select.pack(side=tk.LEFT, padx=5)
        
        self.btn_analyze = tk.Button(button_frame, 
                                      text="🔍 Analizar con Gemini AI", 
                                      command=self.on_analyze,
                                      bg=color_verde_bolivia, 
                                      fg='white', 
                                      font=('Arial', 11, 'bold'),
                                      padx=20, 
                                      pady=8,
                                      state=tk.DISABLED)
        self.btn_analyze.pack(side=tk.LEFT, padx=5)
        
        self.btn_clear = tk.Button(button_frame, 
                                   text="🗑️ Limpiar", 
                                   command=self.on_clear,
                                   bg='#e74c3c', 
                                   fg='white', 
                                   font=('Arial', 10),
                                   padx=15, 
                                   pady=8)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso debajo de la sección principal
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        self.progress.pack_forget()
        
        # Separador
        separator = tk.Frame(main_frame, height=2, bg='#bdc3c7')
        separator.pack(fill=tk.X, pady=10)
        
        # Resultados en la columna izquierda
        result_title_frame = tk.Frame(left_frame, bg=color_fondo)
        result_title_frame.pack(fill=tk.X, pady=(0, 5))
        
        result_title = tk.Label(result_title_frame, 
                                text="📋 Resultado del Diagnóstico", 
                                font=('Arial', 14, 'bold'), 
                                bg=color_fondo, 
                                fg=color_verde_bolivia)
        result_title.pack(side=tk.LEFT)
        
        btn_export = tk.Button(result_title_frame, 
                               text="📄 Exportar Diagnóstico", 
                               command=self.export_diagnosis,
                               bg='#9b59b6', 
                               fg='white', 
                               font=('Arial', 9),
                               padx=10)
        btn_export.pack(side=tk.RIGHT)
        
        self.result_text = tk.Text(left_frame, 
                                   wrap=tk.WORD, 
                                   height=20, 
                                   font=('Consolas', 10),
                                   bg='#fafafa',
                                   relief=tk.SUNKEN, 
                                   bd=1)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Insertar mensaje de bienvenida
        bienvenida = """
╔══════════════════════════════════════════════════════════════════════╗
║              🌾 BIENVENIDO A AGRODETECT SC - SANTA CRUZ 🌾          ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   Esta herramienta está diseñada para productores y técnicos de      ║
║   Santa Cruz, Bolivia.                                              ║
║                                                                      ║
║   Cultivos soportados:                                              ║
║   • Soja      • Maíz      • Caña de azúcar                          ║
║   • Girasol   • Arroz     • Algodón                                 ║
║                                                                      ║
║   Instrucciones:                                                    ║
║   1. Toma una foto clara de la hoja o planta afectada               ║
║   2. Haz clic en 'Seleccionar Imagen' o arrastra la foto             ║
║   3. Presiona 'Analizar con Gemini AI' para obtener diagnóstico      ║
║                                                                      ║
║   ⚠️ Esta herramienta es de apoyo. Consulta siempre con un          ║
║      técnico de ANAPO o SAGUAPAC para confirmar diagnósticos.       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
        self.welcome_text = bienvenida
        self.result_text.insert('1.0', self.welcome_text)
        self.result_text.config(state=tk.DISABLED)
        
        # Barra de estado
        status_frame = tk.Frame(main_frame, bg=color_fondo)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, 
                                     text="✅ Listo - Selecciona una imagen para comenzar", 
                                     bg=color_fondo, 
                                     fg='#555555', 
                                     anchor='w')
        self.status_label.pack(side=tk.LEFT)
        
        # Botón de ayuda
        btn_help = tk.Button(status_frame, 
                            text="❓ Ayuda", 
                            command=self.show_help,
                            bg='#f39c12', 
                            fg='white',
                            font=('Arial', 9))
        btn_help.pack(side=tk.RIGHT)
    
    def on_clear(self):
        """Limpia la interfaz"""
        self.current_image_path = None
        self.image_label.config(image='', text="📸 Arrastra una imagen del cultivo\n\n o haz clic en 'Seleccionar Imagen'\n\n---\n🌽 Soja  |  🌽 Maíz  |  🍚 Arroz  |  🌻 Girasol  |  🎋 Caña")
        self.btn_analyze.config(state=tk.DISABLED)
        self.status_label.config(text="✅ Listo - Selecciona una imagen para comenzar")
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', self.welcome_text)
        self.result_text.config(state=tk.DISABLED)
    
    def export_diagnosis(self):
        """Exporta el diagnóstico a un archivo de texto"""
        if not hasattr(self, 'last_result') or not self.last_result:
            messagebox.showinfo("Sin diagnóstico", "No hay un diagnóstico para exportar.")
            return
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"diagnostico_agrodetect_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"AGRODETECT SC - DIAGNÓSTICO DE CULTIVO\n")
            f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"{'='*50}\n\n")
            for key, value in self.last_result.items():
                if isinstance(value, list):
                    f.write(f"{key}: {', '.join(value)}\n")
                else:
                    f.write(f"{key}: {value}\n")
        
        messagebox.showinfo("Exportado", f"Diagnóstico guardado en:\n{filename}")
    
    def show_help(self):
        """Muestra ventana de ayuda"""
        help_text = """
🌾 AGRODETECT SC - GUÍA RÁPIDA

📌 CÓMO USAR LA APLICACIÓN:
1. Toma una foto de la hoja o planta afectada
2. Asegúrate de que la imagen tenga buena iluminación
3. Carga la imagen (arrastrar o botón "Seleccionar")
4. Haz clic en "Analizar con Gemini AI"
5. Espera unos segundos el diagnóstico

📌 CULTIVOS SOPORTADOS:
• Soja
• Maíz
• Caña de azúcar
• Girasol
• Arroz
• Algodón

📌 PARA MEJORES RESULTADOS:
• Fotografiar la hoja completa
• Incluir la parte afectada y sana
• Evitar sombras y reflejos

📞 CONTACTOS ÚTILES EN SANTA CRUZ:
• ANAPO (Asociación de Productores de Oleaginosas)
• SAGUAPAC (Recursos hídricos)
• SENASAG (Sanidad agropecuaria)

⚠️ RECUERDA:
Esta es una herramienta de apoyo. Siempre confirma con un técnico especializado.
        """
        messagebox.showinfo("Ayuda - AgroDetect SC", help_text)
    
    def _is_image_file(self, path: str) -> bool:
        extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        return path.lower().endswith(extensions)
    
    def on_select_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen del cultivo - Santa Cruz, Bolivia",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path: str):
        self.current_image_path = file_path
        
        img = Image.open(file_path)
        img.thumbnail((420, 240))
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo, text='')
        self.btn_analyze.config(state=tk.NORMAL)
        self.status_label.config(text=f"📷 Imagen cargada: {os.path.basename(file_path)}")
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', "✅ Imagen cargada. Haz clic en 'Analizar con Gemini AI' para obtener el diagnóstico específico para Santa Cruz.")
        self.result_text.config(state=tk.DISABLED)
    
    def on_analyze(self):
        if not self.current_image_path:
            messagebox.showwarning("Sin imagen", "Por favor, selecciona una imagen del cultivo primero.")
            return
        
        self.btn_analyze.config(state=tk.DISABLED)
        self.btn_select.config(state=tk.DISABLED)
        self.progress.pack(fill=tk.X, pady=10)
        self.progress.start(10)
        self.status_label.config(text="🔄 Analizando con Gemini AI - Detectando enfermedades...")
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', "⏳ Procesando... Gemini AI está analizando la imagen.\n\n🗺️ Analizando para condiciones de Santa Cruz, Bolivia.\n\nEsto puede tomar unos segundos...")
        self.result_text.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._analyze_thread, daemon=True)
        thread.start()
    
    def _analyze_thread(self):
        try:
            result = self.controller.model.predict(self.current_image_path)
            self.root.after(0, self._on_analysis_finished, result)
        except Exception as e:
            self.root.after(0, self._on_analysis_error, str(e))
    
    def _on_analysis_finished(self, result: dict):
        self.last_result = result
        
        self.btn_analyze.config(state=tk.NORMAL)
        self.btn_select.config(state=tk.NORMAL)
        self.progress.stop()
        self.progress.pack_forget()
        
        crop = result.get('crop', 'Desconocido')
        disease = result.get('disease', 'Desconocido')
        confidence = result.get('confidence', 0)
        symptoms = result.get('symptoms', [])
        treatment = result.get('treatment', 'No especificado')
        prevention = result.get('prevention', 'No especificado')
        severity = result.get('severity', 'desconocido')
        local_rec = result.get('local_recommendation', '')
        
        # Determinar color según severidad
        severity_color = {'leve': '🟢', 'moderado': '🟡', 'grave': '🔴'}.get(severity, '⚪')
        
        symptoms_text = "\n".join([f"   • {s}" for s in symptoms]) if symptoms else "   • No se especificaron síntomas"
        
        result_text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🌾 AGRODETECT SC - SANTA CRUZ - BOLIVIA 🌾               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   🌽 CULTIVO IDENTIFICADO: {crop}
║                                                                              ║
║   📌 ENFERMEDAD: {disease}
║                                                                              ║
║   🎯 CONFIANZA: {confidence}%
║                                                                              ║
║   ⚕️ SEVERIDAD: {severity_color} {severity.capitalize()}
║                                                                              ║
║   🔬 SÍNTOMAS OBSERVADOS:                                                   ║
{symptoms_text}
║                                                                              ║
║   💊 TRATAMIENTO RECOMENDADO:                                               ║
║   {treatment}
║                                                                              ║
║   🛡️ MEDIDAS PREVENTIVAS:                                                   ║
║   {prevention}
║                                                                              ║
║   🗺️ RECOMENDACIÓN LOCAL (Santa Cruz):                                      ║
║   {local_rec if local_rec else "Consultar con técnico de ANAPO o SENASAG"}
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📞 CONTACTOS ÚTILES EN SANTA CRUZ:
   • ANAPO: (3) 333-1234
   • SENASAG: (3) 342-5678
   • SAGUAPAC: (3) 336-9012

⚠️ Esta herramienta es de apoyo. Siempre confirma el diagnóstico con un técnico especializado.
        """
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', result_text)
        self.result_text.config(state=tk.DISABLED)
        
        self.status_label.config(text=f"✅ Diagnóstico completado: {disease} en {crop}")
    
    def _on_analysis_error(self, error_msg: str):
        self.btn_analyze.config(state=tk.NORMAL)
        self.btn_select.config(state=tk.NORMAL)
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="❌ Error en el análisis")
        
        error_text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              ❌ ERROR                                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   {error_msg}
║                                                                              ║
║   SOLUCIONES:                                                               ║
║   • Verifica tu conexión a internet                                         ║
║   • Asegúrate de que la API key sea válida                                  ║
║   • Intenta con otra imagen más clara                                       ║
║   • Reinicia la aplicación                                                  ║
║                                                                              ║
║   📞 Si el problema persiste, contacta a soporte técnico                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', error_text)
        self.result_text.config(state=tk.DISABLED)
        
        messagebox.showerror("Error", f"No se pudo analizar la imagen:\n{error_msg}")
    
    def run(self):
        self.root.mainloop()