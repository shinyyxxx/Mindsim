import os
import reflex as rx
import httpx
from .mentalfactorsdata import MENTAL_FACTOR_DATA

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")


class RegisterState(rx.State):
    email: str = ""
    password: str = ""
    agree_terms: bool = True
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    def set_email(self, value: str):
        self.email = value.strip()
        self._clear_feedback()

    def set_password(self, value: str):
        self.password = value
        self._clear_feedback()

    def set_agree_terms(self, value: bool):
        self.agree_terms = value
        self._clear_feedback()

    def _clear_feedback(self):
        self.error_message = ""
        self.success_message = ""

    async def register(self, form_data: dict | None = None):
        if self.is_loading:
            return

        if not self.email or not self.password:
            self.error_message = "Email and password are required."
            return

        if not self.agree_terms:
            self.error_message = "You must accept the terms to continue."
            return

        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        payload = {"email": self.email, "password": self.password}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(f"{BACKEND_URL}/register/", json=payload)

            if 200 <= response.status_code < 300:
                message = "Registration successful. You can now sign in."
                try:
                    data = response.json()
                    message = data.get("message") or data.get("detail") or message
                except ValueError:
                    pass

                self.success_message = message
                self.password = ""
                return rx.redirect("/login")
            else:
                try:
                    data = response.json()
                    detail = data.get("detail") or data.get("message")
                except ValueError:
                    detail = response.text.strip()

                self.error_message = detail or "Registration failed. Please try again."
        except httpx.HTTPError as exc:
            self.error_message = f"Could not reach the server: {exc}"
        finally:
            self.is_loading = False

    def reset_form(self):
        self.email = ""
        self.password = ""
        self.agree_terms = True
        self.error_message = ""
        self.success_message = ""


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    session_token: rx.Cookie = rx.Cookie(
        "",
        name="session_token",
        secure=False,
        same_site="lax",
    )
    user_email: rx.Cookie = rx.Cookie(
        "",
        name="user_email",
        secure=False,
        same_site="lax",
    )
    is_admin: bool = False

    def set_email(self, value: str):
        self.email = value.strip()
        self._clear_feedback()

    def set_password(self, value: str):
        self.password = value
        self._clear_feedback()

    def _clear_feedback(self):
        self.error_message = ""
        self.success_message = ""

    async def login(self, form_data: dict | None = None):
        if self.is_loading:
            return

        if not self.email or not self.password:
            self.error_message = "Email and password are required."
            return

        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        payload = {"email": self.email, "password": self.password}

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(f"{BACKEND_URL}/login/", json=payload)

            if 200 <= response.status_code < 300:
                message = "Login successful."
                try:
                    data = response.json()
                    message = data.get("message") or data.get("detail") or message
                except ValueError:
                    data = {}

                session_token = response.cookies.get("sessionid", "")
                email_cookie = response.cookies.get("email", "")

                self.session_token = rx.Cookie(
                    session_token,
                    name="session_token",
                    secure=False,
                    same_site="lax",
                )
                self.user_email = rx.Cookie(
                    email_cookie or data.get("email", self.email),
                    name="user_email",
                    secure=False,
                    same_site="lax",
                )
                self.is_admin = bool(data.get("is_admin"))
                self.success_message = message
                self.password = ""
                return rx.redirect("/")

            try:
                data = response.json()
                detail = data.get("detail") or data.get("message") or data.get("error")
            except ValueError:
                detail = response.text.strip()

            self.error_message = detail or "Login failed. Please try again."
            self.session_token = rx.Cookie(
                "",
                name="session_token",
                secure=False,
                same_site="lax",
            )
            self.user_email = rx.Cookie(
                "",
                name="user_email",
                secure=False,
                same_site="lax",
            )
        except httpx.HTTPError as exc:
            self.error_message = f"Could not reach the server: {exc}"
            self.session_token = rx.Cookie(
                "",
                name="session_token",
                secure=False,
                same_site="lax",
            )
            self.user_email = rx.Cookie(
                "",
                name="user_email",
                secure=False,
                same_site="lax",
            )
        finally:
            self.is_loading = False

    def reset_form(self):
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.success_message = ""
        self.session_token = rx.Cookie(
            "",
            name="session_token",
            secure=False,
            same_site="lax",
        )
        self.user_email = rx.Cookie(
            "",
            name="user_email",
            secure=False,
            same_site="lax",
        )
        self.is_admin = False


class MindState(rx.State):
    mental_factors_map: dict[str, list[dict]] = {}
    available_factors: list[dict] = MENTAL_FACTOR_DATA
    active_mind_id: str = "mind_0"

    @rx.var
    def mental_factors(self) -> list[dict]:
        return self.mental_factors_map.get(self.active_mind_id, [])

    @rx.var
    def mind_0_factors(self) -> list[dict]:
        return self.mental_factors_map.get("mind_0", [])

    @rx.var
    def mind_1_factors(self) -> list[dict]:
        return self.mental_factors_map.get("mind_1", [])

    def set_mind_0(self):
        self.active_mind_id = "mind_0"

    def set_mind_1(self):
        self.active_mind_id = "mind_1"

    def add_mental_factor(self, factor_name: str):
        target_mind = self.active_mind_id

        if target_mind not in self.mental_factors_map:
            self.mental_factors_map[target_mind] = []

        if any(f["name"] == factor_name for f in self.mental_factors_map[target_mind]):
            return

        factor = next((f for f in self.available_factors if f["name"] == factor_name), None)
        if factor:
            new_factor = {**factor, "position": [0, 0, 0]}
            self.mental_factors_map[target_mind] = self.mental_factors_map[target_mind] + [new_factor]