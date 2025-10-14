# player.py
import reflex as rx

class Player(rx.Component):
    """A first-person player component with WASD movement and mouse look."""

    tag = "Player"

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const Player = () => {
              const { camera } = useThree();
              const [keys, setKeys] = useState({});
              const [isPointerLocked, setIsPointerLocked] = useState(false);
              const moveSpeed = 0.05;
              const lookSpeed = 0.0005;
              
              // Create reusable Euler object to prevent snapping
              const euler = new THREE.Euler(0, 0, 0, 'YXZ');

              // Set initial camera position
              useEffect(() => {
                camera.position.set(0, 1.5, 5);
                camera.lookAt(0, 1.5, 0);
              }, [camera]);

              // Handle keyboard input
              useEffect(() => {
                const handleKeyDown = (event) => {
                  console.log('Key pressed:', event.code);
                  setKeys(prev => ({ ...prev, [event.code]: true }));
                  
                  // Handle E key for pointer lock toggle
                  if (event.code === 'KeyE') {
                    if (isPointerLocked) {
                      document.exitPointerLock();
                    } else {
                      document.body.requestPointerLock();
                    }
                  }
                };

                const handleKeyUp = (event) => {
                  console.log('Key released:', event.code);
                  setKeys(prev => ({ ...prev, [event.code]: false }));
                };

                window.addEventListener('keydown', handleKeyDown);
                window.addEventListener('keyup', handleKeyUp);

                return () => {
                  window.removeEventListener('keydown', handleKeyDown);
                  window.removeEventListener('keyup', handleKeyUp);
                };
              }, [isPointerLocked]);

              // Handle mouse movement for camera look
              useEffect(() => {
                const handleMouseMove = (event) => {
                  if (isPointerLocked) {
                    const deltaX = event.movementX;
                    const deltaY = event.movementY;
                    
                    // Use Euler angles for proper FPS camera
                    euler.setFromQuaternion(camera.quaternion);
                    
                    // Update yaw and pitch
                    euler.y -= deltaX * lookSpeed;
                    euler.x -= deltaY * lookSpeed;
                    
                    // Clamp pitch to prevent over-rotation
                    euler.x = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, euler.x));
                    
                    // Apply the rotation
                    camera.quaternion.setFromEuler(euler);
                  }
                };

                const handlePointerLockChange = () => {
                  const locked = document.pointerLockElement === document.body;
                  console.log('Pointer lock changed:', locked);
                  setIsPointerLocked(locked);
                };

                document.addEventListener('mousemove', handleMouseMove);
                document.addEventListener('pointerlockchange', handlePointerLockChange);

                return () => {
                  document.removeEventListener('mousemove', handleMouseMove);
                  document.removeEventListener('pointerlockchange', handlePointerLockChange);
                };
              }, [camera, isPointerLocked]);

              // Movement logic
              useFrame(() => {
                if (!isPointerLocked) return;

                // Get camera rotation as Euler angles
                euler.setFromQuaternion(camera.quaternion);
                
                // Calculate movement vectors from yaw only (ignore pitch for horizontal movement)
                const yaw = euler.y;
                const forward = new THREE.Vector3(
                  -Math.sin(yaw),
                  0,
                  -Math.cos(yaw)
                );
                const right = new THREE.Vector3(
                  Math.cos(yaw),
                  0,
                  -Math.sin(yaw)
                );

                // Apply movement based on pressed keys
                if (keys['KeyW']) {
                  camera.position.addScaledVector(forward, moveSpeed);
                }
                if (keys['KeyS']) {
                  camera.position.addScaledVector(forward, -moveSpeed);
                }
                if (keys['KeyA']) {
                  camera.position.addScaledVector(right, -moveSpeed);
                }
                if (keys['KeyD']) {
                  camera.position.addScaledVector(right, moveSpeed);
                }

                // Keep player above ground
                if (camera.position.y < 1) {
                  camera.position.y = 1;
                }

                // Keep player within room bounds
                const roomSize = 8;
                camera.position.x = Math.max(-roomSize, Math.min(roomSize, camera.position.x));
                camera.position.z = Math.max(-roomSize, Math.min(roomSize, camera.position.z));
              });

              return null; // Player doesn't render anything visible
            };
            """
        ]


def create_player() -> Player:
    return Player.create()