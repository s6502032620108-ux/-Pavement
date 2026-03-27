import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pavement Engineering Tool", layout="wide")

html_engineering_system = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d1117; --card: #161b22; --border: #30363d; --accent: #f0a500; --text: #e6edf3;
        --ac: #374151; --base: #854d0e; --sb: #a16207; --sg: #166534;
    }
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; }
    .container { max-width: 1200px; margin: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    h2, h3 { color: var(--accent); margin-top: 0; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    h4 { color: #58a6ff; margin: 10px 0 5px 0; font-size: 0.9rem; }
    
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 3px; }
    input, select { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 6px; font-family: 'IBM Plex Mono'; }
    
    .btn { width: 100%; padding: 18px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; font-size: 1rem; }
    .result-panel { background: #010409; border: 1px solid #3fb950; padding: 15px; border-radius: 8px; margin-top: 15px; display: none; }
    
    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 30px; min-height: 450px; text-align: center; }
    .layer { margin: 0 auto; width: 70%; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 1px solid rgba(255,255,255,0.1); transition: 0.5s; position: relative; }
    .layer-info { position: absolute; left: 105%; white-space: nowrap; color: var(--accent); font-family: 'IBM Plex Mono'; font-size: 0.8rem; text-align: left; }
</style>
</head>
<body>
<div class="container">
    <div class="grid">
        <div>
            <div class="card">
                <h3>🛠️ 1. ข้อมูลจากหน้าสนาม (Field Data)</h3>
                
                <h4>🔍 ข้อมูลดิน (Subgrade)</h4>
                <div class="input-row">
                    <div>
                        <label>ค่า CBR (%) จากการทดสอบ</label>
                        <input type="number" id="f_cbr" value="5" oninput="convertCBR()">
                    </div>
                    <div>
                        <label>MR ที่คำนวณได้ (psi)</label>
                        <input type="number" id="f_mr" value="7500">
                    </div>
                </div>

                <h4>🚛 ข้อมูลจราจร (Traffic Count)</h4>
                <div class="input-row">
                    <div><label>จำนวนรถบรรทุก (คัน/วัน)</label><input type="number" id="f_trucks" value="500"></div>
                    <div><label>อายุออกแบบ (ปี)</label><input type="number" id="f_years" value="15"></div>
                </div>
                <div class="input-row">
                    <div>
                        <label>ประเภทรถเด่น</label>
                        <select id="f_tf_type">
                            <option value="1.1">รถบรรทุก 10 ล้อ (TF=1.1)</option>
                            <option value="2.2">รถพ่วง (TF=2.2)</option>
                            <option value="0.3">รถบรรทุก 6 ล้อ (TF=0.3)</option>
                        </select>
                    </div>
                    <div><label>อัตราเติบโต (%)</label><input type="number" id="f_growth" value="3"></div>
                </div>
            </div>

            <div class="card">
                <h3>🏗️ 2. ข้อมูลวัสดุโครงสร้าง</h3>
                <div class="input-row">
                    <div><label>a1 (ความแกร่ง AC)</label><input type="number" id="f_a1" value="0.44"></div>
                    <div><label>a2 (ความแกร่ง Base)</label><input type="number" id="f_a2" value="0.14"></div>
                </div>
                <div class="input-row">
                    <div><label>D2 (หนา Base - นิ้ว)</label><input type="number" id="f_d2" value="8"></div>
                    <div><label>D3 (หนา Subbase - นิ้ว)</label><input type="number" id="f_d3" value="6"></div>
                </div>
                <button class="btn" onclick="processEngineering()">⚡ คำนวณและสรุปรายการ</button>
            </div>
        </div>

        <div>
            <div id="eng_res" class="result-panel">
                <h3 style="border:none; color:#3fb950;">📋 รายการคำนวณ (Calculation Note)</h3>
                <div id="eng_content" style="font-size: 0.9rem; line-height: 1.6;"></div>
            </div>

            <div class="diagram-area">
                <h4 style="text-align:center; color:#8b949e;">Final Pavement Section</h4>
                <div id="v_ac" class="layer" style="background:var(--ac); height:40px; color:#fff;">
                    SURFACE (AC) <div id="lbl_ac" class="layer-info"></div>
                </div>
                <div id="v_base" class="layer" style="background:var(--base); height:80px; color:#fff;">
                    BASE COURSE <div id="lbl_base" class="layer-info"></div>
                </div>
                <div id="v_sb" class="layer" style="background:var(--sb); height:60px; color:#fff;">
                    SUBBASE <div id="lbl_sb" class="layer-info"></div>
                </div>
                <div class="layer" style="background:var(--sg); height:40px; color:#fff;">
                    SUBGRADE (ดินเดิม) <div id="lbl_sg" class="layer-info"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function convertCBR() {
    // สูตรแปลง CBR เป็น MR (psi) โดยทั่วไปคือ MR = 1500 * CBR
    const cbr = parseFloat(document.getElementById('f_cbr').value);
    const mr = cbr * 1500;
    document.getElementById('f_mr').value = mr;
}

function processEngineering() {
    // 1. คำนวณหา W18 จากข้อมูลสนาม
    const trucks = parseFloat(document.getElementById('f_trucks').value);
    const tf = parseFloat(document.getElementById('f_tf_type').value);
    const years = parseFloat(document.getElementById('f_years').value);
    const growth = parseFloat(document.getElementById('f_growth').value) / 100;
    
    const growth_factor = growth > 0 ? (Math.pow(1 + growth, years) - 1) / growth : years;
    const w18 = trucks * tf * 365 * growth_factor * 0.5; // Lane Factor 0.5

    // 2. คำนวณ SN Required (AASHTO)
    const mr = parseFloat(document.getElementById('f_mr').value);
    const zr = -1.282; // 90% Reliability
    const so = 0.45;
    const dpsi = 1.9;
    
    let sn_req = 1.0;
    const target = Math.log10(w18);
    for(let i=0; i<200; i++) {
        let logW = zr * so + 9.36 * Math.log10(sn_req + 1) - 0.2 + Math.log10(dpsi/2.7)/(0.4 + 1094/Math.pow(sn_req+1, 5.19)) + 2.32*Math.log10(mr) - 8.07;
        sn_req += (target - logW) * 0.1;
    }

    // 3. หาความหนา D1
    const a1 = parseFloat(document.getElementById('f_a1').value);
    const a2 = parseFloat(document.getElementById('f_a2').value);
    const d2 = parseFloat(document.getElementById('f_d2').value);
    const d3 = parseFloat(document.getElementById('f_d3').value);
    const a3 = 0.11;
    
    const sn_existing = (a2 * d2) + (a3 * d3);
    let d1 = (sn_req - sn_existing) / a1;
    d1 = Math.max(2, Math.ceil(d1 * 2) / 2);

    // 4. สรุปผลลัพธ์
    document.getElementById('eng_res').style.display = 'block';
    document.getElementById('eng_content').innerHTML = `
        • <b>Traffic:</b> W18 = ${w18.toLocaleString(undefined, {maximumFractionDigits:0})} ESALs<br>
        • <b>Soil:</b> Resilient Modulus (MR) = ${mr.toLocaleString()} psi<br>
        • <b>Structure:</b> SN Required = ${sn_req.toFixed(3)}<br>
        • <b>Design:</b> แนะนำความหนา AC = <span style="color:var(--accent); font-size:1.1rem;">${d1} นิ้ว (${(d1*2.54).toFixed(1)} ซม.)</span>
    `;

    // 5. อัปเดตกราฟิก
    document.getElementById('v_ac').style.height = (d1 * 12) + 'px';
    document.getElementById('v_base').style.height = (d2 * 10) + 'px';
    document.getElementById('v_sb').style.height = (d3 * 10) + 'px';
    
    document.getElementById('lbl_ac').innerHTML = `D1 = ${d1}" (${(d1*2.54).toFixed(1)} cm)`;
    document.getElementById('lbl_base').innerHTML = `D2 = ${d2}" (${(d2*2.54).toFixed(1)} cm)`;
    document.getElementById('lbl_sb').innerHTML = `D3 = ${d3}" (${(d3*2.54).toFixed(1)} cm)`;
    document.getElementById('lbl_sg').innerHTML = `CBR = ${document.getElementById('f_cbr').value}%`;
}
</script>
</body>
</html>
"""

components.html(html_engineering_system, height=1000, scrolling=True)
