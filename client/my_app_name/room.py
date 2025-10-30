# room.py
import reflex as rx

class Room(rx.Component):
    """A 3D room component with customizable walls, floor, and ceiling."""
    tag = "Room"

    def __init__(self, rooms, **kwargs):
        super().__init__(**kwargs)
        self.rooms = rooms

    def add_custom_code(self) -> list[str]:
        room_jsx = ""
        for i, room in enumerate(self.rooms):
            px, py, pz = room.get("position", (0,0,0))
            w = room.get("width", 20)
            l = room.get("length", 20)
            h = room.get("height", 10)
            c = room.get("color", "#FFFFFF")
            doors = room.get("doors", [])  # List of door positions: "front", "back", "left", "right"
            
            y_floor = -2
            y_ceil = h - 2
            y_mid = (h / 2) - 2
            x_left = -(w / 2)
            x_right = (w / 2)
            z_back = -(l / 2)
            z_front = (l / 2)

            # Prebuild strings with single JSX braces
            group_pos = '{' + f'[{px}, {py}, {pz}]' + '}'
            floor_pos = '{' + f'[0, {y_floor}, 0]' + '}'
            ceil_pos = '{' + f'[0, {y_ceil}, 0]' + '}'

            args_wl = '{' + f'[{w}, {l}]' + '}'

            rot_down = '{[-Math.PI / 2, 0, 0]}'
            rot_up = '{[Math.PI / 2, 0, 0]}'
            rot_left = '{[0, Math.PI / 2, 0]}'
            rot_right = '{[0, -Math.PI / 2, 0]}'
            
            # Door dimensions
            door_width = 3
            door_height = 6

            room_jsx += f"""
                  <group key={{{i}}} position={group_pos}>
                    <mesh position={floor_pos} rotation={rot_down} receiveShadow>
                      <planeGeometry args={args_wl} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.8}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={ceil_pos} rotation={rot_up} receiveShadow>
                      <planeGeometry args={args_wl} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.9}} side={{THREE.DoubleSide}} />
                    </mesh>
            """
            
            # Back wall (with optional door)
            if "back" not in doors:
                back_pos = '{' + f'[0, {y_mid}, {z_back}]' + '}'
                args_wh = '{' + f'[{w}, {h}]' + '}'
                room_jsx += f"""
                    <mesh position={back_pos} receiveShadow>
                      <planeGeometry args={args_wh} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            else:
                # Create wall segments around door
                wall_side_width = (w - door_width) / 2
                wall_top_height = h - door_height
                
                # Left segment
                left_seg_pos = '{' + f'[{-w/4 - door_width/4}, {y_mid}, {z_back}]' + '}'
                left_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                # Right segment
                right_seg_pos = '{' + f'[{w/4 + door_width/4}, {y_mid}, {z_back}]' + '}'
                right_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                # Top segment
                top_seg_pos = '{' + f'[0, {y_mid + door_height/2 + wall_top_height/2}, {z_back}]' + '}'
                top_seg_args = '{' + f'[{door_width}, {wall_top_height}]' + '}'
                
                room_jsx += f"""
                    <mesh position={left_seg_pos} receiveShadow>
                      <planeGeometry args={left_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={right_seg_pos} receiveShadow>
                      <planeGeometry args={right_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={top_seg_pos} receiveShadow>
                      <planeGeometry args={top_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            
            # Front wall (with optional door)
            if "front" not in doors:
                front_pos = '{' + f'[0, {y_mid}, {z_front}]' + '}'
                args_wh = '{' + f'[{w}, {h}]' + '}'
                room_jsx += f"""
                    <mesh position={front_pos} receiveShadow>
                      <planeGeometry args={args_wh} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            else:
                # Create wall segments around door
                wall_side_width = (w - door_width) / 2
                wall_top_height = h - door_height
                
                left_seg_pos = '{' + f'[{-w/4 - door_width/4}, {y_mid}, {z_front}]' + '}'
                left_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                right_seg_pos = '{' + f'[{w/4 + door_width/4}, {y_mid}, {z_front}]' + '}'
                right_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                top_seg_pos = '{' + f'[0, {y_mid + door_height/2 + wall_top_height/2}, {z_front}]' + '}'
                top_seg_args = '{' + f'[{door_width}, {wall_top_height}]' + '}'
                
                room_jsx += f"""
                    <mesh position={left_seg_pos} receiveShadow>
                      <planeGeometry args={left_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={right_seg_pos} receiveShadow>
                      <planeGeometry args={right_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={top_seg_pos} receiveShadow>
                      <planeGeometry args={top_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            
            # Left wall (with optional door)
            if "left" not in doors:
                left_pos = '{' + f'[{x_left}, {y_mid}, 0]' + '}'
                args_lh = '{' + f'[{l}, {h}]' + '}'
                room_jsx += f"""
                    <mesh position={left_pos} rotation={rot_left} receiveShadow>
                      <planeGeometry args={args_lh} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            else:
                wall_side_width = (l - door_width) / 2
                wall_top_height = h - door_height
                
                left_seg_pos = '{' + f'[{x_left}, {y_mid}, {-l/4 - door_width/4}]' + '}'
                left_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                right_seg_pos = '{' + f'[{x_left}, {y_mid}, {l/4 + door_width/4}]' + '}'
                right_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                top_seg_pos = '{' + f'[{x_left}, {y_mid + door_height/2 + wall_top_height/2}, 0]' + '}'
                top_seg_args = '{' + f'[{door_width}, {wall_top_height}]' + '}'
                
                room_jsx += f"""
                    <mesh position={left_seg_pos} rotation={rot_left} receiveShadow>
                      <planeGeometry args={left_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={right_seg_pos} rotation={rot_left} receiveShadow>
                      <planeGeometry args={right_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={top_seg_pos} rotation={rot_left} receiveShadow>
                      <planeGeometry args={top_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            
            # Right wall (with optional door)
            if "right" not in doors:
                right_pos = '{' + f'[{x_right}, {y_mid}, 0]' + '}'
                args_lh = '{' + f'[{l}, {h}]' + '}'
                room_jsx += f"""
                    <mesh position={right_pos} rotation={rot_right} receiveShadow>
                      <planeGeometry args={args_lh} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            else:
                wall_side_width = (l - door_width) / 2
                wall_top_height = h - door_height
                
                left_seg_pos = '{' + f'[{x_right}, {y_mid}, {-l/4 - door_width/4}]' + '}'
                left_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                right_seg_pos = '{' + f'[{x_right}, {y_mid}, {l/4 + door_width/4}]' + '}'
                right_seg_args = '{' + f'[{wall_side_width}, {h}]' + '}'
                top_seg_pos = '{' + f'[{x_right}, {y_mid + door_height/2 + wall_top_height/2}, 0]' + '}'
                top_seg_args = '{' + f'[{door_width}, {wall_top_height}]' + '}'
                
                room_jsx += f"""
                    <mesh position={left_seg_pos} rotation={rot_right} receiveShadow>
                      <planeGeometry args={left_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={right_seg_pos} rotation={rot_right} receiveShadow>
                      <planeGeometry args={right_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                    <mesh position={top_seg_pos} rotation={rot_right} receiveShadow>
                      <planeGeometry args={top_seg_args} />
                      <meshStandardMaterial color=\"{c}\" roughness={{0.7}} side={{THREE.DoubleSide}} />
                    </mesh>
                """
            
            room_jsx += """
                  </group>
            """
        return [
            f"""
            export const Room = () => {{
              return (<group>{room_jsx}\n</group>);
            }};
            """
        ]

def create_rooms(room_configs=None):
    """Factory for one or more rooms."""
    if not room_configs:
        # Default single room
        room_configs = [{
            "position": (0,0,0),
            "width": 20,
            "length": 20,
            "height": 10,
            "color": "#FFFFFF"
        }]
    return Room.create(rooms=room_configs)

def create_room():
    # Backwards compatibility: creates default room
    return create_rooms()

