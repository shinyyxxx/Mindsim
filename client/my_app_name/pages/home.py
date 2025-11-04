import reflex as rx
from ..components.base import base_page
from ..components.canvacompo import R3FCanvas, ThreeScene, ModelViewer3D
from ..components.clickable_image import ClickableImage
from ..components.auto_rotating_gltf import AutoRotatingGLTF
from ..components.static_image import StaticImage
from ..components.rotatable_gltf import RotatableGLTF
from ..components.mentalfactor import Mind
from ..mentalfactorsdata import MENTAL_FACTOR_DATA

def home() -> rx.Component:
    """Homepage with welcome section and call-to-action."""
    
    hero_section = rx.vstack(
        rx.vstack(
            rx.image(
                src="/logo.jpg",
                width="4em",
                height="auto",
                border_radius="25%",
                margin_bottom="1em",
            ),
            rx.heading(
                "Welcome to Mindsim",
                size="9",
                weight="bold",
                text_align="center",
                background="linear-gradient(to right, #667eea 0%, #764ba2 100%)",
                background_clip="text",
                style={"-webkit-background-clip": "text", "-webkit-text-fill-color": "transparent"},
            ),
            rx.text(
                "Explore and visualize mental factors in an interactive 3D environment",
                size="6",
                text_align="center",
                color="gray",
                max_width="600px",
                margin_top="0.5em",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Get Started",
                        size="4",
                        color_scheme="blue",
                        padding_x="2em",
                    ),
                    href="/register",
                ),
                rx.link(
                    rx.button(
                        "Sign In",
                        size="4",
                        variant="outline",
                        color_scheme="blue",
                        padding_x="2em",
                    ),
                    href="/login",
                ),
                spacing="4",
                justify="center",
                margin_top="2em",
            ),
            spacing="4",
            align="center",
            width="100%",
            padding_y="4em",
        ),
        style={
            "width": "100%",
            "min_height": "60vh",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
            "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        },
    )
    
    features_section = rx.vstack(
        rx.heading(
            "The Five Skandhas",
            size="8",
            weight="bold",
            text_align="center",
            color="#333",
            margin_bottom="2em",
        ),
        rx.vstack(
            # Skandha 1: Rupa (Form) - card left, GLTF right
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.icon("circle", size=48),
                        style={"color": "#667eea"},
                    ),
                    rx.heading("Rupa (Form)", size="6", margin_top="1em", color="#333"),
                    rx.text(
                        "The physical form and material aspects of existence",
                        size="4",
                        text_align="center",
                        color="gray",
                    ),
                    align="center",
                    padding="2em",
                    spacing="3",
                    style={
                        "background": "white",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                # GLTF box for Rupa
                rx.box(
                    R3FCanvas.create(
                        ThreeScene.create(),
                        RotatableGLTF.create(
                            url=rx.asset("humanMind/human.gltf"),
                            position=[0, -18, 0],
                            scale=1.0,
                            initial_rotation=[0, 0, 0],
                        ),
                    ),
                    style={
                        "width": "100%",
                        "height": "300px",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "overflow": "hidden",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="1200px",
                wrap="wrap",
            ),
            # Skandha 2: Vedana (Sensation) - GLTF left, card right
            rx.hstack(
                # Emotion image for Vedana - static, non-interactive
                rx.box(
                    R3FCanvas.create(
                        ThreeScene.create(),
                        StaticImage.create(
                            image_url=rx.asset("emotion/emotion.png"),
                            position=[0, 0, 0],
                            scale=3.0,
                        ),
                    ),
                    style={
                        "width": "100%",
                        "height": "300px",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "overflow": "hidden",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                rx.vstack(
                    rx.box(
                        rx.icon("heart", size=48),
                        style={"color": "#e74c3c"},
                    ),
                    rx.heading("Vedana (Sensation)", size="6", margin_top="1em", color="#333"),
                    rx.text(
                        "Feelings and sensations arising from contact with objects",
                        size="4",
                        text_align="center",
                        color="gray",
                    ),
                    align="center",
                    padding="2em",
                    spacing="3",
                    style={
                        "background": "white",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="1200px",
                wrap="wrap",
            ),
            # Skandha 3: Samjna (Perception) - card left, GLTF right
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.icon("eye", size=48),
                        style={"color": "#764ba2"},
                    ),
                    rx.heading("Samjna (Perception)", size="6", margin_top="1em", color="#333"),
                    rx.text(
                        "Recognition and perception of objects and their characteristics",
                        size="4",
                        text_align="center",
                        color="gray",
                    ),
                    align="center",
                    padding="2em",
                    spacing="3",
                    style={
                        "background": "white",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                # Image box for Samjna (Perception)
                rx.box(
                    R3FCanvas.create(
                        ThreeScene.create(),
                        ClickableImage.create(
                            image_url=rx.asset("optical/opticBunny.png"),
                            position=[0, 0, 0],
                            scale=4.5,
                            initial_rotation=[0, 0, -0.5],
                        ),
                    ),
                    style={
                        "width": "100%",
                        "height": "300px",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "overflow": "hidden",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="1200px",
                wrap="wrap",
            ),
            # Skandha 4: Samskara (Mental Formations) - GLTF left, card right
            rx.hstack(
                # Mental sphere with bouncing factors for Samskara
                rx.box(
                    R3FCanvas.create(
                        ThreeScene.create(),
                        Mind.create(
                            mental_spheres=MENTAL_FACTOR_DATA,
                            container_radius=3.0,
                            container_opacity=0.3,
                            position=[0, 0, 0],
                            glass_tint="#f39c12",
                            glass_transmission=0.9,
                            glass_thickness=0.4,
                            glass_roughness=0.05,
                        ),
                    ),
                    style={
                        "width": "100%",
                        "height": "300px",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "overflow": "hidden",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                rx.vstack(
                    rx.box(
                        rx.icon("layers", size=48),
                        style={"color": "#f39c12"},
                    ),
                    rx.heading("Samskara (Mental Formations)", size="6", margin_top="1em", color="#333"),
                    rx.text(
                        "Volitional factors, mental formations, and conditioned responses",
                        size="4",
                        text_align="center",
                        color="gray",
                    ),
                    align="center",
                    padding="2em",
                    spacing="3",
                    style={
                        "background": "white",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="1200px",
                wrap="wrap",
            ),
            # Skandha 5: Vijnana (Consciousness) - card left, GLTF right
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.icon("brain", size=48),
                        style={"color": "#27ae60"},
                    ),
                    rx.heading("Vijnana (Consciousness)", size="6", margin_top="1em", color="#333"),
                    rx.text(
                        "Awareness and consciousness that cognizes and distinguishes",
                        size="4",
                        text_align="center",
                        color="gray",
                    ),
                    align="center",
                    padding="2em",
                    spacing="3",
                    style={
                        "background": "white",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                # GLTF box for Vijnana - auto-rotating, non-interactable
                rx.box(
                    R3FCanvas.create(
                        ThreeScene.create(),
                        AutoRotatingGLTF.create(
                            url=rx.asset("brain/scene.gltf"),
                            position=[0, -1.0, 0],
                            scale=0.02,
                            rotation_speed=0.3,
                        ),
                    ),
                    style={
                        "width": "100%",
                        "height": "300px",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                        "overflow": "hidden",
                        "flex": "1",
                        "min_width": "300px",
                    },
                ),
                spacing="6",
                align="center",
                width="100%",
                max_width="1200px",
                wrap="wrap",
            ),
            spacing="6",
            align="center",
            width="100%",
        ),
        spacing="6",
        align="center",
        width="100%",
        padding_y="4em",
        padding_x="2em",
        style={"background": "white"},
    )
    
    cta_section = rx.vstack(
        rx.heading(
            "Ready to explore?",
            size="8",
            weight="bold",
            text_align="center",
            color="white",
        ),
        rx.text(
            "Join Mindsim today and start visualizing mental factors",
            size="5",
            text_align="center",
            color="rgba(255, 255, 255, 0.9)",
            margin_top="0.5em",
        ),
        rx.hstack(
            rx.link(
                rx.button(
                    "Create Account",
                    size="4",
                    color_scheme="blue",
                    padding_x="2em",
                ),
                href="/register",
            ),
            rx.link(
                rx.button(
                    "Learn More",
                    size="4",
                    variant="outline",
                    color_scheme="gray",
                    padding_x="2em",
                ),
                href="/login",
            ),
            spacing="4",
            justify="center",
            margin_top="2em",
        ),
        spacing="4",
        align="center",
        width="100%",
        padding_y="4em",
        style={
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        },
    )
    
    page_content = rx.vstack(
        hero_section,
        features_section,
        cta_section,
        spacing="0",
        width="100%",
        style={"min_height": "100vh"},
    )
    
    return base_page(page_content, allow_scroll=True)

