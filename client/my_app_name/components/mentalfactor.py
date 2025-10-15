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
    position: rx.Var[list] = [0, 0, 0]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const MentalSphere = ({ name, detail, color, position = [0, 0, 0], scale = 1.0, index = 0, allSpheres = [], containerRadius = 3.0 }) => {
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

                    // Update position from parent component
                    currentPosRef.current = [...position];
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

            export const Mind = ({ mentalSpheres = [], containerRadius = 3.0, containerOpacity = 0.2, position = [0, 0, 0] }) => {
                const [positions, setPositions] = useState([]);
                const [velocities, setVelocities] = useState([]);
                const sphereRefs = useRef([]);

                // Initialize random starting positions and velocities
                useEffect(() => {
                    if (mentalSpheres.length > 0 && positions.length === 0) {
                        const newPositions = mentalSpheres.map(() => {
                            const theta = Math.random() * Math.PI * 2;
                            const phi = Math.random() * Math.PI;
                            const r = Math.random() * containerRadius * 0.6; // Start closer to center
                            return [
                                r * Math.sin(phi) * Math.cos(theta),
                                r * Math.cos(phi),
                                r * Math.sin(phi) * Math.sin(theta)
                            ];
                        });
                        
                        const newVelocities = mentalSpheres.map(() => [
                            (Math.random() - 0.5) * 0.2,
                            (Math.random() - 0.5) * 0.2,
                            (Math.random() - 0.5) * 0.2
                        ]);
                        
                        setPositions(newPositions);
                        setVelocities(newVelocities);
                    }
                }, [mentalSpheres, containerRadius, positions.length]);

                // Collision detection and response
                useFrame(() => {
                    if (positions.length === 0 || velocities.length === 0) return;

                    const newPositions = [...positions];
                    const newVelocities = [...velocities];
                    const dt = 0.016; // frame time
                    const maxSpeed = 1.5;

                    // Update positions and handle container collisions
                    for (let i = 0; i < newPositions.length; i++) {
                        const pos = newPositions[i];
                        const vel = newVelocities[i];
                        const radius = mentalSpheres[i].scale || 0.8;
                        const maxRadius = containerRadius - radius;

                        // Add some random movement
                        if (Math.random() > 0.95) {
                            vel[0] += (Math.random() - 0.5) * 0.1;
                            vel[1] += (Math.random() - 0.5) * 0.1;
                            vel[2] += (Math.random() - 0.5) * 0.1;
                        }

                        // Clamp velocity
                        vel[0] = Math.max(-maxSpeed, Math.min(maxSpeed, vel[0]));
                        vel[1] = Math.max(-maxSpeed, Math.min(maxSpeed, vel[1]));
                        vel[2] = Math.max(-maxSpeed, Math.min(maxSpeed, vel[2]));

                        // Update position
                        pos[0] += vel[0] * dt;
                        pos[1] += vel[1] * dt;
                        pos[2] += vel[2] * dt;

                        // Container boundary collision
                        const dist = Math.sqrt(pos[0] * pos[0] + pos[1] * pos[1] + pos[2] * pos[2]);
                        if (dist > maxRadius) {
                            const nx = pos[0] / dist;
                            const ny = pos[1] / dist;
                            const nz = pos[2] / dist;

                            // Push back inside
                            pos[0] = nx * maxRadius;
                            pos[1] = ny * maxRadius;
                            pos[2] = nz * maxRadius;

                            // Reflect velocity
                            const dot = vel[0] * nx + vel[1] * ny + vel[2] * nz;
                            vel[0] -= 2 * dot * nx;
                            vel[1] -= 2 * dot * ny;
                            vel[2] -= 2 * dot * nz;

                            // Damping
                            vel[0] *= 0.8;
                            vel[1] *= 0.8;
                            vel[2] *= 0.8;
                        }
                    }

                    // Sphere-to-sphere collision detection and response
                    for (let i = 0; i < newPositions.length; i++) {
                        for (let j = i + 1; j < newPositions.length; j++) {
                            const pos1 = newPositions[i];
                            const pos2 = newPositions[j];
                            const vel1 = newVelocities[i];
                            const vel2 = newVelocities[j];
                            const radius1 = mentalSpheres[i].scale || 0.8;
                            const radius2 = mentalSpheres[j].scale || 0.8;

                            // Calculate distance between spheres
                            const dx = pos2[0] - pos1[0];
                            const dy = pos2[1] - pos1[1];
                            const dz = pos2[2] - pos1[2];
                            const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
                            const minDistance = radius1 + radius2;

                            // Collision detected
                            if (distance < minDistance && distance > 0) {
                                // Normalize collision vector
                                const nx = dx / distance;
                                const ny = dy / distance;
                                const nz = dz / distance;

                                // Separate spheres to prevent overlap
                                const overlap = minDistance - distance;
                                const separation = overlap * 0.5;
                                
                                pos1[0] -= nx * separation;
                                pos1[1] -= ny * separation;
                                pos1[2] -= nz * separation;
                                
                                pos2[0] += nx * separation;
                                pos2[1] += ny * separation;
                                pos2[2] += nz * separation;

                                // Calculate relative velocity
                                const rvx = vel2[0] - vel1[0];
                                const rvy = vel2[1] - vel1[1];
                                const rvz = vel2[2] - vel1[2];

                                // Relative velocity along collision normal
                                const velAlongNormal = rvx * nx + rvy * ny + rvz * nz;

                                // Don't resolve if velocities are separating
                                if (velAlongNormal > 0) continue;

                                // Calculate restitution (bounciness)
                                const restitution = 0.7;

                                // Calculate impulse scalar
                                const impulse = -(1 + restitution) * velAlongNormal;
                                const impulseScalar = impulse / 2; // Assuming equal mass

                                // Apply impulse
                                vel1[0] -= impulseScalar * nx;
                                vel1[1] -= impulseScalar * ny;
                                vel1[2] -= impulseScalar * nz;

                                vel2[0] += impulseScalar * nx;
                                vel2[1] += impulseScalar * ny;
                                vel2[2] += impulseScalar * nz;

                                // Add some damping to prevent infinite bouncing
                                vel1[0] *= 0.9;
                                vel1[1] *= 0.9;
                                vel1[2] *= 0.9;
                                
                                vel2[0] *= 0.9;
                                vel2[1] *= 0.9;
                                vel2[2] *= 0.9;
                            }
                        }
                    }

                    setPositions(newPositions);
                    setVelocities(newVelocities);
                });

                return (
                    <group position={position}>
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
                                ref={el => sphereRefs.current[idx] = el}
                                name={sphere.name}
                                detail={sphere.detail}
                                color={sphere.color}
                                position={positions[idx] || [0, 0, 0]}
                                scale={sphere.scale || 0.8}
                                index={idx}
                                allSpheres={mentalSpheres}
                                containerRadius={containerRadius}
                            />
                        ))}
                    </group>
                );
            };
            """
        ]