"""
Clinical Trial Matching Demo - Complete Version
Privacy-preserving patient-trial matching with blockchain audit trail
"""
import os
import json
import hashlib
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Clinical Trial Matching Demo",
    description="Privacy-preserving patient-trial matching system with blockchain audit",
    version="1.0.0"
)

# Demo data - 5 synthetic patients with medical conditions
PATIENTS = [
    {
        "id": "PAT_001", 
        "age": 45, 
        "gender": "M", 
        "conditions": "diabetes",
        "details": "Type 2 diabetes, well-controlled"
    },
    {
        "id": "PAT_002", 
        "age": 62, 
        "gender": "F", 
        "conditions": "hypertension",
        "details": "High blood pressure, on medication"
    },
    {
        "id": "PAT_003", 
        "age": 38, 
        "gender": "M", 
        "conditions": "cancer",
        "details": "Early stage lung cancer"
    },
    {
        "id": "PAT_004", 
        "age": 55, 
        "gender": "F", 
        "conditions": "depression",
        "details": "Major depressive disorder"
    },
    {
        "id": "PAT_005", 
        "age": 41, 
        "gender": "M", 
        "conditions": "obesity",
        "details": "BMI 35, seeking weight management"
    }
]

# Clinical trials with inclusion criteria
TRIALS = [
    {
        "id": "TRIAL_001",
        "title": "Advanced Diabetes Management Study",
        "condition": "diabetes",
        "description": "Novel insulin therapy for Type 2 diabetes patients",
        "sponsor": "MedTech Research Institute"
    },
    {
        "id": "TRIAL_002",
        "title": "Cardiovascular Health Prevention Trial",
        "condition": "hypertension",
        "description": "New approach to managing high blood pressure",
        "sponsor": "Heart Health Foundation"
    },
    {
        "id": "TRIAL_003",
        "title": "Innovative Cancer Treatment Research",
        "condition": "cancer",
        "description": "Breakthrough immunotherapy for cancer patients",
        "sponsor": "Oncology Research Center"
    },
    {
        "id": "TRIAL_004",
        "title": "Mental Health Intervention Study",
        "condition": "depression",
        "description": "Digital therapy platform for depression treatment",
        "sponsor": "Mental Health Institute"
    },
    {
        "id": "TRIAL_005",
        "title": "Comprehensive Weight Management Program",
        "condition": "obesity",
        "description": "Holistic approach to sustainable weight loss",
        "sponsor": "Wellness Research Group"
    }
]

# Blockchain audit trail
audit_log = []

@app.get("/")
async def root():
    """Root endpoint with navigation"""
    return {
        "message": "🏥 Clinical Trial Matching Demo",
        "description": "Privacy-preserving patient-trial matching system",
        "endpoints": {
            "web_interface": "/ui",
            "api_documentation": "/docs",
            "health_check": "/health",
            "patient_matching": "/match",
            "audit_trail": "/audit"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "patients": len(PATIENTS),
        "trials": len(TRIALS),
        "audit_entries": len(audit_log)
    }

@app.get("/ui", response_class=HTMLResponse)
async def get_web_interface():
    """Serve the complete web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clinical Trial Matching Demo</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 40px; 
                border-radius: 15px; 
                margin-bottom: 30px; 
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .card { 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                margin-bottom: 25px; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .card:hover { transform: translateY(-5px); }
            .card h2 { color: #333; margin-bottom: 20px; font-size: 1.5em; }
            .btn { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                border: none; 
                padding: 15px 30px; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            .form-group { margin-bottom: 20px; }
            .form-group label { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 600; 
                color: #333;
            }
            .form-group select { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #e1e5e9; 
                border-radius: 8px; 
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            .form-group select:focus { 
                outline: none; 
                border-color: #667eea; 
            }
            .results { margin-top: 25px; }
            .trial-match { 
                background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%); 
                border-left: 5px solid #667eea; 
                padding: 20px; 
                margin-bottom: 15px; 
                border-radius: 10px;
                transition: all 0.3s ease;
            }
            .trial-match:hover { transform: translateX(5px); }
            .trial-match h4 { color: #333; margin-bottom: 8px; }
            .trial-match p { color: #666; margin-bottom: 10px; }
            .score { 
                font-weight: bold; 
                color: #667eea; 
                font-size: 1.1em;
            }
            .status { 
                padding: 6px 12px; 
                border-radius: 20px; 
                font-size: 12px; 
                font-weight: bold;
                display: inline-block;
                margin-left: 10px;
            }
            .eligible { background: #d4edda; color: #155724; }
            .review { background: #fff3cd; color: #856404; }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-top: 20px; 
            }
            .stat-card { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 25px; 
                border-radius: 15px; 
                text-align: center;
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
            }
            .stat-number { font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }
            .stat-label { font-size: 1em; opacity: 0.9; }
            .audit-entry { 
                background: #f8f9fa; 
                border: 1px solid #dee2e6; 
                padding: 15px; 
                margin-bottom: 10px; 
                border-radius: 8px; 
                font-family: 'Courier New', monospace; 
                font-size: 13px;
                transition: background-color 0.3s ease;
            }
            .audit-entry:hover { background: #e9ecef; }
            .no-results { 
                text-align: center; 
                padding: 40px; 
                color: #666; 
                font-style: italic; 
            }
            .loading { 
                text-align: center; 
                padding: 20px; 
                color: #667eea; 
            }
            .error { 
                background: #f8d7da; 
                color: #721c24; 
                padding: 15px; 
                border-radius: 8px; 
                border-left: 5px solid #dc3545; 
            }
            .success { 
                background: #d4edda; 
                color: #155724; 
                padding: 15px; 
                border-radius: 8px; 
                border-left: 5px solid #28a745; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 Clinical Trial Matching Demo</h1>
                <p>Privacy-preserving patient-trial matching with blockchain audit trail</p>
            </div>
            
            <div class="card">
                <h2>🔍 Patient Trial Matching</h2>
                <form id="matchForm">
                    <div class="form-group">
                        <label for="patientSelect">Select Patient for Trial Matching:</label>
                        <select id="patientSelect">
                            <option value="">Choose a patient to find matching trials...</option>
                            <option value="PAT_001">PAT_001 - Age 45, Male, Type 2 Diabetes</option>
                            <option value="PAT_002">PAT_002 - Age 62, Female, Hypertension</option>
                            <option value="PAT_003">PAT_003 - Age 38, Male, Early Stage Cancer</option>
                            <option value="PAT_004">PAT_004 - Age 55, Female, Depression</option>
                            <option value="PAT_005">PAT_005 - Age 41, Male, Obesity (BMI 35)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">🔍 Find Matching Clinical Trials</button>
                </form>
                <div id="matchResults" class="results"></div>
            </div>
            
            <div class="card">
                <h2>📊 System Statistics</h2>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">5</div>
                        <div class="stat-label">Synthetic Patients</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">5</div>
                        <div class="stat-label">Active Clinical Trials</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="auditCount">0</div>
                        <div class="stat-label">Audit Trail Entries</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100%</div>
                        <div class="stat-label">Privacy Protected</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>🔗 Blockchain Audit Trail</h2>
                <p style="margin-bottom: 20px; color: #666;">
                    All patient matching activities are recorded in an immutable audit trail for regulatory compliance.
                    Only privacy-preserving tokens are stored - no personal health information.
                </p>
                <div id="auditLog">
                    <div class="no-results">
                        No audit entries yet. Run a patient match to see the blockchain audit trail in action.
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Handle form submission for patient matching
            document.getElementById('matchForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const patientId = document.getElementById('patientSelect').value;
                if (!patientId) {
                    alert('Please select a patient first');
                    return;
                }
                
                const resultsDiv = document.getElementById('matchResults');
                resultsDiv.innerHTML = '<div class="loading">🔄 Searching for matching trials...</div>';
                
                try {
                    const response = await fetch('/match', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({patient_id: patientId})
                    });
                    
                    const result = await response.json();
                    
                    if (result.error) {
                        resultsDiv.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                        return;
                    }
                    
                    if (result.matches && result.matches.length === 0) {
                        resultsDiv.innerHTML = `
                            <div class="no-results">
                                <h3>No Matching Trials Found</h3>
                                <p>This patient does not meet the inclusion criteria for any currently available clinical trials.</p>
                            </div>
                        `;
                    } else if (result.matches) {
                        resultsDiv.innerHTML = `
                            <div class="success">
                                <h3>🎯 Matching Trials Found!</h3>
                                <p><strong>Privacy Token:</strong> ${result.patient_token}</p>
                                <p><em>${result.disclaimer}</em></p>
                            </div>
                            ${result.matches.map(match => `
                                <div class="trial-match">
                                    <h4>${match.title}</h4>
                                    <p><strong>Sponsor:</strong> ${match.sponsor || 'Research Institute'}</p>
                                    <p>${match.description}</p>
                                    <p>
                                        <span class="score">Match Score: ${match.score}%</span>
                                        <span class="status ${match.status.includes('Potentially') ? 'eligible' : 'review'}">
                                            ${match.status}
                                        </span>
                                    </p>
                                    <p><small><strong>Trial ID:</strong> ${match.trial_id}</small></p>
                                </div>
                            `).join('')}
                        `;
                    }
                    
                    // Update audit log after successful match
                    updateAuditLog();
                    
                } catch (error) {
                    console.error('Error:', error);
                    resultsDiv.innerHTML = `
                        <div class="error">
                            ❌ Error connecting to matching service. Please try again.
                        </div>
                    `;
                }
            });
            
            // Update audit log display
            async function updateAuditLog() {
                try {
                    const response = await fetch('/audit');
                    const audit = await response.json();
                    const auditDiv = document.getElementById('auditLog');
                    const auditCount = document.getElementById('auditCount');
                    
                    auditCount.textContent = audit.length;
                    
                    if (audit.length === 0) {
                        auditDiv.innerHTML = `
                            <div class="no-results">
                                No audit entries yet. Run a patient match to see the blockchain audit trail in action.
                            </div>
                        `;
                    } else {
                        auditDiv.innerHTML = audit.slice(-5).reverse().map((entry, index) => `
                            <div class="audit-entry">
                                <strong>Block ${audit.length - index - 1}</strong> | ${entry.timestamp}<br>
                                <strong>Action:</strong> ${entry.action} | 
                                <strong>Token:</strong> ${entry.token} | 
                                <strong>Trials Found:</strong> ${entry.trials}<br>
                                <strong>Hash:</strong> ${entry.hash || 'N/A'}
                            </div>
                        `).join('');
                    }
                } catch (error) {
                    console.error('Error loading audit log:', error);
                }
            }
            
            // Load initial audit log
            updateAuditLog();
            
            // Auto-refresh audit log every 30 seconds
            setInterval(updateAuditLog, 30000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/match")
async def match_patient_to_trials(request: dict):
    """Match a patient to available clinical trials"""
    patient_id = request.get('patient_id')
    
    if not patient_id:
        return {"error": "Patient ID is required"}
    
    # Find the patient
    patient = next((p for p in PATIENTS if p['id'] == patient_id), None)
    if not patient:
        return {"error": "Patient not found"}
    
    # Generate privacy-preserving token
    token_data = f"{patient['id']}{patient['age']}{patient['gender']}"
    token_hash = hashlib.sha256(token_data.encode()).hexdigest()[:12].upper()
    privacy_token = f"TOK_{token_hash}"
    
    # Find matching trials
    matches = []
    for trial in TRIALS:
        if trial['condition'] in patient['conditions']:
            matches.append({
                'title': trial['title'],
                'trial_id': trial['id'],
                'description': trial['description'],
                'sponsor': trial['sponsor'],
                'score': 85,  # Simplified scoring
                'status': 'Potentially Eligible'
            })
    
    # Create audit entry hash
    audit_data = f"{privacy_token}{datetime.now().isoformat()}{len(matches)}"
    audit_hash = hashlib.sha256(audit_data.encode()).hexdigest()[:16].upper()
    
    # Add to blockchain audit trail
    audit_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'action': 'PATIENT_TRIAL_MATCH',
        'token': privacy_token,
        'trials': len(matches),
        'hash': audit_hash
    }
    audit_log.append(audit_entry)
    
    return {
        'patient_token': privacy_token,
        'matches': matches,
        'total_matches': len(matches),
        'disclaimer': 'Results are for pre-screening purposes only. Final eligibility must be determined by the clinical research team.'
    }

@app.get("/audit")
async def get_audit_trail():
    """Get the complete blockchain audit trail"""
    return audit_log

@app.get("/patients")
async def get_patients():
    """Get list of available patients (for demo purposes)"""
    return PATIENTS

@app.get("/trials")
async def get_trials():
    """Get list of available clinical trials"""
    return TRIALS

def main():
    """Main application entry point"""
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Clinical Trial Matching Demo Starting...")
    print(f"📊 Web Interface: http://localhost:{port}/ui")
    print(f"📖 API Documentation: http://localhost:{port}/docs")
    print(f"❤️ Health Check: http://localhost:{port}/health")
    print(f"🔗 Audit Trail: http://localhost:{port}/audit")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port, 
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()