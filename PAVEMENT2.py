import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rigid Pavement Design Pro", layout="wide")

# แยกส่วน HTML/JS ออกมาเพื่อป้องกัน Syntax Error ใน Python
html_content = """
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
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    h2, h3 { color: var(--accent); margin-top: 0; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    h4 { color: #58a6ff; margin: 15px 0 5px 0; font-size: 0.9rem; border-left: 3px solid var(--accent); padding-left: 10px; }
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 3px; }
    input, select { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    .btn { width: 100%; padding: 18px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; color: #000; }
    .note-panel { background: #010409; border-left: 4px solid var(--accent); padding: 15px; border-radius: 4px; margin-top: 15px; font-size: 0.9rem; line-height: 1.6; }
    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 40px 20px; min-height: 450px; text-align: center; }
    .slab-layer { margin: 0 auto; width: 75%; background: var(--slab); color: #1e293b; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid #94a3b8; transition: height 0.5s ease; position: relative; }
    .dim-line { position: absolute; left: calc(100% + 15px); color: var(--accent); font-family: 'IBM Plex Mono'; white-space: nowrap; }
</style>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>⬜ ออกแบบถนนคอนกรีตจากค่าสนาม (Step-by-Step)</h2>
        <div class="grid">
            <div>
                <h4>🚛 STEP 1: หาค่า ESAL (จราจรสะสม)</h4>
                <div class="input-row">
                    <div><label>รถบรรทุกรวม (คัน/วัน/2 ทิศ)</label><input type="number" id="f_truck" value="1200"></div>
                    <div><label>อายุออกแบบ (ปี)</label><input type="number" id="f_years" value="20"></div>
                </div>
                <div class="input-row">
                    <div>
                        <label>ประเภทรถ (Truck Factor)</label>
                        <select id="f_tf">
                            <option value="1.5">รถ 10 ล้อ (TF=1.5)</option>
                            <option value="2.8">รถพ่วง (TF=2.8)</option>
                            <option value="0.5">รถ 6 ล้อ (TF=0.5)</option>
                        </select>
                    </div>
                    <div><label>Growth Rate (%)</label><input type="number" id="f_growth" value="3.5"></div>
                </div>

                <h4>🌱 STEP 2: ข้อมูลดินและวัสดุพื้นทาง</h4>
                <div class="input-row">
                    <div><label>ค่า CBR ดินเดิม (%)</label><input type="number" id="f_cbr" value="4"></div>
                    <div><label>Reliability (%)</label><select id="f_rel"><option value="-1.282">90%</option><option value="-1.645">95%</option></select></div>
                </div>

                <h4>🏗️ STEP 3: ชนิดคอนกรีต</h4>
                <div class="input-row">
                    <div>
                        <label>เลือกชนิดผิวทาง</label>
                        <select id="f_type">
                            <option value="JPCP">JPCP (Plain + Dowel)</option>
                            <option value="JRCP">JRCP (Reinforced Mesh)</option>
                            <option value="CRCP">CRCP (Continuous Steel)</option>
                        </select>
                    </div>
                    <div><label>Flexural Strength (psi)</label><input type="number" id="f_sc" value="650"></div>
                </div>
                <button class="btn" onclick="calculateAll()">🚀 เริ่มคำนวณและแสดงผล</button>
            </div>

            <div class="diagram-area">
                <div id="result_note" class="note-panel" style="display:none;"></div>
                <div id="v_slab" class="slab-layer" style="height: 60px;">
                    CONCRETE SLAB <div id="dim_slab" class="dim-line">D = ?</div>
                </div>
                <div style="margin:0 auto; width:75%; background:var(--base); height:50px; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.7rem;">BASE COURSE</div>
                <div style="margin:0 auto; width:75%; background:var(--sg); height:40px; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.7rem;">SUBGRADE (CBR <span id="cbr_val">4</span>%)</div>
            </div>
        </div>
    </div>
</div>

<script>
function calculateAll() {
    // 1. ESAL Calculation
    const trucks = parseFloat(document.getElementById('f_truck').value);
    const tf = parseFloat(document.getElementById('f_tf').value);
    const years = parseFloat(document.getElementById('f_years').value);
    const growth = parseFloat(document.getElementById('f_growth').value) / 100;
    const gf = (Math.pow(1 + growth, years) - 1) / growth;
    const w18 = trucks * tf * 365 * gf * 0.5 * 0.9; // Lane/Dir factor

    // 2. CBR to k-value
    const cbr = parseFloat(document.getElementById('f_cbr').value);
    const k_val = cbr * 45; 
    document.getElementById('cbr_val').innerText = cbr;

    // 3. AASHTO Rigid Iteration
    const type = document.getElementById('f_type').value;
    const J = (type === 'CRCP') ? 2.6 : 3.2;
    const Sc = parseFloat(document.getElementById('f_sc').value);
    const Zr = parseFloat(document.getElementById('f_rel').value);
    const dPSI = 1.8;
    
    let D = 5.0;
    const target = Math.log10(w18);
    for(let i=0; i<400; i++) {
        let logW = Zr * 0.39 + 7.35 * Math.log10(D + 1) - 0.06 + Math.log10(dPSI/3)/(1 + 1.62e7/Math.pow(D+1, 8.46)) + (4.22 - 0.48) * Math.log10((Sc * (Math.pow(D, 0.75)-1.132)) / (215.63 * J * (Math.pow(D, 0.75) - 18.42/Math.pow(4000000/k_val, 0.25))));
        if (Math.abs(logW - target) < 0.001) break;
        D += (target - logW) * 0.05;
    }

    const finalD = Math.max(8, Math.ceil(D * 2) / 2); 

    // Update UI
    document.getElementById('result_note').style.display = 'block';
    document.getElementById('result_note').innerHTML = `
        <b>📊 วิเคราะห์จราจร:</b> W18 = ${w18.toLocaleString(undefined, {maximumFractionDigits:0})} ESALs<br>
        <b>🌱 ฐานราก:</b> Modulus k = ${Math.round(k_val)} pci<br>
        <b style="color:var(--accent)">✅ ความหนาแนะนำ: ${finalD}" (${(finalD*2.54).toFixed(1)} ซม.)</b>
    `;
    document.getElementById('v_slab').style.height = (finalD * 12) + 'px';
    document.getElementById('dim_slab').innerText = 'D = ' + finalD + '" (' + (finalD*2.54).toFixed(1) + ' cm)';
}
</script>
</body>
</html>
"""

# คำสั่งรันใน Streamlit
components.html(html_content, height=900, scrolling=True)
