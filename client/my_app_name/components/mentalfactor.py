import reflex as rx
from typing import List, Optional

def _mental_sphere_js() -> str:
    return (
        """
        // Define MentalSphere once and register globally
        if (!globalThis.MentalSphere) {
            const MentalSphere = ({ name, detail, color, position = [0, 0, 0], scale = 1.0, index = 0, allSpheres = [], containerRadius = 3.0, onSelect }) => {
                const groupRef = useRef();
                const [hovered, setHovered] = useState(false);
                const { camera } = useThree();
                const initialPos = useRef(position);
                const velocityRef = useRef([
                    (Math.random() - 0.5) * 0.15,
                    (Math.random() - 0.5) * 0.15,
                    (Math.random() - 0.5) * 0.15
                ]);
                const currentPosRef = useRef([...position]);

                // Build a billboarded label texture for the sphere name
                const labelTex = useMemo(() => {
                    const label = name || '';
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    if (!ctx) return null;

                    const fontSize = 160;
                    const padding = 28;
                    ctx.font = `bold ${fontSize}px Arial`;
                    const metrics = ctx.measureText(label);
                    const textWidth = Math.ceil(metrics.width);

                    // High-DPI canvas for crisper texture
                    const dpi = 2;
                    canvas.width = (textWidth + padding * 2) * dpi;
                    canvas.height = (fontSize + padding * 2) * dpi;
                    ctx.scale(dpi, dpi);

                    // Background rounded rect with semi-transparency
                    const drawRoundedRect = (x, y, w, h, r) => {
                        ctx.beginPath();
                        ctx.moveTo(x + r, y);
                        ctx.arcTo(x + w, y, x + w, y + h, r);
                        ctx.arcTo(x + w, y + h, x, y + h, r);
                        ctx.arcTo(x, y + h, x, y, r);
                        ctx.arcTo(x, y, x + w, y, r);
                        ctx.closePath();
                    };
                    ctx.fillStyle = 'rgba(0,0,0,0.6)';
                    drawRoundedRect(0, 0, textWidth + padding * 2, fontSize + padding * 2, 12);
                    ctx.fill();

                    // Text
                    ctx.fillStyle = '#ffffff';
                    ctx.textBaseline = 'top';
                    ctx.textAlign = 'left';
                    ctx.font = `bold ${fontSize}px Arial`;
                    ctx.fillText(label, padding, padding);

                    const tex = new THREE.CanvasTexture(canvas);
                    tex.needsUpdate = true;
                    tex.minFilter = THREE.LinearFilter;
                    return { tex, widthUnits: (textWidth + padding * 2) / fontSize };
                }, [name]);

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
                });

                return (
                    <group ref={groupRef} position={position}>
                        {labelTex && (
                            <sprite position={[0, scale + 0.02, 0]} scale={[Math.max(0.15, labelTex.widthUnits * 0.15), 0.25, 0.25]} renderOrder={1000}>
                                <spriteMaterial attach="material" map={labelTex.tex} transparent depthTest={false} depthWrite={false} />
                            </sprite>
                        )}
                        <mesh
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
                    </group>
                );
            };
            globalThis.MentalSphere = MentalSphere;
        }
        """
    )

class MentalSphere(rx.Component):
    """Single floating sphere inside the mind container."""
    tag = "MentalSphere"

    name: str
    detail: str
    color: str  # hex color
    position: List[float]  # [x, y, z]
    scale: float

    def add_custom_code(self) -> list[str]:
        return [
            _mental_sphere_js()
        ]


class Mind(rx.Component):
    """Container sphere with floating MentalSpheres inside."""
    tag = "Mind"

    mental_spheres: rx.Var[list]
    mind_id: rx.Var[str] = ""
    container_radius: rx.Var[float] = 3.0
    container_opacity: rx.Var[float] = 1
    position: rx.Var[list] = [0, 0, 0]
    glass_texture: rx.Var[str] = ""
    glass_tint: rx.Var[str] = "#ffffff"
    glass_transmission: rx.Var[float] = 0.9
    glass_thickness: rx.Var[float] = 0.4
    glass_roughness: rx.Var[float] = 0.05

    def add_custom_code(self) -> list[str]:
        return [
            _mental_sphere_js(),
            """
            export const Mind = ({
                mentalSpheres = [],
                containerRadius = 3.0,
                containerOpacity = 0.2,
                position = [0, 0, 0],
                glassTexture = '',
                glassTint = '#ffffff',
                glassTransmission = 0.9,
                glassThickness = 0.4,
                glassRoughness = 0.05,
            }) => {
                const [positions, setPositions] = useState([]);
                const [velocities, setVelocities] = useState([]);
                const [selected, setSelected] = useState(null);
                const [centerPopupTex, setCenterPopupTex] = useState(null);
                const overlayRef = useRef();
                const MentalSphereComp = globalThis.MentalSphere;

                // Optional glass texture
                const glassMap = useMemo(() => {
                    if (!glassTexture) return null;
                    try {
                        const loader = new THREE.TextureLoader();
                        const tex = loader.load(glassTexture);
                        return tex;
                    } catch (e) {
                        console.warn('Failed to load glass texture', glassTexture, e);
                        return null;
                    }
                }, [glassTexture]);

                // Initialize random starting positions and velocities
                useEffect(() => {
                    if (mentalSpheres.length > positions.length) {
                        // Add positions for newly added spheres
                        const newPositions = [...positions];
                        const newVelocities = [...velocities];
                        
                        for (let i = positions.length; i < mentalSpheres.length; i++) {
                            const theta = Math.random() * Math.PI * 2;
                            const phi = Math.random() * Math.PI;
                            const r = Math.random() * containerRadius * 0.6; // Start closer to center
                            newPositions.push([
                                r * Math.sin(phi) * Math.cos(theta),
                                r * Math.cos(phi),
                                r * Math.sin(phi) * Math.sin(theta)
                            ]);
                            
                            newVelocities.push([
                                (Math.random() - 0.5) * 0.08,
                                (Math.random() - 0.5) * 0.08,
                                (Math.random() - 0.5) * 0.08
                            ]);
                        }
                        
                        setPositions(newPositions);
                        setVelocities(newVelocities);
                    }
                }, [mentalSpheres, containerRadius, positions.length]);

                // Build label texture for center popup when selected changes
                useEffect(() => {
                    if (!selected) { setCenterPopupTex(null); return; }
                    const canvas = document.createElement('canvas');
                    canvas.width = 1024; // bigger for crispness
                    canvas.height = 512;
                    const ctx = canvas.getContext('2d');
                    if (!ctx) return;
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 8;
                    ctx.strokeRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = '#111111';
                    ctx.font = 'bold 64px Arial';
                    ctx.textAlign = 'left';
                    ctx.textBaseline = 'top';
                    ctx.fillText(selected.name || 'Detail', 36, 36);
                    const maxWidth = canvas.width - 72;
                    const lineHeight = 44;
                    let y = 130;
                    ctx.font = '32px Arial';
                    const words = (selected.detail || '').split(/\s+/);
                    let line = '';
                    for (let i = 0; i < words.length; i++) {
                        const testLine = line + words[i] + ' ';
                        const metrics = ctx.measureText(testLine);
                        if (metrics.width > maxWidth && i > 0) {
                            ctx.fillText(line, 36, y);
                            line = words[i] + ' ';
                            y += lineHeight;
                        } else {
                            line = testLine;
                        }
                        if (y > canvas.height - 56) break;
                    }
                    if (y <= canvas.height - 56) ctx.fillText(line, 36, y);
                    const tex = new THREE.CanvasTexture(canvas);
                    tex.needsUpdate = true;
                    setCenterPopupTex(tex);
                }, [selected]);

                // Collision detection and response
                useFrame(() => {
                    if (positions.length === 0 || velocities.length === 0) return;

                    const newPositions = [...positions];
                    const newVelocities = [...velocities];
                    const dt = 0.016; // frame time
                    const maxSpeed = 0.6;

                    // Update positions and handle container collisions
                    for (let i = 0; i < newPositions.length; i++) {
                        const pos = newPositions[i];
                        const vel = newVelocities[i];
                        const radius = mentalSpheres[i].scale || 0.8;
                        const maxRadius = containerRadius - radius;

                        // Add some random movement
                        if (Math.random() > 0.95) {
                            vel[0] += (Math.random() - 0.5) * 0.04;
                            vel[1] += (Math.random() - 0.5) * 0.04;
                            vel[2] += (Math.random() - 0.5) * 0.04;
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

                // Keep overlay in front of camera and centered (positioned in world space, independent of Mind position)
                useFrame(({ camera }) => {
                    if (!overlayRef.current) return;
                    const dir = new THREE.Vector3();
                    camera.getWorldDirection(dir);
                    const forward = dir.multiplyScalar(4.0); // distance in front of camera
                    const down = camera.up.clone().multiplyScalar(-0.8); // slightly lower on screen
                    overlayRef.current.position.copy(camera.position.clone().add(forward).add(down));
                    // Match camera rotation to keep perfectly facing screen
                    overlayRef.current.quaternion.copy(camera.quaternion);
                });

                return (
                    <>
                        {/* Mind container and spheres - positioned group */}
                        <group position={position}>
                            <mesh renderOrder={998} castShadow={false} receiveShadow={false}>
                                <sphereGeometry args={[containerRadius, 64, 64]} />
                                <meshPhysicalMaterial
                                    color={glassTint}
                                    transparent
                                    opacity={containerOpacity}
                                    transmission={glassTransmission}
                                    thickness={glassThickness}
                                    roughness={glassRoughness}
                                    metalness={0.0}
                                    map={glassMap || undefined}
                                    side={THREE.BackSide}
                                    depthWrite={false}
                                    depthTest={false}
                                />
                            </mesh>

                            {/* Floating mental spheres */}
                            {mentalSpheres.map((sphere, idx) => (
                                <MentalSphereComp
                                    key={idx}
                                    name={sphere.name}
                                    detail={sphere.detail}
                                    color={sphere.color}
                                    position={positions[idx] || [0, 0, 0]}
                                    scale={sphere.scale || 0.8}
                                    index={idx}
                                    allSpheres={mentalSpheres}
                                    containerRadius={containerRadius}
                                    onSelect={(s) => setSelected(s)}
                                />
                            ))}
                        </group>

                        {/* Centered screen overlay popup - outside positioned group so it's independent of Mind position */}
                        {selected && (
                            <group ref={overlayRef} renderOrder={999}>
                                {/* Flat card as a plane for perfect border alignment */}
                                <sprite onClick={(e) => e.stopPropagation()}>
                                    <planeGeometry args={[6, 3.5]} />
                                    <spriteMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={0.5} depthTest={false} depthWrite={false} />
                                </sprite>
                                <lineSegments>
                                    <edgesGeometry args={[new THREE.PlaneGeometry(6, 3.5)]} />
                                    <lineBasicMaterial color="#000000" linewidth={2} depthTest={false} depthWrite={false} />
                                </lineSegments>
                                {centerPopupTex && (
                                    <sprite position={[0, 0, 0.01]} scale={[5.4, 3.0, 1]} renderOrder={1000}>
                                        <spriteMaterial attach="material" map={centerPopupTex} transparent depthTest={false} depthWrite={false} />
                                    </sprite>
                                )}
                                {/* Close button */}
                                <mesh position={[2.6, 1.4, 0.05]} renderOrder={1001} onClick={(e) => { e.stopPropagation(); setSelected(null); }}>
                                    <boxGeometry args={[0.4, 0.4, 0.02]} />
                                    <meshStandardMaterial color="#ff6666" emissive="#ff6666" emissiveIntensity={0.4} depthTest={false} depthWrite={false} transparent opacity={1} />
                                </mesh>
                            </group>
                        )}
                    </>
                );
            };
            """
        ]