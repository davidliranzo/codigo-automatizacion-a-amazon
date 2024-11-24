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


screenshot_dir = "screenshots_busqueda_amazon"
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
    nombre_reporte = f"reporte_busqueda_{timestamp}.html"
    with open(nombre_reporte, "w") as f:
        f.write("""
        <html>
        <head>
            <title>Reporte de Automatización - Búsqueda Amazon</title>
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
            <h1>Reporte de Automatización - Búsqueda Amazon</h1>
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


    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys("disco duro")
    driver.find_element(By.ID, "nav-search-submit-button").click()
    captura = tomar_captura("buscar_producto")
    registrar_paso("Buscar producto 'disco duro'", True, captura)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot .s-result-item")))
    captura = tomar_captura("resultados_busqueda")
    registrar_paso("Mostrar resultados de búsqueda", True, captura)

    print("Automatización completada con éxito.")

except Exception as e:
    captura = tomar_captura("error")
    registrar_paso("Error durante la automatización", False, captura)
    print(f"Error durante la automatización: {str(e)}")

finally:
    driver.quit()
    generar_reporte_html()

