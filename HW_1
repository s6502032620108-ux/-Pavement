<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ระบบออกแบบโครงสร้างชั้นทาง</title>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0d1117;
    --panel: #161b22;
    --border: #30363d;
    --accent: #f0a500;
    --accent2: #58a6ff;
    --accent3: #3fb950;
    --accent4: #ff7b72;
    --text: #e6edf3;
    --text2: #8b949e;
    --concrete: #94a3b8;
    --asphalt: #374151;
    --subbase: #92400e;
    --subgrade: #166534;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Sarabun', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 24px;
  }

  header {
    text-align: center;
    margin-bottom: 32px;
    padding: 28px;
    background: linear-gradient(135deg, #161b22 0%, #1a2233 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 12px;
    position: relative;
    overflow: hidden;
  }
  header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
      45deg, transparent, transparent 20px,
      rgba(240,165,0,0.03) 20px, rgba(240,165,0,0.03) 21px
    );
  }
  header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.03em;
    position: relative;
  }
  header p {
    color: var(--text2);
    font-size: 0.9rem;
    margin-top: 6px;
    position: relative;
  }

  .tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0;
  }
  .tab-btn {
    padding: 10px 20px;
    border: none;
    background: none;
    color: var(--text2);
    font-family: 'Sarabun', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
    border-radius: 6px 6px 0 0;
  }
  .tab-btn:hover { color: var(--text); background: rgba(255,255,255,0.03); }
  .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); background: rgba(240,165,0,0.05); }

  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
  @media (max-width: 900px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }

  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
  }
  .card-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent2);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card-title .icon { font-size: 1.2rem; }

  .form-group { margin-bottom: 14px; }
  label {
    display: block;
    font-size: 0.85rem;
    color: var(--text2);
    margin-bottom: 5px;
    font-weight: 500;
  }
  input[type="number"], select {
    width: 100%;
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    transition: border-color 0.2s;
  }
  input[type="number"]:focus, select:focus {
    outline: none;
    border-color: var(--accent);
  }
  select option { background: #161b22; }

  .btn {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-family: 'Sarabun', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 8px;
  }
  .btn-primary {
    background: linear-gradient(135deg, var(--accent), #d97706);
    color: #0d1117;
  }
  .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 20px rgba(240,165,0,0.3); }

  .result-box {
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    margin-top: 16px;
    display: none;
  }
  .result-box.show { display: block; animation: fadeIn 0.3s ease; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

  .result-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent3);
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }

  .result-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    font-size: 0.9rem;
    border-bottom: 1px solid rgba(48,54,61,0.5);
  }
  .result-row:last-child { border-bottom: none; }
  .result-label { color: var(--text2); }
  .result-value {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    color: var(--accent);
  }
  .result-value.ok { color: var(--accent3); }
  .result-value.warn { color: var(--accent4); }

  /* Cross-section diagram */
  .cross-section {
    margin-top: 20px;
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
  }
  .cross-section h3 {
    font-size: 0.9rem;
    color: var(--text2);
    margin-bottom: 12px;
    font-weight: 500;
  }
  .layer-diagram { position: relative; }
  .layer {
    display: flex;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 4px;
    margin-bottom: 3px;
    overflow: hidden;
    transition: all 0.3s;
    cursor: default;
  }
  .layer:hover { border-color: var(--accent); }
  .layer-color {
    width: 40px;
    min-height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
  }
  .layer-info {
    flex: 1;
    padding: 6px 12px;
    font-size: 0.82rem;
  }
  .layer-name { font-weight: 600; color: var(--text); }
  .layer-depth {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text2);
    font-size: 0.78rem;
  }
  .layer-sn {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--accent);
    font-size: 0.78rem;
    padding-right: 12px;
  }

  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 6px;
  }
  .badge-ac { background: rgba(55,65,81,0.8); color: #9ca3af; }
  .badge-concrete { background: rgba(148,163,184,0.15); color: #94a3b8; }
  .badge-check { background: rgba(63,185,80,0.15); color: var(--accent3); }

  .info-note {
    background: rgba(88,166,255,0.08);
    border: 1px solid rgba(88,166,255,0.2);
    border-radius: 8px;
    padding: 12px;
    font-size: 0.82rem;
    color: var(--text2);
    margin-top: 12px;
    line-height: 1.6;
  }
  .info-note strong { color: var(--accent2); }

  .section-divider {
    text-align: center;
    color: var(--text2);
    font-size: 0.8rem;
    margin: 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-divider::before, .section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  .subtitle-label {
    font-size: 0.78rem;
    color: var(--text2);
    margin-bottom: 12px;
    padding: 6px 10px;
    background: rgba(240,165,0,0.05);
    border-left: 3px solid var(--accent);
    border-radius: 0 4px 4px 0;
  }

  /* Concrete specific */
  .concrete-type-card {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 12px;
    background: rgba(255,255,255,0.02);
    transition: border-color 0.2s;
  }
  .concrete-type-card:hover { border-color: rgba(88,166,255,0.4); }
  .concrete-type-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--accent2);
    margin-bottom: 10px;
  }

  table.result-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    margin-top: 10px;
  }
  table.result-table th {
    background: rgba(255,255,255,0.05);
    color: var(--text2);
    padding: 8px 10px;
    text-align: center;
    font-weight: 600;
    font-size: 0.8rem;
    border: 1px solid var(--border);
  }
  table.result-table td {
    padding: 7px 10px;
    text-align: center;
    border: 1px solid var(--border);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: var(--text);
  }
  table.result-table tr:hover td { background: rgba(255,255,255,0.02); }
  .highlight-td { color: var(--accent) !important; font-weight: 600; }
</style>
</head>
<body>

<header>
  <h1>🛣️ ระบบออกแบบโครงสร้างชั้นทาง</h1>
  <p>Flexible Pavement (AASHTO 1993) &nbsp;|&nbsp; Rigid Pavement (PCA Method)</p>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('ac')">🔲 ผิวทาง AC (Flexible)</button>
  <button class="tab-btn" onclick="switchTab('concrete')">⬜ ผิวทาง Concrete (Rigid)</button>
</div>

<!-- ========== TAB 1: AC ========== -->
<div id="tab-ac" class="tab-content active">
  <div class="subtitle-label">วิธีออกแบบ: AASHTO 1993 — คำนวณค่า Structural Number (SN) และหาความหนาชั้นทาง</div>
  <div class="grid-2">
    <div>
      <div class="card">
        <div class="card-title"><span class="icon">📊</span>ข้อมูลจราจรและสิ่งแวดล้อม</div>
        <div class="form-group">
          <label>W18 — ปริมาณ ESALs (ล้านคัน) ตลอดอายุการออกแบบ</label>
          <input type="number" id="ac_w18" value="2.5" step="0.1" min="0.1">
        </div>
        <div class="form-group">
          <label>ZR — Reliability Factor (ค่ามาตรฐาน เช่น -1.282 = 90%)</label>
          <input type="number" id="ac_zr" value="-1.282" step="0.001">
        </div>
        <div class="form-group">
          <label>So — Overall Standard Deviation (ปกติ 0.45–0.50)</label>
          <input type="number" id="ac_so" value="0.45" step="0.01">
        </div>
        <div class="form-group">
          <label>ΔPSI — Loss in Serviceability (Pi − Pt)</label>
          <input type="number" id="ac_psi" value="1.9" step="0.1">
        </div>
        <div class="form-group">
          <label>MR — Subgrade Resilient Modulus (psi)</label>
          <input type="number" id="ac_mr" value="7500" step="100">
        </div>
      </div>

      <div class="card" style="margin-top:16px">
        <div class="card-title"><span class="icon">🔧</span>สัมประสิทธิ์ชั้นทางและค่าระบายน้ำ</div>

        <div class="section-divider">ชั้น Surface (AC)</div>
        <div class="form-group">
          <label>a1 — Layer Coefficient (ปกติ 0.42–0.44)</label>
          <input type="number" id="ac_a1" value="0.44" step="0.01">
        </div>
        <div class="form-group">
          <label>m1 — Drainage Coefficient</label>
          <input type="number" id="ac_m1" value="1.0" step="0.1">
        </div>

        <div class="section-divider">ชั้น Base</div>
        <div class="form-group">
          <label>a2 — Layer Coefficient (Crushed Stone ≈ 0.14)</label>
          <input type="number" id="ac_a2" value="0.14" step="0.01">
        </div>
        <div class="form-group">
          <label>m2 — Drainage Coefficient</label>
          <input type="number" id="ac_m2" value="0.9" step="0.1">
        </div>
        <div class="form-group">
          <label>D2 — ความหนา Base ที่สมมติ (นิ้ว)</label>
          <input type="number" id="ac_d2" value="8" step="1">
        </div>

        <div class="section-divider">ชั้น Subbase</div>
        <div class="form-group">
          <label>a3 — Layer Coefficient (≈ 0.11)</label>
          <input type="number" id="ac_a3" value="0.11" step="0.01">
        </div>
        <div class="form-group">
          <label>m3 — Drainage Coefficient</label>
          <input type="number" id="ac_m3" value="0.8" step="0.1">
        </div>
        <div class="form-group">
          <label>D3 — ความหนา Subbase ที่สมมติ (นิ้ว)</label>
          <input type="number" id="ac_d3" value="6" step="1">
        </div>

        <button class="btn btn-primary" onclick="calcAC()">⚡ คำนวณออกแบบ AC</button>
      </div>
    </div>

    <div>
      <div id="ac_result" class="result-box">
        <div class="result-title">✅ ผลการออกแบบโครงสร้างชั้นทาง AC</div>
        <div id="ac_result_content"></div>
        <div id="ac_diagram"></div>
        <div class="info-note" id="ac_note"></div>
      </div>
      <div class="card" style="margin-top:16px">
        <div class="card-title"><span class="icon">📐</span>สูตรที่ใช้</div>
        <div style="font-size:0.82rem; color:var(--text2); line-height:1.8;">
          <strong style="color:var(--text)">AASHTO 1993 Equation:</strong><br>
          log(W18) = ZR·So + 9.36·log(SN+1) − 0.20<br>
          &nbsp;&nbsp;&nbsp;&nbsp;+ log[ΔPSI/(4.2−1.5)] / (0.40 + 1094/(SN+1)^5.19)<br>
          &nbsp;&nbsp;&nbsp;&nbsp;+ 2.32·log(MR) − 8.07<br><br>
          <strong style="color:var(--text)">SN = a1D1 + a2D2m2 + a3D3m3</strong><br><br>
          <strong style="color:var(--text)">Reliability Levels:</strong><br>
          50% → ZR = 0 &nbsp;|&nbsp; 85% → −1.04<br>
          90% → −1.282 &nbsp;|&nbsp; 95% → −1.645<br>
          99% → −2.327
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ========== TAB 2: CONCRETE ========== -->
<div id="tab-concrete" class="tab-content">
  <div class="subtitle-label">ออกแบบ 3 วิธี: (1) AASHTO 1993  (2) PCA Thickness Design  (3) IRC:58 Simplified</div>

  <div class="grid-2">
    <div>
      <div class="card">
        <div class="card-title"><span class="icon">🏗️</span>ข้อมูลหลัก (ใช้ร่วมกันทั้ง 3 วิธี)</div>

        <div class="form-group">
          <label>W18 — ESALs ตลอดอายุการออกแบบ (ล้านคัน)</label>
          <input type="number" id="c_w18" value="5" step="0.5">
        </div>
        <div class="form-group">
          <label>k — Modulus of Subgrade Reaction (pci)</label>
          <input type="number" id="c_k" value="150" step="10">
        </div>
        <div class="form-group">
          <label>Ec — Modulus of Elasticity of Concrete (psi)</label>
          <input type="number" id="c_ec" value="4000000" step="100000">
        </div>
        <div class="form-group">
          <label>Sc — Modulus of Rupture / flexural strength (psi)</label>
          <input type="number" id="c_sc" value="650" step="10">
        </div>
        <div class="form-group">
          <label>J — Load Transfer Coefficient (3.2 dowel / 3.8 no dowel)</label>
          <input type="number" id="c_j" value="3.2" step="0.1">
        </div>
        <div class="form-group">
          <label>Cd — Drainage Coefficient (1.0 normal)</label>
          <input type="number" id="c_cd" value="1.0" step="0.1">
        </div>
        <div class="form-group">
          <label>ΔPSI — Serviceability Loss (Pi−Pt)</label>
          <input type="number" id="c_psi" value="1.7" step="0.1">
        </div>
        <div class="form-group">
          <label>ZR — Reliability Factor (90% = -1.282)</label>
          <input type="number" id="c_zr" value="-1.282" step="0.001">
        </div>
        <div class="form-group">
          <label>So — Standard Deviation (0.35 concrete)</label>
          <input type="number" id="c_so" value="0.35" step="0.01">
        </div>
        <div class="form-group">
          <label>AxleLoad — Standard Axle Load (kN) สำหรับ PCA</label>
          <input type="number" id="c_axle" value="80" step="5">
        </div>

        <button class="btn btn-primary" onclick="calcConcrete()">⚡ คำนวณทั้ง 3 วิธี</button>
      </div>
    </div>

    <div>
      <div id="c_result" class="result-box">
        <div class="result-title">✅ ผลการออกแบบผิวทางคอนกรีต — 3 วิธี</div>
        <div id="c_result_content"></div>
        <div id="c_diagram"></div>
        <div class="info-note" id="c_note"></div>
      </div>
      <div class="card" style="margin-top:16px">
        <div class="card-title"><span class="icon">📐</span>วิธีการออกแบบ 3 แบบ</div>
        <div style="font-size:0.82rem; color:var(--text2); line-height:1.8;">
          <strong style="color:var(--accent2)">① AASHTO 1993 (Rigid)</strong><br>
          log(W18) = ZR·So + 7.35·log(D+1) − 0.06<br>
          &nbsp;&nbsp;&nbsp;+ log[ΔPSI/(4.5−1.5)]/(1+1.624×10⁷/(D+1)^8.46)<br>
          &nbsp;&nbsp;&nbsp;+ (4.22−0.32Pt)·log[Sc·Cd·(D^0.75−1.132)<br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/(215.63·J·(D^0.75−18.42/(Ec/k)^0.25))]<br><br>
          <strong style="color:var(--accent2)">② PCA Method</strong><br>
          σ = (3(1+ν)·P) / (2π·h²) · [2·ln(b/r)+1]<br>
          h = √(3(1+ν)·P·FS / (π·σ_allow))<br><br>
          <strong style="color:var(--accent2)">③ IRC:58 / ทล. ไทย Simplified</strong><br>
          h = 0.149·√(P·FS / (MR·k^0.25))
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// ===== AC DESIGN =====
function calcSN(w18_million, zr, so, dpsi, mr) {
  const W18 = Math.log10(w18_million * 1e6);
  // Solve SN iteratively via AASHTO equation
  let sn = 3.0;
  for (let iter = 0; iter < 200; iter++) {
    const lhs = zr * so + 9.36 * Math.log10(sn + 1) - 0.20
      + Math.log10(dpsi / 2.7) / (0.40 + 1094 / Math.pow(sn + 1, 5.19))
      + 2.32 * Math.log10(mr) - 8.07;
    if (Math.abs(lhs - W18) < 0.0001) break;
    sn += (W18 - lhs) * 0.05;
    if (sn < 0.1) sn = 0.1;
  }
  return sn;
}

function calcAC() {
  const w18 = parseFloat(document.getElementById('ac_w18').value);
  const zr = parseFloat(document.getElementById('ac_zr').value);
  const so = parseFloat(document.getElementById('ac_so').value);
  const dpsi = parseFloat(document.getElementById('ac_psi').value);
  const mr = parseFloat(document.getElementById('ac_mr').value);
  const a1 = parseFloat(document.getElementById('ac_a1').value);
  const m1 = parseFloat(document.getElementById('ac_m1').value);
  const a2 = parseFloat(document.getElementById('ac_a2').value);
  const m2 = parseFloat(document.getElementById('ac_m2').value);
  const d2 = parseFloat(document.getElementById('ac_d2').value);
  const a3 = parseFloat(document.getElementById('ac_a3').value);
  const m3 = parseFloat(document.getElementById('ac_m3').value);
  const d3 = parseFloat(document.getElementById('ac_d3').value);

  const SN_req = calcSN(w18, zr, so, dpsi, mr);
  const SN_base = a2 * d2 * m2 + a3 * d3 * m3;
  let D1 = (SN_req - SN_base) / (a1 * m1);
  D1 = Math.max(D1, 1.0);
  D1 = Math.ceil(D1 * 2) / 2; // round up to nearest 0.5"

  const SN_provided = a1 * D1 * m1 + a2 * d2 * m2 + a3 * d3 * m3;
  const D1_cm = (D1 * 2.54).toFixed(1);
  const D2_cm = (d2 * 2.54).toFixed(1);
  const D3_cm = (d3 * 2.54).toFixed(1);

  const reliability = getReliability(zr);

  const html = `
    <div class="result-row"><span class="result-label">ค่า SN ที่ต้องการ (Required)</span><span class="result-value">${SN_req.toFixed(3)}</span></div>
    <div class="result-row"><span class="result-label">ค่า SN ที่ออกแบบได้ (Provided)</span><span class="result-value ok">${SN_provided.toFixed(3)}</span></div>
    <div class="result-row"><span class="result-label">Reliability</span><span class="result-value">${reliability}</span></div>
    <div class="result-row"><span class="result-label">W18 (ESALs)</span><span class="result-value">${(w18 * 1e6).toLocaleString()} คัน</span></div>
    <hr style="border-color:var(--border);margin:12px 0">
    <div class="result-row"><span class="result-label">🔲 D1 — Surface AC</span><span class="result-value">${D1}" = ${D1_cm} ซม.</span></div>
    <div class="result-row"><span class="result-label">🟤 D2 — Base Course</span><span class="result-value">${d2}" = ${D2_cm} ซม.</span></div>
    <div class="result-row"><span class="result-label">🟫 D3 — Subbase</span><span class="result-value">${d3}" = ${D3_cm} ซม.</span></div>
    <div class="result-row"><span class="result-label">รวมความหนาทั้งหมด</span><span class="result-value ok">${(D1_cm*1+D2_cm*1+D3_cm*1).toFixed(1)} ซม.</span></div>
  `;

  document.getElementById('ac_result_content').innerHTML = html;

  // Diagram
  document.getElementById('ac_diagram').innerHTML = buildDiagram([
    { name: 'ชั้น Surface (AC)', depth: `${D1}" (${D1_cm} ซม.)`, color: '#374151', text: 'AC', sn: `SN1=${(a1*D1*m1).toFixed(2)}` },
    { name: 'ชั้น Base Course', depth: `${d2}" (${D2_cm} ซม.)`, color: '#6b4226', text: 'BC', sn: `SN2=${(a2*d2*m2).toFixed(2)}` },
    { name: 'ชั้น Subbase', depth: `${d3}" (${D3_cm} ซม.)`, color: '#a16207', text: 'SB', sn: `SN3=${(a3*d3*m3).toFixed(2)}` },
    { name: 'Subgrade (ดินเดิม)', depth: 'ไม่กำหนด', color: '#166534', text: 'SG', sn: `MR=${mr} psi` },
  ], 'หน้าตัดโครงสร้างชั้นทาง AC');

  document.getElementById('ac_note').innerHTML = `
    <strong>หมายเหตุ:</strong> ความหนา D1 ถูกปัดขึ้นเป็น 0.5 นิ้วที่ใกล้ที่สุด เพื่อความสะดวกในการก่อสร้าง
    ควรตรวจสอบกับเกณฑ์ขั้นต่ำของหน่วยงาน เช่น ทล. กำหนดชั้น Surface ขั้นต่ำ 5 ซม.
    ค่า SN ที่ได้ต้องมากกว่าหรือเท่ากับค่าที่ต้องการ <strong style="color:var(--accent3)">✓ ผ่าน</strong>
  `;

  const box = document.getElementById('ac_result');
  box.classList.add('show');
}

// ===== CONCRETE DESIGN =====
function calcConcrete() {
  const w18 = parseFloat(document.getElementById('c_w18').value);
  const k = parseFloat(document.getElementById('c_k').value);
  const Ec = parseFloat(document.getElementById('c_ec').value);
  const Sc = parseFloat(document.getElementById('c_sc').value);
  const J = parseFloat(document.getElementById('c_j').value);
  const Cd = parseFloat(document.getElementById('c_cd').value);
  const dpsi = parseFloat(document.getElementById('c_psi').value);
  const zr = parseFloat(document.getElementById('c_zr').value);
  const so = parseFloat(document.getElementById('c_so').value);
  const axle = parseFloat(document.getElementById('c_axle').value); // kN

  // --- Method 1: AASHTO 1993 Rigid ---
  const D1 = solveAASHTORigid(w18, zr, so, dpsi, Sc, Cd, J, Ec, k);

  // --- Method 2: PCA Thickness Design ---
  // Westergaard interior loading formula simplified
  // h = sqrt(3*(1+nu)*P*FS / (pi * sigma_allow)) with nu=0.15
  const P_kip = axle * 0.2248 / 2; // half axle in kips
  const FS = 1.7;
  const nu = 0.15;
  // Approximate: h² = 3*(1+nu)*P*FS / (pi * Sc) in consistent units (kip, in)
  // Sc in psi, P in kips -> use lb
  const P_lb = P_kip * 1000;
  const h_pca_sq = 3 * (1 + nu) * P_lb * FS / (Math.PI * Sc);
  const D2_raw = Math.sqrt(h_pca_sq);
  const D2 = Math.ceil(D2_raw * 2) / 2; // round to 0.5"

  // --- Method 3: IRC:58 Simplified ---
  // h ≈ 0.149 * sqrt(P_kN * FS / (fc * k^0.25)) adapted
  // Use: h (in) = 0.149 * sqrt(P_lb * FS / (Sc * k^0.25))
  const h_irc_raw = 0.149 * Math.sqrt(P_lb * FS / (Sc * Math.pow(k, 0.25)));
  const D3_irc = Math.ceil(h_irc_raw * 2) / 2;

  const D1_cm = (D1 * 2.54).toFixed(1);
  const D2_cm = (D2 * 2.54).toFixed(1);
  const D3_cm = (D3_irc * 2.54).toFixed(1);
  const reliability = getReliability(zr);

  const html = `
    <table class="result-table">
      <tr>
        <th>วิธีการ</th>
        <th>ความหนาคอนกรีต (นิ้ว)</th>
        <th>ความหนาคอนกรีต (ซม.)</th>
        <th>หมายเหตุ</th>
      </tr>
      <tr>
        <td>① AASHTO 1993</td>
        <td class="highlight-td">${D1.toFixed(1)}"</td>
        <td class="highlight-td">${D1_cm} ซม.</td>
        <td>Reliability ${reliability}</td>
      </tr>
      <tr>
        <td>② PCA Method</td>
        <td class="highlight-td">${D2.toFixed(1)}"</td>
        <td class="highlight-td">${D2_cm} ซม.</td>
        <td>FS = ${FS}, Westergaard</td>
      </tr>
      <tr>
        <td>③ IRC:58 Simplified</td>
        <td class="highlight-td">${D3_irc.toFixed(1)}"</td>
        <td class="highlight-td">${D3_cm} ซม.</td>
        <td>P = ${axle} kN</td>
      </tr>
    </table>
    <div class="result-row" style="margin-top:12px"><span class="result-label">ค่าเฉลี่ยแนะนำ</span>
      <span class="result-value ok">${(((D1+D2+D3_irc)/3)*2.54).toFixed(1)} ซม.</span>
    </div>
    <div class="result-row"><span class="result-label">ค่าสูงสุด (Conservative)</span>
      <span class="result-value">${(Math.max(D1,D2,D3_irc)*2.54).toFixed(1)} ซม.</span>
    </div>
  `;

  document.getElementById('c_result_content').innerHTML = html;

  // Use AASHTO result for diagram
  const D_use = Math.max(D1, D2, D3_irc);
  document.getElementById('c_diagram').innerHTML = buildDiagram([
    { name: 'Concrete Slab', depth: `${D_use.toFixed(1)}" (${(D_use*2.54).toFixed(1)} ซม.)`, color: '#64748b', text: 'PCC', sn: `Sc=${Sc} psi` },
    { name: 'Granular Subbase', depth: '6" (15 ซม.) แนะนำ', color: '#854d0e', text: 'GSB', sn: `k=${k} pci` },
    { name: 'Subgrade', depth: 'ไม่กำหนด', color: '#166534', text: 'SG', sn: `MR อ้างอิง k` },
  ], 'หน้าตัดโครงสร้างผิวทางคอนกรีต (Conservative)');

  document.getElementById('c_note').innerHTML = `
    <strong>สรุป:</strong> ค่าที่แนะนำให้ใช้คือค่าจากวิธีที่ให้ความหนามากที่สุด (Conservative Design) เพื่อความปลอดภัย
    AASHTO 1993 เหมาะกับถนนไทย | PCA เน้นน้ำหนักล้อเดี่ยว | IRC:58 เหมาะกับถนนชนบท/ทางเกษตร
    <br><strong style="color:var(--accent3)">ควรปัดความหนาสุดท้ายขึ้นเป็น 5 ซม. ที่ใกล้ที่สุด</strong>
  `;

  document.getElementById('c_result').classList.add('show');
}

function solveAASHTORigid(w18_mil, zr, so, dpsi, Sc, Cd, J, Ec, k) {
  const W18 = Math.log10(w18_mil * 1e6);
  let D = 8.0;
  for (let iter = 0; iter < 500; iter++) {
    const pt = 2.5;
    const term1 = zr * so;
    const term2 = 7.35 * Math.log10(D + 1) - 0.06;
    const psi_term = Math.log10((dpsi) / (4.5 - 1.5)) / (1 + 1.624e7 / Math.pow(D + 1, 8.46));
    const inner = Sc * Cd * (Math.pow(D, 0.75) - 1.132) /
      (215.63 * J * (Math.pow(D, 0.75) - 18.42 / Math.pow(Ec / k, 0.25)));
    if (inner <= 0) { D += 0.1; continue; }
    const term4 = (4.22 - 0.32 * pt) * Math.log10(inner);
    const lhs = term1 + term2 + psi_term + term4;
    if (Math.abs(lhs - W18) < 0.0001) break;
    D += (W18 - lhs) * 0.08;
    if (D < 4) D = 4;
    if (D > 30) { D = 30; break; }
  }
  return Math.ceil(D * 2) / 2;
}

function buildDiagram(layers, title) {
  const heights = [48, 36, 32, 28];
  let html = `<div class="cross-section"><h3>📐 ${title}</h3><div class="layer-diagram">`;
  layers.forEach((l, i) => {
    const h = heights[i] || 28;
    html += `
      <div class="layer" style="min-height:${h}px">
        <div class="layer-color" style="background:${l.color};min-height:${h}px;color:rgba(255,255,255,0.7)">
          ${l.text}
        </div>
        <div class="layer-info">
          <div class="layer-name">${l.name}</div>
          <div class="layer-depth">${l.depth}</div>
        </div>
        <div class="layer-sn">${l.sn}</div>
      </div>`;
  });
  html += `</div></div>`;
  return html;
}

function getReliability(zr) {
  if (zr >= 0) return '50%';
  if (zr > -1.1) return '75–80%';
  if (zr > -1.2) return '85%';
  if (zr > -1.35) return '90%';
  if (zr > -1.7) return '95%';
  return '99%';
}

function switchTab(tab) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  event.target.classList.add('active');
}
</script>
</body>
</html>
