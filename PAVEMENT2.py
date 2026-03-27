import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rigid Pavement Design (Pro)", layout="wide")

html_concrete_fixed = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117; --card: #161b22; --border: #30363d; --accent: #00d2ff; --text: #e6edf3;
        --slab: #cbd5e1; --base: #854d0e; --sg: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .container { max-width: 1200px; margin: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    h2, h3 { color: var(--accent); margin-top: 0; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    h4 { color: #58a6ff; margin: 15px 0 5px 0; font-size: 0.9rem; border-left: 3px solid var(--accent); padding-left: 10px; }
    
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 3px; }
    input, select { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    
    .btn { width: 100%; padding: 18px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; font-size: 1rem; color: #000; }
    .note-panel { background: #010409; border-left: 4px solid #ff4b4b; padding: 15px; border-radius: 4px; margin-top: 15px; font-size: 0.9rem; line-height: 1.6; }
    
    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 40px 20px; min-height: 450px; text-align: center; }
    .slab-layer { margin: 0 auto; width: 75%; background: var(--slab); color: #1e293b; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid #94a3b8; transition: height 0.5s ease; position: relative; }
    .dim-line { position: absolute; left: calc(100% + 15px); color: var(--accent); font-family: 'IBM Plex Mono'; white-space: nowrap; }
</style>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>⬜ ออกแบบผิวทางคอนกรีต (Rigid Pavement) - High Load Version</h2>
        <div class="grid">
            <div>
                <h4>🚛 1. ข้อมูลจราจรสะสม (Traffic Input)</h4>
                <div class="input-row">
                    <div><label>จำนวนรถบรรทุกรวม (คัน/วัน/2 ทิศทาง)</label><input type="number" id="f_truck" value="2500"></div>
                    <div><label>อายุออกแบบ (ปี)</label><input type="number" id="f_years" value="20"></div>
                </div>
                <div class="input-row">
                    <div>
                        <label>ประเภทรถ (TF เฉลี่ย)</label>
                        <select id="f_tf">
                            <option value="1.8">ทั่วไป (10 ล้อผสมพ่วง) TF=1.8</option>
                            <option value="2.8">หนักมาก (Heavy Logistics) TF=2.8</option>
                            <option value="0.8">รถบรรทุกกลาง (6-10 ล้อ) TF=0.8</option>
                        </select>
                    </div>
                    <div><label>Lane Distribution (DL)</label><input type="number" id="f_dl" value="0.9" step="0.1"></div>
                </div>

                <h4>🌱 2. ค่าทดสอบสนาม (Field Test)</h4>
                <div class="input-row">
                    <div><label>ค่า CBR ดินเดิม (%)</label><input type="number" id="f_cbr" value="4"></div>
                    <div><label>Reliability (95%)</label><input type="number" id="f_zr" value="-1.645"></div>
                </div>

                <h4>🏗️ 3. ชนิดโครงสร้าง (Structure)</h4>
                <div class="input-row">
                    <div>
                        <label>ประเภทผิวทาง</label>
                        <select id="f_type">
                            <option value="JPCP">JPCP (ตัด Joint + Dowel)</option>
                            <option value="JRCP">JRCP (ตะแกรงเหล็กเสริม)</option>
                            <option value="CRCP">CRCP (เสริมเหล็กต่อเนื่อง)</option>
                        </select>
                    </div>
                    <div><label>Flexural Strength (psi)</label><input type="number" id="f_sc" value="650"></div>
                </div>
                <button class="btn" onclick="calculateRigidFinal()">⚡ คำนวณความหนา Slab</button>
            </div>

            <div class="diagram-area">
                <div id="result_note" class="note-panel" style="display:none;">
                    <div id="calc_steps"></div>
                </div>
                <div id="v_slab" class="slab-layer" style="height: 80px;">
                    CONCRETE SLAB <div id="dim_slab" class="dim-line">D = ?</div>
                </div>
                <div style="margin:0 auto; width:75%; background:var(--base); height:50px; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.8rem;">CEMENT STABILIZED BASE (15 cm)</div>
                <div style="margin:0 auto; width:75%; background:var(--sg); height:40px; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.8rem;">SUBGRADE</div>
            </div>
        </div>
    </div>
</div>

<script>
function calculateRigidFinal() {
    // 1. คำนวณ W18 (ESAL) แบบละเอียด
    const trucks = parseFloat(document.getElementById('f_truck').value);
    const tf = parseFloat(document.getElementById('f_tf').value);
    const years = parseFloat(document.getElementById('f_years').value);
    const growth = 0.04; // สมมติ 4% ต่อปี
    const DL = parseFloat(document.getElementById('f_dl').value);
    const growth_factor = (Math.pow(1 + growth, years) - 1) / growth;
    
    // W18 = ADT_truck * TF * 365 * Gf * Directional_Factor(0.5) * Lane_Factor(DL)
    const w18 = trucks * tf * 365 * growth_factor * 0.5 * DL;

    // 2. แปลง CBR เป็น k-value (แบบ AASHTO)
    const cbr = parseFloat(document.getElementById('f_cbr').value);
    const k_val = cbr * 45; // ปรับตัวคูณให้สะท้อนชั้น Subbase/Base ที่ช่วยเสริม

    // 3. กำหนดตัวแปร AASHTO
    const type = document.getElementById('f_type').value;
    let J = (type === 'CRCP') ? 2.6 : 3.2; // JPCP/JRCP with Dowels = 3.2
    const Sc = parseFloat(document.getElementById('f_sc').value);
    const Ec = 4200000; 
    const Cd = 1.0;
    const Zr = parseFloat(document.getElementById('f_zr').value);
    const So = 0.39; 
    const dPSI = 2.0; // ค่ามาตรฐานงานทางหลวง

    // 4. วนลูปแก้สมการ (Iteration)
    let D = 5.0;
    const target = Math.log10(w18);
    for(let i=0; i<500; i++) {
        let term1 = Zr * So + 7.35 * Math.log10(D + 1) - 0.06;
        let term2 = Math.log10(dPSI / 3.0) / (1 + 1.62e7 / Math.pow(D + 1, 8.46));
        let term3 = (4.22 - 0.32 * 1.5) * Math.log10( (Sc * Cd * (Math.pow(D, 0.75) - 1.132)) / (215.63 * J * (Math.pow(D, 0.75) - 18.42 / Math.pow(Ec/k_val, 0.25))) );
        let logW = term1 + term2 + term3;
        if (Math.abs(logW - target) < 0.001) break;
        D += (target - logW) * 0.05;
    }

    // 5. ปัดค่าตามมาตรฐานไทย (ขั้นต่ำ 20 ซม. สำหรับทางหลวง)
    let finalD_inch = Math.max(8, Math.ceil(D * 2) / 2); // ขั้นต่ำ 8 นิ้ว (ประมาณ 20 ซม.)
    let finalD_cm = finalD_inch * 2.54;

    // 6. แสดงผล
    document.getElementById('result_note').style.display = 'block';
    document.getElementById('calc_steps').innerHTML = `
        <b>📊 วิเคราะห์จราจร:</b> W18 = ${w18.toLocaleString(undefined, {maximumFractionDigits:0})} ESALs<br>
        <b>🌱 ค่าฐานราก:</b> k-value = ${Math.round(k_val)} pci (CBR ${cbr}%)<br>
        <hr>
        <b style="color:var(--accent); font-size:1.1rem;">✅ ความหนาแนะนำ: ${finalD_inch}" (${finalD_cm.toFixed(1)} ซม.)</b>
    `;

    document.getElementById('v_slab').style.height = (finalD_inch * 12) + 'px';
    document.getElementById('dim_slab').innerText = 'D = ' + finalD_inch + '" (' + finalD_cm.toFixed(1) + ' cm)';
}
</script>
</body>
</html>
"""

components.html(html_concrete_fixed, height=900, scrolling=True)
"""

components.html(html_concrete_system, height=1000, scrolling=True)
