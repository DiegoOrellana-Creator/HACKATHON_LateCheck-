#!/usr/bin/env python3
"""
Detector de Enfermedades en Cultivos
Aplicación de escritorio que usa Gemini API para diagnosticar enfermedades en plantas
"""

import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     🌿 DETECTOR DE ENFERMEDADES EN CULTIVOS 🌿           ║
    ║     Usando Gemini AI para diagnóstico preciso           ║
    ║     Arquitectura MVC con Python y Tkinter               ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        from control.controller import AppController
        app = AppController()
        app.run()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Instala las dependencias: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()