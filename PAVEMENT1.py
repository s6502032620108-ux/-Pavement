import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้ากระดาษ Streamlit
st.set_page_config(page_title="Pavement Design System", layout="wide")

html_all_in_one = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117;
        --panel: #161b22;
        --border: #30363d;
        --accent: #f0a500;
        --text: #e6edf3;
        --ac-color: #374151;
        --con-color: #94a3b8;
        --base-color: #854d0e;
        --subgrade-color: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; margin: 0; }
    
    /* Tabs */
    .tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid var(--border); }
    .tab-btn { padding: 10px 20px; background: none; border: none; color: #8b949e; cursor: pointer; font-size: 1rem; font-weight: bold; }
    .tab-btn.active { color: var(--accent); border-bottom: 3px solid var(--accent); }
    .tab-content { display: none; }
    .tab-content.active { display: block; }

    .card { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
    .grid { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 25px; }
    
    label { display: block; margin-top: 10px; font-size: 0.85rem; color: #8b949e; }
    input { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: white; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    .btn { width: 100%; padding: 15px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    
    /* Diagram */
    .diagram-container { background: #010409; padding: 20px; border-radius: 10px; border: 1px solid var(--border); text-align: center; }
    .road-layer { margin: 0 auto; width: 80%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75rem; transition: height 0.4s; border: 1px solid rgba(255,255,255,0.1); }
    .layer-label { margin-left: 10px; font-family: 'IBM Plex Mono'; color: var(--accent); font-size: 0.85rem; }
</style>
</head>
<body>

<div class="tabs">
    <button class="tab-btn active" onclick="switchTab('ac')">🔲 Flexible (AC)</button>
    <button class="tab-btn" onclick="switchTab('concrete')">⬜ Rigid (Concrete)</button>
</div>

<div id="tab-ac" class="tab-content active">
    <div class="card">
        <h2 style="color:var(--accent)">Asphalt Concrete Design (AASHTO 1993)</h2>
        <div class="grid">
            <div>
                <label>จราจรสะสม (W18 - Million ESALs)</label>
                <input type="number" id="ac_w18" value="2.5">
                <label>Subgrade MR (psi)</label>
                <input type="number" id="ac_mr" value="7500">
                <label>ความหนา Base (D2) - นิ้ว</label>
                <input type="number" id="ac_d2" value="8">
                <button class="btn" onclick="calcAC()">⚡ คำนวณความหนา AC</button>
                <div id="ac_res" style="margin-top:15px; color:#3fb950; font-weight:bold;"></div>
            </div>
            <div class="diagram-container">
                <h4>AC Cross-Section</h4>
                <div id="ac_vis_1" class="road-layer" style="background:var(--ac-color); height:30px;">SURFACE (AC)</div>
                <div id="ac_vis_2" class="road-layer" style="background:var(--base-color); height:60px;">BASE</div>
                <div class="road-layer" style="background:var(--subgrade-color); height:40px;">SUBGRADE</div>
            </div>
        </div>
    </div>
</div>

<div id="tab-concrete" class="tab-content">
    <div class="card">
        <h2 style="color:var(--accent)">Rigid Pavement Design (AASHTO/PCA)</h2>
        <div class="grid">
            <div>
                <label>จราจรสะสม (W18 - Million ESALs)</label>
                <input type="number" id="c_w18" value="5.0">
                <label>Modulus of Rupture (Sc - psi)</label>
                <input type="number" id="c_sc" value="650">
                <label>Subgrade k-value (pci)</label>
                <input type="number" id="c_k" value="150">
                <button class="btn" onclick="calcConcrete()">⚡ คำนวณความหนา Concrete</button>
                <div id="c_res" style="margin-top:15px; color:#3fb950; font-weight:bold;"></div>
            </div>
            <div class="diagram-container">
                <h4>Concrete Cross-Section</h4>
                <div id="c_vis_1" class="road-layer" style="background:var(--con-color); height:40px; color:#000;">CONCRETE SLAB</div>
                <div id="c_vis_2" class="road-layer" style="background:var(--base-color); height:40px;">SUBBASE</div>
                <div class="road-layer" style="background:var(--subgrade-color); height:40px;">SUBGRADE</div>
            </div>
        </div>
    </div>
</div>

<script>
function switchTab(type) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + type).classList.add('active');
    event.currentTarget.classList.add('active');
}

function calcAC() {
    const w18 = parseFloat(document.getElementById('ac_w18').value) * 1e6;
    const mr = parseFloat(document.getElementById('ac_mr').value);
    const d2 = parseFloat(document.getElementById('ac_d2').value);
    
    // AASHTO Iteration (Simplified)
    let sn_req = 3.0;
    for(let i=0; i<100; i++) {
        let logW = -1.282 * 0.45 + 9.36 * Math.log10(sn_req+1) - 0.20 + 0.35 + 2.32 * Math.log10(mr) - 8.07;
        sn_req += (Math.log10(w18) - logW) * 0.1;
    }
    
    let d1 = (sn_req - (0.14 * d2)) / 0.44;
    d1 = Math.max(2, Math.ceil(d1 * 2) / 2);
    
    document.getElementById('ac_res').innerText = "แนะนำความหนา AC (D1): " + d1 + " นิ้ว (" + (d1*2.54).toFixed(1) + " ซม.)";
    document.getElementById('ac_vis_1').style.height = (d1 * 10) + "px";
    document.getElementById('ac_vis_2').style.height = (d2 * 5) + "px";
}

function calcConcrete() {
    const w18 = parseFloat(document.getElementById('c_w18').value) * 1e6;
    const sc = parseFloat(document.getElementById('c_sc').value);
    
    // AASHTO Rigid (Simplified Empirical)
    let d = Math.pow((Math.log10(w18) * 1000) / (sc), 0.7);
    d = Math.max(6, Math.ceil(d * 2) / 2);
    
    document.getElementById('c_res').innerText = "แนะนำความหนา Concrete (D): " + d + " นิ้ว (" + (d*2.54).toFixed(1) + " ซม.)";
    document.getElementById('c_vis_1').style.height = (d * 8) + "px";
}
</script>
</body>
</html>
"""

components.html(html_all_in_one, height=750, scrolling=True)
