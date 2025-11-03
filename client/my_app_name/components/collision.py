# collision.py
import reflex as rx

class GLTFCollision(rx.Component):
    """Component that provides collision detection for GLTF room models using raycasting."""
    tag = "GLTFCollision"

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const GLTFCollision = () => {
              const { scene, camera } = useThree();
              const raycaster = React.useMemo(() => new THREE.Raycaster(), []);
              const playerRadius = 0.5; // Player collision radius
              const collisionHeight = 1.5; // Height to check collisions at (player eye level)
              
              // Collect all meshes from the GLTF room model for collision detection
              const getRoomMeshes = React.useCallback(() => {
                const meshes = [];
                
                // Search the scene for all meshes
                scene.traverse((child) => {
                  if (child.isMesh && child.geometry) {
                    // Skip camera
                    if (child === camera) return;
                    
                    // Skip very small objects (likely characters or small props)
                    // Check bounding sphere radius
                    child.geometry.computeBoundingSphere();
                    const radius = child.geometry.boundingSphere?.radius || 0;
                    
                    // Only include larger objects (room geometry)
                    // Adjust this threshold based on your models
                    if (radius > 0.5) {
                      meshes.push(child);
                    }
                  }
                });
                
                return meshes;
              }, [scene, camera]);
              
              // Check collision at a given x, z position
              const checkCollision = React.useCallback((x, z) => {
                const meshes = getRoomMeshes();
                if (meshes.length === 0) {
                  return false; // No meshes loaded yet, allow movement
                }
                
                // Check collisions in multiple directions around the player
                const directions = [
                  new THREE.Vector3(0, 0, 1),   // Forward
                  new THREE.Vector3(0, 0, -1),  // Backward
                  new THREE.Vector3(1, 0, 0),  // Right
                  new THREE.Vector3(-1, 0, 0), // Left
                  new THREE.Vector3(0.707, 0, 0.707),   // Forward-right
                  new THREE.Vector3(-0.707, 0, 0.707),  // Forward-left
                  new THREE.Vector3(0.707, 0, -0.707),  // Backward-right
                  new THREE.Vector3(-0.707, 0, -0.707), // Backward-left
                ];
                
                // Check collisions at player height
                const checkHeight = collisionHeight;
                const checkPosition = new THREE.Vector3(x, checkHeight, z);
                
                for (const direction of directions) {
                  raycaster.set(checkPosition, direction);
                  raycaster.far = playerRadius;
                  
                  const intersects = raycaster.intersectObjects(meshes, false);
                  
                  if (intersects.length > 0) {
                    const distance = intersects[0].distance;
                    if (distance < playerRadius) {
                      return true; // Collision detected
                    }
                  }
                }
                
                // Also check vertical collision (ceiling/floor)
                raycaster.set(checkPosition, new THREE.Vector3(0, 1, 0));
                raycaster.far = 0.5;
                const verticalIntersects = raycaster.intersectObjects(meshes, false);
                if (verticalIntersects.length > 0 && verticalIntersects[0].distance < 0.5) {
                  return true; // Hitting ceiling
                }
                
                raycaster.set(checkPosition, new THREE.Vector3(0, -1, 0));
                raycaster.far = 1.0;
                const floorIntersects = raycaster.intersectObjects(meshes, false);
                if (floorIntersects.length > 0 && floorIntersects[0].distance < 0.5) {
                  // Floor collision is OK, but too close means we're inside the floor
                  if (floorIntersects[0].distance < 0.3) {
                    return true;
                  }
                }
                
                return false; // No collision
              }, [getRoomMeshes, raycaster]);
              
              // Store collision function globally so Player can access it
              React.useEffect(() => {
                window.checkCollision = checkCollision;
                
                return () => {
                  // Cleanup
                  if (window.checkCollision === checkCollision) {
                    delete window.checkCollision;
                  }
                };
              }, [checkCollision]);
              
              return null;
            };
            """
        ]

def create_gltf_collision():
    """Factory for GLTF collision detection."""
    return GLTFCollision.create()

