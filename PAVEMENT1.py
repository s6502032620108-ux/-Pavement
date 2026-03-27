import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pavement Design Pro", layout="wide")

html_all_variables = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117; --panel: #161b22; --border: #30363d; --accent: #f0a500; --text: #e6edf3;
        --ac-color: #374151; --con-color: #94a3b8; --base-color: #854d0e; --sb-color: #a16207; --sg-color: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid var(--border); }
    .tab-btn { padding: 10px 20px; background: none; border: none; color: #8b949e; cursor: pointer; font-weight: bold; }
    .tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .card { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    .input-group { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    label { display: block; font-size: 0.8rem; color: #8b949e; margin-bottom: 2px; }
    input { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: white; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    .btn { width: 100%; padding: 15px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; }
    .diagram-container { background: #010409; padding: 20px; border-radius: 10px; border: 1px solid var(--border); }
    .road-layer { margin: 0 auto; width: 70%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.7rem; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; }
</style>
</head>
<body>

<div class="tabs">
    <button class="tab-btn active" onclick="switchTab('ac')">🔲 Flexible (AC)</button>
    <button class="tab-btn" onclick="switchTab('concrete')">⬜ Rigid (Concrete)</button>
</div>

<div id="tab-ac" class="tab-content active">
    <div class="card">
        <h2 style="color:var(--accent)">Flexible Pavement (SN = a1D1 + a2D2m2 + a3D3m3)</h2>
        <div class="grid">
            <div>
                <label>จราจรสะสม (W18 - ล้าน ESALs)</label>
                <input type="number" id="ac_w18" value="2.5">
                <label>Subgrade Resilient Modulus (MR - psi)</label>
                <input type="number" id="ac_mr" value="7500">
                
                <p style="color:var(--accent); margin: 15px 0 5px 0;">ชั้นทางและสัมประสิทธิ์ (Layer Coeff / Drainage / Thickness)</p>
                <div class="input-group">
                    <div><label>a1 (Surface)</label><input type="number" id="ac_a1" value="0.44" step="0.01"></div>
                    <div><label>D1 (คำนวณอัตโนมัติ)</label><input type="text" value="Auto" disabled></div>
                </div>
                <div class="input-group">
                    <div><label>a2 (Base)</label><input type="number" id="ac_a2" value="0.14" step="0.01"></div>
                    <div><label>m2 (Drainage)</label><input type="number" id="ac_m2" value="1.0" step="0.1"></div>
                    <div><label>D2 (Base - นิ้ว)</label><input type="number" id="ac_d2" value="8"></div>
                </div>
                <div class="input-group">
                    <div><label>a3 (Subbase)</label><input type="number" id="ac_a3" value="0.11" step="0.01"></div>
                    <div><label>m3 (Drainage)</label><input type="number" id="ac_m3" value="1.0" step="0.1"></div>
                    <div><label>D3 (Subbase - นิ้ว)</label><input type="number" id="ac_d3" value="6"></div>
                </div>
                
                <button class="btn" onclick="calcAC()">⚡ คำนวณความหนา D1</button>
                <div id="ac_res" style="margin-top:10px; color:#3fb950; font-weight:bold; font-size:1.1rem;"></div>
            </div>
            
            <div class="diagram-container">
                <h4 style="text-align:center;">AC Layer Visualization</h4>
                <div id="v_ac_d1" class="road-layer" style="background:var(--ac-color); height:30px;">AC</div>
                <div id="v_ac_d2" class="road-layer" style="background:var(--base-color); height:60px;">BASE</div>
                <div id="v_ac_d3" class="road-layer" style="background:var(--sb-color); height:50px;">SUBBASE</div>
                <div class="road-layer" style="background:var(--sg-color); height:30px;">SUBGRADE</div>
            </div>
        </div>
    </div>
</div>

<div id="tab-concrete" class="tab-content">
    <div class="card">
        <h2 style="color:var(--accent)">Rigid Pavement (Thickness D)</h2>
        <div class="grid">
            <div>
                <label>จราจรสะสม (W18 - ล้าน ESALs)</label>
                <input type="number" id="c_w18" value="5.0">
                <label>Flexural Strength (Sc - psi)</label>
                <input type="number" id="c_sc" value="650">
                <label>Modulus of Subgrade Reaction (k - pci)</label>
                <input type="number" id="c_k" value="150">
                <label>Load Transfer (J) [Dowel=3.2]</label>
                <input type="number" id="c_j" value="3.2" step="0.1">
                
                <button class="btn" onclick="calcConcrete()">⚡ คำนวณความหนาแผ่นพื้น</button>
                <div id="c_res" style="margin-top:10px; color:#3fb950; font-weight:bold; font-size:1.1rem;"></div>
            </div>
            <div class="diagram-container">
                <h4 style="text-align:center;">Rigid Visualization</h4>
                <div id="v_c_d" class="road-layer" style="background:var(--con-color); height:60px; color:black;">CONCRETE</div>
                <div class="road-layer" style="background:var(--base-color); height:40px;">BASE/SUBBASE</div>
                <div class="road-layer" style="background:var(--sg-color); height:30px;">SUBGRADE</div>
            </div>
        </div>
    </div>
</div>

<script>
function switchTab(t) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-'+t).classList.add('active');
    event.currentTarget.classList.add('active');
}

function calcAC() {
    const w18 = parseFloat(document.getElementById('ac_w18').value)*1e6;
    const mr = parseFloat(document.getElementById('ac_mr').value);
    const a1 = parseFloat(document.getElementById('ac_a1').value);
    const a2 = parseFloat(document.getElementById('ac_a2').value);
    const m2 = parseFloat(document.getElementById('ac_m2').value);
    const d2 = parseFloat(document.getElementById('ac_d2').value);
    const a3 = parseFloat(document.getElementById('ac_a3').value);
    const m3 = parseFloat(document.getElementById('ac_m3').value);
    const d3 = parseFloat(document.getElementById('ac_d3').value);

    // Iteration for SN required
    let sn_req = 3.0;
    for(let i=0; i<150; i++) {
        let logW = -1.282*0.45 + 9.36*Math.log10(sn_req+1) - 0.2 + Math.log10(1.9/2.7)/(0.4 + 1094/Math.pow(sn_req+1, 5.19)) + 2.32*Math.log10(mr) - 8.07;
        sn_req += (Math.log10(w18) - logW)*0.1;
    }

    const sn_sub = (a2*d2*m2) + (a3*d3*m3);
    let d1 = (sn_req - sn_sub) / a1;
    d1 = Math.max(2, Math.ceil(d1 * 2) / 2); // ปัดขึ้น 0.5 นิ้ว

    document.getElementById('ac_res').innerHTML = "ผลลัพธ์ D1: " + d1 + " นิ้ว (" + (d1*2.54).toFixed(1) + " ซม.) <br><small style='color:#8b949e'>SN Req: "+sn_req.toFixed(3)+"</small>";
    
    // Update Diagram
    document.getElementById('v_ac_d1').style.height = (d1*10)+"px";
    document.getElementById('v_ac_d2').style.height = (d2*6)+"px";
    document.getElementById('v_ac_d3').style.height = (d3*6)+"px";
}

function calcConcrete() {
    const w18 = parseFloat(document.getElementById('c_w18').value)*1e6;
    const sc = parseFloat(document.getElementById('c_sc').value);
    const k = parseFloat(document.getElementById('c_k').value);
    const j = parseFloat(document.getElementById('c_j').value);

    // Simplified AASHTO Rigid Logic
    let d = Math.pow((Math.log10(w18) * 150 * j) / (sc * Math.pow(k, 0.25)), 0.6);
    d = Math.max(6, Math.ceil(d * 2) / 2);

    document.getElementById('c_res').innerText = "ผลลัพธ์ D: " + d + " นิ้ว (" + (d*2.54).toFixed(1) + " ซม.)";
    document.getElementById('v_c_d').style.height = (d*10)+"px";
}
</script>
</body>
</html>
"""

components.html(html_all_variables, height=850, scrolling=True)
