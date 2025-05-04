import time
import yagmail
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Gmail hesabı ilə əlaqə yaratmaq
def send_email(subject, body, to_email, from_email, app_password):
    yag = yagmail.SMTP(from_email, app_password)
    yag.send(to_email, subject, body)
    print("E-poçt göndərildi!")

# Wolt endirimlərini əldə etmək
def get_wolt_discounts():
    options = Options()
    options.add_argument("--headless")  # Brauzerin görünməməsi üçün
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://life.wolt.com/az/aze/howto/wolt-promo-codes")
        time.sleep(3)  # Sayfanın tam yüklənməsi üçün gözləyirik

        # Endirim məlumatlarını çəkirik
        promo_elements = driver.find_elements(By.CLASS_NAME, "promo-item")
        discounts = []
        for promo in promo_elements:
            title = promo.find_element(By.TAG_NAME, "h3").text
            description = promo.find_element(By.TAG_NAME, "p").text
            discounts.append(f"<b>{title}</b><br>{description}<br><br>")
        
        return discounts
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return []
    finally:
        driver.quit()

# Avtomatik işləmə funksiyası
def job():
    discounts = get_wolt_discounts()
    if discounts:
        subject = "Wolt Endirimləri"
        body = "".join(discounts)
        send_email(subject, body, "sənin_email@gmail.com", "sənin_email@gmail.com", "app_password")
    else:
        print("Endirim tapılmadı.")

# Cədvəl qurma
schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
