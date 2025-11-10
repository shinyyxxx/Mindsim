import reflex as rx

config = rx.Config(
    app_name="my_app_name",
    frontend_packages=[
        "@react-three/fiber@9.3.0",
        "@react-three/drei@10.7.6",
        "three@0.179.1",
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)