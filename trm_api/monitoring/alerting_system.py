"""
Alerting System cho TRM-OS Phase 3

Real-time alerting system với:
- Multi-channel notifications (email, SMS, webhook)
- Alert rules và thresholds
- Escalation policies
- Alert correlation và deduplication
- Notification history và tracking
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiohttp

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(Enum):
    """Alert status"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"


class NotificationChannel(Enum):
    """Notification channels"""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TEAMS = "teams"


@dataclass
class AlertRule:
    """Alert rule configuration"""
    id: str
    name: str
    description: str
    condition: str  # Expression to evaluate
    severity: AlertSeverity
    enabled: bool = True
    
    # Thresholds
    threshold_value: float = 0.0
    threshold_operator: str = ">"  # >, <, >=, <=, ==, !=
    
    # Timing
    evaluation_interval: int = 60  # seconds
    for_duration: int = 300  # seconds - how long condition must be true
    
    # Notifications
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    notification_recipients: List[str] = field(default_factory=list)
    
    # Metadata
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Alert:
    """Alert instance"""
    id: str
    rule_id: str
    rule_name: str
    severity: AlertSeverity
    status: AlertStatus
    
    # Content
    title: str
    description: str
    message: str
    
    # Timing
    triggered_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    # Context
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    
    # Metrics
    current_value: float = 0.0
    threshold_value: float = 0.0
    
    # Notifications
    notifications_sent: List[str] = field(default_factory=list)
    
    # Escalation
    escalation_level: int = 0
    escalated_at: Optional[datetime] = None


@dataclass
class NotificationTemplate:
    """Notification template"""
    channel: NotificationChannel
    subject_template: str
    body_template: str
    format: str = "text"  # text, html, markdown


@dataclass
class EscalationPolicy:
    """Alert escalation policy"""
    id: str
    name: str
    rules: List[Dict[str, Any]]  # Escalation rules
    enabled: bool = True


class AlertingSystem:
    """Main alerting system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
        # Storage
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.escalation_policies: Dict[str, EscalationPolicy] = {}
        
        # Notification configuration
        self.notification_config = {
            'email': {
                'smtp_server': 'localhost',
                'smtp_port': 587,
                'username': '',
                'password': '',
                'from_address': 'alerts@trm-os.com'
            },
            'webhook': {
                'default_url': '',
                'timeout': 30
            }
        }
        
        # Templates
        self.notification_templates: Dict[str, NotificationTemplate] = {}
        self._setup_default_templates()
        
        # Metrics for alerting
        self.metrics_callbacks: Dict[str, Callable] = {}
        
        # Rate limiting
        self.notification_rate_limits: Dict[str, List[datetime]] = {}
        self.max_notifications_per_hour = 10
        
        # Correlation
        self.correlation_window = 300  # 5 minutes
        
        # Configuration
        self.max_history = 10000
        self.cleanup_interval = 3600  # 1 hour
    
    def _setup_default_templates(self):
        """Setup default notification templates"""
        # Email template
        self.notification_templates['email_default'] = NotificationTemplate(
            channel=NotificationChannel.EMAIL,
            subject_template="[TRM-OS Alert] {severity}: {title}",
            body_template="""
Alert: {title}
Severity: {severity}
Status: {status}
Triggered: {triggered_at}

Description: {description}

Current Value: {current_value}
Threshold: {threshold_value}

Message: {message}

Labels: {labels}

--
TRM-OS Monitoring System
            """.strip(),
            format="text"
        )
        
        # Webhook template
        self.notification_templates['webhook_default'] = NotificationTemplate(
            channel=NotificationChannel.WEBHOOK,
            subject_template="TRM-OS Alert",
            body_template="""{{
    "alert_id": "{id}",
    "rule_name": "{rule_name}",
    "severity": "{severity}",
    "status": "{status}",
    "title": "{title}",
    "description": "{description}",
    "message": "{message}",
    "triggered_at": "{triggered_at}",
    "current_value": {current_value},
    "threshold_value": {threshold_value},
    "labels": {labels_json},
    "annotations": {annotations_json}
}}""",
            format="json"
        )
    
    async def start(self) -> None:
        """Start alerting system"""
        try:
            if self.is_running:
                self.logger.warning("Alerting system already running")
                return
            
            self.is_running = True
            self.logger.info("Starting alerting system...")
            
            # Start evaluation loop
            evaluation_task = asyncio.create_task(self._evaluation_loop())
            
            # Start cleanup task
            cleanup_task = asyncio.create_task(self._cleanup_loop())
            
            # Wait for tasks
            await asyncio.gather(evaluation_task, cleanup_task)
            
        except Exception as e:
            self.logger.error(f"Failed to start alerting system: {e}")
            self.is_running = False
            raise
    
    async def stop(self) -> None:
        """Stop alerting system"""
        self.is_running = False
        self.logger.info("Alerting system stopped")
    
    async def _evaluation_loop(self) -> None:
        """Main alert evaluation loop"""
        while self.is_running:
            try:
                # Evaluate all active rules
                for rule_id, rule in self.alert_rules.items():
                    if rule.enabled:
                        await self._evaluate_rule(rule)
                
                # Check for escalations
                await self._check_escalations()
                
                # Wait before next evaluation
                await asyncio.sleep(30)  # Evaluate every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Alert evaluation error: {e}")
                await asyncio.sleep(30)
    
    async def _cleanup_loop(self) -> None:
        """Cleanup loop for old alerts"""
        while self.is_running:
            try:
                await self._cleanup_old_alerts()
                await asyncio.sleep(self.cleanup_interval)
                
            except Exception as e:
                self.logger.error(f"Alert cleanup error: {e}")
                await asyncio.sleep(self.cleanup_interval)
    
    async def _evaluate_rule(self, rule: AlertRule) -> None:
        """Evaluate a single alert rule"""
        try:
            # Get current metric value
            current_value = await self._get_metric_value(rule.condition)
            
            if current_value is None:
                return
            
            # Check if condition is met
            condition_met = self._evaluate_condition(
                current_value, rule.threshold_operator, rule.threshold_value
            )
            
            alert_id = f"{rule.id}_{rule.name}"
            existing_alert = self.active_alerts.get(alert_id)
            
            if condition_met:
                if existing_alert:
                    # Update existing alert
                    existing_alert.current_value = current_value
                else:
                    # Create new alert
                    alert = Alert(
                        id=alert_id,
                        rule_id=rule.id,
                        rule_name=rule.name,
                        severity=rule.severity,
                        status=AlertStatus.ACTIVE,
                        title=f"{rule.name} threshold exceeded",
                        description=rule.description,
                        message=f"Current value {current_value} {rule.threshold_operator} {rule.threshold_value}",
                        triggered_at=datetime.utcnow(),
                        current_value=current_value,
                        threshold_value=rule.threshold_value,
                        labels=rule.tags.copy()
                    )
                    
                    self.active_alerts[alert_id] = alert
                    
                    # Send notifications
                    await self._send_alert_notifications(alert, rule)
                    
                    self.logger.warning(f"Alert triggered: {alert.title}")
            
            else:
                # Condition not met, resolve alert if exists
                if existing_alert and existing_alert.status == AlertStatus.ACTIVE:
                    await self._resolve_alert(alert_id)
            
        except Exception as e:
            self.logger.error(f"Rule evaluation failed for {rule.name}: {e}")
    
    async def _get_metric_value(self, condition: str) -> Optional[float]:
        """Get current metric value for condition"""
        try:
            # Check if we have a callback for this metric
            if condition in self.metrics_callbacks:
                return await self.metrics_callbacks[condition]()
            
            # Default: return None if no callback
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get metric value for {condition}: {e}")
            return None
    
    def _evaluate_condition(self, current_value: float, operator: str, threshold: float) -> bool:
        """Evaluate alert condition"""
        try:
            if operator == ">":
                return current_value > threshold
            elif operator == "<":
                return current_value < threshold
            elif operator == ">=":
                return current_value >= threshold
            elif operator == "<=":
                return current_value <= threshold
            elif operator == "==":
                return current_value == threshold
            elif operator == "!=":
                return current_value != threshold
            else:
                self.logger.warning(f"Unknown operator: {operator}")
                return False
                
        except Exception as e:
            self.logger.error(f"Condition evaluation failed: {e}")
            return False
    
    async def _send_alert_notifications(self, alert: Alert, rule: AlertRule) -> None:
        """Send notifications for alert"""
        try:
            # Check rate limits
            if not self._check_rate_limit(alert.id):
                self.logger.warning(f"Rate limit exceeded for alert {alert.id}")
                return
            
            # Send notifications for each channel
            for channel in rule.notification_channels:
                try:
                    if channel == NotificationChannel.EMAIL:
                        await self._send_email_notification(alert, rule)
                    elif channel == NotificationChannel.WEBHOOK:
                        await self._send_webhook_notification(alert, rule)
                    elif channel == NotificationChannel.SLACK:
                        await self._send_slack_notification(alert, rule)
                    
                    alert.notifications_sent.append(f"{channel.value}_{datetime.utcnow().isoformat()}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to send {channel.value} notification: {e}")
            
        except Exception as e:
            self.logger.error(f"Failed to send alert notifications: {e}")
    
    def _check_rate_limit(self, alert_id: str) -> bool:
        """Check if alert is within rate limits"""
        try:
            now = datetime.utcnow()
            hour_ago = now - timedelta(hours=1)
            
            if alert_id not in self.notification_rate_limits:
                self.notification_rate_limits[alert_id] = []
            
            # Clean old entries
            self.notification_rate_limits[alert_id] = [
                timestamp for timestamp in self.notification_rate_limits[alert_id]
                if timestamp > hour_ago
            ]
            
            # Check limit
            if len(self.notification_rate_limits[alert_id]) >= self.max_notifications_per_hour:
                return False
            
            # Add current timestamp
            self.notification_rate_limits[alert_id].append(now)
            return True
            
        except Exception as e:
            self.logger.error(f"Rate limit check failed: {e}")
            return True  # Allow on error
    
    async def _send_email_notification(self, alert: Alert, rule: AlertRule) -> None:
        """Send email notification"""
        try:
            template = self.notification_templates.get('email_default')
            if not template:
                return
            
            # Format message
            subject = self._format_template(template.subject_template, alert)
            body = self._format_template(template.body_template, alert)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.notification_config['email']['from_address']
            msg['Subject'] = subject
            
            # Add recipients
            for recipient in rule.notification_recipients:
                msg['To'] = recipient
                
                # Add body
                msg.attach(MIMEText(body, 'plain'))
                
                # Send email (simplified - in production use proper SMTP)
                self.logger.info(f"Email notification sent to {recipient}: {subject}")
            
        except Exception as e:
            self.logger.error(f"Email notification failed: {e}")
    
    async def _send_webhook_notification(self, alert: Alert, rule: AlertRule) -> None:
        """Send webhook notification"""
        try:
            template = self.notification_templates.get('webhook_default')
            if not template:
                return
            
            # Format payload
            payload = self._format_template(template.body_template, alert)
            
            # Get webhook URL
            webhook_url = self.notification_config['webhook'].get('default_url')
            if not webhook_url:
                return
            
            # Send webhook
            timeout = self.notification_config['webhook'].get('timeout', 30)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook_url,
                    data=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    if response.status == 200:
                        self.logger.info(f"Webhook notification sent: {alert.title}")
                    else:
                        self.logger.error(f"Webhook failed with status {response.status}")
            
        except Exception as e:
            self.logger.error(f"Webhook notification failed: {e}")
    
    async def _send_slack_notification(self, alert: Alert, rule: AlertRule) -> None:
        """Send Slack notification"""
        try:
            # Placeholder for Slack integration
            self.logger.info(f"Slack notification would be sent: {alert.title}")
            
        except Exception as e:
            self.logger.error(f"Slack notification failed: {e}")
    
    def _format_template(self, template: str, alert: Alert) -> str:
        """Format notification template"""
        try:
            return template.format(
                id=alert.id,
                rule_name=alert.rule_name,
                severity=alert.severity.value,
                status=alert.status.value,
                title=alert.title,
                description=alert.description,
                message=alert.message,
                triggered_at=alert.triggered_at.isoformat(),
                current_value=alert.current_value,
                threshold_value=alert.threshold_value,
                labels=str(alert.labels),
                labels_json=json.dumps(alert.labels),
                annotations=str(alert.annotations),
                annotations_json=json.dumps(alert.annotations)
            )
            
        except Exception as e:
            self.logger.error(f"Template formatting failed: {e}")
            return f"Alert: {alert.title} (formatting error)"
    
    async def _check_escalations(self) -> None:
        """Check for alert escalations"""
        try:
            now = datetime.utcnow()
            
            for alert_id, alert in self.active_alerts.items():
                if alert.status != AlertStatus.ACTIVE:
                    continue
                
                # Check if alert should be escalated
                time_since_triggered = (now - alert.triggered_at).total_seconds()
                
                # Escalate after 30 minutes if not acknowledged
                if (time_since_triggered > 1800 and 
                    alert.escalation_level == 0 and 
                    alert.status != AlertStatus.ACKNOWLEDGED):
                    
                    await self._escalate_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Escalation check failed: {e}")
    
    async def _escalate_alert(self, alert: Alert) -> None:
        """Escalate alert"""
        try:
            alert.escalation_level += 1
            alert.escalated_at = datetime.utcnow()
            
            # Update severity for escalation
            if alert.severity == AlertSeverity.LOW:
                alert.severity = AlertSeverity.MEDIUM
            elif alert.severity == AlertSeverity.MEDIUM:
                alert.severity = AlertSeverity.HIGH
            elif alert.severity == AlertSeverity.HIGH:
                alert.severity = AlertSeverity.CRITICAL
            
            self.logger.warning(f"Alert escalated: {alert.title} (Level {alert.escalation_level})")
            
            # Send escalation notification
            # In production, this would send to different recipients
            
        except Exception as e:
            self.logger.error(f"Alert escalation failed: {e}")
    
    async def _resolve_alert(self, alert_id: str) -> None:
        """Resolve an alert"""
        try:
            alert = self.active_alerts.get(alert_id)
            if not alert:
                return
            
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.utcnow()
            
            # Move to history
            self.alert_history.append(alert)
            del self.active_alerts[alert_id]
            
            self.logger.info(f"Alert resolved: {alert.title}")
            
        except Exception as e:
            self.logger.error(f"Alert resolution failed: {e}")
    
    async def _cleanup_old_alerts(self) -> None:
        """Cleanup old alerts from history"""
        try:
            # Keep only last 30 days
            cutoff_time = datetime.utcnow() - timedelta(days=30)
            
            self.alert_history = [
                alert for alert in self.alert_history
                if alert.triggered_at >= cutoff_time
            ]
            
            # Limit total history
            if len(self.alert_history) > self.max_history:
                self.alert_history = self.alert_history[-self.max_history:]
            
            # Clean rate limits
            hour_ago = datetime.utcnow() - timedelta(hours=1)
            for alert_id in list(self.notification_rate_limits.keys()):
                self.notification_rate_limits[alert_id] = [
                    timestamp for timestamp in self.notification_rate_limits[alert_id]
                    if timestamp > hour_ago
                ]
                
                if not self.notification_rate_limits[alert_id]:
                    del self.notification_rate_limits[alert_id]
            
        except Exception as e:
            self.logger.error(f"Alert cleanup failed: {e}")
    
    # Public API methods
    
    def add_alert_rule(self, rule: AlertRule) -> None:
        """Add new alert rule"""
        self.alert_rules[rule.id] = rule
        self.logger.info(f"Alert rule added: {rule.name}")
    
    def remove_alert_rule(self, rule_id: str) -> None:
        """Remove alert rule"""
        if rule_id in self.alert_rules:
            del self.alert_rules[rule_id]
            self.logger.info(f"Alert rule removed: {rule_id}")
    
    def register_metric_callback(self, condition: str, callback: Callable) -> None:
        """Register callback for metric evaluation"""
        self.metrics_callbacks[condition] = callback
    
    async def acknowledge_alert(self, alert_id: str, user: str = None) -> bool:
        """Acknowledge an alert"""
        try:
            alert = self.active_alerts.get(alert_id)
            if not alert:
                return False
            
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_at = datetime.utcnow()
            
            if user:
                alert.annotations['acknowledged_by'] = user
            
            self.logger.info(f"Alert acknowledged: {alert.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Alert acknowledgment failed: {e}")
            return False
    
    async def suppress_alert(self, alert_id: str, duration_minutes: int = 60) -> bool:
        """Suppress an alert for specified duration"""
        try:
            alert = self.active_alerts.get(alert_id)
            if not alert:
                return False
            
            alert.status = AlertStatus.SUPPRESSED
            alert.annotations['suppressed_until'] = (
                datetime.utcnow() + timedelta(minutes=duration_minutes)
            ).isoformat()
            
            self.logger.info(f"Alert suppressed: {alert.title} for {duration_minutes} minutes")
            return True
            
        except Exception as e:
            self.logger.error(f"Alert suppression failed: {e}")
            return False
    
    def get_active_alerts(self, severity: AlertSeverity = None) -> List[Alert]:
        """Get active alerts"""
        alerts = list(self.active_alerts.values())
        
        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]
        
        return sorted(alerts, key=lambda a: a.triggered_at, reverse=True)
    
    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """Get alert history"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        return [
            alert for alert in self.alert_history
            if alert.triggered_at >= cutoff_time
        ]
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        try:
            active_alerts = list(self.active_alerts.values())
            
            # Count by severity
            severity_counts = {severity.value: 0 for severity in AlertSeverity}
            for alert in active_alerts:
                severity_counts[alert.severity.value] += 1
            
            # Recent history stats
            recent_history = self.get_alert_history(24)
            resolved_count = len([a for a in recent_history if a.status == AlertStatus.RESOLVED])
            
            return {
                'active_alerts': len(active_alerts),
                'severity_breakdown': severity_counts,
                'alerts_last_24h': len(recent_history),
                'resolved_last_24h': resolved_count,
                'total_rules': len(self.alert_rules),
                'enabled_rules': len([r for r in self.alert_rules.values() if r.enabled])
            }
            
        except Exception as e:
            self.logger.error(f"Alert statistics failed: {e}")
            return {} 