from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime


chrome_options = Options()
chrome_options.add_argument("--start-maximized")  
chrome_options.add_argument("--disable-extensions")  

screenshot_dir = "screenshots_registro_amazon"
os.makedirs(screenshot_dir, exist_ok=True)

test_results = []

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def tomar_captura(nombre):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ruta = os.path.join(screenshot_dir, f"{nombre}_{timestamp}.png")
    driver.save_screenshot(ruta)
    return ruta

def registrar_paso(paso, estado, captura=None):
    test_results.append({"paso": paso, "estado": estado, "captura": captura})

def generar_reporte_html():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_reporte = f"reporte_registro_{timestamp}.html"
    with open(nombre_reporte, "w") as f:
        f.write("""
        <html>
        <head>
            <title>Reporte de Automatización - Registro Amazon</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f4f4f4; }
                .success { color: green; }
                .failure { color: red; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                tr:hover { background-color: #f1f1f1; }
            </style>
        </head>
        <body>
            <h1>Reporte de Automatización - Registro Amazon</h1>
            <table>
                <tr>
                    <th>Paso</th>
                    <th>Estado</th>
                    <th>Captura de Pantalla</th>
                </tr>
        """)
        for resultado in test_results:
            f.write("<tr>")
            f.write(f"<td>{resultado['paso']}</td>")
            f.write(f"<td class='{'success' if resultado['estado'] else 'failure'}'>{'Éxito' if resultado['estado'] else 'Error'}</td>")
            if resultado['captura']:
                f.write(f"<td><a href='{resultado['captura']}' target='_blank'>Ver captura</a></td>")
            else:
                f.write("<td>No disponible</td>")
            f.write("</tr>")
        f.write("""
            </table>
            <p>Reporte generado automáticamente con capturas de pantalla incluidas.</p>
        </body>
        </html>
        """)
    print(f"Reporte HTML generado: {nombre_reporte}")


try:
    driver.get("https://www.amazon.com")
    captura = tomar_captura("pagina_inicio_amazon")
    registrar_paso("Abrir la página de Amazon", True, captura)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "nav-link-accountList"))).click()
    captura = tomar_captura("pagina_inicio_sesion")
    registrar_paso("Abrir la página de inicio de sesión", True, captura)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "createAccountSubmit"))).click()
    captura = tomar_captura("pagina_crear_cuenta")
    registrar_paso("Abrir el formulario de registro", True, captura)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ap_customer_name"))).send_keys("david roso")
    driver.find_element(By.ID, "ap_email").send_keys("davidroso663@gmail.com")
    driver.find_element(By.ID, "ap_password").send_keys("zabala809")
    driver.find_element(By.ID, "ap_password_check").send_keys("zabala809")
    captura = tomar_captura("formulario_lleno")
    registrar_paso("Llenar el formulario de registro", True, captura)

    driver.find_element(By.ID, "continue").click()
    captura = tomar_captura("enviar_formulario")
    registrar_paso("Enviar el formulario de registro", True, captura)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "auth-captcha-verify-image")))
        captura = tomar_captura("codigo_validacion")
        registrar_paso("Solicitud de código de validación", True, captura)
    except Exception as e:
        captura = tomar_captura("error_codigo_validacion")
        registrar_paso(f"Error: {str(e)}", False, captura)

    print("Automatización completada con éxito.")

except Exception as e:
    captura = tomar_captura("error")
    registrar_paso("Error durante la automatización", False, captura)
    print(f"Error durante la automatización: {str(e)}")

finally:
    driver.quit()
    generar_reporte_html()
