import reflex as rx

class RotatableGLTF(rx.Component):
    """Rotatable GLTF model component that spins on drag and resets on release."""

    tag = "RotatableGLTF"

    url: rx.Var[str]
    position: rx.Var[list[float]]
    scale: rx.Var[float]
    initial_rotation: rx.Var[list[float]] = [0, 0, 0]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const RotatableGLTF = ({ 
              url, 
              position=[0,0,0], 
              scale=1,
              initial_rotation=[0,0,0]
            }) => {
              const groupRef = React.useRef();
              const { gl } = useThree();
              const [isDragging, setIsDragging] = React.useState(false);
              const lastMousePos = React.useRef({ x: 0, y: 0 });
              
              // Load GLTF model
              const { scene } = useGLTF(url);
              const clonedScene = React.useMemo(() => scene.clone(), [scene]);

              const handlePointerDown = (event) => {
                event.stopPropagation();
                setIsDragging(true);
                gl.domElement.style.cursor = 'grabbing';
                lastMousePos.current = { x: event.clientX, y: event.clientY };
              };

              const handlePointerUp = () => {
                setIsDragging(false);
                gl.domElement.style.cursor = 'grab';
              };

              const handlePointerMove = (event) => {
                if (!isDragging || !groupRef.current) return;
                
                const deltaX = event.clientX - lastMousePos.current.x;
                const deltaY = event.clientY - lastMousePos.current.y;
                
                // Update rotation: horizontal = Y-axis, vertical = X-axis
                const rotationSpeed = 0.01;
                groupRef.current.rotation.y += deltaX * rotationSpeed;
                groupRef.current.rotation.x -= deltaY * rotationSpeed;
                
                // Clamp X rotation - limit forward tilt more (less negative)
                groupRef.current.rotation.x = Math.max(-Math.PI / 6, Math.min(Math.PI / 24, groupRef.current.rotation.x));
                
                lastMousePos.current = { x: event.clientX, y: event.clientY };
              };

              React.useEffect(() => {
                if (isDragging) {
                  document.addEventListener('pointermove', handlePointerMove);
                  document.addEventListener('pointerup', handlePointerUp);
                  return () => {
                    document.removeEventListener('pointermove', handlePointerMove);
                    document.removeEventListener('pointerup', handlePointerUp);
                  };
                }
              }, [isDragging]);

              // Animate back to initial rotation when not dragging
              useFrame(() => {
                if (!groupRef.current || isDragging) return;
                
                const current = groupRef.current.rotation;
                const target = initial_rotation;
                const lerpFactor = 0.04;
                
                current.x += (target[0] - current.x) * lerpFactor;
                current.y += (target[1] - current.y) * lerpFactor;
                current.z += (target[2] - current.z) * lerpFactor;
              });

              return (
                <group
                  ref={groupRef}
                  position={position}
                  scale={scale}
                  rotation={initial_rotation}
                  onPointerDown={handlePointerDown}
                  onPointerEnter={() => !isDragging && (gl.domElement.style.cursor = 'grab')}
                  onPointerLeave={() => !isDragging && (gl.domElement.style.cursor = 'default')}
                >
                  <primitive object={clonedScene} />
                </group>
              );
            };
            """
        ]


def create_rotatable_gltf(url, position=[0, 0, 0], scale=1.0, initial_rotation=[0, 0, 0]) -> RotatableGLTF:
    """Helper function to create a rotatable GLTF model."""
    return RotatableGLTF.create(
        url=url, 
        position=position, 
        scale=scale,
        initial_rotation=initial_rotation
    )

