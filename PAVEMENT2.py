import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rigid Pavement Design Pro", layout="wide")

html_concrete_pro = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117; --card: #161b22; --border: #30363d; --accent: #00a8ff; --text: #e6edf3;
        --slab: #cbd5e1; --base: #854d0e; --sg: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .container { max-width: 1200px; margin: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 25px; }
    h2 { color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 10px; margin-top:0; }
    
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }
    label { display: block; font-size: 0.8rem; color: #8b949e; margin-bottom: 5px; }
    select, input { width: 100%; padding: 10px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    
    .btn { width: 100%; padding: 18px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; color: #fff; font-size: 1rem; }
    .btn:hover { background: #0081c4; }

    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 40px 20px; min-height: 400px; text-align: center; }
    .slab-layer { margin: 0 auto; width: 80%; background: var(--slab); color: #334155; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid #94a3b8; transition: height 0.5s; position: relative; }
    .base-layer { margin: 0 auto; width: 80%; background: var(--base); height: 50px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1); }
    .sg-layer { margin: 0 auto; width: 80%; background: var(--sg); height: 40px; display: flex; align-items: center; justify-content: center; }
    
    .dim-line { position: absolute; left: calc(100% + 10px); color: var(--accent); font-family: 'IBM Plex Mono'; font-size: 0.9rem; border-left: 2px solid var(--accent); padding-left: 10px; white-space: nowrap; }
</style>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>⬜ เครื่องมือออกแบบผิวทางคอนกรีต (Rigid Pavement)</h2>
        <div class="grid">
            <div>
                <h4>1. ประเภทถนนและจราจร</h4>
                <div class="input-row">
                    <div>
                        <label>ประเภทคอนกรีต</label>
                        <select id="p_type" onchange="updateJ()">
                            <option value="JPCP">JPCP (มีเหล็กเดือย Dowel)</option>
                            <option value="JRCP">JRCP (มีเหล็กเสริม Mesh)</option>
                            <option value="CRCP">CRCP (เหล็กเสริมต่อเนื่อง)</option>
                        </select>
                    </div>
                    <div><label>W18 (ล้าน ESALs)</label><input type="number" id="w18" value="10"></div>
                </div>

                <h4>2. คุณสมบัติวัสดุและฐานราก</h4>
                <div class="input-row">
                    <div><label>Modulus of Rupture (S'c - psi)</label><input type="number" id="sc" value="650"></div>
                    <div><label>Concrete Modulus (Ec - psi)</label><input type="number" id="ec" value="4000000"></div>
                </div>
                <div class="input-row">
                    <div><label>Subgrade k-value (pci)</label><input type="number" id="k" value="150"></div>
                    <div><label>Drainage Coeff (Cd)</label><input type="number" id="cd" value="1.0"></div>
                </div>

                <h4>3. ตัวแปรทางวิศวกรรม</h4>
                <div class="input-row">
                    <div><label>Load Transfer (J)</label><input type="number" id="j_val" value="3.2"></div>
                    <div><label>Reliability (Zr)</label><input type="number" id="zr" value="-1.282"></div>
                </div>

                <button class="btn" onclick="calculateRigid()">⚡ คำนวณความหนา Slab</button>
            </div>

            <div class="diagram-area">
                <div id="res_box" style="display:none; margin-bottom:20px; padding:15px; background:rgba(0,168,255,0.1); border-radius:8px;">
                    <span id="res_text" style="font-size:1.2rem; color:var(--accent); font-weight:bold;"></span>
                </div>

                <div id="v_slab" class="slab-layer" style="height: 60px;">
                    CONCRETE SLAB <div id="dim_slab" class="dim-line">D = ?</div>
                </div>
                <div class="base-layer">SUBBASE (6")</div>
                <div class="sg-layer">SUBGRADE</div>
                <p style="margin-top:20px; color:#8b949e; font-size:0.8rem;">*ภาพจำลองหน้าตัดตามสัดส่วนความหนาจริง</p>
            </div>
        </div>
    </div>
</div>

<script>
function updateJ() {
    const type = document.getElementById('p_type').value;
    const jInput = document.getElementById('j_val');
    if(type === 'JPCP') jInput.value = 3.2;
    else if(type === 'JRCP') jInput.value = 3.2;
    else if(type === 'CRCP') jInput.value = 2.6;
}

function calculateRigid() {
    const W18 = parseFloat(document.getElementById('w18').value) * 1e6;
    const Sc = parseFloat(document.getElementById('sc').value);
    const Ec = parseFloat(document.getElementById('ec').value);
    const k = parseFloat(document.getElementById('k').value);
    const J = parseFloat(document.getElementById('j_val').value);
    const Cd = parseFloat(document.getElementById('cd').value);
    const Zr = parseFloat(document.getElementById('zr').value);
    const So = 0.35; // Std Dev สำหรับ Rigid
    const dPSI = 1.7;

    // AASHTO Rigid Equation Iteration
    let D = 6.0; 
    const target = Math.log10(W18);
    
    for(let i=0; i<300; i++) {
        let term1 = Zr * So + 7.35 * Math.log10(D + 1) - 0.06;
        let term2 = Math.log10(dPSI / (4.5 - 1.5)) / (1 + 1.62e7 / Math.pow(D + 1, 8.46));
        let term3 = (4.22 - 0.32 * 1.5) * Math.log10( (Sc * Cd * (Math.pow(D, 0.75) - 1.132)) / (215.63 * J * (Math.pow(D, 0.75) - 18.42 / Math.pow(Ec/k, 0.25))) );
        let logW = term1 + term2 + term3;
        
        if (Math.abs(logW - target) < 0.001) break;
        D += (target - logW) * 0.1;
    }

    const finalD = Math.max(6, Math.ceil(D * 2) / 2); // ขั้นต่ำ 6 นิ้ว ปัดทุก 0.5

    // แสดงผล
    document.getElementById('res_box').style.display = 'block';
    document.getElementById('res_text').innerText = `ความหนาที่ต้องการ: ${finalD} นิ้ว (${(finalD*2.54).toFixed(1)} ซม.)`;
    
    // อัปเดตรูป
    document.getElementById('v_slab').style.height = (finalD * 12) + 'px';
    document.getElementById('dim_slab').innerText = 'D = ' + finalD + '" (' + (finalD*2.54).toFixed(1) + ' cm)';
}
</script>
</body>
</html>
"""

components.html(html_concrete_pro, height=850, scrolling=True)
