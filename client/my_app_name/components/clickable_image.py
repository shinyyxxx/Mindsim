import reflex as rx
from typing import List

class ClickableImage(rx.Component):
    """Image component that rotates 20 degrees on click, toggles back on second click."""
    tag = "ClickableImageComponent"

    image_url: rx.Var[str] = ""
    position: rx.Var[List[float]] = [0, 0, 0]
    scale: rx.Var[float] = 50
    initial_rotation: rx.Var[List[float]] = [0, 0, 0]

    def add_custom_code(self) -> List[str]:
        return [
            """
            export const ClickableImageComponent = ({ imageUrl, position=[0,0,0], scale=1, initialRotation=[0,0,0] }) => {
                const meshRef = React.useRef();
                const [texture, setTexture] = React.useState(null);
                const [isRotated, setIsRotated] = React.useState(false);
                const [aspectRatio, setAspectRatio] = React.useState(1);
                const { gl } = useThree();
                
                // Load image texture
                React.useEffect(() => {
                    if (!imageUrl) return;
                    
                    const loader = new THREE.TextureLoader();
                    loader.load(
                        imageUrl,
                        (tex) => {
                            tex.needsUpdate = true;
                            tex.flipY = false; // Don't flip Y - we'll handle orientation with plane rotation
                            tex.format = THREE.RGBAFormat;
                            tex.colorSpace = THREE.SRGBColorSpace;
                            // Ensure proper transparency handling
                            if (tex.format === THREE.RGBAFormat) {
                                tex.premultiplyAlpha = false;
                            }
                            
                            // Calculate aspect ratio from actual texture dimensions
                            if (tex.image) {
                                const imgWidth = tex.image.width || tex.image.videoWidth || 1;
                                const imgHeight = tex.image.height || tex.image.videoHeight || 1;
                                setAspectRatio(imgWidth / imgHeight);
                            } else {
                                // Fallback: wait for image to load
                                const img = new Image();
                                img.onload = () => {
                                    setAspectRatio(img.width / img.height);
                                };
                                img.src = imageUrl;
                            }
                            
                            setTexture(tex);
                        },
                        undefined,
                        (err) => console.error("Error loading image:", err)
                    );
                }, [imageUrl]);

                // Smooth rotation animation
                useFrame(() => {
                    if (!meshRef.current) return;
                    
                    // Toggle between [0,0,0] and [0,0,-0.5]
                    const targetRotation = isRotated ? [0, 0, -0.5] : [0, 0, 0];
                    const currentRotation = meshRef.current.rotation;
                    
                    // Smooth interpolation for all axes
                    const lerpFactor = 0.1;
                    currentRotation.x += (targetRotation[0] - currentRotation.x) * lerpFactor;
                    currentRotation.y += (targetRotation[1] - currentRotation.y) * lerpFactor;
                    currentRotation.z += (targetRotation[2] - currentRotation.z) * lerpFactor;
                    
                    // Snap to target if close enough
                    if (Math.abs(targetRotation[2] - currentRotation.z) < 0.001) {
                        meshRef.current.rotation.set(...targetRotation);
                    }
                });

                const handleClick = (event) => {
                    event.stopPropagation();
                    setIsRotated(!isRotated);
                };

                // Calculate plane dimensions based on actual texture aspect ratio
                const planeHeight = 2; // Base height for the plane
                const planeWidth = aspectRatio * planeHeight;

                if (!texture) {
                    return (
                        <mesh position={position} ref={meshRef}>
                            <planeGeometry args={[planeWidth, planeHeight]} />
                            <meshStandardMaterial color="gray" />
                        </mesh>
                    );
                }

                return (
                    <mesh
                        ref={meshRef}
                        position={position}
                        scale={scale}
                        rotation={[0, 0, 0]}
                        onClick={handleClick}
                        onPointerEnter={() => gl.domElement.style.cursor = 'pointer'}
                        onPointerLeave={() => gl.domElement.style.cursor = 'default'}
                    >
                        <group rotation={[Math.PI, 0, 0]}>
                            <mesh>
                                <planeGeometry args={[planeWidth, planeHeight]} />
                                <meshBasicMaterial 
                                    map={texture} 
                                    side={THREE.DoubleSide}
                                    toneMapped={false}
                                    transparent={true}
                                    alphaTest={0.01}
                                />
                            </mesh>
                        </group>
                    </mesh>
                );
            };
            """
        ]

