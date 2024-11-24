from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)


screenshot_dir = "screenshots_pago_amazon"
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
    nombre_reporte = f"reporte_pago_{timestamp}.html"
    with open(nombre_reporte, "w") as f:
        f.write("""
        <html>
        <head>
            <title>Reporte de Automatización - Proceso de Pago Amazon</title>
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
            <h1>Reporte de Automatización - Proceso de Pago Amazon</h1>
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

    driver.find_element(By.ID, "nav-link-accountList").click()
    captura = tomar_captura("pagina_login")
    registrar_paso("Abrir la página de inicio de sesión", True, captura)
    driver.find_element(By.ID, "ap_email").send_keys("davidroso663@gmail.com")
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "ap_password").send_keys("zabala809") 
    driver.find_element(By.ID, "signInSubmit").click()
    captura = tomar_captura("pagina_inicio_sesion")
    registrar_paso("Iniciar sesión", True, captura)
    time.sleep(2)

    driver.find_element(By.ID, "twotabsearchtextbox").send_keys("perfume dior" + Keys.RETURN)
    captura = tomar_captura("resultado_busqueda")
    registrar_paso("Buscar producto", True, captura)
    time.sleep(2)
    
    producto = driver.find_element(By.CSS_SELECTOR, ".s-main-slot .s-result-item h2 a")
    producto.click()
    captura = tomar_captura("producto_seleccionado")
    registrar_paso("Seleccionar producto", True, captura)
    time.sleep(2)
    
    driver.find_element(By.ID, "add-to-cart-button").click()
    captura = tomar_captura("producto_agregado_carrito")
    registrar_paso("Agregar producto al carrito", True, captura)
    time.sleep(2)
    
    driver.find_element(By.ID, "nav-cart").click()
    captura = tomar_captura("pagina_carrito")
    registrar_paso("Ir al carrito", True, captura)
    time.sleep(2)

    driver.find_element(By.NAME, "proceedToRetailCheckout").click()
    captura = tomar_captura("pagina_checkout")
    registrar_paso("Proceder al checkout", True, captura)
    time.sleep(2)
   
   
    try:
       
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "addressBookEntryAddressId"))).click()
        captura = tomar_captura("direccion_envio_seleccionada")
        registrar_paso("Seleccionar dirección de envío existente", True, captura)
    except Exception as e:
        print("No se encontró dirección guardada, agregando una nueva dirección.")
        
        try:
         
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "address-ui-widgets-addAddressBookButton"))).click()
            captura = tomar_captura("pagina_agregar_direccion")
            registrar_paso("Abrir página para agregar nueva dirección", True, captura)

            driver.find_element(By.ID, "address-ui-widgets-enterAddressFullName").send_keys("David Rosso")
            driver.find_element(By.ID, "address-ui-widgets-enterAddressAddressLine1").send_keys("13469 Nw 9th Ln")
            driver.find_element(By.ID, "address-ui-widgets-enterAddressCity").send_keys("Miami")
            driver.find_element(By.ID, "address-ui-widgets-enterAddressStateOrRegion").send_keys("Florida")
            driver.find_element(By.ID, "address-ui-widgets-enterAddressPostalCode").send_keys("33182")
            driver.find_element(By.ID, "address-ui-widgets-enterAddressPhoneNumber").send_keys("8094432080")
            
            driver.find_element(By.NAME, "address-ui-widgets-form-submit-button").click()
            captura = tomar_captura("direccion_guardada")
            registrar_paso("Nueva dirección agregada y guardada", True, captura)
            
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "addressBookEntryAddressId"))).click()
            captura = tomar_captura("direccion_envio_seleccionada")
            registrar_paso("Seleccionar nueva dirección de envío", True, captura)
        
        except Exception as add_error:
            captura = tomar_captura("error_agregar_direccion")
            registrar_paso("Error al agregar dirección", False, captura)
            print(f"Error al agregar dirección: {str(add_error)}")
    
    time.sleep(2)
    
   
    driver.find_element(By.NAME, "ppw-instrumentRowSelection-0").click()  
    captura = tomar_captura("metodo_pago_seleccionado")
    registrar_paso("Seleccionar método de pago", True, captura)
    time.sleep(2)
    
  
    driver.find_element(By.NAME, "placeYourOrder1").click()
    captura = tomar_captura("confirmacion_compra")
    registrar_paso("Confirmar la compra", True, captura)
    time.sleep(2)

    print("Automatización de pago completada con éxito.")

except Exception as e:
    captura = tomar_captura("error")
    registrar_paso("Error durante la automatización", False, captura)
    print(f"Error durante la automatización: {str(e)}")

finally:
    driver.quit()
    generar_reporte_html()
