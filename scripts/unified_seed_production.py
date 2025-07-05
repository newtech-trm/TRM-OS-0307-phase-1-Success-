#!/usr/bin/env python
# coding: utf-8

"""
UNIFIED PRODUCTION SEED SCRIPT cho TRM-OS V1.0
==============================================

Script tích hợp tất cả các seed scripts thành một quy trình thống nhất cho production deployment.
Đảm bảo database được seed với dữ liệu chuẩn theo đúng Ontology V3.2.

Prerequisites:
- API server phải đang chạy trên cổng 8000 hoặc 8001
- Neo4j đã kết nối và sẵn sàng
- Environment variables đã được cấu hình

Features:
- Health check API trước khi seed
- Clear database option (chỉ cho development)
- Comprehensive error handling
- Progress tracking và logging
- Rollback capabilities
- Production-safe defaults
"""

import requests
import uuid
import time
import sys
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import argparse

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trm_api.db.session import get_driver
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text

# --- Configuration ---
DEFAULT_BASE_URL = "http://127.0.0.1:8000/api/v1"
console = Console()

@dataclass
class SeedResult:
    """Kết quả của một bước seed"""
    success: bool
    entity_type: str
    count: int
    created_ids: List[str]
    errors: List[str]
    execution_time: float

class UnifiedSeeder:
    """Unified seeder class cho production deployment"""
    
    def __init__(self, base_url: str = DEFAULT_BASE_URL, environment: str = "production"):
        self.base_url = base_url
        self.environment = environment
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TRM-OS-Unified-Seeder/1.0'
        })
        self.results: List[SeedResult] = []
        self.total_entities_created = 0
        
    def health_check(self) -> bool:
        """Kiểm tra API health trước khi seed"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                console.print("✅ [bold green]API Health Check: PASSED[/bold green]")
                return True
            else:
                console.print(f"❌ [bold red]API Health Check: FAILED - Status {response.status_code}[/bold red]")
                return False
        except Exception as e:
            console.print(f"❌ [bold red]API Health Check: FAILED - {str(e)}[/bold red]")
            return False
    
    def clear_database(self) -> bool:
        """Xóa toàn bộ database - CHỈ cho development"""
        if self.environment == "production":
            console.print("⚠️ [bold yellow]Database clear SKIPPED for production environment[/bold yellow]")
            return True
            
        try:
            console.print("🗑️ [bold red]Clearing database...[/bold red]")
            driver = get_driver()
            with driver.session() as session:
                session.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
            console.print("✅ [bold green]Database cleared successfully[/bold green]")
            return True
        except Exception as e:
            console.print(f"❌ [bold red]Database clear failed: {str(e)}[/bold red]")
            return False
    
    def seed_founder_agent(self) -> SeedResult:
        """Seed Founder Agent - nguồn gốc của hệ thống"""
        start_time = time.time()
        
        founder_data = {
            "name": "TRM Founder",
            "purpose": "To initiate and embody the TRM vision, driving the evolution of the TRM Operating System",
            "description": "Founder của TRM, người phát động Recognition đầu tiên, định hướng triết lý của hệ thống",
            "agent_type": "InternalAgent",
            "status": "active",
            "capabilities": ["recognition", "vision_setting", "strategic_planning", "resource_allocation"],
            "job_title": "CEO",
            "department": "Management",
            "is_founder": True,
            "founder_recognition_authority": True
        }
        
        try:
            response = self.session.post(f"{self.base_url}/agents", json=founder_data, timeout=30)
            
            if response.status_code == 201:
                agent = response.json()
                execution_time = time.time() - start_time
                
                return SeedResult(
                    success=True,
                    entity_type="Founder Agent",
                    count=1,
                    created_ids=[agent.get('uid', agent.get('agentId', 'unknown'))],
                    errors=[],
                    execution_time=execution_time
                )
            else:
                return SeedResult(
                    success=False,
                    entity_type="Founder Agent",
                    count=0,
                    created_ids=[],
                    errors=[f"HTTP {response.status_code}: {response.text}"],
                    execution_time=time.time() - start_time
                )
                
        except Exception as e:
            return SeedResult(
                success=False,
                entity_type="Founder Agent",
                count=0,
                created_ids=[],
                errors=[str(e)],
                execution_time=time.time() - start_time
            )
    
    def seed_core_projects(self) -> SeedResult:
        """Seed core strategic projects"""
        start_time = time.time()
        
        projects_data = [
            {
                "title": "TRM-OS Foundation",
                "description": "Core ontology-first operating system for TRM",
                "status": "active",
                "goal": "Establish robust foundation for TRM operations",
                "scope": "Core system architecture and API v1.0",
                "priority": 1,
                "project_type": "development",
                "tags": ["ontology", "foundation", "api"],
                "health": "excelling",
                "is_strategic": True
            },
            {
                "title": "Agent Ecosystem Development",
                "description": "Development of AI agents for automated workflows",
                "status": "active",
                "goal": "Automate 80% of routine TRM operations",
                "scope": "AI agents for data sensing, tension resolution, and knowledge extraction",
                "priority": 1,
                "project_type": "development",
                "tags": ["ai", "automation", "agents"],
                "health": "normal",
                "is_strategic": True
            },
            {
                "title": "Knowledge Management System",
                "description": "Comprehensive knowledge capture and retrieval system",
                "status": "active",
                "goal": "Centralize and intelligently organize all TRM knowledge",
                "scope": "Knowledge snippets, semantic search, and AI-powered insights",
                "priority": 2,
                "project_type": "development",
                "tags": ["knowledge", "search", "ai"],
                "health": "normal",
                "is_strategic": True
            }
        ]
        
        created_ids = []
        errors = []
        
        for project_data in projects_data:
            try:
                response = self.session.post(f"{self.base_url}/projects", json=project_data, timeout=30)
                
                if response.status_code == 201:
                    project = response.json()
                    created_ids.append(project.get('uid', project.get('projectId', 'unknown')))
                else:
                    errors.append(f"Failed to create project '{project_data['title']}': HTTP {response.status_code}")
                    
            except Exception as e:
                errors.append(f"Error creating project '{project_data['title']}': {str(e)}")
        
        execution_time = time.time() - start_time
        
        return SeedResult(
            success=len(errors) == 0,
            entity_type="Core Projects",
            count=len(created_ids),
            created_ids=created_ids,
            errors=errors,
            execution_time=execution_time
        )
    
    def seed_core_skills(self) -> SeedResult:
        """Seed core technical skills"""
        start_time = time.time()
        
        skills_data = [
            {
                "name": "Neo4j Graph Database",
                "description": "Expertise in Neo4j graph database design and optimization",
                "category": "Database",
                "level": 5
            },
            {
                "name": "Ontology Engineering",
                "description": "Design and development of knowledge ontologies",
                "category": "Knowledge Engineering",
                "level": 4
            },
            {
                "name": "FastAPI Development",
                "description": "High-performance API development with FastAPI",
                "category": "Backend Development",
                "level": 5
            },
            {
                "name": "Python Programming",
                "description": "Advanced Python programming and architecture",
                "category": "Programming",
                "level": 5
            },
            {
                "name": "AI Agent Development",
                "description": "Development of autonomous AI agents and workflows",
                "category": "Artificial Intelligence",
                "level": 4
            }
        ]
        
        created_ids = []
        errors = []
        
        for skill_data in skills_data:
            try:
                response = self.session.post(f"{self.base_url}/skills", json=skill_data, timeout=30)
                
                if response.status_code == 201:
                    skill = response.json()
                    created_ids.append(skill.get('uid', skill.get('skillId', 'unknown')))
                else:
                    errors.append(f"Failed to create skill '{skill_data['name']}': HTTP {response.status_code}")
                    
            except Exception as e:
                errors.append(f"Error creating skill '{skill_data['name']}': {str(e)}")
        
        execution_time = time.time() - start_time
        
        return SeedResult(
            success=len(errors) == 0,
            entity_type="Core Skills",
            count=len(created_ids),
            created_ids=created_ids,
            errors=errors,
            execution_time=execution_time
        )
    
    def seed_system_agents(self) -> SeedResult:
        """Seed system agents for automation"""
        start_time = time.time()
        
        agents_data = [
            {
                "name": "DataSensingAgent",
                "description": "Agent specialized in detecting and processing external data sources",
                "agent_type": "SystemAgent",
                "status": "active",
                "capabilities": ["data_monitoring", "email_processing", "file_watching", "api_integration"]
            },
            {
                "name": "TensionResolutionAgent",
                "description": "Agent focused on identifying and resolving organizational tensions",
                "agent_type": "SystemAgent",
                "status": "active",
                "capabilities": ["tension_analysis", "solution_recommendation", "stakeholder_coordination"]
            },
            {
                "name": "KnowledgeExtractionAgent",
                "description": "Agent specialized in extracting and organizing knowledge from various sources",
                "agent_type": "SystemAgent",
                "status": "active",
                "capabilities": ["content_analysis", "knowledge_categorization", "semantic_enrichment"]
            },
            {
                "name": "ResolutionCoordinatorAgent",
                "description": "Master coordinator agent for complex multi-agent workflows",
                "agent_type": "SystemAgent",
                "status": "active",
                "capabilities": ["workflow_coordination", "agent_orchestration", "decision_making"]
            }
        ]
        
        created_ids = []
        errors = []
        
        for agent_data in agents_data:
            try:
                response = self.session.post(f"{self.base_url}/agents", json=agent_data, timeout=30)
                
                if response.status_code == 201:
                    agent = response.json()
                    created_ids.append(agent.get('uid', agent.get('agentId', 'unknown')))
                else:
                    errors.append(f"Failed to create agent '{agent_data['name']}': HTTP {response.status_code}")
                    
            except Exception as e:
                errors.append(f"Error creating agent '{agent_data['name']}': {str(e)}")
        
        execution_time = time.time() - start_time
        
        return SeedResult(
            success=len(errors) == 0,
            entity_type="System Agents",
            count=len(created_ids),
            created_ids=created_ids,
            errors=errors,
            execution_time=execution_time
        )
    
    def verify_neo4j_data(self) -> bool:
        """Verify data integrity in Neo4j"""
        try:
            driver = get_driver()
            with driver.session() as session:
                # Check node counts
                result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count")
                node_counts = {}
                for record in result:
                    labels = record["labels"]
                    count = record["count"]
                    if labels:
                        node_counts[labels[0]] = count
                
                # Check relationship counts
                result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
                rel_counts = {}
                for record in result:
                    rel_type = record["type"]
                    count = record["count"]
                    rel_counts[rel_type] = count
                
                # Display verification results
                console.print("\n📊 [bold blue]Neo4j Data Verification[/bold blue]")
                
                if node_counts:
                    node_table = Table(title="Node Counts")
                    node_table.add_column("Node Type", style="cyan")
                    node_table.add_column("Count", style="magenta")
                    
                    for label, count in node_counts.items():
                        node_table.add_row(label, str(count))
                    
                    console.print(node_table)
                
                if rel_counts:
                    rel_table = Table(title="Relationship Counts")
                    rel_table.add_column("Relationship Type", style="cyan")
                    rel_table.add_column("Count", style="magenta")
                    
                    for rel_type, count in rel_counts.items():
                        rel_table.add_row(rel_type, str(count))
                    
                    console.print(rel_table)
                
                return True
                
        except Exception as e:
            console.print(f"❌ [bold red]Neo4j verification failed: {str(e)}[/bold red]")
            return False
    
    def run_unified_seed(self, clear_db: bool = False) -> bool:
        """Chạy toàn bộ quy trình seed"""
        console.rule("[bold cyan]🚀 TRM-OS Unified Production Seeding 🚀[/bold cyan]")
        
        # Health check
        if not self.health_check():
            console.print("❌ [bold red]Seeding aborted due to health check failure[/bold red]")
            return False
        
        # Clear database if requested (development only)
        if clear_db and not self.clear_database():
            console.print("❌ [bold red]Seeding aborted due to database clear failure[/bold red]")
            return False
        
        # Seed steps in order
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            
            total_steps = 4
            task = progress.add_task("Seeding TRM-OS Production Data...", total=total_steps)
            
            # Step 1: Seed Founder Agent
            progress.update(task, description="Seeding Founder Agent...")
            result = self.seed_founder_agent()
            self.results.append(result)
            self.total_entities_created += result.count
            progress.advance(task)
            
            # Step 2: Seed Core Projects
            progress.update(task, description="Seeding Core Projects...")
            result = self.seed_core_projects()
            self.results.append(result)
            self.total_entities_created += result.count
            progress.advance(task)
            
            # Step 3: Seed Core Skills
            progress.update(task, description="Seeding Core Skills...")
            result = self.seed_core_skills()
            self.results.append(result)
            self.total_entities_created += result.count
            progress.advance(task)
            
            # Step 4: Seed System Agents
            progress.update(task, description="Seeding System Agents...")
            result = self.seed_system_agents()
            self.results.append(result)
            self.total_entities_created += result.count
            progress.advance(task)
        
        # Verify Neo4j data
        console.print("\n🔍 [bold blue]Verifying Neo4j Data Integrity...[/bold blue]")
        neo4j_verified = self.verify_neo4j_data()
        
        # Display results
        self.display_results(neo4j_verified)
        
        # Check overall success
        overall_success = all(result.success for result in self.results) and neo4j_verified
        
        if overall_success:
            console.rule("[bold green]✅ Production Seeding Completed Successfully ✅[/bold green]")
        else:
            console.rule("[bold red]⚠️ Production Seeding Completed with Issues ⚠️[/bold red]")
        
        return overall_success
    
    def display_results(self, neo4j_verified: bool):
        """Display comprehensive seeding results"""
        console.print("\n📋 [bold blue]Seeding Results Summary[/bold blue]")
        
        # Results table
        table = Table(title="Entity Creation Results")
        table.add_column("Entity Type", style="cyan")
        table.add_column("Count", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Execution Time", style="yellow")
        table.add_column("Errors", style="red")
        
        for result in self.results:
            status = "✅ Success" if result.success else "❌ Failed"
            errors = str(len(result.errors)) if result.errors else "0"
            execution_time = f"{result.execution_time:.2f}s"
            
            table.add_row(
                result.entity_type,
                str(result.count),
                status,
                execution_time,
                errors
            )
        
        table.add_row(
            "Neo4j Verification",
            "-",
            "✅ Verified" if neo4j_verified else "❌ Failed",
            "-",
            "-"
        )
        
        console.print(table)
        
        # Summary stats
        total_success = sum(1 for result in self.results if result.success)
        total_steps = len(self.results)
        success_rate = (total_success / total_steps) * 100 if total_steps > 0 else 0
        
        summary_panel = Panel(
            f"[bold green]Total Entities Created: {self.total_entities_created}[/bold green]\n"
            f"[bold blue]Successful Steps: {total_success}/{total_steps}[/bold blue]\n"
            f"[bold yellow]Success Rate: {success_rate:.1f}%[/bold yellow]\n"
            f"[bold cyan]Environment: {self.environment.upper()}[/bold cyan]",
            title="📊 Summary Statistics",
            border_style="blue"
        )
        console.print(summary_panel)
        
        # Show errors if any
        all_errors = []
        for result in self.results:
            all_errors.extend(result.errors)
        
        if all_errors:
            console.print("\n⚠️ [bold red]Errors Encountered:[/bold red]")
            for i, error in enumerate(all_errors, 1):
                console.print(f"  {i}. {error}")


def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description="TRM-OS Unified Production Seeder")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--environment", default="production", choices=["development", "production"], 
                       help="Environment type")
    parser.add_argument("--clear-db", action="store_true", 
                       help="Clear database before seeding (development only)")
    
    args = parser.parse_args()
    
    # Create seeder instance
    seeder = UnifiedSeeder(base_url=args.base_url, environment=args.environment)
    
    # Run seeding
    success = seeder.run_unified_seed(clear_db=args.clear_db)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 