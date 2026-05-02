"""
Professional Test Reporter - Generates HTML, JSON & Allure-compatible reports.
Perfect for CI/CD dashboards and stakeholder updates.
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict, field
import jinja2

from utils.logger import logger


@dataclass
class TestStep:
    """Represents a single test step execution."""
    name: str
    status: str  # 'passed', 'failed', 'skipped'
    duration_ms: float
    error: Optional[str] = None
    screenshot: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TestResult:
    """Complete test execution result."""
    test_name: str
    status: str
    total_duration_ms: float
    steps: List[TestStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_step(self, step: TestStep):
        self.steps.append(step)
        if step.status == 'failed':
            self.status = 'failed'


class ReportGenerator:
    """Generate professional test reports in multiple formats."""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[TestResult] = []
    
    def record_test(self, result: TestResult):
        """Add a test result to the report."""
        self.results.append(result)
        logger.info(f"Recorded test: {result.test_name} → {result.status}")
    
    def generate_summary(self) -> Dict:
        """Generate execution summary statistics."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == 'passed')
        failed = sum(1 for r in self.results if r.status == 'failed')
        skipped = sum(1 for r in self.results if r.status == 'skipped')
        
        avg_duration = sum(r.total_duration_ms for r in self.results) / max(total, 1)
        
        return {
            "executed_at": datetime.now().isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": f"{(passed/total*100):.1f}%" if total else "N/A",
            "avg_duration_ms": f"{avg_duration:.0f}",
            "total_duration_ms": sum(r.total_duration_ms for r in self.results)
        }
    
    def save_json(self, filename: str = "report.json") -> Path:
        """Save results as JSON (machine-readable)."""
        filepath = self.output_dir / filename
        report = {
            "summary": self.generate_summary(),
            "results": [asdict(r) for r in self.results]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON report saved: {filepath}")
        return filepath
    
    def save_html(self, filename: str = "report.html") -> Path:
        """Generate beautiful HTML report with embedded CSS."""
        filepath = self.output_dir / filename
        summary = self.generate_summary()
        
        # Inline CSS for portability
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Automation Report - {{ summary.executed_at }}</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                       margin: 40px; background: #f8f9fa; color: #333; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                         color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                          gap: 15px; margin-bottom: 30px; }
                .card { background: white; padding: 15px; border-radius: 6px; 
                       box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
                .card h3 { margin: 0 0 5px 0; font-size: 24px; color: #667eea; }
                .card p { margin: 0; color: #666; font-size: 14px; }
                .test { background: white; margin: 10px 0; padding: 15px; 
                       border-radius: 6px; border-left: 4px solid #667eea; }
                .test.failed { border-left-color: #e74c3c; }
                .test.passed { border-left-color: #27ae60; }
                .step { margin: 8px 0 8px 20px; padding: 8px; background: #f8f9fa; 
                       border-radius: 4px; font-size: 14px; }
                .step.failed { background: #ffeaea; border-left: 3px solid #e74c3c; }
                .badge { display: inline-block; padding: 3px 8px; border-radius: 12px; 
                        font-size: 12px; font-weight: 600; text-transform: uppercase; }
                .badge.passed { background: #d4edda; color: #155724; }
                .badge.failed { background: #f8d7da; color: #721c24; }
                .badge.skipped { background: #fff3cd; color: #856404; }
                .error { color: #e74c3c; font-family: monospace; font-size: 13px; 
                        background: #ffeaea; padding: 8px; border-radius: 4px; margin-top: 5px; }
                .screenshot { margin-top: 8px; }
                .screenshot img { max-width: 100%; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Automation Test Report</h1>
                <p>Generated: {{ summary.executed_at }}</p>
            </div>
            
            <div class="summary">
                <div class="card"><h3>{{ summary.total_tests }}</h3><p>Total Tests</p></div>
                <div class="card"><h3 style="color:#27ae60">{{ summary.passed }}</h3><p>Passed</p></div>
                <div class="card"><h3 style="color:#e74c3c">{{ summary.failed }}</h3><p>Failed</p></div>
                <div class="card"><h3>{{ summary.pass_rate }}</h3><p>Pass Rate</p></div>
            </div>
            
            <h2>Test Results</h2>
            {% for result in results %}
            <div class="test {{ result.status }}">
                <strong>{{ loop.index }}. {{ result.test_name }}</strong>
                <span class="badge {{ result.status }}">{{ result.status }}</span>
                <span style="float:right; color:#666">{{ "%.1f"|format(result.total_duration_ms/1000) }}s</span>
                
                {% for step in result.steps %}
                <div class="step {% if step.status=='failed' %}failed{% endif %}">
                    <strong>{{ step.name }}</strong> 
                    <span class="badge {{ step.status }}">{{ step.status }}</span>
                    {% if step.error %}
                    <div class="error">❌ {{ step.error }}</div>
                    {% endif %}
                    {% if step.screenshot %}
                    <div class="screenshot">
                        <a href="{{ step.screenshot }}" target="_blank">📸 View Screenshot</a>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endfor %}
            
            <footer style="margin-top:40px; text-align:center; color:#666; font-size:14px;">
                Generated with ❤️ by Automation Framework v1.0
            </footer>
        </body>
        </html>
        """
        
        env = jinja2.Environment()
        template = env.from_string(html_template)
        html_content = template.render(summary=summary, results=self.results)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved: {filepath}")
        return filepath
    
    def save_allure_results(self):
        """Generate Allure-compatible result files for CI integration."""
        allure_dir = self.output_dir / "allure-results"
        allure_dir.mkdir(exist_ok=True)
        
        for i, result in enumerate(self.results):
            # Allure result JSON structure
            allure_result = {
                "name": result.test_name,
                "status": result.status.upper(),
                "start": int(datetime.fromisoformat(result.started_at).timestamp() * 1000),
                "stop": int((datetime.fromisoformat(result.started_at).timestamp() + result.total_duration_ms/1000) * 1000),
                "steps": [
                    {
                        "name": step.name,
                        "status": step.status.upper(),
                        "start": int(datetime.fromisoformat(step.timestamp).timestamp() * 1000),
                        "parameters": []
                    }
                    for step in result.steps
                ],
                "labels": [
                    {"name": "suite", "value": "RegistrationFlow"},
                    {"name": "framework", "value": "selenium-pytest"},
                    {"name": "language", "value": "python"}
                ]
            }
            
            if result.metadata:
                allure_result["parameters"] = [
                    {"name": k, "value": str(v)} for k, v in result.metadata.items()
                ]
            
            filepath = allure_dir / f"{i+1}-result.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(allure_result, f, indent=2)
        
        # Allure environment properties
        env_file = allure_dir / "environment.properties"
        with open(env_file, 'w') as f:
            f.write(f"Browser=Chrome\n")
            f.write(f"Framework=Selenium+Pytest\n")
            f.write(f"Report.Generated={datetime.now().isoformat()}\n")
        
        logger.info(f"Allure results saved to: {allure_dir}")
        return allure_dir