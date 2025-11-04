import reflex as rx
from typing import List

class StaticImage(rx.Component):
    """Static image component without any interaction."""
    tag = "StaticImageComponent"

    image_url: rx.Var[str] = ""
    position: rx.Var[List[float]] = [0, 0, 0]
    scale: rx.Var[float] = 1.0

    def add_custom_code(self) -> List[str]:
        return [
            """
            export const StaticImageComponent = ({ imageUrl, position=[0,0,0], scale=1 }) => {
                const [texture, setTexture] = React.useState(null);
                
                // Load image texture
                React.useEffect(() => {
                    if (!imageUrl) return;
                    
                    const loader = new THREE.TextureLoader();
                    loader.load(
                        imageUrl,
                        (tex) => {
                            tex.needsUpdate = true;
                            tex.flipY = false;
                            tex.format = THREE.RGBAFormat;
                            tex.colorSpace = THREE.SRGBColorSpace;
                            if (tex.format === THREE.RGBAFormat) {
                                tex.premultiplyAlpha = false;
                            }
                            setTexture(tex);
                        },
                        undefined,
                        (err) => console.error("Error loading image:", err)
                    );
                }, [imageUrl]);

                // Calculate aspect ratio for 1280x963
                const targetWidth = 1280;
                const targetHeight = 963;
                const aspectRatio = targetWidth / targetHeight;
                const planeHeight = 2;
                const planeWidth = aspectRatio * planeHeight;

                if (!texture) {
                    return (
                        <mesh position={position}>
                            <planeGeometry args={[planeWidth, planeHeight]} />
                            <meshStandardMaterial color="gray" />
                        </mesh>
                    );
                }

                return (
                    <mesh position={position} scale={scale}>
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

