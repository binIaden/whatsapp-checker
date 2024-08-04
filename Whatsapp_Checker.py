import asyncio
import random
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
from PIL import Image
import pytesseract


prefix = '+57'
n = int(input('Ingrese la cantidad de números a generar' + '\n'))
i = n - 1

async def numeros(n, prefix):
    lista = ['311','312', '314', '316', '320', '302', '313', '300']
    inicio_aleatorio = random.choice(lista)
    numero_aleatorio = str(random.randint(1000000, 9999999))
    telefono = prefix+inicio_aleatorio+numero_aleatorio
    print(f'{telefono}')
    return telefono



async def main(i, n):   
    print("Por favor, escanea el código QR de WhatsApp Web para iniciar sesión.")
    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(headless=False)

    
        context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        bypass_csp=True, 
        java_script_enabled=True
        )

        inicio = await context.new_page()
        await inicio.goto(f'https://web.whatsapp.com/', wait_until = 'networkidle')
        await inicio.wait_for_selector('div._aigu', timeout=300000)
        await inicio.close()

        for i in range(n):
            telefono = await numeros(n = n, prefix = prefix)
            checkPage = await context.new_page()
            await checkPage.goto(f'https://web.whatsapp.com/send?phone={telefono}', wait_until = 'networkidle')
            await checkPage.wait_for_selector('.x12lqup9', timeout=300000)
            html_content = await checkPage.content()


        await asyncio.sleep(1)
        screenshot_path = 'screenshot.png'
        await checkPage.screenshot(path=screenshot_path)

        image = Image.open(screenshot_path)
        text = pytesseract.image_to_string(image)

        if "Phone number shared via url is invalid." in text:
            print(f'{telefono} Numero invalido')
        else:
            print(f'{telefono} Numero valido')
        await checkPage.close()
asyncio.run(main(i, n))
