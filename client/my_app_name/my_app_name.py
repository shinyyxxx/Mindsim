from reflex.components.component import NoSSRComponent
import reflex as rx
from .pages.demo import first_page


app = rx.App()
app.add_page(first_page, route='/')

if __name__ == "__main__":
    app.run()