"""
TRM-OS Quantum WIN States - Core Types
Định nghĩa các types cho quantum state management với ML
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
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


class WINCategory(Enum):
    """Categories of WINs for quantum analysis"""
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
    win_category: WINCategory
    organizational_level: str            # "individual", "team", "department", "organization"
    stakeholders: List[str] = None       # Affected stakeholders
    
    # Temporal properties
    coherence_time: float = 0.0         # How long state remains coherent
    decoherence_rate: float = 0.0       # Rate of decoherence
    created_at: datetime = None
    
    # Measurement properties
    measured: bool = False               # Has state been measured/collapsed?
    measurement_result: Optional[Any] = None
    measurement_time: Optional[datetime] = None
    
    # Entanglement
    entangled_states: List[str] = None   # IDs of entangled states
    entanglement_strength: float = 0.0   # Strength of entanglement
    
    def __post_init__(self):
        if self.stakeholders is None:
            self.stakeholders = []
        if self.entangled_states is None:
            self.entangled_states = []
        if self.created_at is None:
            self.created_at = datetime.now()
        
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
    win_id: str
    win_description: str
    win_category: WINCategory
    
    # Probability calculations
    base_probability: float              # Classical probability
    quantum_probability: float           # Quantum-enhanced probability
    superposition_factor: float          # Contribution from superposition
    entanglement_boost: float           # Boost from entangled states
    
    # Confidence metrics
    confidence_level: float = Field(ge=0.0, le=1.0, default=0.7)
    prediction_accuracy: float = Field(ge=0.0, le=1.0, default=0.6)
    
    # Supporting factors
    contributing_factors: List[str] = None
    risk_factors: List[str] = None
    
    # Temporal analysis
    probability_trend: str = "stable"    # "increasing", "decreasing", "stable", "volatile"
    optimal_timing: Optional[datetime] = None
    time_sensitivity: float = Field(ge=0.0, le=1.0, default=0.5)
    
    # Dependencies
    prerequisite_states: List[str] = None  # Required quantum states
    blocking_states: List[str] = None      # States that prevent this WIN
    
    def __post_init__(self):
        if self.contributing_factors is None:
            self.contributing_factors = []
        if self.risk_factors is None:
            self.risk_factors = []
        if self.prerequisite_states is None:
            self.prerequisite_states = []
        if self.blocking_states is None:
            self.blocking_states = []
    
    def calculate_net_probability(self) -> float:
        """Calculate net probability considering all factors"""
        net_prob = self.quantum_probability
        
        # Apply entanglement boost
        net_prob += self.entanglement_boost
        
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
    transition_amplitude: complex        # Quantum transition amplitude
    transition_time: float              # Expected transition time
    
    # Triggers and conditions
    trigger_conditions: Dict[str, Any] = None
    required_energy: float = 0.0        # Energy required for transition
    catalyst_factors: List[str] = None   # Factors that accelerate transition
    
    # Measurement effects
    measurement_induced: bool = False    # Is transition caused by measurement?
    decoherence_effect: float = 0.0     # How much decoherence this causes
    
    # Organizational impact
    stakeholder_impact: Dict[str, float] = None  # Impact on each stakeholder
    resource_requirements: Dict[str, float] = None
    
    # Success metrics
    success_indicators: List[str] = None
    failure_modes: List[str] = None
    
    def __post_init__(self):
        if self.trigger_conditions is None:
            self.trigger_conditions = {}
        if self.catalyst_factors is None:
            self.catalyst_factors = []
        if self.stakeholder_impact is None:
            self.stakeholder_impact = {}
        if self.resource_requirements is None:
            self.resource_requirements = {}
        if self.success_indicators is None:
            self.success_indicators = []
        if self.failure_modes is None:
            self.failure_modes = []
    
    def calculate_transition_rate(self, current_conditions: Dict[str, Any]) -> float:
        """Calculate transition rate given current conditions"""
        base_rate = self.transition_probability
        
        # Check trigger conditions
        condition_met_ratio = 0.0
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
    system_id: str = Field(default_factory=lambda: f"quantum_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # System components
    quantum_states: Dict[str, QuantumState] = {}
    win_probabilities: Dict[str, WINProbability] = {}
    state_transitions: Dict[str, StateTransition] = {}
    
    # System properties
    total_coherence: float = Field(ge=0.0, le=1.0, default=1.0)
    system_entropy: float = 0.0
    entanglement_network: Dict[str, List[str]] = {}  # State -> Connected states
    
    # Temporal evolution
    hamiltonian: Optional[np.ndarray] = Field(default=None, exclude=True)  # System evolution operator
    time_step: float = 1.0              # Time step for evolution
    last_update: datetime = Field(default_factory=datetime.now)
    
    # Machine learning integration
    ml_predictions: Dict[str, Any] = {}  # ML model predictions
    learning_rate: float = Field(ge=0.0, le=1.0, default=0.01)
    adaptation_history: List[Dict[str, Any]] = []
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_quantum_state(self, state: QuantumState) -> None:
        """Add quantum state to system"""
        self.quantum_states[state.state_id] = state
        
        # Update entanglement network
        for entangled_id in state.entangled_states:
            if entangled_id not in self.entanglement_network:
                self.entanglement_network[entangled_id] = []
            self.entanglement_network[entangled_id].append(state.state_id)
    
    def calculate_system_coherence(self) -> float:
        """Calculate total system coherence"""
        if not self.quantum_states:
            return 0.0
        
        total_coherence = 0.0
        total_weight = 0.0
        
        for state in self.quantum_states.values():
            if not state.measured:
                weight = state.probability
                coherence = state.calculate_decoherence(
                    (datetime.now() - state.created_at).total_seconds()
                )
                total_coherence += weight * coherence
                total_weight += weight
        
        self.total_coherence = total_coherence / total_weight if total_weight > 0 else 0.0
        return self.total_coherence
    
    def evolve_system(self, time_step: Optional[float] = None) -> None:
        """Evolve quantum system forward in time"""
        dt = time_step or self.time_step
        current_time = datetime.now()
        
        # Update decoherence for all states
        for state in self.quantum_states.values():
            if not state.measured:
                time_elapsed = (current_time - state.created_at).total_seconds()
                current_coherence = state.calculate_decoherence(time_elapsed)
                
                # Apply decoherence to amplitude
                state.amplitude *= current_coherence
                state.probability = abs(state.amplitude) ** 2
        
        # Process state transitions
        for transition in self.state_transitions.values():
            # This would implement quantum evolution operator
            # For now, simplified classical transition logic
            pass
        
        # Update system properties
        self.calculate_system_coherence()
        self.last_update = current_time
    
    def measure_state(self, state_id: str) -> Any:
        """Measure quantum state, causing collapse"""
        if state_id not in self.quantum_states:
            return None
        
        state = self.quantum_states[state_id]
        if state.measured:
            return state.measurement_result
        
        # Quantum measurement - probabilistic collapse
        measurement_result = np.random.random() < state.probability
        state.collapse_to_classical(measurement_result)
        
        # Decoherence effect on entangled states
        for entangled_id in state.entangled_states:
            if entangled_id in self.quantum_states:
                entangled_state = self.quantum_states[entangled_id]
                if not entangled_state.measured:
                    # Entanglement causes correlated measurement
                    correlation = state.entanglement_strength
                    if np.random.random() < correlation:
                        entangled_state.collapse_to_classical(measurement_result)
        
        return measurement_result 