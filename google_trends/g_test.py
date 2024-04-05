def login(driver, user=None):
    username = os.environ.get('google_email')
    password = os.environ.get('google_password')

    # url = "https://authn.edx.org/login"
    url = 'https://trends.google.com/'

    driver = load_page(url, driver)