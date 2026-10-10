"use strict";

const MIN_TEMPERATURE = 10;
const MAX_TEMPERATURE = 40;
const COLORS = { cold: "#2e86de", mild: "#10ac84", hot: "#ee5253", speed: "#7d3c98" };

function coldMembership(t) {
  return t < 20 ? 1 : 0;
}

function mildMembership(t) {
  if (t < 20 || t >= 40) return 0;
  return (40 - t) / 20;
}

function hotMembership(t) {
  if (t <= 20) return 0;
  if (t >= 40) return 1;
  return (t - 20) / 20;
}

function calculateSpeed(t) {
  const cold = coldMembership(t);
  const mild = mildMembership(t);
  const hot = hotMembership(t);
  const total = cold + mild + hot;
  const speed = total === 0 ? 0 : (cold * 0 + mild * 25 + hot * 100) / total;
  return { speed, cold, mild, hot };
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

const elements = {
  form: document.querySelector("#temperature-form"),
  input: document.querySelector("#temperature"),
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
  simSpeed: document.querySelector("#sim-speed"),
  simState: document.querySelector("#sim-state"),
  simExplanation: document.querySelector("#sim-explanation"),
  simRules: {
    cold: document.querySelector("#sim-cold"),
    mild: document.querySelector("#sim-mild"),
    hot: document.querySelector("#sim-hot")
  }
};

let selectedTemperature = null;
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

function updateResult(temperature) {
  const result = calculateSpeed(temperature);
  selectedTemperature = temperature;
  elements.speed.textContent = `${result.speed.toFixed(2)}%`;
  elements.level.textContent = `${speedLevel(result.speed)} para un salón a ${temperature.toFixed(1)} °C`;
  elements.gauge.style.strokeDasharray = `${result.speed} 100`;
  elements.gauge.style.stroke = speedColor(result.speed);

  ["cold", "mild", "hot"].forEach((key) => {
    elements.values[key].textContent = result[key].toFixed(2);
    elements.bars[key].style.width = `${result[key] * 100}%`;
  });

  drawAllCharts();
  updateSimulator(temperature, result);
}

function updateSimulator(temperature, result) {
  const state = speedLevel(result.speed);
  elements.simTemperature.textContent = `${temperature.toFixed(1)} °C`;
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
    ? `A ${temperature.toFixed(1)} °C predomina la regla fría. El sistema mantiene el ventilador apagado.`
    : `A ${temperature.toFixed(1)} °C se activan las reglas con distintos grados. Su promedio ponderado recomienda ${result.speed.toFixed(1)} % de ventilación.`;
}

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
    updateResult(parseTemperature(elements.input.value));
  } catch (error) {
    elements.error.textContent = error.message;
    elements.input.setAttribute("aria-invalid", "true");
    elements.input.focus();
  }
});

function getCoordinates() {
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
    const place = await getCoordinates();
    const params = new URLSearchParams({
      latitude: place.latitude,
      longitude: place.longitude,
      current: "temperature_2m",
      timezone: "auto"
    });
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`);
    if (!response.ok) throw new Error("La API meteorológica no respondió correctamente.");
    const data = await response.json();
    const temperature = parseTemperature(data.current.temperature_2m);
    elements.input.value = temperature.toFixed(1);
    updateResult(temperature);
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
  const result = selectedTemperature === null ? { cold: 0, mild: 0, hot: 0 } : calculateSpeed(selectedTemperature);
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
  drawLine(plot, temperatures.map((t) => [t, calculateSpeed(t).speed]), COLORS.speed, 2.7);
  if (selectedTemperature !== null && selectedTemperature >= 10 && selectedTemperature <= 40) {
    const result = calculateSpeed(selectedTemperature);
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
