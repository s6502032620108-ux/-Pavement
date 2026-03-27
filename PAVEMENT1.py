import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้ากระดาษกว้างพิเศษ
st.set_page_config(page_title="Professional Pavement Design", layout="wide")

html_pro_version = """
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
    body { font-family: 'Sarabun', sans-serif; background: var(--bg); color: var(--text); padding: 20px; margin: 0; }
    .container { max-width: 1200px; margin: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
    h2 { color: var(--accent); margin-top: 0; border-bottom: 2px solid var(--accent); padding-bottom: 10px; }
    h4 { margin: 15px 0 5px 0; color: #58a6ff; font-size: 0.9rem; text-transform: uppercase; }
    
    /* Form Styling */
    .input-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 3px; }
    input { width: 100%; padding: 8px; background: #0d1117; border: 1px solid var(--border); color: #fff; border-radius: 6px; font-family: 'IBM Plex Mono'; font-size: 0.9rem; }
    input:focus { border-color: var(--accent); outline: none; }
    .btn { width: 100%; padding: 18px; background: var(--accent); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 20px; font-size: 1rem; transition: 0.3s; }
    .btn:hover { background: #d97706; transform: translateY(-2px); }

    /* Diagram Scaling */
    .diagram-area { background: #010409; border: 1px solid var(--border); border-radius: 10px; padding: 30px; position: relative; min-height: 450px; }
    .layer { margin: 0 auto; width: 75%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; transition: all 0.5s ease; border: 1px solid rgba(255,255,255,0.1); text-shadow: 1px 1px 2px #000; position: relative; }
    .layer-info { position: absolute; left: calc(100% + 15px); width: 150px; text-align: left; font-family: 'IBM Plex Mono'; font-size: 0.85rem; color: var(--accent); white-space: nowrap; }
</style>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>🛣️ AASHTO 1993 Pavement Design (Full Parameters)</h2>
        <div class="grid">
            
            <div>
                <h4>1. จราจรและสภาพแวดล้อม (Design Inputs)</h4>
                <div class="input-row">
                    <div><label>W18 (ล้าน ESALs)</label><input type="number" id="w18" value="2.5"></div>
                    <div><label>Reliability (Zr)</label><input type="number" id="zr" value="-1.282"></div>
                    <div><label>Std. Dev (So)</label><input type="number" id="so" value="0.45"></div>
                </div>
                <div class="input-row">
                    <div><label>ΔPSI (Service Loss)</label><input type="number" id="dpsi" value="1.9"></div>
                    <div><label>Subgrade MR (psi)</label><input type="number" id="mr" value="7500"></div>
                </div>

                <h4>2. สัมประสิทธิ์วัสดุ (Layer Coefficients - a)</h4>
                <div class="input-row">
                    <div><label>a1 (Surface/AC)</label><input type="number" id="a1" value="0.44"></div>
                    <div><label>a2 (Base Course)</label><input type="number" id="a2" value="0.14"></div>
                    <div><label>a3 (Subbase)</label><input type="number" id="a3" value="0.11"></div>
                </div>

                <h4>3. ค่าการระบายน้ำ (Drainage Coeff - m)</h4>
                <div class="input-row">
                    <div><label>m1 (Not used)</label><input type="number" value="1.0" disabled></div>
                    <div><label>m2 (Base)</label><input type="number" id="m2" value="1.0"></div>
                    <div><label>m3 (Subbase)</label><input type="number" id="m3" value="1.0"></div>
                </div>

                <h4>4. ความหนาชั้นรอง (Known Thickness - D)</h4>
                <div class="input-row">
                    <div><label>D1 (To be Calc)</label><input type="text" value="FINDING..." disabled></div>
                    <div><label>D2 (Base - นิ้ว)</label><input type="number" id="d2" value="8"></div>
                    <div><label>D3 (Subbase - นิ้ว)</label><input type="number" id="d3" value="6"></div>
                </div>

                <button class="btn" onclick="runCalculation()">⚡ คำนวณโครงสร้างชั้นทาง</button>
            </div>

            <div>
                <div id="result_summary" style="display:none; margin-bottom:15px; background:#010409; padding:15px; border-radius:8px; border-left:4px solid var(--accent);">
                    <span id="final_text"></span>
                </div>
                <div class="diagram-area">
                    <h5 style="text-align:center; margin-top:0; color:#8b949e;">Cross-Section Visualizer</h5>
                    
                    <div id="layer_ac" class="layer" style="background:var(--ac); height:40px;">
                        SURFACE (AC) <div id="info_ac" class="layer-info">D1 = ?</div>
                    </div>
                    <div id="layer_base" class="layer" style="background:var(--base); height:80px;">
                        BASE COURSE <div id="info_base" class="layer-info">D2 = 8"</div>
                    </div>
                    <div id="layer_sb" class="layer" style="background:var(--sb); height:60px;">
                        SUBBASE <div id="info_sb" class="layer-info">D3 = 6"</div>
                    </div>
                    <div id="layer_sg" class="layer" style="background:var(--sg); height:40px; border-bottom: none;">
                        SUBGRADE (ดินเดิม) <div class="layer-info">∞</div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</div>

<script>
function runCalculation() {
    // ดึงค่าทั้งหมด
    const W18 = parseFloat(document.getElementById('w18').value) * 1e6;
    const Zr = parseFloat(document.getElementById('zr').value);
    const So = parseFloat(document.getElementById('so').value);
    const dPSI = parseFloat(document.getElementById('dpsi').value);
    const MR = parseFloat(document.getElementById('mr').value);
    
    const a1 = parseFloat(document.getElementById('a1').value);
    const a2 = parseFloat(document.getElementById('a2').value);
    const a3 = parseFloat(document.getElementById('a3').value);
    const m2 = parseFloat(document.getElementById('m2').value);
    const m3 = parseFloat(document.getElementById('m3').value);
    const D2 = parseFloat(document.getElementById('d2').value);
    const D3 = parseFloat(document.getElementById('d3').value);

    // 1. หา Required Structural Number (SN) ด้วย Iteration
    let sn_req = 3.0;
    const target = Math.log10(W18);
    for(let i=0; i<200; i++) {
        let logW = Zr * So + 9.36 * Math.log10(sn_req + 1) - 0.20 + Math.log10(dPSI/(4.2-1.5)) / (0.40 + 1094 / Math.pow(sn_req + 1, 5.19)) + 2.32 * Math.log10(MR) - 8.07;
        sn_req += (target - logW) * 0.1;
    }

    // 2. คำนวณความแข็งแรงชั้นล่าง
    const sn_existing = (a2 * D2 * m2) + (a3 * D3 * m3);
    
    // 3. หาความหนา D1 (Surface)
    let D1 = (sn_req - sn_existing) / a1;
    if (D1 < 2) D1 = 2; // ขั้นต่ำ 2 นิ้ว (5 ซม.)
    
    // ปัดขึ้น 0.5 นิ้ว
    const D1_final = Math.ceil(D1 * 2) / 2;
    const sn_provided = (a1 * D1_final) + sn_existing;

    // 4. แสดงผลตัวเลข
    document.getElementById('result_summary').style.display = 'block';
    document.getElementById('final_text').innerHTML = `
        <b>ผลการออกแบบ:</b> <br>
        Required SN: <span style="color:var(--accent)">${sn_req.toFixed(3)}</span> | 
        Provided SN: <span style="color:#3fb950">${sn_provided.toFixed(3)}</span> <br>
        ความหนาที่แนะนำ (D1): <span style="color:var(--accent); font-size:1.2rem;">${D1_final} นิ้ว (${(D1_final*2.54).toFixed(1)} ซม.)</span>
    `;

    // 5. อัปเดตกราฟิก (Visual Scaling)
    document.getElementById('layer_ac').style.height = (D1_final * 12) + 'px';
    document.getElementById('layer_base').style.height = (D2 * 12) + 'px';
    document.getElementById('layer_sb').style.height = (D3 * 12) + 'px';
    
    document.getElementById('info_ac').innerText = 'D1 = ' + D1_final + '" (' + (D1_final*2.54).toFixed(1) + ' cm)';
    document.getElementById('info_base').innerText = 'D2 = ' + D2 + '" (' + (D2*2.54).toFixed(1) + ' cm)';
    document.getElementById('info_sb').innerText = 'D3 = ' + D3 + '" (' + (D3*2.54).toFixed(1) + ' cm)';
}
</script>
</body>
</html>
"""

components.html(html_pro_version, height=850, scrolling=True)
