"""
TRM-OS Quantum WIN States - Core Types
Định nghĩa các types cho quantum state management với ML
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
import numpy as np


class QuantumStateType(Enum):
    """Types of quantum states trong TRM-OS"""
    SUPERPOSITION = "superposition"      # Multiple potential outcomes
    ENTANGLEMENT = "entanglement"        # Interconnected states
    COHERENCE = "coherence"              # Aligned organizational state
    DECOHERENCE = "decoherence"          # Loss of quantum properties
    MEASUREMENT = "measurement"          # Collapsed to classical state
    TUNNELING = "tunneling"              # Breakthrough potential
    INTERFERENCE = "interference"        # Wave function interference
    WIN = "win"                          # WIN state


class WINCategory(Enum):
    """Categories of WINs for quantum analysis"""
    WISDOM = "wisdom"
    INTELLIGENCE = "intelligence"
    NETWORKING = "networking"
    COMPOSITE = "composite"
    BUSINESS_VALUE = "business_value"
    INNOVATION = "innovation"
    EFFICIENCY = "efficiency"
    COLLABORATION = "collaboration"
    LEARNING = "learning"
    TRANSFORMATION = "transformation"
    EMERGENCE = "emergence"


class ProbabilityDistribution(BaseModel):
    """Probability distribution for quantum states"""
    model_config = {"arbitrary_types_allowed": True}
    
    states: Dict[str, float] = {}        # State -> Probability mapping
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    entropy: float = 0.0                 # Information entropy
    coherence_factor: float = Field(ge=0.0, le=1.0, default=0.5)
    
    def normalize(self) -> None:
        """Normalize probabilities to sum to 1"""
        total = sum(self.states.values())
        if total > 0:
            self.states = {k: v/total for k, v in self.states.items()}
    
    def calculate_entropy(self) -> float:
        """Calculate Shannon entropy"""
        entropy = 0.0
        for prob in self.states.values():
            if prob > 0:
                entropy -= prob * np.log2(prob)
        self.entropy = entropy
        return entropy


@dataclass
class QuantumState:
    """Represents a quantum state trong organizational context"""
    state_id: str
    state_type: QuantumStateType
    
    # Quantum properties
    amplitude: complex                    # Quantum amplitude
    phase: float                         # Quantum phase
    probability: float                   # |amplitude|^2
    
    # Organizational context
    description: str = ""
    organizational_level: str = "team"   # "individual", "team", "department", "organization"
    stakeholders: List[str] = field(default_factory=list)  # Affected stakeholders
    win_category: Optional[WINCategory] = None  # Associated WIN category
    
    # Temporal properties
    coherence_time: float = 0.0         # How long state remains coherent
    decoherence_rate: float = 0.0       # Rate of decoherence
    created_at: datetime = field(default_factory=datetime.now)
    
    # Measurement properties
    measured: bool = False               # Has state been measured/collapsed?
    measurement_result: Optional[Any] = None
    measurement_time: Optional[datetime] = None
    
    # Entanglement
    entangled_states: List[str] = field(default_factory=list)  # IDs of entangled states
    entanglement_strength: float = 0.0   # Strength of entanglement
    
    def __post_init__(self):
        # Calculate probability from amplitude
        if isinstance(self.amplitude, complex):
            self.probability = abs(self.amplitude) ** 2
    
    def collapse_to_classical(self, measurement_result: Any) -> None:
        """Collapse quantum state to classical state"""
        self.measured = True
        self.measurement_result = measurement_result
        self.measurement_time = datetime.now()
        self.amplitude = complex(1.0, 0.0) if measurement_result else complex(0.0, 0.0)
        self.probability = 1.0 if measurement_result else 0.0
    
    def calculate_decoherence(self, time_elapsed: float) -> float:
        """Calculate current coherence based on decoherence rate"""
        if self.decoherence_rate == 0:
            return 1.0
        return np.exp(-self.decoherence_rate * time_elapsed)


@dataclass
class WINProbability:
    """Probability analysis for potential WIN outcomes"""
    probability_id: str
    win_category: WINCategory
    
    # Probability calculations
    base_probability: float              # Classical probability
    confidence_level: float = 0.7       # Confidence in calculation
    
    # Supporting factors
    contributing_factors: Dict[str, float] = field(default_factory=dict)
    
    # Context và calculation details
    calculation_context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calculate_net_probability(self) -> float:
        """Calculate net probability considering all factors"""
        net_prob = self.base_probability
        
        # Apply confidence factor
        net_prob *= self.confidence_level
        
        # Ensure probability bounds
        return max(0.0, min(1.0, net_prob))


@dataclass
class StateTransition:
    """Represents transition between quantum states"""
    transition_id: str
    from_state: str                      # Source state ID
    to_state: str                        # Target state ID
    
    # Transition properties
    transition_probability: float        # Probability of transition
    transition_amplitude: complex = complex(1.0, 0.0)  # Quantum transition amplitude
    transition_time: float = 1.0        # Expected transition time
    
    # Triggers and conditions
    trigger_conditions: Dict[str, Any] = field(default_factory=dict)
    required_energy: float = 0.0        # Energy required for transition
    catalyst_factors: List[str] = field(default_factory=list)  # Factors that accelerate transition
    
    # Measurement effects
    measurement_induced: bool = False    # Is transition caused by measurement?
    decoherence_effect: float = 0.0     # How much decoherence this causes
    
    # Organizational impact
    stakeholder_impact: Dict[str, float] = field(default_factory=dict)  # Impact on each stakeholder
    resource_requirements: Dict[str, float] = field(default_factory=dict)
    
    # Success metrics
    success_indicators: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    
    def calculate_transition_rate(self, current_conditions: Dict[str, Any]) -> float:
        """Calculate transition rate given current conditions"""
        base_rate = self.transition_probability
        
        # Check trigger conditions
        condition_met_ratio = 1.0  # Default to 1.0 if no conditions
        if self.trigger_conditions:
            met_conditions = 0
            for condition, required_value in self.trigger_conditions.items():
                if condition in current_conditions:
                    current_value = current_conditions[condition]
                    if isinstance(required_value, (int, float)):
                        if current_value >= required_value:
                            met_conditions += 1
                    elif current_value == required_value:
                        met_conditions += 1
            condition_met_ratio = met_conditions / len(self.trigger_conditions)
        
        # Apply condition factor
        effective_rate = base_rate * condition_met_ratio
        
        # Apply catalyst effects
        catalyst_boost = 1.0
        for catalyst in self.catalyst_factors:
            if catalyst in current_conditions and current_conditions[catalyst]:
                catalyst_boost *= 1.2  # 20% boost per catalyst
        
        return min(1.0, effective_rate * catalyst_boost)


class QuantumSystem(BaseModel):
    """Represents complete quantum system state"""
    model_config = {"arbitrary_types_allowed": True}
    
    system_id: str = Field(default_factory=lambda: f"quantum_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # System components
    quantum_states: Dict[str, QuantumState] = {}
    state_transitions: Dict[str, StateTransition] = {}
    
    # System properties
    total_coherence: float = Field(ge=0.0, le=1.0, default=1.0)
    system_entropy: float = 0.0
    entanglement_network: Dict[str, List[str]] = {}  # State -> Connected states
    
    # Temporal evolution
    time_step: float = 1.0              # Time step for evolution
    last_update: datetime = Field(default_factory=datetime.now)
    
    # Machine learning integration
    ml_predictions: Dict[str, Any] = {}  # ML model predictions
    learning_rate: float = Field(ge=0.0, le=1.0, default=0.01)
    adaptation_history: List[Dict[str, Any]] = []
    
    def add_quantum_state(self, state: QuantumState) -> None:
        """Add quantum state to system"""
        self.quantum_states[state.state_id] = state
        self.last_update = datetime.now()
    
    def calculate_system_coherence(self) -> float:
        """Calculate overall system coherence"""
        if not self.quantum_states:
            return 0.0
        
        # Calculate coherence as weighted average of state probabilities
        total_coherence = 0.0
        total_weight = 0.0
        
        for state in self.quantum_states.values():
            if not state.measured:  # Only consider unmeasured states
                weight = abs(state.amplitude) ** 2
                coherence = state.calculate_decoherence(
                    (datetime.now() - state.created_at).total_seconds()
                )
                total_coherence += weight * coherence
                total_weight += weight
        
        if total_weight > 0:
            self.total_coherence = total_coherence / total_weight
        else:
            self.total_coherence = 0.0
        
        return self.total_coherence
    
    def evolve_system(self, time_step: Optional[float] = None) -> None:
        """Evolve quantum system over time"""
        if time_step is None:
            time_step = self.time_step
        
        # Simple evolution: apply decoherence
        for state in self.quantum_states.values():
            if not state.measured:
                time_elapsed = (datetime.now() - state.created_at).total_seconds()
                coherence = state.calculate_decoherence(time_elapsed)
                
                # Reduce amplitude based on decoherence
                state.amplitude *= coherence
                state.probability = abs(state.amplitude) ** 2
        
        # Update system properties
        self.calculate_system_coherence()
        self.last_update = datetime.now()
    
    def measure_state(self, state_id: str) -> Any:
        """Measure a quantum state, causing collapse"""
        if state_id not in self.quantum_states:
            return None
        
        state = self.quantum_states[state_id]
        if state.measured:
            return state.measurement_result
        
        # Probabilistic measurement
        measurement_result = np.random.random() < state.probability
        state.collapse_to_classical(measurement_result)
        
        # Update system coherence
        self.calculate_system_coherence()
        
        return measurement_result
    
    def get_entangled_states(self, state_id: str) -> List[QuantumState]:
        """Get all states entangled with given state"""
        if state_id not in self.entanglement_network:
            return []
        
        entangled_ids = self.entanglement_network[state_id]
        return [self.quantum_states[sid] for sid in entangled_ids if sid in self.quantum_states] 