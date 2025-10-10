import reflex as rx

class DraggableCube(rx.Component):
    """Cube with custom drag controls."""

    tag = "DraggableCube"

    position: rx.Var[list[float]]
    color: rx.Var[str]
    size: rx.Var[float]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const DraggableCube = ({ position=[0,0,0], color="skyblue", size=1 }) => {
              const meshRef = React.useRef();
              const { camera, gl, scene } = useThree();
              const [isDragging, setIsDragging] = React.useState(false);
              const [currentPosition, setCurrentPosition] = React.useState(position);
              const [dragOffset, setDragOffset] = React.useState([0, 0]);
              
              const raycaster = React.useMemo(() => new THREE.Raycaster(), []);
              const dragPlane = React.useMemo(() => new THREE.Plane(new THREE.Vector3(0, 0, 1), -position[2]), [position]);

              const handlePointerDown = (event) => {
                event.stopPropagation();
                setIsDragging(true);
                gl.domElement.style.cursor = 'grabbing';
                
                // Calculate initial drag offset
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
                
                if (meshRef.current) {
                  meshRef.current.position.set(...newPosition);
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
                <mesh
                  ref={meshRef}
                  position={currentPosition}
                  castShadow
                  receiveShadow
                  onPointerDown={handlePointerDown}
                  onPointerEnter={() => !isDragging && (gl.domElement.style.cursor = 'grab')}
                  onPointerLeave={() => !isDragging && (gl.domElement.style.cursor = 'default')}
                  scale={isDragging ? [1.1, 1.1, 1.1] : [1, 1, 1]}
                >
                  <boxGeometry args={[size, size, size]} />
                  <meshStandardMaterial color={color} />
                </mesh>
              );
            };
            """
        ]