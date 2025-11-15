async function ask() {
  const question = document.getElementById("query").value;
  const res = await fetch("http://127.0.0.1:8000/health");
  const data = await res.json();
  document.getElementById("response").innerText = JSON.stringify(data, null, 2);
}
