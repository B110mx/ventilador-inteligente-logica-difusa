"use strict";

const MIN_TEMPERATURE = 10;
const MAX_TEMPERATURE = 40;
const COLORS = { cold: "#2e86de", mild: "#10ac84", hot: "#ee5253", speed: "#7d3c98" };

function coldMembership(t) {
  if (t <= 18) return 1;
  if (t >= 24) return 0;
  return (24 - t) / 6;
}

function mildMembership(t) {
  if (t <= 18 || t >= 34) return 0;
  if (t <= 26) return (t - 18) / 8;
  return (34 - t) / 8;
}

function hotMembership(t) {
  if (t <= 28) return 0;
  if (t >= 36) return 1;
  return (t - 28) / 8;
}

function dryMembership(h) { if (h <= 30) return 1; if (h >= 50) return 0; return (50 - h) / 20; }
function comfortableHumidityMembership(h) { if (h <= 30 || h >= 70) return 0; return h <= 50 ? (h - 30) / 20 : (70 - h) / 20; }
function humidMembership(h) { if (h <= 50) return 0; if (h >= 70) return 1; return (h - 50) / 20; }

function calculateSpeed(t, humidity = 50) {
  const cold = coldMembership(t);
  const mild = mildMembership(t);
  const hot = hotMembership(t);
  const total = cold + mild + hot;
  const baseSpeed = total === 0 ? 0 : (cold * 0 + mild * 50 + hot * 100) / total;
  const dry = dryMembership(humidity);
  const comfortable = comfortableHumidityMembership(humidity);
  const humid = humidMembership(humidity);
  const humidityTotal = dry + comfortable + humid;
  const adjustment = humidityTotal === 0 ? 0 : (dry * -5 + humid * 10) / humidityTotal;
  const speed = Math.max(0, Math.min(100, baseSpeed + adjustment));
  return { speed, cold, mild, hot, dry, comfortable, humid, adjustment };
}

function parseTemperature(value) {
  const normalized = String(value).trim().replace(",", ".");
  if (!normalized) throw new Error("Ingrese una temperatura.");
  const temperature = Number(normalized);
  if (!Number.isFinite(temperature)) throw new Error("Ingrese una temperatura numérica válida.");
  if (temperature < MIN_TEMPERATURE || temperature > MAX_TEMPERATURE) {
    throw new Error(`La temperatura debe estar entre ${MIN_TEMPERATURE} y ${MAX_TEMPERATURE} °C.`);
  }
  return temperature;
}

function parseHumidity(value) {
  const normalized = String(value).trim().replace(",", ".");
  if (!normalized) throw new Error("Ingrese la humedad relativa.");
  const humidity = Number(normalized);
  if (!Number.isFinite(humidity) || humidity < 0 || humidity > 100) throw new Error("La humedad debe estar entre 0 y 100 %.");
  return humidity;
}

const elements = {
  form: document.querySelector("#temperature-form"),
  input: document.querySelector("#temperature"),
  humidity: document.querySelector("#humidity"),
  city: document.querySelector("#city"),
  error: document.querySelector("#temperature-error"),
  speed: document.querySelector("#speed-value"),
  level: document.querySelector("#speed-level"),
  gauge: document.querySelector("#gauge-value"),
  values: {
    cold: document.querySelector("#cold-value"),
    mild: document.querySelector("#mild-value"),
    hot: document.querySelector("#hot-value")
  },
  bars: {
    cold: document.querySelector("#cold-bar"),
    mild: document.querySelector("#mild-bar"),
    hot: document.querySelector("#hot-bar")
  },
  weatherButton: document.querySelector("#weather-button"),
  autoUpdate: document.querySelector("#auto-update"),
  weatherStatus: document.querySelector("#weather-status"),
  tabs: {
    control: document.querySelector("#control-tab"),
    simulator: document.querySelector("#simulator-tab")
  },
  views: {
    control: document.querySelector("#control-view"),
    simulator: document.querySelector("#simulator-view")
  },
  simulatorWeatherButton: document.querySelector("#simulator-weather-button"),
  classroom: document.querySelector("#classroom"),
  fanBlades: document.querySelector("#fan-blades"),
  simTemperature: document.querySelector("#sim-temperature"),
  simHumidity: document.querySelector("#sim-humidity"),
  simSpeed: document.querySelector("#sim-speed"),
  simState: document.querySelector("#sim-state"),
  simExplanation: document.querySelector("#sim-explanation"),
  simRules: {
    cold: document.querySelector("#sim-cold"),
    mild: document.querySelector("#sim-mild"),
    hot: document.querySelector("#sim-hot")
  },
  historyBody: document.querySelector("#history-body"),
  clearHistory: document.querySelector("#clear-history")
};

let selectedTemperature = null;
let selectedHumidity = 50;
let automaticTimer = null;

function speedLevel(speed) {
  if (speed === 0) return "Ventilador apagado";
  if (speed < 50) return "Ventilación baja";
  if (speed < 80) return "Ventilación media";
  return "Ventilación alta";
}

function speedColor(speed) {
  if (speed < 40) return COLORS.cold;
  if (speed < 75) return COLORS.mild;
  return COLORS.hot;
}

const decisionHistory = [];

function updateResult(temperature, humidity = 50, source = "Manual", record = true) {
  const result = calculateSpeed(temperature, humidity);
  selectedTemperature = temperature;
  selectedHumidity = humidity;
  elements.speed.textContent = `${result.speed.toFixed(2)}%`;
  elements.level.textContent = `${speedLevel(result.speed)} a ${temperature.toFixed(1)} °C y ${humidity.toFixed(0)} % de humedad`;
  elements.gauge.style.strokeDasharray = `${result.speed} 100`;
  elements.gauge.style.stroke = speedColor(result.speed);

  ["cold", "mild", "hot"].forEach((key) => {
    elements.values[key].textContent = result[key].toFixed(2);
    elements.bars[key].style.width = `${result[key] * 100}%`;
  });

  drawAllCharts();
  updateSimulator(temperature, humidity, result);
  if (record) addHistory(source, temperature, humidity, result.speed);
}

function updateSimulator(temperature, humidity, result) {
  const state = speedLevel(result.speed);
  elements.simTemperature.textContent = `${temperature.toFixed(1)} °C`;
  elements.simHumidity.textContent = `${humidity.toFixed(0)} %`;
  elements.simSpeed.textContent = `${result.speed.toFixed(1)} %`;
  elements.simState.textContent = state;
  elements.simRules.cold.textContent = `Fría: ${(result.cold * 100).toFixed(0)} %`;
  elements.simRules.mild.textContent = `Templada: ${(result.mild * 100).toFixed(0)} %`;
  elements.simRules.hot.textContent = `Caliente: ${(result.hot * 100).toFixed(0)} %`;
  elements.classroom.classList.toggle("running", result.speed > 0);
  elements.fanBlades.style.animationDuration = result.speed > 0
    ? `${Math.max(.18, 1.5 - result.speed * .012)}s`
    : "0s";
  elements.simExplanation.textContent = result.speed === 0
    ? `A ${temperature.toFixed(1)} °C predomina la regla fría. La humedad de ${humidity.toFixed(0)} % no requiere aumentar la ventilación.`
    : `A ${temperature.toFixed(1)} °C las reglas de temperatura producen una velocidad base y la humedad de ${humidity.toFixed(0)} % aplica un ajuste de ${result.adjustment.toFixed(1)} puntos. El resultado es ${result.speed.toFixed(1)} %.`;
}

function addHistory(source, temperature, humidity, speed) {
  decisionHistory.unshift({ time: new Date().toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"}), source, temperature, humidity, speed });
  decisionHistory.splice(8);
  elements.historyBody.innerHTML = decisionHistory.map((item) => `<tr><td>${item.time}</td><td>${item.source}</td><td>${item.temperature.toFixed(1)} °C</td><td>${item.humidity.toFixed(0)} %</td><td>${item.speed.toFixed(1)} %</td></tr>`).join("");
}

elements.clearHistory.addEventListener("click", () => {
  decisionHistory.length = 0;
  elements.historyBody.innerHTML = '<tr class="empty-history"><td colspan="5">Todavía no hay cálculos registrados.</td></tr>';
});

function showView(name) {
  Object.keys(elements.views).forEach((key) => {
    const active = key === name;
    elements.views[key].hidden = !active;
    elements.tabs[key].classList.toggle("active", active);
    elements.tabs[key].setAttribute("aria-selected", String(active));
  });
  if (name === "control") drawAllCharts();
}

elements.tabs.control.addEventListener("click", () => showView("control"));
elements.tabs.simulator.addEventListener("click", () => showView("simulator"));

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  elements.error.textContent = "";
  elements.input.removeAttribute("aria-invalid");
  try {
    updateResult(parseTemperature(elements.input.value), parseHumidity(elements.humidity.value));
  } catch (error) {
    elements.error.textContent = error.message;
    elements.input.setAttribute("aria-invalid", "true");
    elements.input.focus();
  }
});

async function getCoordinates(city) {
  if (city) {
    const params = new URLSearchParams({ name: city, count: "1", language: "es", format: "json" });
    const response = await fetch(`https://geocoding-api.open-meteo.com/v1/search?${params}`);
    if (!response.ok) throw new Error("No fue posible buscar la ciudad.");
    const data = await response.json();
    if (!data.results || !data.results.length) throw new Error("No se encontró la ciudad indicada.");
    const match = data.results[0];
    return { latitude: match.latitude, longitude: match.longitude, location: `${match.name}${match.admin1 ? `, ${match.admin1}` : ""}` };
  }
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      resolve({ latitude: 18.4615, longitude: -97.3928, location: "Tehuacán, Puebla" });
      return;
    }
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => resolve({ latitude: coords.latitude, longitude: coords.longitude, location: "ubicación actual" }),
      () => resolve({ latitude: 18.4615, longitude: -97.3928, location: "Tehuacán, Puebla" }),
      { enableHighAccuracy: false, timeout: 6000, maximumAge: 600000 }
    );
  });
}

async function updateFromWeather() {
  elements.weatherButton.disabled = true;
  elements.weatherButton.textContent = "Consultando Open-Meteo...";
  elements.error.textContent = "";
  try {
    const place = await getCoordinates(elements.city.value.trim());
    const params = new URLSearchParams({
      latitude: place.latitude,
      longitude: place.longitude,
      current: "temperature_2m,relative_humidity_2m",
      timezone: "auto"
    });
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`);
    if (!response.ok) throw new Error("La API meteorológica no respondió correctamente.");
    const data = await response.json();
    const temperature = parseTemperature(data.current.temperature_2m);
    const humidity = parseHumidity(data.current.relative_humidity_2m);
    elements.input.value = temperature.toFixed(1);
    elements.humidity.value = humidity.toFixed(0);
    updateResult(temperature, humidity, `Open-Meteo · ${place.location}`);
    const observedAt = String(data.current.time || "").replace("T", " ");
    elements.weatherStatus.textContent = `Open-Meteo · ${place.location} · ${observedAt}`;
  } catch (error) {
    elements.error.textContent = `${error.message} Puedes continuar en modo manual.`;
    elements.autoUpdate.checked = false;
    window.clearInterval(automaticTimer);
  } finally {
    elements.weatherButton.disabled = false;
    elements.weatherButton.textContent = "Actualizar temperatura actual";
  }
}

elements.weatherButton.addEventListener("click", updateFromWeather);
elements.simulatorWeatherButton.addEventListener("click", async () => {
  elements.simulatorWeatherButton.disabled = true;
  elements.simulatorWeatherButton.textContent = "Consultando clima...";
  await updateFromWeather();
  elements.simulatorWeatherButton.disabled = false;
  elements.simulatorWeatherButton.textContent = "Actualizar clima y simular";
});
elements.autoUpdate.addEventListener("change", () => {
  window.clearInterval(automaticTimer);
  if (elements.autoUpdate.checked) {
    updateFromWeather();
    automaticTimer = window.setInterval(updateFromWeather, 600000);
  } else {
    elements.weatherStatus.textContent = "Modo manual. La API utiliza la temperatura exterior.";
  }
});

function chartContext(id) {
  const canvas = document.getElementById(id);
  const width = Math.max(300, canvas.clientWidth);
  const height = Number(canvas.getAttribute("height")) || 290;
  const ratio = window.devicePixelRatio || 1;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  const ctx = canvas.getContext("2d");
  ctx.scale(ratio, ratio);
  return { ctx, width, height };
}

function basePlot(id, xMin, xMax, yMin, yMax, xLabel, yLabel) {
  const { ctx, width, height } = chartContext(id);
  const margin = { left: 54, right: 18, top: 18, bottom: 46 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const x = (value) => margin.left + ((value - xMin) / (xMax - xMin)) * plotWidth;
  const y = (value) => margin.top + plotHeight - ((value - yMin) / (yMax - yMin)) * plotHeight;

  ctx.clearRect(0, 0, width, height);
  ctx.font = "11px Arial";
  ctx.fillStyle = "#5e6d79";
  ctx.strokeStyle = "#e2e8ec";
  ctx.lineWidth = 1;

  for (let i = 0; i <= 5; i += 1) {
    const value = yMin + ((yMax - yMin) * i) / 5;
    const py = y(value);
    ctx.beginPath(); ctx.moveTo(margin.left, py); ctx.lineTo(width - margin.right, py); ctx.stroke();
    ctx.textAlign = "right"; ctx.fillText(value.toFixed(yMax <= 1.2 ? 1 : 0), margin.left - 8, py + 4);
  }
  for (let i = 0; i <= 6; i += 1) {
    const value = xMin + ((xMax - xMin) * i) / 6;
    const px = x(value);
    ctx.beginPath(); ctx.moveTo(px, margin.top); ctx.lineTo(px, margin.top + plotHeight); ctx.stroke();
    ctx.textAlign = "center"; ctx.fillText(value.toFixed(0), px, height - 25);
  }

  ctx.strokeStyle = "#8997a2";
  ctx.beginPath(); ctx.moveTo(margin.left, margin.top); ctx.lineTo(margin.left, margin.top + plotHeight); ctx.lineTo(width - margin.right, margin.top + plotHeight); ctx.stroke();
  ctx.textAlign = "center"; ctx.fillText(xLabel, margin.left + plotWidth / 2, height - 4);
  ctx.save(); ctx.translate(13, margin.top + plotHeight / 2); ctx.rotate(-Math.PI / 2); ctx.fillText(yLabel, 0, 0); ctx.restore();
  return { ctx, x, y, width, height, margin, plotWidth, plotHeight };
}

function drawLine(plot, points, color, width = 2.5) {
  plot.ctx.beginPath();
  points.forEach(([px, py], index) => {
    const command = index === 0 ? "moveTo" : "lineTo";
    plot.ctx[command](plot.x(px), plot.y(py));
  });
  plot.ctx.strokeStyle = color;
  plot.ctx.lineWidth = width;
  plot.ctx.stroke();
}

function valuesBetween(min, max, step) {
  const values = [];
  for (let value = min; value <= max + step / 2; value += step) values.push(value);
  return values;
}

function drawMembershipChart() {
  const plot = basePlot("membership-chart", 10, 40, 0, 1, "Temperatura (°C)", "Pertenencia");
  const temperatures = valuesBetween(10, 40, .25);
  drawLine(plot, temperatures.map((t) => [t, coldMembership(t)]), COLORS.cold);
  drawLine(plot, temperatures.map((t) => [t, mildMembership(t)]), COLORS.mild);
  drawLine(plot, temperatures.map((t) => [t, hotMembership(t)]), COLORS.hot);
  if (selectedTemperature !== null && selectedTemperature >= 10 && selectedTemperature <= 40) {
    plot.ctx.setLineDash([5, 4]); plot.ctx.strokeStyle = "#1d2935"; plot.ctx.lineWidth = 1.5;
    plot.ctx.beginPath(); plot.ctx.moveTo(plot.x(selectedTemperature), plot.y(0)); plot.ctx.lineTo(plot.x(selectedTemperature), plot.y(1)); plot.ctx.stroke();
    plot.ctx.setLineDash([]);
  }
}

function drawActivationChart() {
  const plot = basePlot("activation-chart", 0, 3, 0, 1, "Reglas", "Activación");
  const result = selectedTemperature === null ? { cold: 0, mild: 0, hot: 0 } : calculateSpeed(selectedTemperature, selectedHumidity);
  const data = [[.5, result.cold, COLORS.cold, "Fría"], [1.5, result.mild, COLORS.mild, "Templada"], [2.5, result.hot, COLORS.hot, "Caliente"]];
  const barWidth = Math.min(80, plot.plotWidth / 5);
  plot.ctx.font = "11px Arial";
  data.forEach(([position, value, color, label]) => {
    const left = plot.x(position) - barWidth / 2;
    const top = plot.y(value);
    plot.ctx.fillStyle = color; plot.ctx.fillRect(left, top, barWidth, plot.y(0) - top);
    plot.ctx.fillStyle = "#1d2935"; plot.ctx.textAlign = "center";
    plot.ctx.fillText(value.toFixed(2), plot.x(position), Math.max(14, top - 7));
    plot.ctx.fillText(label, plot.x(position), plot.height - 25);
  });
}

function drawResponseChart() {
  const plot = basePlot("response-chart", 10, 40, 0, 100, "Temperatura (°C)", "Ventilación (%)");
  const temperatures = valuesBetween(10, 40, .25);
  drawLine(plot, temperatures.map((t) => [t, calculateSpeed(t, selectedHumidity).speed]), COLORS.speed, 2.7);
  if (selectedTemperature !== null && selectedTemperature >= 10 && selectedTemperature <= 40) {
    const result = calculateSpeed(selectedTemperature, selectedHumidity);
    plot.ctx.beginPath(); plot.ctx.arc(plot.x(selectedTemperature), plot.y(result.speed), 5.5, 0, Math.PI * 2);
    plot.ctx.fillStyle = "#1d2935"; plot.ctx.fill();
  }
}

function drawAllCharts() {
  drawMembershipChart();
  drawActivationChart();
  drawResponseChart();
}

let resizeTimer;
window.addEventListener("resize", () => {
  window.clearTimeout(resizeTimer);
  resizeTimer = window.setTimeout(drawAllCharts, 120);
});

drawAllCharts();
