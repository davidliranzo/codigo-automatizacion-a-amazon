from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

screenshot_dir = "screenshots_carrito_amazon"
os.makedirs(screenshot_dir, exist_ok=True)


test_results = []


def tomar_captura(nombre):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ruta = os.path.join(screenshot_dir, f"{nombre}_{timestamp}.png")
    driver.save_screenshot(ruta)
    return ruta


def registrar_paso(paso, estado, captura=None):
    test_results.append({"paso": paso, "estado": estado, "captura": captura})


def generar_reporte_html():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_reporte = f"reporte_carrito_{timestamp}.html"
    with open(nombre_reporte, "w") as f:
        f.write("""
        <html>
        <head>
            <title>Reporte de Automatización - Carrito Amazon</title>
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
            <h1>Reporte de Automatización - Carrito Amazon</h1>
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
    registrar_paso("Abrir página de inicio de Amazon", True, captura)

    driver.find_element(By.ID, "nav-link-accountList").click()
    captura = tomar_captura("pagina_login")
    registrar_paso("Abrir página de login", True, captura)

    driver.find_element(By.ID, "ap_email").send_keys("davidroso663@gmail.com") 
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "ap_password").send_keys("zabala809") 
    driver.find_element(By.ID, "signInSubmit").click()
    captura = tomar_captura("pagina_inicio_sesion")
    registrar_paso("Iniciar sesión", True, captura)

    
    driver.find_element(By.ID, "twotabsearchtextbox").send_keys("monitor" + Keys.RETURN)
    captura = tomar_captura("resultado_busqueda")
    registrar_paso("Buscar producto", True, captura)

    producto = driver.find_element(By.CSS_SELECTOR, ".s-main-slot .s-result-item h2 a")
    producto.click()
    captura = tomar_captura("producto_seleccionado")
    registrar_paso("Seleccionar producto", True, captura)

    driver.find_element(By.ID, "add-to-cart-button").click()
    captura = tomar_captura("producto_agregado_carrito")
    registrar_paso("Agregar producto al carrito", True, captura)


    driver.find_element(By.ID, "nav-cart").click()
    captura = tomar_captura("pagina_carrito")
    registrar_paso("Abrir página del carrito", True, captura)

   
    driver.find_element(By.XPATH, "//input[@value='Eliminar']").click()
    captura = tomar_captura("producto_eliminado_carrito")
    registrar_paso("Eliminar producto del carrito", True, captura)


    driver.back()
    driver.find_element(By.ID, "add-to-cart-button").click()
    driver.find_element(By.ID, "nav-cart").click()
    cantidad_dropdown = driver.find_element(By.NAME, "quantity")
    cantidad_dropdown.click()
    cantidad_opcion = driver.find_element(By.XPATH, "//option[@value='2']")
    cantidad_opcion.click()
    captura = tomar_captura("cantidad_actualizada")
    registrar_paso("Actualizar cantidad de producto", True, captura)


    driver.find_element(By.XPATH, "//input[@value='Guardar para más tarde']").click()
    captura = tomar_captura("producto_guardado_para_despues")
    registrar_paso("Guardar producto para después", True, captura)

    print("Automatización completada con éxito.")

except Exception as e:
    captura = tomar_captura("error")
    registrar_paso("Error en la automatización", False, captura)
    print(f"Error durante la automatización: {str(e)}")

finally:
    driver.quit()
    generar_reporte_html()

