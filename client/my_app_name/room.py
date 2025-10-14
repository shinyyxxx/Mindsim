# room.py
import reflex as rx

class Room(rx.Component):
    """A 3D room component with walls, floor, and ceiling."""

    tag = "Room"

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const Room = () => {
              return (
                <group>
                  {/* Floor */}
                  <mesh position={[0, -2, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                    <planeGeometry args={[20, 20]} />
                    <meshStandardMaterial color="#8B4513" roughness={0.8} />
                  </mesh>

                  {/* Ceiling */}
                  <mesh position={[0, 8, 0]} rotation={[Math.PI / 2, 0, 0]} receiveShadow>
                    <planeGeometry args={[20, 20]} />
                    <meshStandardMaterial color="#F5F5DC" roughness={0.9} />
                  </mesh>

                  {/* Back wall */}
                  <mesh position={[0, 3, -10]} receiveShadow>
                    <planeGeometry args={[20, 10]} />
                    <meshStandardMaterial color="#DEB887" roughness={0.7} />
                  </mesh>

                  {/* Front wall */}
                  <mesh position={[0, 3, 10]} receiveShadow>
                    <planeGeometry args={[20, 10]} />
                    <meshStandardMaterial color="#DEB887" roughness={0.7} />
                  </mesh>

                  {/* Left wall */}
                  <mesh position={[-10, 3, 0]} rotation={[0, Math.PI / 2, 0]} receiveShadow>
                    <planeGeometry args={[20, 10]} />
                    <meshStandardMaterial color="#DEB887" roughness={0.7} />
                  </mesh>

                  {/* Right wall */}
                  <mesh position={[10, 3, 0]} rotation={[0, -Math.PI / 2, 0]} receiveShadow>
                    <planeGeometry args={[20, 10]} />
                    <meshStandardMaterial color="#DEB887" roughness={0.7} />
                  </mesh>

                  {/* (All furniture removed) */}
                </group>
              );
            };
            """
        ]


def create_room() -> Room:
    return Room.create()

