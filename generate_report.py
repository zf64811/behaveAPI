#!/usr/bin/env python3
"""Generate enhanced HTML report from behave JSON output."""

import json
import os
from datetime import datetime
from pathlib import Path


def generate_html_report(json_file="reports/behave-report.json",
                         output_file="reports/enhanced-report.html"):
    """Generate an enhanced HTML report from behave JSON output."""

    # Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"JSON report file not found: {json_file}")
        return

    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Calculate statistics
    total_features = len(data)
    total_scenarios = sum(len(feature.get('elements', [])) for feature in data)
    passed_scenarios = 0
    failed_scenarios = 0
    total_steps = 0
    passed_steps = 0
    failed_steps = 0

    for feature in data:
        for scenario in feature.get('elements', []):
            scenario_passed = True
            for step in scenario.get('steps', []):
                total_steps += 1
                if step.get('result', {}).get('status') == 'passed':
                    passed_steps += 1
                elif step.get('result', {}).get('status') == 'failed':
                    failed_steps += 1
                    scenario_passed = False

            if scenario_passed:
                passed_scenarios += 1
            else:
                failed_scenarios += 1

    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BehaveAPI Test Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }}
        .passed {{ color: #22c55e; }}
        .failed {{ color: #ef4444; }}
        .feature {{
            background: white;
            margin-bottom: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .feature-header {{
            padding: 1rem;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            cursor: pointer;
        }}
        .feature-header:hover {{
            background: #e9ecef;
        }}
        .scenario {{
            padding: 1rem;
            border-bottom: 1px solid #e9ecef;
        }}
        .scenario:last-child {{
            border-bottom: none;
        }}
        .step {{
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
        }}
        .step.passed {{
            border-left: 4px solid #22c55e;
        }}
        .step.failed {{
            border-left: 4px solid #ef4444;
        }}
        .timestamp {{
            color: #6b7280;
            font-size: 0.875rem;
            text-align: center;
            margin-top: 2rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BehaveAPI Test Report</h1>
        <p>Automated API Testing Results</p>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>Features</h3>
                <div class="stat-number">{total_features}</div>
            </div>
            <div class="stat-card">
                <h3>Scenarios</h3>
                <div class="stat-number">{total_scenarios}</div>
                <div><span class="passed">{passed_scenarios} passed</span> | <span class="failed">{failed_scenarios} failed</span></div>
            </div>
            <div class="stat-card">
                <h3>Steps</h3>
                <div class="stat-number">{total_steps}</div>
                <div><span class="passed">{passed_steps} passed</span> | <span class="failed">{failed_steps} failed</span></div>
            </div>
            <div class="stat-card">
                <h3>Success Rate</h3>
                <div class="stat-number">{(passed_steps/total_steps*100 if total_steps > 0 else 0):.1f}%</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
"""

    # Add feature details
    for feature in data:
        feature_name = feature.get('name', 'Unnamed Feature')
        feature_status = 'passed'

        html_content += f"""
        <div class="feature">
            <div class="feature-header">
                <h3>{feature_name}</h3>
                <p>{feature.get('description', '')}</p>
            </div>
"""

        for scenario in feature.get('elements', []):
            scenario_name = scenario.get('name', 'Unnamed Scenario')
            scenario_type = scenario.get('type', 'scenario')

            html_content += f"""
            <div class="scenario">
                <h4>{scenario_type.title()}: {scenario_name}</h4>
"""

            for step in scenario.get('steps', []):
                step_name = step.get('name', '')
                step_keyword = step.get('keyword', '')
                step_status = step.get('result', {}).get('status', 'skipped')

                html_content += f"""
                <div class="step {step_status}">
                    {step_keyword} {step_name}
                </div>
"""

            html_content += """
            </div>
"""

        html_content += """
        </div>
"""

    html_content += f"""
        <div class="timestamp">
            Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""

    # Write HTML file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"Enhanced HTML report generated: {output_file}")


if __name__ == "__main__":
    generate_html_report()
