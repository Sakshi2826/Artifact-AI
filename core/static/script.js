// Professional Master System Dashboard (Protocol v2.1 Sync)
document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const dropZoneRuined = document.getElementById('drop-zone-ruined');
    const ruinedInput = document.getElementById('file-input-ruined');
    const referenceInput = document.getElementById('file-input-reference');
    const analyzeBtn = document.getElementById('analyze-btn');
    const ruinedPreview = document.getElementById('image-preview-ruined');
    const referencePreview = document.getElementById('image-preview-reference');
    const processingSection = document.getElementById('processing-section');
    const resultsSection = document.getElementById('results-section');
    const engineerTasksContainer = document.getElementById('engineer-tasks-container');
    const workerTasksContainer = document.getElementById('worker-tasks-container');
    const engineerView = document.getElementById('engineer-view');
    const workerView = document.getElementById('worker-view');

    const API_BASE_URL = '/api/';
    let currentTaskId = null;
    let activePollInterval = null;

    // --- Tab Switching ---
    window.switchTab = (tab) => {
        const btnEng = document.getElementById('btn-engineer-tab');
        const btnWrk = document.getElementById('btn-worker-tab');
        if (tab === 'engineer') {
            engineerView.classList.remove('hidden');
            workerView.classList.add('hidden');
            btnEng.classList.add('active');
            btnWrk.classList.remove('active');
        } else {
            engineerView.classList.add('hidden');
            workerView.classList.remove('hidden');
            btnWrk.classList.add('active');
            btnEng.classList.remove('active');
            fetchTasks(); 
        }
    };

    // --- Dual Upload & Preview ---
    function setupPreview(input, imgElement, dropZone) {
        if(input) input.addEventListener('change', () => {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imgElement.src = e.target.result;
                    imgElement.style.display = 'block';
                    imgElement.style.opacity = '1';
                    analyzeBtn.disabled = !ruinedInput.files[0];
                };
                reader.readAsDataURL(file);
            }
        });
        if(dropZone) dropZone.onclick = (e) => { if(e.target.tagName !== 'SPAN') input.click(); };
    }
    setupPreview(ruinedInput, ruinedPreview, dropZoneRuined);
    setupPreview(referenceInput, referencePreview, document.getElementById('drop-zone-reference'));

    // --- Master Synthesis Execution ---
    analyzeBtn.addEventListener('click', async () => {
        if (!ruinedInput.files[0]) return;
        const formData = new FormData();
        formData.append('ruined_image', ruinedInput.files[0]);
        if (referenceInput.files[0]) formData.append('reference_image', referenceInput.files[0]);

        try {
            analyzeBtn.disabled = true;
            processingSection.classList.remove('hidden');
            resultsSection.classList.add('hidden');
            const res = await fetch(`${API_BASE_URL}analyze/`, { method: 'POST', body: formData });
            const data = await res.json();
            currentTaskId = data.upload.id;
            
            // OPEN DASHBOARD IN "READY" STATE
            displayReportById(currentTaskId);
            fetchTasks(); // Refresh list immediately
        } catch (e) { analyzeBtn.disabled = false; }
    });

    function openDashboardWithLoaders() {
        processingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        analyzeBtn.disabled = false;
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        if (activePollInterval) clearInterval(activePollInterval);
        
        // --- INSTANCE DATA PURGE ---
        document.getElementById('res-instructions').innerText = "MASTER PROTOCOL v2.1: INITIALIZING SYNTHESIS...";
        document.getElementById('res-blueprint').src = "";
        document.getElementById('res-repaired').src = "";
        document.getElementById('download-manual-btn').style.display = 'none';
        document.getElementById('download-blueprint-btn').style.display = 'none';
        document.getElementById('assign-btn').style.display = 'none';
        document.getElementById('validate-btn').style.display = 'none';
        document.getElementById('resend-btn').style.display = 'none';
        document.getElementById('verification-card').style.display = 'none';
        document.getElementById('validated-seal').style.display = 'none';
        document.getElementById('btn-generate-report').style.display = 'none';
        document.getElementById('btn-generate-blueprint').style.display = 'none';
        document.getElementById('btn-generate-3d').style.display = 'none';
        
        ['blueprint-loader', 'manual-loader', '3d-loader'].forEach(id => {
            const el = document.getElementById(id); if(el) el.style.display = 'flex';
        });
        document.getElementById('manual-loader').style.display = 'flex'; 
        document.getElementById('blueprint-loader').style.display = 'flex';
        document.getElementById('3d-loader').style.display = 'none';
        document.getElementById('res-3d-viewer').style.display = 'none';
        document.getElementById('3d-placeholder').style.display = 'flex';
        document.getElementById('download-3d-group').style.display = 'none';
    }

    window.triggerManualSynthesis = async () => {
        if(!currentTaskId) return;
        const res = await fetch(`${API_BASE_URL}task/${currentTaskId}/generate-report/`, { method: 'POST' });
        if(res.ok) {
            document.getElementById('btn-generate-report').style.display = 'none';
            document.getElementById('manual-loader').style.display = 'flex';
            document.getElementById('res-instructions').innerText = "MASTER PROTOCOL v2.1: FORENSIC SCANNING IN PROGRESS...";
        }
    };

    window.triggerBlueprintSynthesis = async () => {
        if(!currentTaskId) return;
        const res = await fetch(`${API_BASE_URL}task/${currentTaskId}/generate-blueprint/`, { method: 'POST' });
        if(res.ok) {
            document.getElementById('btn-generate-blueprint').style.display = 'none';
            document.getElementById('blueprint-loader').style.display = 'flex';
        }
    };

    window.trigger3DSynthesis = async () => {
        if(!currentTaskId) return;
        const res = await fetch(`${API_BASE_URL}task/${currentTaskId}/generate-3d/`, { method: 'POST' });
        if(res.ok) {
            document.getElementById('btn-generate-3d').style.display = 'none';
            document.getElementById('3d-loader').style.display = 'flex';
            document.getElementById('3d-placeholder').style.display = 'none';
        }
    };

    async function pollForMasterSynthesis(taskId) {
        if (activePollInterval) clearInterval(activePollInterval);
        activePollInterval = setInterval(async () => {
            if (taskId !== currentTaskId) {
                clearInterval(activePollInterval);
                return;
            }
            try {
                const r = await fetch(`${API_BASE_URL}task/${taskId}/`);
                if (!r.ok) return;
                const task = await r.json();

                // 1. FRESH MANUAL (INSTANCE SYNC)
                if (task.repair_instructions && task.repair_instructions.length > 10) {
                    document.getElementById('res-instructions').innerText = task.repair_instructions;
                    document.getElementById('manual-loader').style.display = 'none';
                    document.getElementById('download-manual-btn').style.display = 'inline-block';
                    document.getElementById('btn-generate-report').style.display = 'none';
                } else if (task.status === 'INITIALIZING') {
                    document.getElementById('btn-generate-report').style.display = 'inline-block';
                } else if (task.status === 'ANALYZING' || task.status === 'SCANNING') {
                    document.getElementById('manual-loader').style.display = 'flex';
                    document.getElementById('btn-generate-report').style.display = 'none';
                }

                // 2. BLUEPRINT TRIGGER (AFTER READING)
                if (task.status === 'READY_FOR_BLUEPRINT' && !task.blueprint_image) {
                    document.getElementById('btn-generate-blueprint').style.display = 'inline-block';
                    document.getElementById('blueprint-loader').style.display = 'none';
                } else if (task.status === 'DRAFTING' || task.status === 'DRAFTING_BLUEPRINT') {
                    document.getElementById('btn-generate-blueprint').style.display = 'none';
                    document.getElementById('blueprint-loader').style.display = 'flex';
                }

                // 2. CAD BLUEPRINT (STRICT ACCURACY MODE)
                if (task.blueprint_image) {
                    document.getElementById('res-blueprint').src = task.blueprint_image + "?t=" + new Date().getTime();
                    document.getElementById('blueprint-loader').style.display = 'none';
                    document.getElementById('download-blueprint-btn').style.display = 'inline-block';
                }

                // 2.5 3D MESH (VOLUMETRIC RECONSTRUCTION)
                if (task.mesh_glb) {
                    const viewer = document.getElementById('res-3d-viewer');
                    if (viewer.src !== task.mesh_glb) {
                        viewer.src = task.mesh_glb;
                        viewer.style.display = 'block';
                        document.getElementById('3d-placeholder').style.display = 'none';
                        document.getElementById('3d-loader').style.display = 'none';
                        document.getElementById('download-3d-group').style.display = 'flex';
                    }
                } else if (task.status === 'SCANNING_3D') {
                    document.getElementById('btn-generate-3d').style.display = 'none';
                    document.getElementById('3d-loader').style.display = 'flex';
                    document.getElementById('3d-placeholder').style.display = 'none';
                } else if (!task.mesh_glb && task.status === 'COMPLETED') {
                    document.getElementById('btn-generate-3d').style.display = 'inline-block';
                }

                // 3. SPECIMEN VERIFICATION
                if (task.repaired_image) {
                    document.getElementById('res-repaired').src = task.repaired_image + "?t=" + new Date().getTime();
                    document.getElementById('verification-card').style.display = 'block';
                    if (task.status === 'REPAIRED') {
                        document.getElementById('validate-btn').style.display = 'inline-block';
                        document.getElementById('resend-btn').style.display = 'inline-block';
                        document.getElementById('assign-btn').style.display = 'none';
                        document.getElementById('ver-badge-status').innerText = 'PENDING VALIDATION';
                        document.getElementById('ver-prompt').style.display = 'block';
                        document.getElementById('validated-seal').style.display = 'none';
                    }
                }

                if (task.status === 'COMPLETED' && !task.repaired_image) {
                    document.getElementById('assign-btn').style.display = 'inline-block';
                }
                
                if (task.status === 'VALIDATED') {
                    document.getElementById('validate-btn').style.display = 'none';
                    document.getElementById('resend-btn').style.display = 'none';
                    document.getElementById('assign-btn').style.display = 'none';
                    document.getElementById('validated-seal').style.display = 'block';
                    document.getElementById('ver-badge-status').innerText = '100% VALIDATED';
                }

                if (task.status === 'VALIDATED' || task.status === 'COMPLETED') {
                    // We don't necessarily clear it if it's COMPLETED because blueprint might still be coming
                    if (task.status === 'VALIDATED') {
                        clearInterval(activePollInterval);
                        activePollInterval = null;
                    }
                    fetchTasks();
                }
                if (task.status === 'COMPLETED' || task.status === 'SENT_TO_WORKER' || task.status === 'REPAIRED') {
                    fetchTasks();
                }
            } catch (e) {}
        }, 3000);
    }

    // --- Action: Download Protocol & Exports ---
    window.downloadManual = () => {
        const content = document.getElementById('res-instructions').innerText;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Forensic_Report_v2.1_${currentTaskId}.txt`;
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
    };

    window.downloadBlueprint = () => {
        const img = document.getElementById('res-blueprint');
        if (!img.src) return;
        const a = document.createElement('a');
        a.href = img.src;
        a.download = `CAD_Draft_v2.1_${currentTaskId}.png`;
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
    };

    window.download3D = (format) => {
        if(!currentTaskId) return;
        fetch(`${API_BASE_URL}task/${currentTaskId}/`).then(r => r.json()).then(task => {
            const url = format === 'obj' ? task.mesh_obj : task.mesh_glb;
            if(!url) return;
            const a = document.createElement('a');
            a.href = url;
            a.download = `3D_Model_${currentTaskId}.${format}`;
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
        });
    };

    // --- Collaborative Workflow ---
    async function assignTask(taskId) {
        const res = await fetch(`${API_BASE_URL}task/${taskId}/assign/`, { method: 'POST' });
        if(res.ok) { alert("DISPATCHED to Specialist Portal."); fetchTasks(); document.getElementById('assign-btn').style.display = 'none'; }
    }
    document.getElementById('assign-btn').onclick = () => assignTask(currentTaskId);

    window.validateTask = async (taskId) => {
        const res = await fetch(`${API_BASE_URL}task/${taskId}/validate/`, { method: 'POST' });
        if(res.ok) { alert("VALIDATED 100%"); document.getElementById('validate-btn').style.display = 'none'; document.getElementById('resend-btn').style.display = 'none'; fetchTasks(); }
    };
    document.getElementById('validate-btn').onclick = () => validateTask(currentTaskId);

    window.resendTask = async (taskId) => {
        const res = await fetch(`${API_BASE_URL}task/${taskId}/resend/`, { method: 'POST' });
        if(res.ok) { alert("REJECTED: Task resent to Worker."); document.getElementById('validate-btn').style.display = 'none'; document.getElementById('resend-btn').style.display = 'none'; document.getElementById('verification-card').style.display = 'none'; fetchTasks(); }
    };
    document.getElementById('resend-btn').onclick = () => resendTask(currentTaskId);

    async function fetchTasks() {
        try {
            const r = await fetch(`${API_BASE_URL}tasks/`);
            const tasks = await r.json();
            engineerTasksContainer.innerHTML = tasks.slice(0, 10).map(t => `
                <div class="task-card" style="padding:15px; background:rgba(255,255,255,0.05); margin-bottom:12px; border-radius:12px; display:flex; justify-content:space-between; align-items:center; border-left: 5px solid ${t.status === 'VALIDATED' ? 'var(--primary)' : 'rgba(255,255,255,0.25)'};">
                    <div>
                        <strong style="color:var(--primary);">Restoration #${t.id}</strong>
                        <div style="font-size:0.7rem; color:var(--text-dim); text-transform:uppercase;">${t.status.replace(/_/g, ' ')}</div>
                    </div>
                    <button onclick="displayReportById(${t.id})" class="btn-primary" style="padding:6px 14px; font-size:0.75rem; background:rgba(255,255,255,0.1);">Dashboard</button>
                </div>
            `).join('');

            workerTasksContainer.innerHTML = tasks.filter(t => t.status === 'SENT_TO_WORKER' || t.status === 'REPAIRED' || t.status === 'VALIDATED').map(t => `
                <div class="glass-panel" style="padding: 1.5rem; text-align: left; border-top: 4px solid var(--secondary);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color: var(--secondary);">ASSIGNMENT #${t.id}</h4>
                        <span style="font-size:0.65rem;">${t.status}</span>
                    </div>
                    <p style="font-size: 0.8rem; color: var(--text-dim); margin-top:1rem;">${t.repair_instructions ? t.repair_instructions.substring(0, 60) + '...' : 'Archeological Manual Pending'}</p>
                    <div style="margin-top: 1.5rem; display:flex; gap:8px;">
                        <button onclick="displayReportById(${t.id})" class="btn-primary" style="flex:1; padding: 6px; font-size: 0.7rem;">View Dossier</button>
                        ${t.status === 'SENT_TO_WORKER' ? `<button onclick="openFulfillmentModal(${t.id})" class="btn-primary" style="flex:1; padding: 6px; font-size:0.7rem; background:var(--secondary); color:#0b0f19;">Fulfill Repair</button>` : ''}
                    </div>
                </div>
            `).join('');
        } catch (e) {}
    }

    window.displayReportById = async (id) => {
        const r = await fetch(`${API_BASE_URL}task/${id}/`);
        const task = await r.json();
        currentTaskId = id;
        switchTab('engineer');
        openDashboardWithLoaders();
        pollForMasterSynthesis(id);
    };

    window.openFulfillmentModal = (id) => {
        const modal = document.getElementById('modal-container');
        const body = document.getElementById('modal-body');
        modal.classList.remove('hidden');
        body.innerHTML = `
            <div style="text-align: center;">
                <p style="color:var(--text-dim); font-size: 0.85rem; margin-bottom: 2rem;">Upload reconstruction photograph for engineering verification.</p>
                <input type="file" id="repaired-file-input" accept="image/*" style="display:none;">
                <button onclick="document.getElementById('repaired-file-input').click()" class="btn-primary" style="width:100%; padding:15px; border: 2px dashed var(--secondary); background:transparent;">SELECT RECONSTRUCTION PHOTO</button>
                <div id="repaired-preview-container" style="margin-top: 2rem; display:none;">
                    <img id="repaired-preview" style="width:100%; border-radius:12px; border: 1px solid var(--primary);">
                    <button onclick="submitRepairedImage(${id})" class="btn-primary large" style="width:100%; margin-top: 2rem;">SUBMIT FOR VALIDATION</button>
                </div>
            </div>
        `;
        document.getElementById('repaired-file-input').onchange = (e) => {
            const file = e.target.files[0];
            if(file) {
                const r = new FileReader(); r.onload = (ev) => {
                    document.getElementById('repaired-preview').src = ev.target.result;
                    document.getElementById('repaired-preview-container').style.display = 'block';
                };
                r.readAsDataURL(file);
            }
        };
    };

    window.submitRepairedImage = async (id) => {
        const f = document.getElementById('repaired-file-input');
        if(!f.files[0]) return;
        const fd = new FormData(); fd.append('repaired_image', f.files[0]);
        const res = await fetch(`${API_BASE_URL}task/${id}/submit-repaired/`, { method: 'POST', body: fd });
        if(res.ok) { alert("SAVED: Sent for verification."); document.getElementById('modal-container').classList.add('hidden'); fetchTasks(); }
    };

    fetchTasks();
});
