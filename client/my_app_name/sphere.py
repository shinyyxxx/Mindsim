# sphere.py
import reflex as rx

class Sphere(rx.Component):
    """A 3D sphere component for R3F."""

    tag = "Sphere"

    position: rx.Var[list[float]]
    color: rx.Var[str]
    size: rx.Var[float]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const Sphere = ({ position=[0,0,0], color="orange", size=1 }) => {
              const meshRef = React.useRef();

              // Rotate animation
              useFrame(() => {
                if (meshRef.current) {
                  meshRef.current.rotation.y += 0.01;
                  meshRef.current.rotation.x += 0.005;
                }
              });

              return (
                <mesh ref={meshRef} position={position} castShadow receiveShadow>
                  <sphereGeometry args={[size, 64, 64]} />
                  <meshStandardMaterial
                    color={color}
                    roughness={0.4}
                    metalness={0.2}
                  />
                </mesh>
              );
            };
            """
        ]


def create_sphere(position=[0, 0, 0], color="orange", size=1.0) -> Sphere:
    return Sphere.create(position=position, color=color, size=size)
