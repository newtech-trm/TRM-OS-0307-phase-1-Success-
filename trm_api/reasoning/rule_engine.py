"""
RuleEngine - Business rules and decision logic engine

Manages:
- Business rules for tension processing
- Decision trees for solution recommendations
- Conditional logic for automated actions
- Rule validation and conflict detection
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json

class RuleType(Enum):
    CONDITION = "condition"
    ACTION = "action"
    VALIDATION = "validation"
    ESCALATION = "escalation"

class OperatorType(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"

@dataclass
class RuleCondition:
    """Điều kiện trong rule"""
    field: str
    operator: OperatorType
    value: Any
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate condition against context"""
        field_value = self._get_field_value(context, self.field)
        
        if self.operator == OperatorType.EQUALS:
            return field_value == self.value
        elif self.operator == OperatorType.NOT_EQUALS:
            return field_value != self.value
        elif self.operator == OperatorType.GREATER_THAN:
            return field_value > self.value
        elif self.operator == OperatorType.LESS_THAN:
            return field_value < self.value
        elif self.operator == OperatorType.CONTAINS:
            return self.value in str(field_value).lower()
        elif self.operator == OperatorType.NOT_CONTAINS:
            return self.value not in str(field_value).lower()
        elif self.operator == OperatorType.IN:
            return field_value in self.value
        elif self.operator == OperatorType.NOT_IN:
            return field_value not in self.value
        else:
            return False
    
    def _get_field_value(self, context: Dict[str, Any], field_path: str) -> Any:
        """Get nested field value using dot notation"""
        keys = field_path.split('.')
        value = context
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value

@dataclass
class RuleAction:
    """Action to execute when rule conditions are met"""
    action_type: str
    parameters: Dict[str, Any]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute action and return results"""
        return {
            "action_type": self.action_type,
            "parameters": self.parameters,
            "context": context,
            "executed": True
        }

@dataclass
class BusinessRule:
    """Business rule với conditions và actions"""
    id: str
    name: str
    description: str
    rule_type: RuleType
    conditions: List[RuleCondition]
    actions: List[RuleAction]
    priority: int = 0
    enabled: bool = True
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate all conditions (AND logic)"""
        if not self.enabled:
            return False
            
        return all(condition.evaluate(context) for condition in self.conditions)
    
    def execute_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute all actions if conditions are met"""
        if not self.evaluate(context):
            return []
        
        results = []
        for action in self.actions:
            result = action.execute(context)
            results.append(result)
        
        return results

class RuleEngine:
    """
    Rule-based decision engine for TRM-OS reasoning system.
    
    Features:
    - Dynamic rule evaluation
    - Conflict detection
    - Rule prioritization
    - Action execution
    - Rule validation
    """
    
    def __init__(self):
        self.rules: Dict[str, BusinessRule] = {}
        self.rule_groups: Dict[str, List[str]] = {}
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default business rules for TRM-OS"""
        
        # Rule 1: Critical tension auto-escalation
        critical_escalation = BusinessRule(
            id="critical_tension_escalation",
            name="Critical Tension Auto-Escalation",
            description="Automatically escalate tensions with critical priority",
            rule_type=RuleType.ESCALATION,
            conditions=[
                RuleCondition("analysis.suggested_priority", OperatorType.EQUALS, 2),
                RuleCondition("analysis.impact_level.value", OperatorType.GREATER_THAN, 3)
            ],
            actions=[
                RuleAction("escalate_tension", {
                    "escalation_level": "critical",
                    "notify_stakeholders": True,
                    "create_incident": True
                }),
                RuleAction("update_priority", {"priority": 2})
            ],
            priority=1
        )
        
        # Rule 2: Security-related tension handling
        security_rule = BusinessRule(
            id="security_tension_handling",
            name="Security Tension Special Handling",
            description="Special handling for security-related tensions",
            rule_type=RuleType.ACTION,
            conditions=[
                RuleCondition("analysis.key_themes", OperatorType.CONTAINS, "Security")
            ],
            actions=[
                RuleAction("assign_security_team", {
                    "team": "security",
                    "sla": "4_hours"
                }),
                RuleAction("create_security_ticket", {
                    "classification": "security_review"
                })
            ],
            priority=2
        )
        
        # Rule 3: High-impact business tension
        business_impact_rule = BusinessRule(
            id="high_business_impact",
            name="High Business Impact Tension",
            description="Handle high business impact tensions",
            rule_type=RuleType.ACTION,
            conditions=[
                RuleCondition("analysis.key_themes", OperatorType.CONTAINS, "Business"),
                RuleCondition("analysis.impact_level.value", OperatorType.GREATER_THAN, 2)
            ],
            actions=[
                RuleAction("notify_business_stakeholders", {
                    "stakeholder_groups": ["product_owners", "business_analysts"]
                }),
                RuleAction("schedule_review", {
                    "review_type": "business_impact_assessment",
                    "timeline": "24_hours"
                })
            ],
            priority=3
        )
        
        # Rule 4: Technology debt identification
        tech_debt_rule = BusinessRule(
            id="tech_debt_identification",
            name="Technology Debt Identification",
            description="Identify and tag technology debt tensions",
            rule_type=RuleType.VALIDATION,
            conditions=[
                RuleCondition("analysis.tension_type.value", OperatorType.EQUALS, "Problem"),
                RuleCondition("analysis.key_themes", OperatorType.CONTAINS, "Technology"),
                RuleCondition("title", OperatorType.CONTAINS, "technical debt")
            ],
            actions=[
                RuleAction("add_tag", {"tag": "technical_debt"}),
                RuleAction("assign_to_team", {"team": "architecture"})
            ],
            priority=4
        )
        
        # Rule 5: Opportunity prioritization
        opportunity_rule = BusinessRule(
            id="opportunity_prioritization",
            name="Opportunity Prioritization",
            description="Prioritize opportunity-type tensions",
            rule_type=RuleType.ACTION,
            conditions=[
                RuleCondition("analysis.tension_type.value", OperatorType.EQUALS, "Opportunity")
            ],
            actions=[
                RuleAction("add_to_backlog", {
                    "backlog_type": "opportunity",
                    "review_cycle": "monthly"
                }),
                RuleAction("calculate_roi_estimate", {
                    "estimation_method": "basic"
                })
            ],
            priority=5
        )
        
        # Add rules to engine
        for rule in [critical_escalation, security_rule, business_impact_rule, 
                    tech_debt_rule, opportunity_rule]:
            self.add_rule(rule)
    
    def add_rule(self, rule: BusinessRule):
        """Add rule to engine"""
        self.rules[rule.id] = rule
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove rule from engine"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[BusinessRule]:
        """Get rule by ID"""
        return self.rules.get(rule_id)
    
    def evaluate_rules(self, context: Dict[str, Any], 
                      rule_type: Optional[RuleType] = None) -> List[Dict[str, Any]]:
        """
        Evaluate all rules against context
        
        Args:
            context: Context data for rule evaluation
            rule_type: Optional filter by rule type
            
        Returns:
            List of rule evaluation results
        """
        results = []
        
        # Filter rules by type if specified
        rules_to_evaluate = []
        for rule in self.rules.values():
            if rule_type is None or rule.rule_type == rule_type:
                rules_to_evaluate.append(rule)
        
        # Sort by priority (higher priority first)
        rules_to_evaluate.sort(key=lambda r: r.priority)
        
        # Evaluate each rule
        for rule in rules_to_evaluate:
            if rule.evaluate(context):
                action_results = rule.execute_actions(context)
                
                result = {
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "rule_type": rule.rule_type.value,
                    "matched": True,
                    "actions_executed": len(action_results),
                    "action_results": action_results
                }
                results.append(result)
        
        return results
    
    def validate_rule(self, rule: BusinessRule) -> Dict[str, Any]:
        """Validate rule configuration"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        if not rule.id:
            validation_result["errors"].append("Rule ID is required")
            validation_result["valid"] = False
        
        if not rule.name:
            validation_result["errors"].append("Rule name is required")
            validation_result["valid"] = False
        
        if not rule.conditions:
            validation_result["warnings"].append("Rule has no conditions")
        
        if not rule.actions:
            validation_result["warnings"].append("Rule has no actions")
        
        # Check for duplicate rule ID
        if rule.id in self.rules and self.rules[rule.id] != rule:
            validation_result["errors"].append(f"Rule ID '{rule.id}' already exists")
            validation_result["valid"] = False
        
        return validation_result
    
    def detect_rule_conflicts(self) -> List[Dict[str, Any]]:
        """Detect potential conflicts between rules"""
        conflicts = []
        
        # Simple conflict detection: rules with same conditions but different actions
        rule_list = list(self.rules.values())
        
        for i, rule1 in enumerate(rule_list):
            for rule2 in rule_list[i+1:]:
                if self._rules_have_conflicting_actions(rule1, rule2):
                    conflicts.append({
                        "rule1_id": rule1.id,
                        "rule1_name": rule1.name,
                        "rule2_id": rule2.id,
                        "rule2_name": rule2.name,
                        "conflict_type": "conflicting_actions",
                        "description": "Rules may have conflicting actions for same conditions"
                    })
        
        return conflicts
    
    def _rules_have_conflicting_actions(self, rule1: BusinessRule, 
                                      rule2: BusinessRule) -> bool:
        """Check if two rules have potentially conflicting actions"""
        # Simplified conflict detection
        # In a real implementation, this would be more sophisticated
        
        # Check if rules have overlapping conditions
        rule1_fields = {cond.field for cond in rule1.conditions}
        rule2_fields = {cond.field for cond in rule2.conditions}
        
        if rule1_fields & rule2_fields:  # Overlapping fields
            # Check for conflicting action types
            rule1_actions = {action.action_type for action in rule1.actions}
            rule2_actions = {action.action_type for action in rule2.actions}
            
            conflicting_actions = {
                ("escalate_tension", "de_escalate_tension"),
                ("assign_to_team", "unassign_from_team"),
                ("increase_priority", "decrease_priority")
            }
            
            for action1 in rule1_actions:
                for action2 in rule2_actions:
                    if (action1, action2) in conflicting_actions or (action2, action1) in conflicting_actions:
                        return True
        
        return False
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """Get summary of all rules in the engine"""
        return {
            "total_rules": len(self.rules),
            "rules_by_type": {
                rule_type.value: len([r for r in self.rules.values() if r.rule_type == rule_type])
                for rule_type in RuleType
            },
            "enabled_rules": len([r for r in self.rules.values() if r.enabled]),
            "disabled_rules": len([r for r in self.rules.values() if not r.enabled]),
            "rule_ids": list(self.rules.keys())
        } 