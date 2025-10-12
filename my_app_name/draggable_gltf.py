import reflex as rx

class DraggableGLTF(rx.Component):
    """Draggable GLTF model component for R3F."""

    tag = "DraggableGLTF"

    url: rx.Var[str]
    position: rx.Var[list[float]]
    scale: rx.Var[float]
    rotation: rx.Var[list[float]]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const DraggableGLTF = ({ 
              url, 
              position=[0,0,0], 
              scale=1, 
              rotation=[0,0,0] 
            }) => {
              const groupRef = React.useRef();
              const { camera, gl } = useThree();
              const [isDragging, setIsDragging] = React.useState(false);
              const [currentPosition, setCurrentPosition] = React.useState(position);
              const [dragOffset, setDragOffset] = React.useState([0, 0]);
              
              const raycaster = React.useMemo(() => new THREE.Raycaster(), []);
              const dragPlane = React.useMemo(() => 
                new THREE.Plane(new THREE.Vector3(0, 0, 1), -position[2]), 
                [position]
              );

              // Load GLTF model
              const { scene } = useGLTF(url);
              
              // Clone the scene to avoid reusing the same instance
              const clonedScene = React.useMemo(() => scene.clone(), [scene]);

              const handlePointerDown = (event) => {
                event.stopPropagation();
                setIsDragging(true);
                gl.domElement.style.cursor = 'grabbing';
                
                console.log('Model clicked at position:', currentPosition);
                
                const mouse = new THREE.Vector2(
                  (event.clientX / window.innerWidth) * 2 - 1,
                  -(event.clientY / window.innerHeight) * 2 + 1
                );
                
                raycaster.setFromCamera(mouse, camera);
                const intersectPoint = new THREE.Vector3();
                raycaster.ray.intersectPlane(dragPlane, intersectPoint);
                
                setDragOffset([
                  currentPosition[0] - intersectPoint.x,
                  currentPosition[1] - intersectPoint.y
                ]);
              };

              const handlePointerUp = () => {
                setIsDragging(false);
                gl.domElement.style.cursor = 'grab';
              };

              const handlePointerMove = (event) => {
                if (!isDragging) return;
                
                const mouse = new THREE.Vector2(
                  (event.clientX / window.innerWidth) * 2 - 1,
                  -(event.clientY / window.innerHeight) * 2 + 1
                );
                
                raycaster.setFromCamera(mouse, camera);
                const intersectPoint = new THREE.Vector3();
                raycaster.ray.intersectPlane(dragPlane, intersectPoint);
                
                const newPosition = [
                  intersectPoint.x + dragOffset[0],
                  intersectPoint.y + dragOffset[1],
                  currentPosition[2]
                ];
                
                setCurrentPosition(newPosition);
                
                if (groupRef.current) {
                  groupRef.current.position.set(...newPosition);
                }
              };

              React.useEffect(() => {
                if (isDragging) {
                  const handleGlobalPointerMove = (event) => handlePointerMove(event);
                  const handleGlobalPointerUp = () => handlePointerUp();
                  
                  document.addEventListener('pointermove', handleGlobalPointerMove);
                  document.addEventListener('pointerup', handleGlobalPointerUp);
                  
                  return () => {
                    document.removeEventListener('pointermove', handleGlobalPointerMove);
                    document.removeEventListener('pointerup', handleGlobalPointerUp);
                  };
                }
              }, [isDragging, dragOffset]);

              return (
                <group
                  ref={groupRef}
                  position={currentPosition}
                  scale={scale}
                  rotation={rotation}
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


def create_draggable_gltf(url, position=[0, 0, 0], scale=1.0, rotation=[0, 0, 0]) -> DraggableGLTF:
    """Helper function to create a draggable GLTF model."""
    return DraggableGLTF.create(
        url=url, 
        position=position, 
        scale=scale, 
        rotation=rotation
    )