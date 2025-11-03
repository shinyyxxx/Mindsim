import reflex as rx
from ..components.draggable_gltf import DraggableGLTF
from ..components.base import base_page
from ..components.mentalfactor import MentalSphere, Mind
from ..components.player import Player, create_player
from ..components.canvacompo import R3FCanvas, ThreeScene, ModelViewer3D
from ..state import MindState


def mental_factor_item(factor: dict) -> rx.Component:
    """Create a clickable mental factor item for the UI panel."""
    return rx.box(
        rx.box(
            rx.text(
                factor["name"],
                font_size="16px",
                font_weight="bold",
                color="white",
            ),
            style={
                "background": factor["color"],
                "padding": "12px 16px",
                "border_radius": "8px",
                "cursor": "grab",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.2)",
                "transition": "all 0.3s ease",
                "width": "100%",
                "text_align": "center",
            },
            on_click=MindState.add_mental_factor(factor["name"]),
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 4px 8px rgba(0,0,0,0.3)",
            },
        ),
        style={
            "width": "100%",
            "margin_bottom": "8px",
        },
    )


def first_page() -> rx.Component:
    """Main page with 3D canvas and mental factor UI."""
    
    side_panel = rx.box(
        rx.box(
            rx.heading(
                "Mental Factors",
                font_size="20px",
                font_weight="bold",
                margin_bottom="16px",
            ),
            rx.vstack(
                rx.text(
                    "Select Mind:",
                    font_size="14px",
                    font_weight="bold",
                    color="#333",
                ),
                rx.hstack(
                    rx.button(
                        "Mind 1",
                        on_click=MindState.set_mind_0,
                        size="2",
                        color_scheme=rx.cond(MindState.active_mind_id == "mind_0", "blue", "gray"),
                        variant=rx.cond(MindState.active_mind_id == "mind_0", "solid", "outline"),
                        width="50%",
                    ),
                    rx.button(
                        "Mind 2",
                        on_click=MindState.set_mind_1,
                        size="2",
                        color_scheme=rx.cond(MindState.active_mind_id == "mind_1", "blue", "gray"),
                        variant=rx.cond(MindState.active_mind_id == "mind_1", "solid", "outline"),
                        width="50%",
                    ),
                    width="100%",
                    spacing="2",
                ),
                width="100%",
                align="stretch",
                spacing="2",
                margin_bottom="16px",
            ),
            rx.text(
                "Click to add to active mind",
                font_size="14px",
                color="#666",
                margin_bottom="16px",
            ),
            rx.foreach(
                MindState.available_factors,
                mental_factor_item,
            ),
            style={
                "padding": "20px",
                "background": "rgba(255, 255, 255, 0.95)",
                "border_radius": "12px",
                "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                "backdrop_filter": "blur(10px)",
            },
        ),
        style={
            "position": "absolute",
            "top": "20px",
            "right": "20px",
            "width": "220px",
            "z_index": "1000",
        },
    )

    my_child = R3FCanvas.create(
        ThreeScene.create(),
        ModelViewer3D.create(
            url=rx.asset("LabPlan.gltf"),
            position=[0, 0, 0],
            scale=1.0,
        ),
        create_player(),
        ModelViewer3D.create(
            url=rx.asset("humanMind/human.gltf"),
            position=[3, 0, -3.5],
            scale=0.1,
        ),
        # Mind 1
        Mind.create(
            mental_spheres=MindState.mind_0_factors,
            mind_id="mind_0",
            container_radius=0.5,
            container_opacity=0.3,
            position=[3, 1.5, -3.5]
        ),
        # Mind 2
        Mind.create(
            mental_spheres=MindState.mind_1_factors,
            mind_id="mind_1",
            container_radius=0.5,
            container_opacity=0.3,
            position=[-3, 1.5, -3.5]
        ),
        style={
            "width": "100%",
            "height": "calc(100vh - 80px)",
        },
    )

    # Combine everything in a relative container
    page_content = rx.box(
        my_child,
        side_panel,
        style={
            "position": "relative",
            "width": "100%",
            "height": "100%",
        },
    )

    return base_page(page_content)