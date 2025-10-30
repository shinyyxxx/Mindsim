# crosshair.py
import reflex as rx

class Crosshair(rx.Component):
    """A crosshair UI component for first-person view."""

    tag = "Crosshair"

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const Crosshair = () => {
              const [isPointerLocked, setIsPointerLocked] = useState(false);
              const [isHoveringObject, setIsHoveringObject] = useState(false);

              useEffect(() => {
                const handlePointerLockChange = () => {
                  const locked = document.pointerLockElement === document.body;
                  setIsPointerLocked(locked);
                };

                const handleMouseMove = (event) => {
                  if (!isPointerLocked) {
                    // Check if mouse is over an interactive object
                    const elements = document.elementsFromPoint(event.clientX, event.clientY);
                    const hasInteractiveElement = elements.some(el => 
                      el.style.cursor === 'grab' || el.style.cursor === 'grabbing'
                    );
                    setIsHoveringObject(hasInteractiveElement);
                  }
                };

                document.addEventListener('pointerlockchange', handlePointerLockChange);
                document.addEventListener('mousemove', handleMouseMove);

                return () => {
                  document.removeEventListener('pointerlockchange', handlePointerLockChange);
                  document.removeEventListener('mousemove', handleMouseMove);
                };
              }, [isPointerLocked]);

              return (
                <div style={{
                  position: 'fixed',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  pointerEvents: 'none',
                  zIndex: 1000
                }}>
                  {/* Crosshair */}
                  <div style={{
                    width: '20px',
                    height: '20px',
                    position: 'relative'
                  }}>
                    {/* Horizontal line */}
                    <div style={{
                      position: 'absolute',
                      top: '50%',
                      left: '0',
                      width: '100%',
                      height: '2px',
                      backgroundColor: isHoveringObject ? 'rgba(255, 255, 0, 0.9)' : 'rgba(255, 255, 255, 0.8)',
                      transform: 'translateY(-50%)',
                      boxShadow: '0 0 3px rgba(0, 0, 0, 0.5)'
                    }} />
                    {/* Vertical line */}
                    <div style={{
                      position: 'absolute',
                      left: '50%',
                      top: '0',
                      width: '2px',
                      height: '100%',
                      backgroundColor: isHoveringObject ? 'rgba(255, 255, 0, 0.9)' : 'rgba(255, 255, 255, 0.8)',
                      transform: 'translateX(-50%)',
                      boxShadow: '0 0 3px rgba(0, 0, 0, 0.5)'
                    }} />
                    {/* Center dot */}
                    <div style={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      width: '4px',
                      height: '4px',
                      backgroundColor: isHoveringObject ? 'rgba(255, 255, 0, 1)' : 'rgba(255, 255, 255, 0.9)',
                      borderRadius: '50%',
                      transform: 'translate(-50%, -50%)',
                      boxShadow: '0 0 2px rgba(0, 0, 0, 0.7)'
                    }} />
                  </div>
                  
                  {/* Instruction text */}
                  {!isPointerLocked && (
                    <div style={{
                      marginTop: '40px',
                      textAlign: 'center',
                      color: 'rgba(255, 255, 255, 0.8)',
                      fontSize: '14px',
                      textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)',
                      fontFamily: 'Arial, sans-serif'
                    }}>
                      Click to start
                    </div>
                  )}
                </div>
              );
            };
            """
        ]


def create_crosshair() -> Crosshair:
    return Crosshair.create()
