# collision.py
import reflex as rx
import json

class CollisionBoundaries(rx.Component):
    """Component that provides collision boundary data for rooms."""
    tag = "CollisionBoundaries"

    def __init__(self, room_configs, **kwargs):
        super().__init__(**kwargs)
        self.room_configs = room_configs

    def add_custom_code(self) -> list[str]:
        # Convert room configs to JSON for use in JS
        rooms_json = json.dumps(self.room_configs)
        
        return [
            f"""
            export const CollisionBoundaries = () => {{
              const {{ camera }} = useThree();
              const rooms = {rooms_json};
              
              // Door dimensions
              const doorWidth = 3;
              const doorHeight = 6;
              
              // Check if position collides with walls
              const checkCollision = (x, z) => {{
                const wallBuffer = 0.8; // Distance to keep from walls (reduced for better door access)
                let insideAnyRoom = false;
                
                // First check if we're inside any room (with small margin)
                for (const room of rooms) {{
                  const [px, py, pz] = room.position;
                  const w = room.width;
                  const l = room.length;
                  
                  const xMin = px - w/2;
                  const xMax = px + w/2;
                  const zMin = pz - l/2;
                  const zMax = pz + l/2;
                  
                  // Check with small outward margin to allow doorway transitions
                  if (x >= xMin - 1 && x <= xMax + 1 && z >= zMin - 1 && z <= zMax + 1) {{
                    insideAnyRoom = true;
                    break;
                  }}
                }}
                
                // If not near any room, block movement
                if (!insideAnyRoom) {{
                  return true; // Collision - too far from all rooms
                }}
                
                // Now check collision with walls (respecting doors)
                for (const room of rooms) {{
                  const [px, py, pz] = room.position;
                  const w = room.width;
                  const l = room.length;
                  const doors = room.doors || [];
                  
                  const xMin = px - w/2;
                  const xMax = px + w/2;
                  const zMin = pz - l/2;
                  const zMax = pz + l/2;
                  
                  // Left wall
                  if (!doors.includes('left')) {{
                    if (x < xMin + wallBuffer && x > xMin - wallBuffer && z >= zMin && z <= zMax) {{
                      return true; // Solid wall
                    }}
                  }} else {{
                    // Wall with door - check if hitting wall segments
                    if (x < xMin + wallBuffer && x > xMin - wallBuffer) {{
                      const doorOffset = doorWidth / 2;
                      if ((z < pz - doorOffset || z > pz + doorOffset) && z >= zMin && z <= zMax) {{
                        return true; // Hit wall segment beside door
                      }}
                    }}
                  }}
                  
                  // Right wall
                  if (!doors.includes('right')) {{
                    if (x > xMax - wallBuffer && x < xMax + wallBuffer && z >= zMin && z <= zMax) {{
                      return true;
                    }}
                  }} else {{
                    if (x > xMax - wallBuffer && x < xMax + wallBuffer) {{
                      const doorOffset = doorWidth / 2;
                      if ((z < pz - doorOffset || z > pz + doorOffset) && z >= zMin && z <= zMax) {{
                        return true;
                      }}
                    }}
                  }}
                  
                  // Back wall
                  if (!doors.includes('back')) {{
                    if (z < zMin + wallBuffer && z > zMin - wallBuffer && x >= xMin && x <= xMax) {{
                      return true;
                    }}
                  }} else {{
                    if (z < zMin + wallBuffer && z > zMin - wallBuffer) {{
                      const doorOffset = doorWidth / 2;
                      if ((x < px - doorOffset || x > px + doorOffset) && x >= xMin && x <= xMax) {{
                        return true;
                      }}
                    }}
                  }}
                  
                  // Front wall
                  if (!doors.includes('front')) {{
                    if (z > zMax - wallBuffer && z < zMax + wallBuffer && x >= xMin && x <= xMax) {{
                      return true;
                    }}
                  }} else {{
                    if (z > zMax - wallBuffer && z < zMax + wallBuffer) {{
                      const doorOffset = doorWidth / 2;
                      if ((x < px - doorOffset || x > px + doorOffset) && x >= xMin && x <= xMax) {{
                        return true;
                      }}
                    }}
                  }}
                }}
                
                return false; // No collision
              }};
              
              // Store collision function globally so Player can access it
              useEffect(() => {{
                window.checkCollision = checkCollision;
              }}, []);
              
              return null;
            }};
            """
        ]

def create_collision_boundaries(room_configs):
    """Factory for collision boundaries."""
    return CollisionBoundaries.create(room_configs=room_configs)

