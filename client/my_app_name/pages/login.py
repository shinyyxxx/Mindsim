import reflex as rx
from ..components.base import base_page
from ..state import LoginState


def login() -> rx.Component:
    login_card = rx.card(
        rx.form(
            rx.vstack(
                rx.flex(
                    rx.image(
                        src="/logo.jpg",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Sign in to your account", size="6", as_="h2", width="100%"),
                    rx.hstack(
                        rx.text("New here?", size="3", text_align="left"),
                        rx.link("Sign up", href="/register", size="3"),
                        spacing="2",
                        opacity="0.8",
                        width="100%",
                    ),
                    justify="start",
                    direction="column",
                    spacing="4",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Email address",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        placeholder="user@example.com",
                        type="email",
                        size="3",
                        width="100%",
                        name="email",
                        value=LoginState.email,
                        on_change=LoginState.set_email,
                    ),
                    spacing="2",
                    justify="start",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Password", size="3", weight="medium"),
                        rx.link("Forgot password?", href="#", size="3"),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Enter your password",
                        type="password",
                        size="3",
                        width="100%",
                        name="password",
                        value=LoginState.password,
                        on_change=LoginState.set_password,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.cond(
                    LoginState.error_message != "",
                    rx.text(
                        LoginState.error_message,
                        color="red",
                        font_size="0.9em",
                        text_align="left",
                        width="100%",
                    ),
                ),
                rx.button(
                    "Sign in",
                    size="3",
                    width="100%",
                    type="submit",
                    loading=LoginState.is_loading,
                    disabled=LoginState.is_loading,
                ),
                rx.hstack(
                    rx.divider(margin="0"),
                    rx.text("Or continue with", white_space="nowrap", weight="medium"),
                    rx.divider(margin="0"),
                    align="center",
                    width="100%",
                ),
                rx.center(
                    rx.icon_button(rx.icon(tag="github"), variant="soft", size="3"),
                    rx.icon_button(rx.icon(tag="facebook"), variant="soft", size="3"),
                    rx.icon_button(rx.icon(tag="twitter"), variant="soft", size="3"),
                    spacing="4",
                    direction="row",
                    width="100%",
                ),
                spacing="6",
                width="100%",
            ),
            on_submit=LoginState.login,
        ),
        size="4",
        max_width="28em",
        width="100%",
    )

    page_content = rx.center(
        login_card,
        style={
            "width": "100%",
            "height": "100%",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
        },
    )

    return base_page(page_content)

