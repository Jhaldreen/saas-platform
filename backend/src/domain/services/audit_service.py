from typing import List, Dict, Any
from uuid import uuid4
from datetime import datetime

from ..entities.audit import Audit
from ..entities.rule import Rule
from ..entities.finding import Finding
from ..exceptions import ValidationError


class AuditService:
    """Domain service for audit business logic"""
    
    def process_csv_data(
        self, 
        audit: Audit, 
        rules: List[Rule], 
        csv_data: List[Dict[str, Any]]
    ) -> List[Finding]:
        """
        Process CSV data and generate findings based on rules
        This is pure business logic
        """
        findings = []
        
        for row in csv_data:
            for rule in rules:
                if not rule.is_active:
                    continue
                
                if not rule.matches_audit_type(audit.audit_type.value):
                    continue
                
                if rule.evaluate(row):
                    # Rule matched - create finding
                    finding = self._create_finding_from_rule(
                        audit_id=audit.id,
                        rule=rule,
                        evidence=row
                    )
                    findings.append(finding)
        
        return findings
    
    def _create_finding_from_rule(
        self,
        audit_id: str,
        rule: Rule,
        evidence: Dict[str, Any]
    ) -> Finding:
        """Create a finding from a matched rule"""
        # Calculate cost impact if possible
        cost_impact = None
        if "cost" in evidence:
            try:
                cost_impact = float(evidence["cost"])
            except (ValueError, TypeError):
                pass
        
        return Finding(
            id=uuid4(),
            audit_id=audit_id,
            rule_id=rule.id,
            title=f"{rule.name} violation",
            description=rule.description or f"Rule {rule.name} was triggered",
            severity=rule.severity.value,
            cost_impact=cost_impact,
            evidence=evidence,
            recommendation=self._generate_recommendation(rule, evidence),
            created_at=datetime.utcnow()
        )
    
    def _generate_recommendation(self, rule: Rule, evidence: Dict[str, Any]) -> str:
        """Generate recommendation based on rule and evidence"""
        # Simple recommendation generator
        # Can be made more sophisticated
        if rule.severity.value == "critical":
            return "Immediate action required to address this issue."
        elif rule.severity.value == "high":
            return "High priority - should be addressed soon."
        elif rule.severity.value == "medium":
            return "Review and plan remediation."
        else:
            return "Monitor and address when convenient."
    
    def calculate_optimization_score(self, findings: List[Finding]) -> int:
        """
        Calculate optimization score (0-100) based on findings
        100 = perfect, 0 = many critical issues
        """
        if not findings:
            return 100
        
        # Weighted severity scoring
        severity_weights = {
            "low": 1,
            "medium": 3,
            "high": 7,
            "critical": 15
        }
        
        total_penalty = sum(
            severity_weights.get(f.severity.lower(), 1) 
            for f in findings
        )
        
        # Calculate score (max penalty = 100)
        max_penalty = 100
        score = max(0, 100 - min(total_penalty, max_penalty))
        
        return score
    
    def calculate_total_cost_impact(self, findings: List[Finding]) -> float:
        """Calculate total cost/revenue impact from findings"""
        return sum(
            f.cost_impact for f in findings 
            if f.cost_impact is not None
        )
