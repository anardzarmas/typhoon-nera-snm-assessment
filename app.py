import streamlit as st
import streamlit.components.v1 as components
import base64
from fpdf import FPDF
import datetime

# ==========================================
# LÓGICA DE RECOMENDACIÓN DE PRODUCTOS CISCO
# ==========================================
def generar_recomendaciones(respuestas):
    recomendaciones = set()
    texto_completo = " ".join(respuestas.values()).lower()
    
    if any(word in texto_completo for word in ["wan", "mpls", "sucursales", "sucursal", "sitios", "fusiones"]):
        recomendaciones.add("- Cisco Catalyst SD-WAN / Meraki SD-WAN: Para una gestión ágil de la WAN, reducción de costos en enlaces MPLS y adaptación rápida a expansiones del negocio.")
        
    if any(word in texto_completo for word in ["ia", "telemetría", "anomalías", "automatización", "automatizarse", "manual"]):
        recomendaciones.add("- Cisco Catalyst Center (DNA Center): Para telemetría impulsada por IA, automatización de tareas operativas de LAN y visibilidad proactiva de anomalías.")
        
    if any(word in texto_completo for word in ["segmentación", "acceso", "postura", "zero trust", "identidad"]):
        recomendaciones.add("- Cisco Identity Services Engine (ISE): Para aplicar políticas de red adaptativas, segmentación dinámica y control de acceso basado en el contexto del usuario y dispositivo.")
        
    if any(word in texto_completo for word in ["api", "desarrolladores", "integraciones", "gobernanza"]):
        recomendaciones.add("- Cisco Secure Firewall & Cisco DevNet Ecosystem: Para proteger las integraciones de API y gestionar la seguridad y el control de versiones al exponer servicios a terceros.")

    if not recomendaciones:
        recomendaciones.add("- Cisco Catalyst Center y Cisco Secure Firewall: Como base fundamental para iniciar una estrategia de gestión de red unificada, automatizada y segura.")

    return list(recomendaciones)

# ==========================================
# FUNCIÓN AUXILIAR DE TEXTO
# ==========================================
def clean_txt(texto):
    """Limpia el texto para evitar el error de caracteres no soportados en latin-1"""
    if not texto:
        return "No especificado"
    return str(texto).encode('latin-1', 'replace').decode('latin-1')

# ==========================================
# GENERACIÓN DE PDF 
# ==========================================
class PDF(FPDF):
    def header(self):
        try:
            self.image('logo_typhoon.jpg', 15, 10, 30)
            self.image('logo_cisco.jpg', 165, 10, 30)
        except Exception:
            pass 
        # SOLUCIÓN DE MARGEN SUPERIOR: Forzamos el inicio del texto debajo de los logos en todas las páginas
        self.set_y(35)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def crear_pdf(datos_proyecto, respuestas_dominios, recomendaciones, dominios_guia):
    pdf = PDF()
    
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    epw = pdf.epw 
    
    # --- Título Principal ---
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(epw, 6, clean_txt('Acta de Evaluación - Caso de uso Secure Network'), ln=1, align='C')
    pdf.set_font('helvetica', '', 11)
    pdf.cell(epw, 6, clean_txt('Elaborado por: Best - Typhoon Technology'), ln=1, align='C')
    pdf.ln(8)
    
    # --- 1. Información General del Proyecto ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(epw, 8, clean_txt('1. Información General del Proyecto'), ln=1)
    pdf.ln(2)
    
    # Fila 1: Empresa | AM Cisco | Vertical
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Empresa:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(60, 6, clean_txt(datos_proyecto.get('Nombre de la empresa')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(22, 6, 'AM Cisco:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(48, 6, clean_txt(datos_proyecto.get('AM de Cisco')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(16, 6, 'Vertical:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('Vertical de negocio')), ln=1)
    
    # Fila 2: Contacto | Responsable Best | Fecha
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(20, 6, 'Contacto:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(60, 6, clean_txt(datos_proyecto.get('Contacto principal')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 6, 'Responsable Best:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(35, 6, clean_txt(datos_proyecto.get('Responsable de Best')), ln=0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 6, 'Fecha:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('Fecha de evaluación')), ln=1)
    
    # Fila 3: Puesto
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 6, 'Puesto:', ln=0)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, clean_txt(datos_proyecto.get('Puesto')), ln=1)
    pdf.ln(6)
    
    # --- 2. Resumen de la Conversación ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(epw, 8, clean_txt('2. Resumen de la Conversación'), ln=1)
    pdf.ln(2)
    
    for titulo, pregunta_guia in dominios_guia.items():
        pdf.set_font('helvetica', 'B', 10)
        pdf.write(6, clean_txt(f"{titulo}: "))
        pdf.set_font('helvetica', '', 10)
        pdf.write(6, clean_txt(f"{pregunta_guia}\n"))
        
        respuesta_texto = respuestas_dominios.get(titulo, "").strip()
        if not respuesta_texto:
            respuesta_texto = " "
            
        pdf.set_font('helvetica', 'B', 10)
        pdf.write(6, "Respuesta: ")
        pdf.set_font('helvetica', '', 10)
        pdf.write(6, clean_txt(f"{respuesta_texto}\n\n"))
        
    # --- 3. Soluciones Cisco Sugeridas ---
    if pdf.get_y() > 240: 
        pdf.add_page()
        
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(epw, 8, clean_txt('3. Soluciones Cisco Sugeridas:'), ln=1)
    pdf.set_font('helvetica', '', 10)
    
    for rec in recomendaciones:
        pdf.multi_cell(epw, 5, clean_txt(rec))
        pdf.ln(2)
        
    pdf.ln(2)
    
    pdf.set_font('helvetica', 'U', 10)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(epw, 6, 'Link de referencia oficial de productos Cisco', link="https://www.cisco.com/site/us/en/products/networking/network-security/index.html", ln=1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)
    
    pdf.set_font('helvetica', 'I', 9)
    disclaimer = "Nota importante: Esta información es una sugerencia preliminar generada a partir de los datos proporcionados. Queda estrictamente sujeta a los comentarios, validación técnica y diseño formal por parte de un profesional preventa o arquitecto de soluciones certificado de Typhoon Technology."
    pdf.multi_cell(epw, 4, clean_txt(disclaimer))
        
    return bytes(pdf.output())

# ==========================================
# INTERFAZ DE STREAMLIT
# ==========================================
st.set_page_config(page_title="NERA Assessment - Typhoon", layout="wide")

st.title("Formulario de Evaluación de Gestión de Red Segura (NERA)")
st.markdown("**Partner de Cisco: Typhoon Technology**")
st.info("Complete este cuestionario simplificado para descubrir la arquitectura de Enterprise Networking recomendada para sus proyectos.")

# --- Sección: Información General ---
st.header("Información General del Proyecto")
col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input("Nombre de la empresa")
    contacto = st.text_input("Contacto principal")
    puesto = st.text_input("Puesto")
    
    opciones_verticales = [
        "Seleccione una opción...", "Tecnología y Telecomunicaciones", "Finanzas y Banca", 
        "Salud y Farmacéutica", "Educación", "Retail y Comercio", 
        "Manufactura y Logística", "Gobierno y Sector Público", "Otro"
    ]
    vertical = st.selectbox("Vertical de negocio", opciones_verticales)

with col2:
    am_cisco = st.text_input("AM de Cisco")
    responsable = st.text_input("Responsable de Best", value="Ana")
    fecha = st.date_input("Fecha de evaluación", datetime.date.today())

# --- Sección: Dominios de Evaluación ---
st.header("Dominios de Evaluación")

dominios_guia = {
    "1. Gestión de LAN y Automatización Operativa": "¿Cuánto tiempo toma típicamente aprovisionar nuevos dispositivos de red o realizar cambios de configuración? ¿Existen tareas repetitivas que podrían automatizarse? ¿Con qué frecuencia ocurren errores de configuración y qué impacto tienen? ¿Cuántos miembros del personal gestionan la LAN y cuál es su experiencia? ¿Cómo se integra con otros sistemas (IPAM, autenticación, monitoreo)?",
    "2. Política de Red Adaptativa y Segmentación": "¿Cómo se adapta su acceso a cambios en tiempo real del usuario (dispositivo, ubicación, postura)? ¿Cómo equilibra seguridad con productividad? ¿Cómo extrae insights de seguridad para mitigar amenazas y cumplir normas? ¿Cómo aplica políticas de segmentación en WAN, campus y remotos?",
    "3. Inteligencia Artificial (IA) y Telemetría": "¿Cómo prioriza el monitoreo sin detección de anomalías de IA? ¿Cuánto esfuerzo manual implica mantener la visibilidad y rendimiento sin automatización IA? ¿Cómo enfrenta los desafíos de seguridad sin insights de IA?",
    "4. Gestión y Seguridad de APIs": "¿Cómo maneja el versionado y compatibilidad de APIs para evitar disrupciones? ¿Cómo gobierna los accesos y permisos? ¿Qué hace para apoyar a los desarrolladores a integrar sus APIs? ¿Cómo garantiza la seguridad de las APIs hacia terceros?",
    "5. Gestión Detallada de WAN": "¿Tiene desafíos con costos o limitaciones de ancho de banda? ¿Busca reducir costos de circuitos MPLS? ¿Qué tan frecuente agrega o quita sitios? ¿Qué tan rápido puede adaptar su WAN a cambios (fusiones, expansiones)?"
}

respuestas = {}

for titulo, pregunta in dominios_guia.items():
    st.markdown(f"**{titulo}**")
    st.caption(f"💡 *Guía:* {pregunta}")
    respuestas[titulo] = st.text_area(label="Respuesta", key=titulo, height=120, label_visibility="collapsed")
    st.markdown("---")

# --- Generación de Reporte y Descarga Automática ---
if st.button("Generar Evaluación y Recomendaciones", type="primary"):
    if not empresa:
        st.warning("Por favor, ingresa el 'Nombre de la empresa' para generar el documento.")
    else:
        vertical_final = vertical if vertical != "Seleccione una opción..." else ""
        
        datos_proyecto = {
            "Nombre de la empresa": empresa,
            "Contacto principal": contacto,
            "Puesto": puesto,
            "AM de Cisco": am_cisco,
            "Responsable de Best": responsable,
            "Fecha de evaluación": fecha.strftime("%d/%m/%Y"),
            "Vertical de negocio": vertical_final
        }
        
        recomendaciones = generar_recomendaciones(respuestas)
        
        st.success("¡Análisis completado exitosamente! Tu descarga comenzará en breve.")
        st.subheader("Arquitectura Cisco Sugerida")
        for rec in recomendaciones:
            st.write(rec)
            
        pdf_bytes = crear_pdf(datos_proyecto, respuestas, recomendaciones, dominios_guia)
        nombre_archivo = f"NERA_Assessment_SNM_{empresa.replace(' ', '_')}.pdf"
        
        # Inyección de JS para forzar la descarga en el mismo clic
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a id="descarga-automatica" href="data:application/pdf;base64,{b64}" download="{nombre_archivo}"></a>'
        js = f"<script>document.getElementById('descarga-automatica').click();</script>"
        components.html(href + js, height=0)
        
        # Mantenemos el botón estático de Streamlit abajo por si el navegador bloquea los pop-ups automáticos
        st.download_button(
            label="📄 Descargar de nuevo (si la descarga automática falló)",
            data=pdf_bytes,
            file_name=nombre_archivo,
            mime="application/pdf"
        )