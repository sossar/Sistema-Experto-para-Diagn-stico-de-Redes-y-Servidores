import json
import tkinter as tk
from tkinter import filedialog, messagebox

# ==========================================
# 1. FUNCIONES LÓGICAS DEL SISTEMA EXPERTO
# ==========================================

def cargar_reglas(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def obtener_sintomas_unicos(reglas):
    sintomas = set()
    for regla in reglas:
        for antecedente in regla["antecedentes"]:
            sintomas.add(antecedente)
    return sorted(list(sintomas))

# ==========================================
# 2. INTERFAZ GRÁFICA (GUI)
# ==========================================

class InterfazSistemaExperto:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.title("Sistema Experto - Diagnóstico de Redes")
        self.ventana.geometry("650x700")
        
        self.base_conocimientos = []
        self.acciones_disponibles = {
            "alerta_ddos": lambda hechos: self.escribir_bitacora("🚨 ¡ACCIÓN CRÍTICA EJECUTADA! Iniciando mitigación DDoS..."),
            "alerta_energia": lambda hechos: self.escribir_bitacora("⚡ ¡ACCIÓN URGENTE EJECUTADA! Notificando a mantenimiento eléctrico.")
        }

        # --- Elementos Visuales ---
        self.btn_cargar = tk.Button(ventana_principal, text="1. Cargar Archivo de Reglas (JSON)", command=self.cargar_archivo)
        self.btn_cargar.pack(pady=10)

        tk.Label(ventana_principal, text="2. Selecciona los síntomas presentes (Ctrl+Clic para múltiples):").pack()

        self.lista_sintomas = tk.Listbox(ventana_principal, selectmode=tk.MULTIPLE, width=60, height=10)
        self.lista_sintomas.pack(pady=5)

        self.btn_diagnosticar = tk.Button(ventana_principal, text="3. Iniciar Diagnóstico", command=self.ejecutar_diagnostico, state=tk.DISABLED)
        self.btn_diagnosticar.pack(pady=10)

        tk.Label(ventana_principal, text="Bitácora de Inferencia (Paso a Paso):").pack()

        self.caja_texto = tk.Text(ventana_principal, width=75, height=20, state=tk.DISABLED)
        self.caja_texto.pack(pady=5)

    def escribir_bitacora(self, mensaje):
        self.caja_texto.config(state=tk.NORMAL)
        self.caja_texto.insert(tk.END, mensaje + "\n")
        self.caja_texto.see(tk.END)
        self.caja_texto.config(state=tk.DISABLED)

    def cargar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if ruta_archivo:
            try:
                self.base_conocimientos = cargar_reglas(ruta_archivo)
                sintomas_posibles = obtener_sintomas_unicos(self.base_conocimientos)
                self.lista_sintomas.delete(0, tk.END)
                for sintoma in sintomas_posibles:
                    self.lista_sintomas.insert(tk.END, sintoma)
                self.btn_diagnosticar.config(state=tk.NORMAL)
                messagebox.showinfo("Éxito", "Base de conocimientos cargada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

    def ejecutar_diagnostico(self):
        self.caja_texto.config(state=tk.NORMAL)
        self.caja_texto.delete(1.0, tk.END)
        self.caja_texto.config(state=tk.DISABLED)

        indices_seleccionados = self.lista_sintomas.curselection()
        if not indices_seleccionados:
            messagebox.showwarning("Atención", "Debes seleccionar al menos un síntoma.")
            return

        datos_iniciales = {}
        for i in indices_seleccionados:
            sintoma = self.lista_sintomas.get(i)
            datos_iniciales[sintoma] = True

        self.escribir_bitacora(f"SÍNTOMAS INICIALES:\n{list(datos_iniciales.keys())}")
        self.escribir_bitacora("-" * 60)

        self.motor_inferencia_avanzado(datos_iniciales, self.base_conocimientos)

    # ==========================================
    # 3. EL MOTOR DE INFERENCIA (Modificado para Recomendaciones)
    # ==========================================
    def motor_inferencia_avanzado(self, datos_iniciales, reglas):
        hechos = set([sintoma for sintoma, valor in datos_iniciales.items() if valor == True])
        hechos_nuevos = set()
        reglas_disparadas = set()
        
        # NUEVO: Lista para guardar las recomendaciones
        recomendaciones_finales = set()

        while True:
            reglas_aplicables = []
            for i, regla in enumerate(reglas):
                if i not in reglas_disparadas:
                    antecedentes = set(regla["antecedentes"])
                    if antecedentes.issubset(hechos):
                        reglas_aplicables.append((i, regla))

            if not reglas_aplicables:
                break

            reglas_aplicables.sort(key=lambda item: (item[1].get("prioridad", 0), len(item[1]["antecedentes"])), reverse=True)
            
            indice_regla_seleccionada, regla_seleccionada = reglas_aplicables[0]
            reglas_disparadas.add(indice_regla_seleccionada)

            nuevos_hechos_inferidos = []
            for consecuente in regla_seleccionada["consecuentes"]:
                if consecuente not in hechos:
                    hechos_nuevos.add(consecuente)
                    hechos.add(consecuente)
                    nuevos_hechos_inferidos.append(consecuente)

            if nuevos_hechos_inferidos:
                prioridad = regla_seleccionada.get("prioridad", 0)
                self.escribir_bitacora(f"✔️ Se cumple: '{regla_seleccionada['nombre']}' (Prioridad: {prioridad})")
                self.escribir_bitacora(f"   ↳ Deduce: {', '.join(nuevos_hechos_inferidos)}")

            if "accion" in regla_seleccionada:
                nombre_accion = regla_seleccionada["accion"]
                if nombre_accion in self.acciones_disponibles:
                    self.acciones_disponibles[nombre_accion](hechos)
                    
            # NUEVO: Si la regla tiene recomendación, la guardamos
            if "recomendacion" in regla_seleccionada:
                recomendaciones_finales.add(regla_seleccionada["recomendacion"])

        self.escribir_bitacora("-" * 60)
        self.escribir_bitacora(f"📝 DIAGNÓSTICO LÓGICO FINAL:\n{list(hechos)}\n")
        
        # NUEVO: Imprimir todas las recomendaciones encontradas al final
        if recomendaciones_finales:
            self.escribir_bitacora("💡 RECOMENDACIONES DEL SISTEMA:")
            for rec in recomendaciones_finales:
                self.escribir_bitacora(f"  • {rec}")
        else:
            self.escribir_bitacora("💡 RECOMENDACIONES: (No hay recomendaciones específicas para este cuadro).")

# ==========================================
# INICIO DE LA APLICACIÓN
# ==========================================
if __name__ == "__main__":
    ventana_raiz = tk.Tk()
    app = InterfazSistemaExperto(ventana_raiz)
    ventana_raiz.mainloop()