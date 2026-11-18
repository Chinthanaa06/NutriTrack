const API = window.NUTRITRACK_API || "http://localhost:8000";
let chart;
const $ = id => document.getElementById(id);
async function request(path, options={}) {
  const response = await fetch(API + path, {headers:{"Content-Type":"application/json"}, ...options});
  if (!response.ok) {
    let detail = "Request failed";
    try { const data = await response.json(); detail = data.detail || detail; } catch {}
    throw new Error(detail);
  }
  return response.status === 204 ? null : response.json();
}
async function load() {
  try {
    const [summary, rows, ml] = await Promise.all([
      request("/api/summary"), request("/api/assessments"), request("/api/ml/status")
    ]);
    $("total").textContent = summary.total_assessments;
    $("young").textContent = summary.under_20_records;
    $("adult").textContent = summary.adult_records;
    $("ml-status").textContent = ml.message;
    $("records").innerHTML = rows.map(r => `<tr>
      <td>${escapeHtml(r.participant_code)}</td><td>${r.age_years}</td><td>${r.bmi}</td>
      <td><span class="status">${escapeHtml(r.indicator_status.replaceAll("_"," "))}</span></td>
      <td>${new Date(r.created_at).toLocaleDateString()}</td>
      <td><button class="delete" data-id="${r.id}" aria-label="Delete record">Delete</button></td></tr>`).join("")
      || '<tr><td colspan="6">No records yet. Add a sample assessment to begin.</td></tr>';
    drawChart(rows);
  } catch (error) { $("form-message").textContent = "Cannot connect to API. Start the backend and refresh."; }
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function drawChart(rows) {
  const ordered = [...rows].reverse().slice(-12);
  if (chart) chart.destroy();
  chart = new Chart($("trend-chart"), {type:"line",data:{
    labels:ordered.map(r=>r.participant_code),
    datasets:[{label:"BMI measurement (descriptive)",data:ordered.map(r=>r.bmi),
      borderColor:"#258365",backgroundColor:"rgba(37,131,101,.12)",fill:true,tension:.3}]
  },options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
    scales:{y:{beginAtZero:false},x:{ticks:{maxRotation:0}}}}});
}
$("assessment-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = new FormData(event.target), data = Object.fromEntries(form.entries());
  ["age_years","height_cm","weight_kg","dietary_diversity","meals_per_day"].forEach(k=>{
    if(data[k] === "" || data[k] == null) data[k] = null; else data[k] = Number(data[k]);
  });
  try {
    await request("/api/assessments",{method:"POST",body:JSON.stringify(data)});
    $("form-message").textContent = "Assessment saved successfully.";
    event.target.reset(); await load();
  } catch(error) { $("form-message").textContent = error.message; }
});
$("records").addEventListener("click", async event => {
  const id = event.target.dataset.id;
  if(id && confirm("Delete this assessment record?")) {
    try { await request("/api/assessments/"+id,{method:"DELETE"}); await load(); }
    catch(error) { alert(error.message); }
  }
});
$("refresh").addEventListener("click",load);
load();
