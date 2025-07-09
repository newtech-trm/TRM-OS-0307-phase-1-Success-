import asyncio
import traceback
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_types import WINCategory

async def test_quantum():
    try:
        learning_system = AdaptiveLearningSystem(agent_id='test')
        quantum_manager = QuantumSystemManager(learning_system=learning_system)
        
        print("Initializing quantum manager...")
        await quantum_manager.initialize()
        
        print(f"Quantum systems: {list(quantum_manager.quantum_systems.keys())}")
        
        if quantum_manager.quantum_systems:
            system_id = list(quantum_manager.quantum_systems.keys())[0]
            print(f"Testing system: {system_id}")
            
            # Check current state detection
            current_state = await quantum_manager.detect_current_quantum_state(system_id)
            print(f"Current state: {current_state}")
            
            # Check quantum states in system
            quantum_system = quantum_manager.quantum_systems[system_id]
            print(f"Quantum states in system: {list(quantum_system.quantum_states.keys())}")
            
            win_probability = await quantum_manager.calculate_win_probability(
                system_id=system_id,
                win_category=WINCategory.COMPOSITE,
                context={"test": True}
            )
            
            print(f"Win probability: {win_probability}")
            if win_probability:
                print(f"Win probability type: {type(win_probability)}")
                print(f"Base probability: {win_probability.base_probability}")
        else:
            print("No quantum systems found")
            
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_quantum()) 