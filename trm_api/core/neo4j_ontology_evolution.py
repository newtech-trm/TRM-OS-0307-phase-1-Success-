#!/usr/bin/env python3
"""
Neo4j Ontology Auto-Evolution System - TRM-OS v2.0

Automatic ontology evolution với "hệ miễn dịch" capabilities:
- Schema migration tự động  
- Conflict resolution và version management
- Backward compatibility preservation
- Evolution impact analysis

Philosophy: Ontology evolution như hệ miễn dịch - detect, analyze, adapt
"""

import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Set
from dataclasses import dataclass, field
from enum import Enum
import neo4j
from neo4j import AsyncGraphDatabase

from trm_api.core.logging_config import get_logger
from trm_api.eventbus.system_event_bus import SystemEventBus, SystemEvent, EventType
from trm_api.core.semantic_change_detector import SemanticChangeDetector, ComprehensiveChangeAnalysis
from trm_api.agents.meta_agent_intelligence import MetaAgentIntelligence

logger = get_logger(__name__)


class EvolutionType(str, Enum):
    """Types of ontology evolution"""
    SCHEMA_ADDITION = "schema_addition"        # Add new nodes/relationships
    SCHEMA_MODIFICATION = "schema_modification"  # Modify existing schema
    SCHEMA_REMOVAL = "schema_removal"          # Remove obsolete schema
    CONSTRAINT_ADDITION = "constraint_addition"  # Add new constraints
    CONSTRAINT_MODIFICATION = "constraint_modification"  # Modify constraints
    INDEX_OPTIMIZATION = "index_optimization"    # Add/modify indexes
    DATA_MIGRATION = "data_migration"          # Migrate data structure
    PROPERTY_EVOLUTION = "property_evolution"   # Evolve node/rel properties


class ConflictSeverity(str, Enum):
    """Severity levels of ontology conflicts"""
    MINOR = "minor"           # Minor compatibility issues
    MODERATE = "moderate"     # Requires careful handling
    SEVERE = "severe"         # Major breaking changes
    CRITICAL = "critical"     # System stability at risk


class EvolutionStatus(str, Enum):
    """Status of evolution process"""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    TESTING = "testing"
    IMPLEMENTING = "implementing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class OntologyVersion:
    """Version information cho ontology"""
    version_id: str
    major: int
    minor: int
    patch: int
    created_at: datetime
    description: str
    schema_hash: str
    compatibility_score: float  # 0.0 - 1.0
    migration_required: bool = False
    rollback_available: bool = True


@dataclass
class SchemaChange:
    """Individual schema change detected"""
    change_id: str
    change_type: EvolutionType
    affected_elements: List[str]  # Node labels, relationship types, properties
    cypher_statement: str
    impact_assessment: Dict[str, Any]
    risk_level: ConflictSeverity
    estimated_duration: float  # seconds
    dependencies: List[str] = field(default_factory=list)
    rollback_statement: Optional[str] = None


@dataclass
class ConflictResolution:
    """Resolution cho ontology conflicts"""
    conflict_id: str
    conflict_type: str
    severity: ConflictSeverity
    affected_components: List[str]
    resolution_strategy: str
    resolution_steps: List[str]
    validation_queries: List[str]
    success_probability: float
    fallback_strategy: Optional[str] = None


@dataclass
class EvolutionPlan:
    """Comprehensive evolution plan"""
    plan_id: str
    created_at: datetime
    source_version: OntologyVersion
    target_version: OntologyVersion
    schema_changes: List[SchemaChange]
    conflict_resolutions: List[ConflictResolution]
    execution_order: List[str]
    estimated_total_time: float
    rollback_plan: Dict[str, Any]
    validation_suite: List[str]


class SchemaAnalyzer:
    """Analyzer cho ontology schema changes"""
    
    def __init__(self, driver: neo4j.AsyncDriver):
        self.logger = get_logger("schema_analyzer")
        self.driver = driver
        self.current_schema: Dict[str, Any] = {}
        self.version_history: List[OntologyVersion] = []
        self.change_patterns: Dict[str, int] = {}
    
    async def analyze_current_schema(self) -> Dict[str, Any]:
        """Analyze current Neo4j schema"""
        try:
            schema = {
                "node_labels": [],
                "relationship_types": [],
                "property_keys": [],
                "constraints": [],
                "indexes": [],
                "procedures": [],
                "functions": []
            }
            
            async with self.driver.session() as session:
                # Get node labels
                result = await session.run("CALL db.labels()")
                schema["node_labels"] = [record["label"] for record in await result.data()]
                
                # Get relationship types
                result = await session.run("CALL db.relationshipTypes()")
                schema["relationship_types"] = [record["relationshipType"] for record in await result.data()]
                
                # Get property keys
                result = await session.run("CALL db.propertyKeys()")
                schema["property_keys"] = [record["propertyKey"] for record in await result.data()]
                
                # Get constraints
                result = await session.run("SHOW CONSTRAINTS")
                schema["constraints"] = await result.data()
                
                # Get indexes
                result = await session.run("SHOW INDEXES")
                schema["indexes"] = await result.data()
                
                # Get procedures và functions
                result = await session.run("SHOW PROCEDURES")
                schema["procedures"] = [record["name"] for record in await result.data()]
                
                result = await session.run("SHOW FUNCTIONS")
                schema["functions"] = [record["name"] for record in await result.data()]
            
            self.current_schema = schema
            self.logger.info(f"Schema analyzed: {len(schema['node_labels'])} labels, "
                           f"{len(schema['relationship_types'])} relationships")
            
            return schema
            
        except Exception as e:
            self.logger.error(f"Error analyzing schema: {e}")
            return {}
    
    def calculate_schema_hash(self, schema: Dict[str, Any]) -> str:
        """Calculate hash cho schema for change detection"""
        try:
            # Create deterministic string representation
            schema_str = json.dumps(schema, sort_keys=True, default=str)
            return hashlib.sha256(schema_str.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating schema hash: {e}")
            return "unknown"
    
    async def detect_schema_changes(self, new_schema: Dict[str, Any]) -> List[SchemaChange]:
        """Detect changes between current và new schema"""
        changes = []
        
        try:
            # Compare node labels
            current_labels = set(self.current_schema.get("node_labels", []))
            new_labels = set(new_schema.get("node_labels", []))
            
            # Added labels
            for label in new_labels - current_labels:
                changes.append(SchemaChange(
                    change_id=f"add_label_{label}_{int(datetime.now().timestamp())}",
                    change_type=EvolutionType.SCHEMA_ADDITION,
                    affected_elements=[f":{label}"],
                    cypher_statement=f"// Label :{label} added automatically",
                    impact_assessment={"new_label": label, "impact": "low"},
                    risk_level=ConflictSeverity.MINOR,
                    estimated_duration=1.0
                ))
            
            # Removed labels
            for label in current_labels - new_labels:
                changes.append(SchemaChange(
                    change_id=f"remove_label_{label}_{int(datetime.now().timestamp())}",
                    change_type=EvolutionType.SCHEMA_REMOVAL,
                    affected_elements=[f":{label}"],
                    cypher_statement=f"// Consider removing unused label :{label}",
                    impact_assessment={"removed_label": label, "impact": "high"},
                    risk_level=ConflictSeverity.SEVERE,
                    estimated_duration=30.0
                ))
            
            # Compare relationship types
            current_rels = set(self.current_schema.get("relationship_types", []))
            new_rels = set(new_schema.get("relationship_types", []))
            
            # Added relationships
            for rel in new_rels - current_rels:
                changes.append(SchemaChange(
                    change_id=f"add_rel_{rel}_{int(datetime.now().timestamp())}",
                    change_type=EvolutionType.SCHEMA_ADDITION,
                    affected_elements=[f":{rel}"],
                    cypher_statement=f"// Relationship :{rel} added automatically",
                    impact_assessment={"new_relationship": rel, "impact": "medium"},
                    risk_level=ConflictSeverity.MINOR,
                    estimated_duration=2.0
                ))
            
            # Compare constraints
            current_constraints = len(self.current_schema.get("constraints", []))
            new_constraints = len(new_schema.get("constraints", []))
            
            if new_constraints > current_constraints:
                changes.append(SchemaChange(
                    change_id=f"add_constraints_{int(datetime.now().timestamp())}",
                    change_type=EvolutionType.CONSTRAINT_ADDITION,
                    affected_elements=["constraints"],
                    cypher_statement="// New constraints detected",
                    impact_assessment={"constraint_changes": new_constraints - current_constraints},
                    risk_level=ConflictSeverity.MODERATE,
                    estimated_duration=10.0
                ))
            
            self.logger.info(f"Detected {len(changes)} schema changes")
            return changes
            
        except Exception as e:
            self.logger.error(f"Error detecting schema changes: {e}")
            return []
    
    def assess_change_impact(self, change: SchemaChange) -> Dict[str, Any]:
        """Assess impact của schema change"""
        impact = {
            "compatibility_score": 1.0,
            "breaking_changes": False,
            "affected_queries": [],
            "data_migration_required": False,
            "estimated_downtime": 0.0
        }
        
        try:
            if change.change_type == EvolutionType.SCHEMA_REMOVAL:
                impact["compatibility_score"] = 0.3
                impact["breaking_changes"] = True
                impact["estimated_downtime"] = 60.0
            elif change.change_type == EvolutionType.SCHEMA_MODIFICATION:
                impact["compatibility_score"] = 0.7
                impact["data_migration_required"] = True
                impact["estimated_downtime"] = 30.0
            elif change.change_type == EvolutionType.CONSTRAINT_ADDITION:
                impact["compatibility_score"] = 0.8
                impact["estimated_downtime"] = 10.0
            else:
                impact["compatibility_score"] = 0.95
                impact["estimated_downtime"] = 0.0
            
            return impact
            
        except Exception as e:
            self.logger.error(f"Error assessing change impact: {e}")
            return impact


class ConflictResolver:
    """Resolver cho ontology conflicts"""
    
    def __init__(self, driver: neo4j.AsyncDriver):
        self.logger = get_logger("conflict_resolver")
        self.driver = driver
        self.resolution_strategies: Dict[str, Dict[str, Any]] = {}
        self.conflict_history: List[ConflictResolution] = []
        
        self._initialize_resolution_strategies()
    
    def _initialize_resolution_strategies(self) -> None:
        """Initialize conflict resolution strategies"""
        self.resolution_strategies = {
            "label_conflict": {
                "strategy": "merge_with_mapping",
                "description": "Merge conflicting labels với property mapping",
                "success_rate": 0.85,
                "rollback_complexity": "medium"
            },
            "constraint_conflict": {
                "strategy": "gradual_enforcement",
                "description": "Gradually enforce constraints với data cleanup",
                "success_rate": 0.90,
                "rollback_complexity": "low"
            },
            "relationship_conflict": {
                "strategy": "relationship_versioning",
                "description": "Version relationships cho backward compatibility",
                "success_rate": 0.80,
                "rollback_complexity": "high"
            },
            "property_conflict": {
                "strategy": "property_migration",
                "description": "Migrate properties với type conversion",
                "success_rate": 0.95,
                "rollback_complexity": "low"
            }
        }
    
    async def detect_conflicts(self, changes: List[SchemaChange]) -> List[ConflictResolution]:
        """Detect conflicts trong schema changes"""
        conflicts = []
        
        try:
            # Group changes by affected elements
            element_changes: Dict[str, List[SchemaChange]] = {}
            for change in changes:
                for element in change.affected_elements:
                    if element not in element_changes:
                        element_changes[element] = []
                    element_changes[element].append(change)
            
            # Detect conflicts when multiple changes affect same element
            for element, element_change_list in element_changes.items():
                if len(element_change_list) > 1:
                    conflicts.append(await self._resolve_element_conflict(element, element_change_list))
            
            # Detect dependency conflicts
            for change in changes:
                dependency_conflicts = await self._check_dependency_conflicts(change, changes)
                conflicts.extend(dependency_conflicts)
            
            self.logger.info(f"Detected {len(conflicts)} conflicts")
            return conflicts
            
        except Exception as e:
            self.logger.error(f"Error detecting conflicts: {e}")
            return []
    
    async def _resolve_element_conflict(
        self, 
        element: str, 
        conflicting_changes: List[SchemaChange]
    ) -> ConflictResolution:
        """Resolve conflicts cho specific element"""
        conflict_type = self._determine_conflict_type(element, conflicting_changes)
        strategy = self.resolution_strategies.get(conflict_type, self.resolution_strategies["property_conflict"])
        
        severity = ConflictSeverity.MINOR
        for change in conflicting_changes:
            if change.risk_level.value == "severe":
                severity = ConflictSeverity.SEVERE
            elif change.risk_level.value == "moderate" and severity == ConflictSeverity.MINOR:
                severity = ConflictSeverity.MODERATE
        
        return ConflictResolution(
            conflict_id=f"conflict_{element}_{int(datetime.now().timestamp())}",
            conflict_type=conflict_type,
            severity=severity,
            affected_components=[element],
            resolution_strategy=strategy["strategy"],
            resolution_steps=[
                f"Analyze {element} conflicts",
                f"Apply {strategy['strategy']} resolution",
                f"Validate resolution effectiveness",
                "Monitor post-resolution stability"
            ],
            validation_queries=[
                f"MATCH (n:{element.replace(':', '')}) RETURN count(n) as node_count",
                f"SHOW CONSTRAINTS WHERE entityType = '{element}'"
            ],
            success_probability=strategy["success_rate"],
            fallback_strategy="rollback_to_previous_version"
        )
    
    def _determine_conflict_type(self, element: str, changes: List[SchemaChange]) -> str:
        """Determine type của conflict"""
        if element.startswith(":") and any(c.change_type == EvolutionType.SCHEMA_REMOVAL for c in changes):
            return "label_conflict"
        elif "constraint" in element.lower():
            return "constraint_conflict"
        elif any(c.change_type == EvolutionType.PROPERTY_EVOLUTION for c in changes):
            return "property_conflict"
        else:
            return "relationship_conflict"
    
    async def _check_dependency_conflicts(
        self, 
        change: SchemaChange, 
        all_changes: List[SchemaChange]
    ) -> List[ConflictResolution]:
        """Check for dependency conflicts"""
        conflicts = []
        
        # Check if dependencies are satisfied
        for dep_id in change.dependencies:
            dep_satisfied = any(c.change_id == dep_id for c in all_changes)
            if not dep_satisfied:
                conflicts.append(ConflictResolution(
                    conflict_id=f"dep_conflict_{change.change_id}_{dep_id}",
                    conflict_type="dependency_conflict",
                    severity=ConflictSeverity.MODERATE,
                    affected_components=[change.change_id, dep_id],
                    resolution_strategy="dependency_injection",
                    resolution_steps=[
                        f"Identify missing dependency: {dep_id}",
                        f"Create or defer change: {change.change_id}",
                        "Re-evaluate execution order"
                    ],
                    validation_queries=[
                        f"// Validate dependency {dep_id} exists"
                    ],
                    success_probability=0.9
                ))
        
        return conflicts


class MigrationExecutor:
    """Executor cho ontology migrations"""
    
    def __init__(self, driver: neo4j.AsyncDriver):
        self.logger = get_logger("migration_executor")
        self.driver = driver
        self.migration_history: List[Dict[str, Any]] = []
        self.active_migrations: Dict[str, Dict[str, Any]] = {}
    
    async def execute_evolution_plan(self, plan: EvolutionPlan) -> bool:
        """Execute complete evolution plan"""
        try:
            self.logger.info(f"Executing evolution plan: {plan.plan_id}")
            
            # Start transaction
            async with self.driver.session() as session:
                async with session.begin_transaction() as tx:
                    try:
                        # Execute changes in planned order
                        for change_id in plan.execution_order:
                            change = next((c for c in plan.schema_changes if c.change_id == change_id), None)
                            if change:
                                success = await self._execute_schema_change(tx, change)
                                if not success:
                                    await tx.rollback()
                                    return False
                        
                        # Validate results
                        validation_success = await self._validate_migration(tx, plan)
                        if not validation_success:
                            await tx.rollback()
                            return False
                        
                        # Commit transaction
                        await tx.commit()
                        
                        # Record successful migration
                        self.migration_history.append({
                            "plan_id": plan.plan_id,
                            "executed_at": datetime.now(),
                            "status": "success",
                            "changes_count": len(plan.schema_changes)
                        })
                        
                        self.logger.info(f"Evolution plan {plan.plan_id} executed successfully")
                        return True
                        
                    except Exception as e:
                        await tx.rollback()
                        self.logger.error(f"Migration failed, rolled back: {e}")
                        return False
            
        except Exception as e:
            self.logger.error(f"Error executing evolution plan: {e}")
            return False
    
    async def _execute_schema_change(self, tx, change: SchemaChange) -> bool:
        """Execute individual schema change"""
        try:
            if change.cypher_statement and not change.cypher_statement.startswith("//"):
                await tx.run(change.cypher_statement)
                self.logger.debug(f"Executed change: {change.change_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing change {change.change_id}: {e}")
            return False
    
    async def _validate_migration(self, tx, plan: EvolutionPlan) -> bool:
        """Validate migration results"""
        try:
            # Run validation queries
            for query in plan.validation_suite:
                if query and not query.startswith("//"):
                    result = await tx.run(query)
                    await result.consume()  # Ensure query executes
            
            return True
            
        except Exception as e:
            self.logger.error(f"Migration validation failed: {e}")
            return False


class OntologyEvolutionEngine:
    """Main engine cho Neo4j ontology auto-evolution"""
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.logger = get_logger("ontology_evolution_engine")
        
        # Neo4j connection
        self.driver = AsyncGraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        # Core components
        self.schema_analyzer = SchemaAnalyzer(self.driver)
        self.conflict_resolver = ConflictResolver(self.driver)
        self.migration_executor = MigrationExecutor(self.driver)
        self.semantic_detector = SemanticChangeDetector()
        self.event_bus = SystemEventBus()
        
        # Configuration
        self.config = {
            "auto_evolution_enabled": True,
            "auto_migration_threshold": 0.8,  # Auto-migrate if success probability > 80%
            "backup_before_migration": True,
            "validation_timeout_seconds": 300,
            "max_concurrent_migrations": 1
        }
        
        # State management
        self.current_version: Optional[OntologyVersion] = None
        self.pending_evolutions: List[EvolutionPlan] = []
        self.is_monitoring = False
        
        # Statistics
        self.stats = {
            "total_evolutions": 0,
            "successful_migrations": 0,
            "failed_migrations": 0,
            "conflicts_resolved": 0,
            "rollbacks_performed": 0
        }
    
    async def initialize(self) -> bool:
        """Initialize ontology evolution engine"""
        try:
            self.logger.info("Initializing Ontology Evolution Engine...")
            
            # Test Neo4j connection
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as test")
                await result.single()
            
            # Analyze current schema
            await self.schema_analyzer.analyze_current_schema()
            
            # Create initial version
            await self._create_initial_version()
            
            # Start monitoring
            if self.config["auto_evolution_enabled"]:
                asyncio.create_task(self._evolution_monitoring_loop())
                self.is_monitoring = True
            
            self.logger.info("Ontology Evolution Engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize evolution engine: {e}")
            return False
    
    async def _create_initial_version(self) -> None:
        """Create initial ontology version"""
        try:
            schema = self.schema_analyzer.current_schema
            schema_hash = self.schema_analyzer.calculate_schema_hash(schema)
            
            self.current_version = OntologyVersion(
                version_id=f"v1.0.0_{schema_hash[:8]}",
                major=1,
                minor=0,
                patch=0,
                created_at=datetime.now(),
                description="Initial ontology version",
                schema_hash=schema_hash,
                compatibility_score=1.0
            )
            
            self.schema_analyzer.version_history.append(self.current_version)
            self.logger.info(f"Initial version created: {self.current_version.version_id}")
            
        except Exception as e:
            self.logger.error(f"Error creating initial version: {e}")
    
    async def _evolution_monitoring_loop(self) -> None:
        """Main monitoring loop cho ontology evolution"""
        while self.is_monitoring:
            try:
                # Check for schema changes
                await self._check_for_evolution_triggers()
                
                # Process pending evolutions
                await self._process_pending_evolutions()
                
                # Wait for next check
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in evolution monitoring loop: {e}")
                await asyncio.sleep(60)
    
    async def _check_for_evolution_triggers(self) -> None:
        """Check for triggers that require ontology evolution"""
        try:
            # Re-analyze current schema
            new_schema = await self.schema_analyzer.analyze_current_schema()
            new_hash = self.schema_analyzer.calculate_schema_hash(new_schema)
            
            # Compare với current version
            if new_hash != self.current_version.schema_hash:
                self.logger.info("Schema changes detected, triggering evolution analysis")
                
                # Detect specific changes
                changes = await self.schema_analyzer.detect_schema_changes(new_schema)
                
                if changes:
                    # Create evolution plan
                    plan = await self._create_evolution_plan(changes, new_schema, new_hash)
                    self.pending_evolutions.append(plan)
                    
                    # Publish evolution event
                    await self.event_bus.publish(SystemEvent(
                        event_type="ontology.evolution_detected",
                        entity_id=plan.plan_id,
                        data={
                            "changes_count": len(changes),
                            "plan_id": plan.plan_id,
                            "estimated_time": plan.estimated_total_time
                        }
                    ))
            
        except Exception as e:
            self.logger.error(f"Error checking evolution triggers: {e}")
    
    async def _create_evolution_plan(
        self, 
        changes: List[SchemaChange], 
        new_schema: Dict[str, Any],
        new_hash: str
    ) -> EvolutionPlan:
        """Create comprehensive evolution plan"""
        try:
            # Detect conflicts
            conflicts = await self.conflict_resolver.detect_conflicts(changes)
            
            # Create target version
            target_version = OntologyVersion(
                version_id=f"v{self.current_version.major}.{self.current_version.minor + 1}.0_{new_hash[:8]}",
                major=self.current_version.major,
                minor=self.current_version.minor + 1,
                patch=0,
                created_at=datetime.now(),
                description=f"Auto-evolution với {len(changes)} changes",
                schema_hash=new_hash,
                compatibility_score=self._calculate_compatibility_score(changes)
            )
            
            # Determine execution order
            execution_order = self._determine_execution_order(changes, conflicts)
            
            # Calculate estimated time
            total_time = sum(change.estimated_duration for change in changes)
            
            plan = EvolutionPlan(
                plan_id=f"evolution_{int(datetime.now().timestamp())}",
                created_at=datetime.now(),
                source_version=self.current_version,
                target_version=target_version,
                schema_changes=changes,
                conflict_resolutions=conflicts,
                execution_order=execution_order,
                estimated_total_time=total_time,
                rollback_plan=self._create_rollback_plan(changes),
                validation_suite=self._create_validation_suite(changes)
            )
            
            self.logger.info(f"Evolution plan created: {plan.plan_id} với {len(changes)} changes")
            return plan
            
        except Exception as e:
            self.logger.error(f"Error creating evolution plan: {e}")
            raise
    
    def _calculate_compatibility_score(self, changes: List[SchemaChange]) -> float:
        """Calculate compatibility score cho changes"""
        if not changes:
            return 1.0
        
        total_impact = 0.0
        for change in changes:
            impact = self.schema_analyzer.assess_change_impact(change)
            total_impact += impact["compatibility_score"]
        
        return total_impact / len(changes)
    
    def _determine_execution_order(
        self, 
        changes: List[SchemaChange], 
        conflicts: List[ConflictResolution]
    ) -> List[str]:
        """Determine optimal execution order cho changes"""
        # Simple topological sort based on dependencies
        ordered = []
        remaining = changes.copy()
        
        while remaining:
            # Find changes without unresolved dependencies
            ready = [
                change for change in remaining 
                if all(dep_id in ordered for dep_id in change.dependencies)
            ]
            
            if not ready:
                # Break cycles by taking lowest risk change
                ready = [min(remaining, key=lambda c: c.risk_level.value)]
            
            # Add ready changes to order
            for change in ready:
                ordered.append(change.change_id)
                remaining.remove(change)
        
        return ordered
    
    def _create_rollback_plan(self, changes: List[SchemaChange]) -> Dict[str, Any]:
        """Create rollback plan cho changes"""
        return {
            "rollback_statements": [
                change.rollback_statement for change in changes 
                if change.rollback_statement
            ],
            "rollback_order": [
                change.change_id for change in reversed(changes)
            ],
            "backup_required": self.config["backup_before_migration"]
        }
    
    def _create_validation_suite(self, changes: List[SchemaChange]) -> List[str]:
        """Create validation queries for changes"""
        queries = []
        
        for change in changes:
            if change.change_type == EvolutionType.SCHEMA_ADDITION:
                # Validate new elements exist
                for element in change.affected_elements:
                    if element.startswith(":"):
                        label = element[1:]
                        queries.append(f"MATCH (n:{label}) RETURN count(n) as count")
            
            elif change.change_type == EvolutionType.CONSTRAINT_ADDITION:
                queries.append("SHOW CONSTRAINTS")
        
        # Add general health checks
        queries.extend([
            "CALL db.labels()",
            "CALL db.relationshipTypes()",
            "CALL db.propertyKeys()"
        ])
        
        return queries
    
    async def _process_pending_evolutions(self) -> None:
        """Process pending evolution plans"""
        if not self.pending_evolutions:
            return
        
        try:
            for plan in self.pending_evolutions.copy():
                # Check if auto-migration threshold met
                compatibility_score = plan.target_version.compatibility_score
                
                if (compatibility_score >= self.config["auto_migration_threshold"] and
                    len(plan.conflict_resolutions) == 0):
                    
                    # Auto-execute migration
                    success = await self.migration_executor.execute_evolution_plan(plan)
                    
                    if success:
                        self.current_version = plan.target_version
                        self.schema_analyzer.version_history.append(self.current_version)
                        self.stats["successful_migrations"] += 1
                        
                        self.logger.info(f"Auto-migration successful: {plan.plan_id}")
                    else:
                        self.stats["failed_migrations"] += 1
                        self.logger.error(f"Auto-migration failed: {plan.plan_id}")
                    
                    self.pending_evolutions.remove(plan)
                    self.stats["total_evolutions"] += 1
                
                else:
                    self.logger.info(f"Evolution {plan.plan_id} requires manual approval "
                                   f"(compatibility: {compatibility_score:.2f}, "
                                   f"conflicts: {len(plan.conflict_resolutions)})")
        
        except Exception as e:
            self.logger.error(f"Error processing pending evolutions: {e}")
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get current evolution status"""
        return {
            "current_version": {
                "version_id": self.current_version.version_id if self.current_version else None,
                "schema_hash": self.current_version.schema_hash if self.current_version else None,
                "compatibility_score": self.current_version.compatibility_score if self.current_version else 0.0
            },
            "monitoring_active": self.is_monitoring,
            "pending_evolutions": len(self.pending_evolutions),
            "statistics": self.stats,
            "version_history_count": len(self.schema_analyzer.version_history)
        }
    
    async def shutdown(self) -> None:
        """Shutdown evolution engine"""
        self.is_monitoring = False
        await self.driver.close()
        self.logger.info("Ontology Evolution Engine shut down")


async def get_ontology_evolution_engine() -> OntologyEvolutionEngine:
    """Get Ontology Evolution Engine instance"""
    import os
    return OntologyEvolutionEngine(
        neo4j_uri=os.getenv("NEO4J_URI"),
        neo4j_user=os.getenv("NEO4J_USER"),
        neo4j_password=os.getenv("NEO4J_PASSWORD")
    ) 