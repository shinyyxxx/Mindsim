import reflex as rx
from typing import List, Optional

class MentalFactor(rx.Component):    
    name: str
    detail: str
    color: str  # hex color
    position: List[float]  # [x, y, z]
    scale: float

class MentalSphere(MentalFactor):
    """Visual representation of a MentalFactor as a 3D sphere with popup on click."""
    tag = "MentalSphere"
    
    # Add event handler for popup
    on_click: rx.EventHandler[lambda: []]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const MentalSphere = ({ name, detail, color, position = [0, 0, 0], scale = 1.0, onClick }) => {
                const meshRef = useRef();
                const boxRef = useRef();
                const [hovered, setHovered] = useState(false);
                const [showPopup, setShowPopup] = useState(false);
                const { camera } = useThree();

                useFrame(() => {

                    // Update popup to face camera
                    if (boxRef.current) {
                        boxRef.current.lookAt(camera.position);
                    }
                });

                const handleClick = () => {
                    setShowPopup(true);
                    if (onClick) {
                        onClick({ name, detail, color, position });
                    }
                };

                const closePopup = () => {
                    setShowPopup(false);
                };

                return (
                    <group>
                        {/* Sphere */}
                        <group position={position}>
                            <mesh
                                ref={meshRef}
                                onClick={handleClick}
                                onPointerEnter={() => setHovered(true)}
                                onPointerLeave={() => setHovered(false)}
                            >
                                <sphereGeometry args={[1, 32, 32]} />
                                <meshStandardMaterial
                                    color={color}
                                    emissive={hovered ? color : '#000000'}
                                    emissiveIntensity={hovered ? 0.3 : 0}
                                    roughness={0.4}
                                    metalness={0.6}
                                />
                            </mesh>
                        </group>

                        {/* Popup 3D Box - Centered */}
                        {showPopup && (
                            <group position={[0, 0, 0]} ref={boxRef}>
                                {/* White Box */}
                                <mesh position={[0, 0, 0]} onClick={closePopup}>
                                    <boxGeometry args={[6, 4, 3]} />
                                    <meshStandardMaterial
                                        color="#ffffff"
                                        emissive="#ffffff"
                                        emissiveIntensity={0.8}
                                        metalness={0.3}
                                        roughness={0.7}
                                    />
                                </mesh>

                                {/* Black Border */}
                                <lineSegments position={[0, 0, 0]}>
                                    <edgesGeometry args={[new THREE.BoxGeometry(6, 4, 3)]} />
                                    <lineBasicMaterial color="#000000" linewidth={2} />
                                </lineSegments>
                            </group>
                        )}
                    </group>
                );
            };
            """
        ]

class Mind(rx.Component):
    """Container sphere with floating MentalSpheres inside."""
    tag = "Mind"

    mental_spheres: rx.Var[list]
    container_radius: rx.Var[float] = 3.0
    container_opacity: rx.Var[float] = 1

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const MentalSphere = ({ name, detail, color, position = [0, 0, 0], scale = 1.0, index = 0 }) => {
                const groupRef = useRef();
                const [hovered, setHovered] = useState(false);
                const [showPopup, setShowPopup] = useState(false);
                const { camera } = useThree();
                const initialPos = useRef(position);
                const velocityRef = useRef([
                    (Math.random() - 0.5) * 0.15,
                    (Math.random() - 0.5) * 0.15,
                    (Math.random() - 0.5) * 0.15
                ]);
                const currentPosRef = useRef([...position]);

                // Update initial position when prop changes
                useEffect(() => {
                    initialPos.current = position;
                    currentPosRef.current = [...position];
                }, [position]);

                useFrame(() => {
                    if (!groupRef.current) return;

                    const vel = velocityRef.current;
                    const radius = scale;              // sphere's own radius
                    const maxRadius = 3 - radius;     // stay inside container

                    // Random wandering
                    if (Math.random() > 0.95) {
                        vel[0] += (Math.random() - 0.5) * 0.1;
                        vel[1] += (Math.random() - 0.5) * 0.1;
                        vel[2] += (Math.random() - 0.5) * 0.1;
                    }

                    // Clamp velocity
                    const maxSpeed = 1;
                    vel[0] = Math.max(-maxSpeed, Math.min(maxSpeed, vel[0]));
                    vel[1] = Math.max(-maxSpeed, Math.min(maxSpeed, vel[1]));
                    vel[2] = Math.max(-maxSpeed, Math.min(maxSpeed, vel[2]));

                    // Update position
                    currentPosRef.current[0] += vel[0] * 0.016;
                    currentPosRef.current[1] += vel[1] * 0.016;
                    currentPosRef.current[2] += vel[2] * 0.016;

                    // Calculate distance from center
                    const x = currentPosRef.current[0];
                    const y = currentPosRef.current[1];
                    const z = currentPosRef.current[2];
                    const dist = Math.sqrt(x * x + y * y + z * z);

                    // Bounce off the container wall
                    if (dist > maxRadius) {
                        const nx = x / dist;
                        const ny = y / dist;
                        const nz = z / dist;

                        // Push back inside
                        currentPosRef.current[0] = nx * maxRadius;
                        currentPosRef.current[1] = ny * maxRadius;
                        currentPosRef.current[2] = nz * maxRadius;

                        // Reflect velocity along normal
                        const dot = vel[0]*nx + vel[1]*ny + vel[2]*nz;
                        vel[0] -= 2 * dot * nx;
                        vel[1] -= 2 * dot * ny;
                        vel[2] -= 2 * dot * nz;

                        // Damping to prevent infinite jitter
                        vel[0] *= 0.8;
                        vel[1] *= 0.8;
                        vel[2] *= 0.8;
                    }

                    // Optional soft boundary: slow down near edge
                    if (dist > maxRadius * 0.95 && dist <= maxRadius) {
                        const nx = x / dist;
                        const ny = y / dist;
                        const nz = z / dist;
                        vel[0] -= nx * 0.02;
                        vel[1] -= ny * 0.02;
                        vel[2] -= nz * 0.02;
                    }

                    // Apply position
                    groupRef.current.position.set(...currentPosRef.current);

                    // Popup always faces camera
                    if (showPopup && groupRef.current.children[0]) {
                        groupRef.current.children[0].lookAt(camera.position);
                    }
                });

                const handleClick = () => setShowPopup(false);

                return (
                    <group ref={groupRef} position={position}>
                        {/* Main sphere */}
                        <mesh
                            onClick={handleClick}
                            onPointerEnter={() => setHovered(true)}
                            onPointerLeave={() => setHovered(false)}
                            castShadow
                        >
                            <sphereGeometry args={[scale, 32, 32]} />
                            <meshStandardMaterial
                                color={color}
                                emissive={hovered ? color : '#000000'}
                                emissiveIntensity={hovered ? 0.3 : 0}
                                roughness={0.4}
                                metalness={0.6}
                            />
                        </mesh>

                        {/* Popup box */}
                        {showPopup && (
                            <group position={[0, scale + 2, 0]}>
                                <mesh onClick={(e) => e.stopPropagation()}>
                                    <boxGeometry args={[4, 2.5, 0.2]} />
                                    <meshStandardMaterial
                                        color="#ffffff"
                                        emissive="#ffffff"
                                        emissiveIntensity={0.6}
                                        metalness={0.3}
                                        roughness={0.7}
                                    />
                                </mesh>
                                <lineSegments>
                                    <edgesGeometry args={[new THREE.BoxGeometry(4, 2.5, 0.2)]} />
                                    <lineBasicMaterial color="#000000" linewidth={2} />
                                </lineSegments>
                            </group>
                        )}
                    </group>
                );
            };

            export const Mind = ({ mentalSpheres = [], containerRadius = 3.0, containerOpacity = 0.2 }) => {
                const [positions, setPositions] = useState([]);

                // Initialize random starting positions
                useEffect(() => {
                    if (mentalSpheres.length > 0 && positions.length === 0) {
                        const newPositions = mentalSpheres.map(() => {
                            const theta = Math.random() * Math.PI * 2;
                            const phi = Math.random() * Math.PI;
                            const r = Math.random() * containerRadius * 0.7;
                            return [
                                r * Math.sin(phi) * Math.cos(theta),
                                r * Math.cos(phi),
                                r * Math.sin(phi) * Math.sin(theta)
                            ];
                        });
                        setPositions(newPositions);
                    }
                }, [mentalSpheres, containerRadius, positions.length]);

                return (
                    <>
                        {/* Container sphere */}
                        <mesh>
                            <sphereGeometry args={[containerRadius, 64, 64]} />
                            <meshStandardMaterial
                                color="#4d4dff"
                                transparent
                                opacity={containerOpacity}
                                wireframe={false}
                                emissive="#2d2d7f"
                                emissiveIntensity={0.2}
                                metalness={0.1}
                                roughness={0.7}
                            />
                        </mesh>

                        {/* Container wireframe */}
                        <lineSegments>
                            <edgesGeometry args={[new THREE.SphereGeometry(containerRadius, 64, 64)]} />
                            <lineBasicMaterial color="#6666ff" linewidth={1} />
                        </lineSegments>

                        {/* Floating mental spheres */}
                        {mentalSpheres.map((sphere, idx) => (
                            <MentalSphere
                                key={idx}
                                name={sphere.name}
                                detail={sphere.detail}
                                color={sphere.color}
                                position={positions[idx] || [0, 0, 0]}
                                scale={sphere.scale || 0.8}
                                index={idx}
                                containerRadius={containerRadius}
                            />
                        ))}
                    </>
                );
            };
            """
        ]
