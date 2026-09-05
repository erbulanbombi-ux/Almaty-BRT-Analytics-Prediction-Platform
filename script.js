const network = {
  'LRT-1': [['LRT-2', 3.2], ['LRT-3', 4.8]],
  'LRT-2': [['LRT-1', 3.2], ['LRT-3', 2.4], ['LRT-4', 3.6]],
  'LRT-3': [['LRT-1', 4.8], ['LRT-2', 2.4], ['LRT-4', 2.1], ['LRT-5', 4.2]],
  'LRT-4': [['LRT-2', 3.6], ['LRT-3', 2.1], ['LRT-5', 2.8]],
  'LRT-5': [['LRT-3', 4.2], ['LRT-4', 2.8], ['LRT-6', 3.5]],
  'LRT-6': [['LRT-5', 3.5]]
};

const stationPositions = { 'LRT-1': 8, 'LRT-2': 27, 'LRT-3': 46, 'LRT-4': 65, 'LRT-5': 82, 'LRT-6': 94 };
const $ = (id) => document.getElementById(id);

function dijkstra(start, end) {
  const distances = Object.fromEntries(Object.keys(network).map((station) => [station, Infinity]));
  const previous = {};
  distances[start] = 0;
  const queue = [[0, start]];
  while (queue.length) {
    queue.sort((a, b) => a[0] - b[0]);
    const [distance, station] = queue.shift();
    if (station === end) break;
    if (distance > distances[station]) continue;
    network[station].forEach(([neighbor, weight]) => {
      const candidate = distance + weight;
      if (candidate < distances[neighbor]) {
        distances[neighbor] = candidate;
        previous[neighbor] = station;
        queue.push([candidate, neighbor]);
      }
    });
  }
  const path = [end];
  while (path[0] !== start) path.unshift(previous[path[0]]);
  return { path, distance: distances[end] };
}

function renderNetwork(path) {
  const networkElement = $('network');
  networkElement.innerHTML = '<div class="rail"></div>';
  Object.entries(stationPositions).forEach(([station, position]) => {
    const node = document.createElement('div');
    node.className = `station ${path.includes(station) ? 'active' : ''}`;
    node.style.left = `${position}%`;
    node.innerHTML = `<span>${station.replace('LRT-', '')}</span><b>${station}</b>`;
    networkElement.appendChild(node);
  });
  path.forEach((station, index) => {
    if (index < path.length - 1) {
      const segment = document.createElement('i');
      segment.className = 'route-segment';
      segment.style.left = `${stationPositions[station]}%`;
      segment.style.width = `${stationPositions[path[index + 1]] - stationPositions[station]}%`;
      networkElement.appendChild(segment);
    }
  });
}

function updateRoute() {
  const result = dijkstra($('startStation').value, $('endStation').value);
  $('routePath').textContent = result.path.join(' → ');
  $('routeDistance').textContent = `${result.distance.toFixed(1)} км`;
  renderNetwork(result.path);
}

function updateSimulation() {
  const traffic = Number($('traffic').value);
  const demand = Number($('demand').value);
  const frequency = Number($('frequency').value);
  const delay = Math.max(0.2, 1.1 + traffic / 100 * 3.4 + demand / 100 * 2.1 + (30 - frequency) / 20 * 1.8);
  const travelTime = 22 + traffic / 100 * 5 + demand / 100 * 3 + (30 - frequency) / 20 * 2;
  const onTime = Math.max(5, Math.round((1 - delay / 12) * 100));
  $('trafficValue').textContent = `${traffic}%`;
  $('demandValue').textContent = `${demand}%`;
  $('frequencyValue').textContent = frequency;
  $('simDelay').innerHTML = `${delay.toFixed(2)} <small>min</small>`;
  $('travelTime').innerHTML = `${travelTime.toFixed(2)} <small>min</small>`;
  $('prediction').textContent = delay.toFixed(2);
  $('onTime').textContent = `${onTime}%`;
  $('meterFill').style.width = `${Math.min(100, delay / 10 * 100)}%`;
  $('delayBar').style.width = `${Math.min(100, delay / 10 * 100)}%`;
  $('timeBar').style.width = `${Math.min(100, travelTime / 35 * 100)}%`;
  $('scenarioLabel').textContent = traffic > 65 ? 'высокая нагрузка' : traffic < 30 ? 'свободный поток' : 'смешанный поток';
  updateModelPrediction(traffic, demand, frequency);
}

async function updateModelPrediction(traffic, demand, frequency) {
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        elevation_slope_deg: 2.5,
        lane_isolation_score: 0.85,
        turning_conflicts: Math.max(1, Math.round(traffic / 15)),
        passenger_density: 20 + demand * 0.8,
        delay_lag_15m: 1.2,
        delay_lag_30m: 0.8,
        corridor_id: 'LRT-1',
        weather_impact: 'clear',
        is_peak_hour: traffic > 60 ? 1 : 0
      })
    });
    if (!response.ok) return;
    const result = await response.json();
    $('prediction').textContent = Number(result.predicted_delay_minutes).toFixed(2);
  } catch (error) {
    // Static demo keeps its local simulation when the API is offline.
  }
}

['traffic', 'demand', 'frequency'].forEach((id) => $(id).addEventListener('input', updateSimulation));
['startStation', 'endStation'].forEach((id) => $(id).addEventListener('change', updateRoute));
$('resetButton').addEventListener('click', () => {
  $('traffic').value = 45;
  $('demand').value = 50;
  $('frequency').value = 15;
  updateSimulation();
});

updateRoute();
updateSimulation();
