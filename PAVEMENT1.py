<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ออกแบบโครงสร้างชั้นทาง</title>

<style>
body {
  font-family: sans-serif;
  background: #0d1117;
  color: #e6edf3;
  padding: 20px;
}
.card {
  background: #161b22;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  background: #0d1117;
  color: white;
  border: 1px solid #30363d;
}
button {
  margin-top: 15px;
  padding: 10px;
  width: 100%;
  background: orange;
  border: none;
  cursor: pointer;
}
.result {
  margin-top: 15px;
  padding: 10px;
  background: #0d1117;
}
.tabs button {
  padding: 10px;
  margin-right: 5px;
}
.hidden { display: none; }
</style>
</head>

<body>

<h2>🛣️ ออกแบบโครงสร้างชั้นทาง</h2>

<div class="tabs">
  <button onclick="showTab('ac')">Flexible (AC)</button>
  <button onclick="showTab('rigid')">Rigid (Concrete)</button>
</div>

<!-- ================= FLEXIBLE ================= -->
<div id="ac" class="card">

<h3>Flexible Pavement (AASHTO 1993)</h3>

<label>W18 (ล้าน ESAL)</label>
<input id="w18" type="number" value="2.5">

<label>ZR</label>
<input id="zr" type="number" value="-1.282">

<label>So</label>
<input id="so" type="number" value="0.45">

<label>ΔPSI</label>
<input id="dpsi" type="number" value="1.7">

<label>MR (psi)</label>
<input id="mr" type="number" value="8000">

<button onclick="calcSN()">คำนวณ SN</button>

<div id="resultSN" class="result"></div>

</div>

<!-- ================= RIGID ================= -->
<div id="rigid" class="card hidden">

<h3>Rigid Pavement (อย่างง่าย)</h3>

<label>k (pci)</label>
<input id="k" type="number" value="100">

<label>โหลด (kN)</label>
<input id="load" type="number" value="40">

<button onclick="calcRigid()">คำนวณความหนา</button>

<div id="resultRigid" class="result"></div>

</div>

<script>

// ================= TAB =================
function showTab(tab) {
  document.getElementById("ac").classList.add("hidden");
  document.getElementById("rigid").classList.add("hidden");
  document.getElementById(tab).classList.remove("hidden");
}

// ================= FLEXIBLE =================
function calcSN() {
  let W18 = parseFloat(document.getElementById("w18").value) * 1000000;
  let ZR = parseFloat(document.getElementById("zr").value);
  let So = parseFloat(document.getElementById("so").value);
  let dpsi = parseFloat(document.getElementById("dpsi").value);
  let MR = parseFloat(document.getElementById("mr").value);

  // สูตร AASHTO (simplified)
  let logW = Math.log10(W18);

  let SN = (logW + ZR*So - Math.log10(dpsi/2.7)) / 0.4;

  document.getElementById("resultSN").innerHTML =
    "SN ≈ " + SN.toFixed(2);
}

// ================= RIGID =================
function calcRigid() {
  let k = parseFloat(document.getElementById("k").value);
  let load = parseFloat(document.getElementById("load").value);

  // สูตรง่าย (approx)
  let thickness = Math.pow(load / k, 0.5) * 10;

  document.getElementById("resultRigid").innerHTML =
    "ความหนาประมาณ ≈ " + thickness.toFixed(2) + " cm";
}

</script>

</body>
</html>
