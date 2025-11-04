# components/base_page.py
import reflex as rx
from .navbar import navbar

def base_page(child: rx.Component, allow_scroll: bool = False) -> rx.Component:
    return rx.box(
        # Top navigation bar
        # navbar(),

        rx.box(
            child,
            style={
                "flex": "1",
                "width": "100%",
                "height": "100%" if not allow_scroll else "auto",
                "overflow_y": "auto" if allow_scroll else "hidden",
            },
        ),

        style={
            "display": "flex",
            "flex_direction": "column",
            "width": "100vw",
            "height": "100vh",
            "overflow": "hidden",
        },
    )
