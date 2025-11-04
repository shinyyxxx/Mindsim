from reflex.components.component import NoSSRComponent
import reflex as rx
from .pages.home import home
from .pages.demo import first_page
from .pages.login import login
from .pages.register import signup


app = rx.App()
app.add_page(home, route='/')
app.add_page(first_page, route='/demo')
app.add_page(login, route='/login')
app.add_page(signup, route='/register')

if __name__ == "__main__":
    app.run()