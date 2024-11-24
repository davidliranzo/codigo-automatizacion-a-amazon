from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

if not os.path.exists('screenshots_amazon'):
    os.makedirs('screenshots_amazon')

test_results = []


def take_screenshot(step_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"screenshots_amazon/{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    return screenshot_name


def log_step(step_name, status, screenshot=None):
    test_results.append({
        "step_name": step_name,
        "status": status,
        "screenshot": screenshot
    })


def generate_html_report():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    report_file = f"reporte_{timestamp}.html"
    with open(report_file, 'w') as f:
        f.write("""
        <html>
        <head>
            <title>Reporte de Pruebas</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                tr:hover {
                    background-color: #ddd;
                }
                .success {
                    color: green;
                }
                .failure {
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>Reporte de Pruebas Automatizadas</h1>
            <table>
                <tr>
                    <th>Paso</th>
                    <th>Estado</th>
                    <th>Captura de Pantalla</th>
                </tr>
        """)

        for result in test_results:
            f.write("<tr>")
            f.write(f"<td>{result['step_name']}</td>")
            f.write(f"<td class='{'success' if result['status'] else 'failure'}'>{'Éxito' if result['status'] else 'Error'}</td>")
            if result['screenshot']:
                f.write(f"<td><a href='{result['screenshot']}' target='_blank'>Ver captura</a></td>")
            else:
                f.write("<td>No disponible</td>")
            f.write("</tr>")

        f.write("""
            </table>
            <p>El reporte muestra los pasos realizados en la prueba automatizada, incluyendo su estado y enlaces a las capturas de pantalla.</p>
        </body>
        </html>
        """)

    print(f"Reporte HTML generado: {report_file}")


try:
    driver.get("https://www.amazon.com/")
    log_step("Abrir página de Amazon", True)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav-link-accountList"))
    )
    driver.find_element(By.ID, "nav-link-accountList").click()
    screenshot = take_screenshot("ir_a_login")
    log_step("Ir a la página de login", True, screenshot)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ap_email"))
    )
    driver.find_element(By.ID, "ap_email").send_keys("davidroso663@gmail.com")
    driver.find_element(By.ID, "continue").click()
    screenshot = take_screenshot("correo_ingresado")
    log_step("Ingresar correo electrónico", True, screenshot)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
    driver.find_element(By.ID, "ap_password").send_keys("zabala809")
    driver.find_element(By.ID, "signInSubmit").click()
    screenshot = take_screenshot("inicio_sesion_completado")
    log_step("Inicio de sesión completado", True, screenshot)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "nav-cart"))
    )
    screenshot = take_screenshot("pagina_principal_amazon")
    log_step("Página principal de Amazon", True, screenshot)

    print("Login exitoso en Amazon!")

except Exception as e:
    screenshot = take_screenshot("error")
    log_step("Error en la automatización", False, screenshot)
    print("Error al automatizar:", e)


driver.quit()
generate_html_report()


