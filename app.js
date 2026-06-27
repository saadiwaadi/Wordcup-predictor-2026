// app.js - Controller for ORACLE-26 UI and Event Handling
import { TEAMS, reloadTeams, getH2H } from './data/index.js';
import { runPrediction } from './engine.js';
import { runLiveBacktest } from './js/verificationEngine.js';
import { getCache } from './data/openFootballLayer.js';
import { runPreMatchFlags } from './engine/preMatchFlags.js';
import { deltaUpdateTeam } from './data/deltaSync.js';
import { enrichMatchup, getLambdaOverride, recomputeScorelines } from './data/enrichTeam.js';
import { getTeamForm, getTeamSquad, getTopScorers, getTeamCleanSheets } from './data/openFootballLayer.js';
import { normalizeName, getCompletedFixtures, getUpcomingFixtures, getMatchEvents, initScrapedData } from './data/scrapedAdapter.js';




const TACTICAL_ICONS = {
  empty: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><circle cx="5" cy="5" r="4" fill="none" stroke="currentColor" stroke-width="1"/></svg>`,
  active: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><circle cx="5" cy="5" r="4" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="5" cy="5" r="1.8" fill="currentColor"/></svg>`,
  selected: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><circle cx="5" cy="5" r="4" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="5" cy="5" r="2.5" fill="none" stroke="currentColor" stroke-dasharray="1.5 1" stroke-width="0.8"/><circle cx="5" cy="5" r="1" fill="currentColor"/></svg>`,
  captain: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><circle cx="5" cy="5" r="4" fill="none" stroke="currentColor" stroke-width="1"/><line x1="5" y1="2.5" x2="5" y2="7.5" stroke="currentColor" stroke-width="1"/><line x1="2.5" y1="5" x2="7.5" y2="5" stroke="currentColor" stroke-width="1"/></svg>`,
  warning: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><polygon points="5,2 8.5,8 1.5,8" fill="none" stroke="currentColor" stroke-width="1"/></svg>`,
  locked: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><rect x="2" y="2" width="6" height="6" fill="none" stroke="currentColor" stroke-width="1"/><rect x="4" y="4" width="2" height="2" fill="currentColor"/></svg>`,
  loading: `<svg class="tactical-icon spin" viewBox="0 0 10 10" width="10" height="10"><circle cx="5" cy="5" r="4" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="6 4"/></svg>`,
  intelligence: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><polygon points="5,1.5 8.5,5 5,8.5 1.5,5" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="5" cy="5" r="1.2" fill="currentColor"/></svg>`,
  simulation: `<svg class="tactical-icon" viewBox="0 0 10 10" width="10" height="10"><polyline points="1.5,5 3,5 4,2 6,8 7,5 8.5,5" fill="none" stroke="currentColor" stroke-width="1"/></svg>`
};

document.addEventListener("DOMContentLoaded", () => {
  // Load match events keyed by FIFA ID into window cache
  fetch('/data/scraped/match_events.json')
    .then(r => r.json())
    .then(d => { window._allMatchEvents = d; })
    .catch(() => { window._allMatchEvents = {}; });

  const FORMATIONS = {
    "4-3-3": {
      label: "4-3-3",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 22, y: 48 },
        { pos: "DF", x: 68, y: 48 },
        { pos: "DF", x: 132, y: 48 },
        { pos: "DF", x: 178, y: 48 },
        { pos: "MF", x: 44, y: 88 },
        { pos: "MF", x: 100, y: 88 },
        { pos: "MF", x: 156, y: 88 },
        { pos: "FW", x: 28, y: 125 },
        { pos: "FW", x: 100, y: 125 },
        { pos: "FW", x: 172, y: 125 },
      ]
    },
    "4-2-3-1": {
      label: "4-2-3-1",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 22, y: 48 },
        { pos: "DF", x: 68, y: 48 },
        { pos: "DF", x: 132, y: 48 },
        { pos: "DF", x: 178, y: 48 },
        { pos: "MF", x: 65, y: 78 },
        { pos: "MF", x: 135, y: 78 },
        { pos: "MF", x: 28, y: 98 },
        { pos: "MF", x: 100, y: 98 },
        { pos: "MF", x: 172, y: 98 },
        { pos: "FW", x: 100, y: 125 },
      ]
    },
    "4-4-2": {
      label: "4-4-2",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 22, y: 48 },
        { pos: "DF", x: 68, y: 48 },
        { pos: "DF", x: 132, y: 48 },
        { pos: "DF", x: 178, y: 48 },
        { pos: "MF", x: 28, y: 88 },
        { pos: "MF", x: 76, y: 88 },
        { pos: "MF", x: 124, y: 88 },
        { pos: "MF", x: 172, y: 88 },
        { pos: "FW", x: 65, y: 125 },
        { pos: "FW", x: 135, y: 125 },
      ]
    },
    "3-5-2": {
      label: "3-5-2",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 44, y: 48 },
        { pos: "DF", x: 100, y: 48 },
        { pos: "DF", x: 156, y: 48 },
        { pos: "MF", x: 16, y: 88 },
        { pos: "MF", x: 58, y: 88 },
        { pos: "MF", x: 100, y: 88 },
        { pos: "MF", x: 142, y: 88 },
        { pos: "MF", x: 184, y: 88 },
        { pos: "FW", x: 65, y: 125 },
        { pos: "FW", x: 135, y: 125 },
      ]
    },
    "3-4-3": {
      label: "3-4-3",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 44, y: 48 },
        { pos: "DF", x: 100, y: 48 },
        { pos: "DF", x: 156, y: 48 },
        { pos: "MF", x: 28, y: 88 },
        { pos: "MF", x: 76, y: 88 },
        { pos: "MF", x: 124, y: 88 },
        { pos: "MF", x: 172, y: 88 },
        { pos: "FW", x: 28, y: 125 },
        { pos: "FW", x: 100, y: 125 },
        { pos: "FW", x: 172, y: 125 },
      ]
    },
    "5-3-2": {
      label: "5-3-2",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 16, y: 48 },
        { pos: "DF", x: 58, y: 48 },
        { pos: "DF", x: 100, y: 48 },
        { pos: "DF", x: 142, y: 48 },
        { pos: "DF", x: 184, y: 48 },
        { pos: "MF", x: 44, y: 88 },
        { pos: "MF", x: 100, y: 88 },
        { pos: "MF", x: 156, y: 88 },
        { pos: "FW", x: 65, y: 125 },
        { pos: "FW", x: 135, y: 125 },
      ]
    },
    "4-5-1": {
      label: "4-5-1",
      slots: [
        { pos: "GK", x: 100, y: 15 },
        { pos: "DF", x: 22, y: 48 },
        { pos: "DF", x: 68, y: 48 },
        { pos: "DF", x: 132, y: 48 },
        { pos: "DF", x: 178, y: 48 },
        { pos: "MF", x: 16, y: 88 },
        { pos: "MF", x: 58, y: 88 },
        { pos: "MF", x: 100, y: 88 },
        { pos: "MF", x: 142, y: 88 },
        { pos: "MF", x: 184, y: 88 },
        { pos: "FW", x: 100, y: 125 },
      ]
    }
  };

  let lineupState = {
    teamA: {
      code: '',
      formation: '4-3-3',
      players: [],
      starters: [],
      bench: []
    },
    teamB: {
      code: '',
      formation: '4-3-3',
      players: [],
      starters: [],
      bench: []
    },
    modified: false,
    selectedPlayer: null
  };

  function initializeLineupState(teamCode, rawSquad, teamKey) {
    const players = rawSquad.map(p => ({
      ...p,
      isStarter: p.starter !== undefined ? p.starter : false
    }));
    lineupState[teamKey] = {
      code: teamCode,
      formation: lineupState[teamKey].formation || '4-3-3',
      players: players,
      starters: players.filter(p => p.isStarter),
      bench: players.filter(p => !p.isStarter)
    };
    adjustStartersForFormation(lineupState[teamKey], lineupState[teamKey].formation);
  }

  function adjustStartersForFormation(teamState, targetFormation) {
    const formation = FORMATIONS[targetFormation];
    if (!formation) return;

    teamState.formation = targetFormation;

    const gkSlots = formation.slots.filter(s => s.pos === "GK");
    const dfSlots = formation.slots.filter(s => s.pos === "DF");
    const mfSlots = formation.slots.filter(s => s.pos === "MF");
    const fwSlots = formation.slots.filter(s => s.pos === "FW");

    const requiredGK = gkSlots.length;
    const requiredDF = dfSlots.length;
    const requiredMF = mfSlots.length;
    const requiredFW = fwSlots.length;

    function adjustPositionGroup(posGroup, requiredCount) {
      const currentStarters = teamState.players.filter(p => p.isStarter && p.posGroup === posGroup);

      if (currentStarters.length < requiredCount) {
        const needed = requiredCount - currentStarters.length;
        const benchPlayers = teamState.players.filter(p => !p.isStarter && p.posGroup === posGroup);
        benchPlayers.sort((a, b) => a.number - b.number);

        for (let i = 0; i < Math.min(needed, benchPlayers.length); i++) {
          benchPlayers[i].isStarter = true;
        }
      } else if (currentStarters.length > requiredCount) {
        const extra = currentStarters.length - requiredCount;
        currentStarters.sort((a, b) => b.number - a.number);

        for (let i = 0; i < Math.min(extra, currentStarters.length); i++) {
          currentStarters[i].isStarter = false;
        }
      }
    }

    adjustPositionGroup("GOALKEEPERS", requiredGK);
    adjustPositionGroup("DEFENDERS", requiredDF);
    adjustPositionGroup("MIDFIELDERS", requiredMF);
    adjustPositionGroup("FORWARDS", requiredFW);

    teamState.starters = teamState.players.filter(p => p.isStarter);
    teamState.bench = teamState.players.filter(p => !p.isStarter);
  }

  function getStartersCoords(starters, formationKey, isTeamB) {
    const formation = FORMATIONS[formationKey];
    if (!formation) return new Map();

    const gkSlots = formation.slots.filter(s => s.pos === "GK");
    const dfSlots = formation.slots.filter(s => s.pos === "DF");
    const mfSlots = formation.slots.filter(s => s.pos === "MF");
    const fwSlots = formation.slots.filter(s => s.pos === "FW");

    gkSlots.sort((a, b) => a.x - b.x);
    dfSlots.sort((a, b) => a.x - b.x);
    mfSlots.sort((a, b) => a.x - b.x);
    fwSlots.sort((a, b) => a.x - b.x);

    const gks = starters.filter(p => p.posGroup === 'GOALKEEPERS');
    const dfs = starters.filter(p => p.posGroup === 'DEFENDERS');
    const mfs = starters.filter(p => p.posGroup === 'MIDFIELDERS');
    const fws = starters.filter(p => p.posGroup === 'FORWARDS');

    const coords = new Map();

    gks.forEach((p, idx) => {
      const slot = gkSlots[idx] || gkSlots[0];
      if (slot) {
        coords.set(p.name, {
          x: slot.x,
          y: isTeamB ? (295 - slot.y) : slot.y
        });
      }
    });

    dfs.forEach((p, idx) => {
      const slot = dfSlots[idx] || dfSlots[0];
      if (slot) {
        coords.set(p.name, {
          x: slot.x,
          y: isTeamB ? (295 - slot.y) : slot.y
        });
      }
    });

    mfs.forEach((p, idx) => {
      const slot = mfSlots[idx] || mfSlots[0];
      if (slot) {
        coords.set(p.name, {
          x: slot.x,
          y: isTeamB ? (295 - slot.y) : slot.y
        });
      }
    });

    fws.forEach((p, idx) => {
      const slot = fwSlots[idx] || fwSlots[0];
      if (slot) {
        coords.set(p.name, {
          x: slot.x,
          y: isTeamB ? (295 - slot.y) : slot.y
        });
      }
    });

    return coords;
  }

  function selectPlayer(player, teamSide, rowElement) {
    clearPlayerSelection();

    lineupState.selectedPlayer = {
      teamSide,
      name: player.name,
      number: player.number,
      pos: player.pos,
      posGroup: player.posGroup,
      isStarter: player.isStarter,
      element: rowElement
    };

    rowElement.classList.add("selected");
    const teamColor = teamSide === 'a' ? '#22c55e' : '#3b82f6';
    const bgColor = teamSide === 'a' ? '#0a1a0a' : '#080d14';
    rowElement.style.background = bgColor;
    rowElement.style.borderLeft = `2px solid ${teamColor}`;
    rowElement.style.color = teamColor;

    // Trigger pitch redraw to display selection ring
    renderSquadAnalysis();

    // Highlight candidates
    const team = lineupState[teamSide === 'a' ? 'teamA' : 'teamB'];
    const candidates = team.players.filter(p => p.isStarter !== player.isStarter && p.posGroup === player.posGroup);

    candidates.forEach(c => {
      const candidateRow = findRowElement(c.name, teamSide);
      if (candidateRow) {
        candidateRow.classList.add("swap-candidate");
        candidateRow.style.borderLeft = "2px solid #f59e0b44";
        candidateRow.style.color = "#f59e0b";

        if (!candidateRow.querySelector(".swap-label")) {
          const swapLabel = document.createElement("span");
          swapLabel.className = "swap-label";
          swapLabel.style.cssText = "font-size: 8px; color: #f59e0b; margin-left: auto; padding-left: 6px;";
          swapLabel.textContent = "[SWAP]";
          candidateRow.appendChild(swapLabel);
        }
      }
    });
  }

  function clearPlayerSelection() {
    if (!lineupState.selectedPlayer) return;

    document.querySelectorAll(".squad-player-row").forEach(row => {
      row.classList.remove("selected", "swap-candidate");
      row.style.background = "";
      row.style.borderLeft = "";
      row.style.color = "";
      const swapLabel = row.querySelector(".swap-label");
      if (swapLabel) swapLabel.remove();
    });

    lineupState.selectedPlayer = null;
    renderSquadAnalysis();
  }

  function swapPlayers(p1Name, p2Name, teamSide) {
    const team = lineupState[teamSide === 'a' ? 'teamA' : 'teamB'];
    const player1 = team.players.find(p => p.name === p1Name);
    const player2 = team.players.find(p => p.name === p2Name);

    if (player1 && player2) {
      const tempIsStarter = player1.isStarter;
      player1.isStarter = player2.isStarter;
      player2.isStarter = tempIsStarter;

      team.starters = team.players.filter(p => p.isStarter);
      team.bench = team.players.filter(p => !p.isStarter);

      lineupState.modified = true;
      clearPlayerSelection();
    }
  }

  function resetTeamLineup(teamState) {
    teamState.players.sort((a, b) => a.number - b.number);
    teamState.players.forEach((p, idx) => {
      p.isStarter = idx < 11;
    });
    teamState.starters = teamState.players.filter(p => p.isStarter);
    teamState.bench = teamState.players.filter(p => !p.isStarter);
    teamState.formation = '4-3-3';
  }

  function findRowElement(playerName, side) {
    return document.querySelector(`.squad-player-row[data-player-name="${playerName}"][data-team-side="${side}"]`);
  }


  const teamASelect = document.getElementById("team-a-select");
  const teamBSelect = document.getElementById("team-b-select");

  const squadTeamASelect = document.getElementById("squad-team-a-select");
  const squadTeamBSelect = document.getElementById("squad-team-b-select");
  const squadAnalysisPlaceholder = document.getElementById("squad-analysis-placeholder");
  const stageSelect = document.getElementById("stage-select");

  const staleToggle = document.getElementById("toggle-stale");
  const injuryAToggle = document.getElementById("toggle-injury-a");
  const injuryBToggle = document.getElementById("toggle-injury-b");

  const predictBtn = document.getElementById("predict-btn");
  const selectionError = document.getElementById("selection-error");
  const loadingState = document.getElementById("loading-state");

  // Results Elements
  const probTeamAName = document.getElementById("prob-team-a-name");
  const probTeamBName = document.getElementById("prob-team-b-name");
  const probTeamAVal = document.getElementById("prob-team-a-val");
  const probTeamBVal = document.getElementById("prob-team-b-val");
  const probDrawVal = document.getElementById("prob-draw-val");

  const probSegmentA = document.getElementById("prob-segment-a");
  const probSegmentDraw = document.getElementById("prob-segment-draw");
  const probSegmentB = document.getElementById("prob-segment-b");

  const cardXgALabel = document.getElementById("card-xg-a-label");
  const cardXgAVal = document.getElementById("card-xg-a-val");
  const cardXgBLabel = document.getElementById("card-xg-b-label");
  const cardXgBVal = document.getElementById("card-xg-b-val");
  const cardScorelineVal = document.getElementById("card-scoreline-val");

  const formTeamAHeader = document.getElementById("form-team-a-header");
  const formTeamBHeader = document.getElementById("form-team-b-header");
  const formTeamASquares = document.getElementById("form-team-a-squares");
  const formTeamBSquares = document.getElementById("form-team-b-squares");

  const h2hMainRecord = document.getElementById("h2h-main-record");
  const h2hMatchNote = document.getElementById("h2h-match-note");

  const matrixListRows = document.getElementById("matrix-list-rows");

  const staleBadge = document.getElementById("stale-badge");
  const confidenceScoreVal = document.getElementById("confidence-score-val");
  const confidenceMeterFill = document.getElementById("confidence-meter-fill");

  const layerStaticVal = document.getElementById("layer-static-val");
  const layerFormVal = document.getElementById("layer-form-val");
  const layerFinalVal = document.getElementById("layer-final-val");

  const engineNotesConsole = document.getElementById("engine-notes-console");
  const venueDisplay = document.getElementById("match-venue-display");
  const completedBanner = document.getElementById("match-completed-banner");
  const fixtureAutoResolved = document.getElementById("fixture-auto-resolved");
  const fixtureResolvedText = document.getElementById("fixture-resolved-text");
  const resultsPlaceholder = document.getElementById("results-placeholder");
  const resultsContent = document.getElementById("results-content");

  function animateProbBar(segA, segDraw, segB, valA, valDraw, valB) {
    segA.style.width = '0%';
    segDraw.style.width = '0%';
    segB.style.width = '0%';

    segA.classList.remove('segment-pulse');
    segDraw.classList.remove('segment-pulse');
    segB.classList.remove('segment-pulse');

    requestAnimationFrame(() => {
      segA.style.transition = 'width 600ms cubic-bezier(0.16, 1, 0.3, 1)';
      segA.style.width = `${valA}%`;

      segDraw.style.transition = 'width 600ms cubic-bezier(0.16, 1, 0.3, 1)';
      segDraw.style.width = `${valDraw}%`;

      segB.style.transition = 'width 600ms cubic-bezier(0.16, 1, 0.3, 1)';
      segB.style.width = `${valB}%`;

      setTimeout(() => {
        if (valA > valDraw && valA > valB) {
          segA.classList.add('segment-pulse');
        } else if (valB > valA && valB > valDraw) {
          segB.classList.add('segment-pulse');
        } else {
          segDraw.classList.add('segment-pulse');
        }
      }, 650);
    });
  }

  function typewriterLines(container, lines, prefix = '> ') {
    container.innerHTML = '';
    let lineIndex = 0;

    function renderNextLine() {
      if (lineIndex >= lines.length) return;
      const text = prefix + lines[lineIndex++];
      const el = document.createElement('div');
      el.className = 'engine-note-line';
      el.textContent = '';
      container.appendChild(el);

      let charIndex = 0;
      const charInterval = setInterval(() => {
        el.textContent += text[charIndex++];
        container.scrollTop = container.scrollHeight;
        if (charIndex >= text.length) {
          clearInterval(charInterval);
          setTimeout(renderNextLine, 60);
        }
      }, 10);
    }

    renderNextLine();
  }

  // Group teams by Tier
  const TIERS = {
    1: "Tier 1 — Elite",
    2: "Tier 2 — Strong",
    3: "Tier 3 — Competitive",
    4: "Tier 4 — Emerging"
  };

  // Populate drop-downs
  function populateDropdowns() {
    [teamASelect, teamBSelect].forEach(select => {
      select.innerHTML = "";

      // Loop tiers 1 to 4
      for (let t = 1; t <= 4; t++) {
        const optgroup = document.createElement("optgroup");
        optgroup.label = TIERS[t].toUpperCase();

        const tierTeams = TEAMS.filter(team => team.tier === t);
        // Sort alphabetically by name
        tierTeams.sort((a, b) => a.name.localeCompare(b.name));

        tierTeams.forEach(team => {
          const option = document.createElement("option");
          option.value = team.id;
          option.textContent = `${team.flag} ${team.name} [${team.id}]`;
          optgroup.appendChild(option);
        });

        select.appendChild(optgroup);
      }
    });

    // Default Selection: France vs Argentina (FRA vs ARG)
    teamASelect.value = "FRA";
    teamBSelect.value = "ARG";
  }

  // Populate form squares for form view
  function renderFormSquares(team, container, rawForm = []) {
    container.innerHTML = "";
    team.last_6.forEach((result, idx) => {
      const tile = document.createElement("div");
      tile.className = `form-tile ${result}`;
      tile.textContent = result;
      const detail = rawForm[idx];
      if (detail && detail.opponent) {
        tile.title = `${detail.result} vs ${detail.opponent} (${detail.goalsFor}-${detail.goalsAgainst}) · ${detail.date}`;
      }
      container.appendChild(tile);
    });
  }

  // Same team inline validation checks
  function validateTeamSelection() {
    if (teamASelect.value === teamBSelect.value) {
      selectionError.classList.remove("hidden");
      predictBtn.disabled = true;
      predictBtn.style.opacity = 0.5;
      predictBtn.style.cursor = "not-allowed";
      return false;
    } else {
      selectionError.classList.add("hidden");
      predictBtn.disabled = false;
      predictBtn.style.opacity = 1;
      predictBtn.style.cursor = "pointer";
      return true;
    }
  }

  async function updateResolvedFixture() {
    const teamAId = teamASelect.value;
    const teamBId = teamBSelect.value;
    if (!teamAId || !teamBId || teamAId === teamBId) {
      fixtureAutoResolved.classList.add('hidden');
      return;
    }
    const teamA = TEAMS.find(t => t.id === teamAId);
    const teamB = TEAMS.find(t => t.id === teamBId);
    if (!teamA || !teamB) {
      fixtureAutoResolved.classList.add('hidden');
      return;
    }
    const { enrichedA, enrichedB, fixture } = await enrichMatchup(teamA, teamB);

    const fixtureDiv = document.getElementById('fixture-auto-resolved');
    const fixtureText = document.getElementById('fixture-resolved-text');

    if (fixture) {
      const homeName = enrichedA.isHome ? teamA.name : teamB.name;
      const awayName = enrichedA.isHome ? teamB.name : teamA.name;
      fixtureText.textContent =
        homeName + ' (H) vs ' + awayName +
        ' (A) · ' + (fixture.ground || 'TBD') +
        ' · ' + (fixture.date || '');
      fixtureDiv.classList.remove('hidden');
    } else {
      fixtureText.textContent = 'No scheduled fixture found — using team order';
      fixtureDiv.classList.remove('hidden');
    }
  }

  teamASelect.addEventListener("change", () => {
    if (validateTeamSelection()) {
      renderSquadAnalysis();
      renderPreMatchFlags();
      updateResolvedFixture();
    }
  });
  teamBSelect.addEventListener("change", () => {
    if (validateTeamSelection()) {
      renderSquadAnalysis();
      renderPreMatchFlags();
      updateResolvedFixture();
    }
  });

  // Update Prediction Dashboard
  async function updateDashboard() {
    const teamAId = teamASelect.value;
    const teamBId = teamBSelect.value;

    if (teamAId === teamBId) return;

    // Show results panel and hide placeholder
    if (resultsPlaceholder) resultsPlaceholder.classList.add('hidden');
    if (resultsContent) resultsContent.classList.remove('hidden');

    const teamA = TEAMS.find(t => t.id === teamAId);
    const teamB = TEAMS.find(t => t.id === teamBId);

    // Call enrichMatchup to get enriched teams with live data and resolved fixture
    const { enrichedA, enrichedB, fixture } = await enrichMatchup(teamA, teamB);

    // Set staleData dynamically based on team live data
    let staleData = staleToggle.checked;
    if (enrichedA.hasLiveData || enrichedB.hasLiveData) {
      staleData = false;
    } else {
      staleData = true;
    }

    const options = {
      staleData,
      injureKeyA: injuryAToggle.checked,
      injureKeyB: injuryBToggle.checked,
      stage: stageSelect.value
    };

    // Calculate prediction metrics using enriched teams
    const results = runPrediction(enrichedA, enrichedB, options);

    // Override lambdas and recompute top 5 scorelines if changed
    const newLambdaA = getLambdaOverride(enrichedA, results.P_dynamic_A, enrichedA.isHome);
    const newLambdaB = getLambdaOverride(enrichedB, results.P_dynamic_B, enrichedB.isHome);

    if (newLambdaA !== results.lambda_A || newLambdaB !== results.lambda_B) {
      results.lambda_A = newLambdaA;
      results.lambda_B = newLambdaB;
      const recomputed = recomputeScorelines(newLambdaA, newLambdaB);
      results.top5 = recomputed.top5;
      results.mostLikelyScoreline = recomputed.mostLikelyScoreline;
      results.sumProb = recomputed.sumProb;
    }

    // Assign results directly (draw correction removed in favor of Dixon-Coles)
    const correctedResults = results;

    // Render Venue & Completed Match Banner
    if (venueDisplay) {
      if (fixture) {
        venueDisplay.textContent = `📍 ${fixture.ground || "Unknown Venue"}`;
        if (fixture.isCompleted && fixture.score && fixture.score.ft) {
          completedBanner.textContent = `⚠️ COMPLETED: ${fixture.score.ft[0]}-${fixture.score.ft[1]}`;
          completedBanner.classList.remove("hidden");
        } else {
          completedBanner.classList.add("hidden");
        }
      } else {
        venueDisplay.textContent = `📍 Neutral Venue / TBD`;
        completedBanner.classList.add("hidden");
      }
    }

    // 1. PROBABILITY BAR TEXT & LABELS
    probTeamAName.textContent = enrichedA.name.toUpperCase();
    probTeamBName.textContent = enrichedB.name.toUpperCase();

    probTeamAVal.textContent = `${correctedResults.winA_pct.toFixed(1)}%`;
    probDrawVal.textContent = `${correctedResults.draw_pct.toFixed(1)}%`;
    probTeamBVal.textContent = `${correctedResults.winB_pct.toFixed(1)}%`;

    animateProbBar(probSegmentA, probSegmentDraw, probSegmentB, correctedResults.winA_pct, correctedResults.draw_pct, correctedResults.winB_pct);

    // 2. EXPECTED GOALS & SCORELINE CARDS
    const labelA = teamA.name.substring(0, 3).toUpperCase();
    const labelB = teamB.name.substring(0, 3).toUpperCase();
    cardXgALabel.textContent = `λ ${labelA}`;
    cardXgAVal.textContent = correctedResults.lambda_A.toFixed(1);

    cardXgBLabel.textContent = `λ ${labelB}`;
    cardXgBVal.textContent = correctedResults.lambda_B.toFixed(1);

    cardScorelineVal.textContent = correctedResults.mostLikelyScoreline;

    // 4. RECENT FORM SQUARES
    formTeamAHeader.textContent = enrichedA.name.toUpperCase();
    formTeamBHeader.textContent = enrichedB.name.toUpperCase();
    const rawFormA = await getTeamForm(teamA.id);
    const rawFormB = await getTeamForm(teamB.id);
    renderFormSquares(enrichedA, formTeamASquares, rawFormA);
    renderFormSquares(enrichedB, formTeamBSquares, rawFormB);

    // 5. HEAD TO HEAD BLOCK
    const h2hData = getH2H(teamA.id, teamB.id);
    if (!h2hData) {
      h2hMainRecord.textContent = '> NO PRIOR MEETINGS IN DATASET';
      h2hMainRecord.style.color = 'var(--text-muted)';
      h2hMatchNote.textContent = 'First meeting between these teams';
      h2hMatchNote.style.opacity = '0.5';
    } else {
      h2hMainRecord.textContent = results.h2hText;
      h2hMainRecord.style.color = '';
      h2hMatchNote.textContent = results.h2hNote || "No notable notes in archive.";
      h2hMatchNote.style.opacity = '';
    }

    // 3. TOP 5 SCORELINES BAR CHART
    matrixListRows.innerHTML = "";
    const maxProb = results.top5[0].probability; // highest probability

    results.top5.forEach((row, index) => {
      const percentageText = `${(row.probability * 100).toFixed(1)}%`;
      // Fill width proportional to probability relative to highest probability (highest = 100% width)
      const fillPercentage = maxProb > 0 ? (row.probability / maxProb) * 100 : 0;

      const matrixRow = document.createElement("div");
      matrixRow.className = "matrix-row matrix-row-animate";
      matrixRow.style.animationDelay = `${index * 70}ms`;

      matrixRow.innerHTML = `
        <div class="matrix-score">${row.scoreA}-${row.scoreB}</div>
        <div class="matrix-bar-cell">
          <div class="matrix-bar-fill" style="width: 0%;"></div>
        </div>
        <div class="matrix-pct">${percentageText}</div>
      `;

      matrixListRows.appendChild(matrixRow);

      // Animate width expansion
      setTimeout(() => {
        const fillBar = matrixRow.querySelector(".matrix-bar-fill");
        if (fillBar) fillBar.style.width = `${fillPercentage}%`;
      }, 50);
    });

    // 7. CONFIDENCE METER
    if (options.staleData) {
      staleBadge.classList.remove("hidden");
    } else {
      staleBadge.classList.add("hidden");
    }

    confidenceScoreVal.textContent = `${results.confidence}/100 — ${results.confidenceBand}`;

    // Clear old bands
    confidenceMeterFill.className = "confidence-meter-fill";

    // Apply proper color class based on band
    let colorClass = "HIGH";
    if (results.confidenceBand === "MEDIUM") colorClass = "MEDIUM";
    else if (results.confidenceBand === "LOW") colorClass = "LOW";
    else if (results.confidenceBand === "VERY LOW") colorClass = "VERY_LOW";

    confidenceMeterFill.classList.add(colorClass);

    // Animate confidence meter width
    confidenceMeterFill.style.width = '0%';
    confidenceMeterFill.style.transition = 'none';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        confidenceMeterFill.style.transition = 'width 900ms cubic-bezier(0.4, 0, 0.2, 1)';
        confidenceMeterFill.style.width = `${results.confidence}%`;
      });
    });

    // 8. LAYER BREAKDOWN
    layerStaticVal.textContent = `P = ${results.P_static_A.toFixed(1)}`;
    layerFormVal.textContent = `P = ${results.P_dynamic_A.toFixed(1)}`;
    layerFinalVal.textContent = `${results.winA_pct.toFixed(1)}%`;

    // 6. PREDICTION DRIVERS (ENGINE NOTES CONSOLE LOGS)
    const prefixedDrivers = results.drivers.map(d =>
      (enrichedA.hasLiveData || enrichedB.hasLiveData ? '[LIVE] ' : '[STATIC] ') + d.toUpperCase()
    );

    typewriterLines(engineNotesConsole, prefixedDrivers);

    // Update Squad Analysis
    renderSquadAnalysis();
    renderPreMatchFlags();

    // Render expansion modules
    await renderExpansionModules(teamAId, teamBId);
  }

  function runLoadingSequence(onComplete) {
    const steps = [
      "INITIALIZING NEURAL WEIGHTS...",
      "CALIBRATING POISSON MODEL FOR OUTCOMES...",
      "RESOLVING HISTORICAL HEAD-TO-HEAD MATRICES...",
      "BLENDING LIVE DATA FEEDS AND WEATHER MODIFIERS...",
      "COMPUTING CONFIDENCE SCORE AND LAMBDAS..."
    ];

    const loadingOverlay = document.getElementById("loading-state");
    const textEl = loadingOverlay.querySelector(".loading-text");
    loadingOverlay.classList.remove("hidden");

    let stepIndex = 0;

    function nextStep() {
      if (stepIndex >= steps.length) {
        setTimeout(() => {
          loadingOverlay.classList.add("hidden");
          onComplete();
        }, 150);
        return;
      }
      textEl.textContent = steps[stepIndex++];
      setTimeout(nextStep, 180);
    }

    nextStep();
  }

  // Trigger Predict click handler
  predictBtn.addEventListener("click", () => {
    if (!validateTeamSelection()) return;
    runLoadingSequence(() => {
      updateDashboard();
    });
  });

  // Tab Switching logic
  const btnTabPredictor = document.getElementById("btn-tab-predictor");
  const btnTabSquad = document.getElementById("btn-tab-squad");
  const btnTabVerification = document.getElementById("btn-tab-verification");
  const btnTabSettings = document.getElementById("btn-tab-settings");
  const predictorView = document.getElementById("predictor-view");
  const squadAnalysisView = document.getElementById("squad-analysis-view");
  const verificationView = document.getElementById("verification-view");
  const settingsView = document.getElementById("settings-view");

  btnTabPredictor.addEventListener("click", () => {
    btnTabPredictor.classList.add("active");
    btnTabSquad.classList.remove("active");
    btnTabVerification.classList.remove("active");
    btnTabSettings.classList.remove("active");
    predictorView.classList.remove("hidden");
    squadAnalysisView.classList.add("hidden");
    document.getElementById("squad-analysis-placeholder").classList.add("hidden");
    verificationView.classList.add("hidden");
    settingsView.classList.add("hidden");
  });

  btnTabSquad.addEventListener("click", () => {
    btnTabSquad.classList.add("active");
    btnTabPredictor.classList.remove("active");
    btnTabVerification.classList.remove("active");
    btnTabSettings.classList.remove("active");
    squadAnalysisView.classList.remove("hidden");
    predictorView.classList.add("hidden");
    verificationView.classList.add("hidden");
    settingsView.classList.add("hidden");

    // Render squad analysis
    renderSquadAnalysis();
  });

  btnTabVerification.addEventListener("click", () => {
    btnTabVerification.classList.add("active");
    btnTabPredictor.classList.remove("active");
    btnTabSquad.classList.remove("active");
    btnTabSettings.classList.remove("active");
    verificationView.classList.remove("hidden");
    predictorView.classList.add("hidden");
    squadAnalysisView.classList.add("hidden");
    document.getElementById("squad-analysis-placeholder").classList.add("hidden");
    settingsView.classList.add("hidden");

    // Execute live backtest dynamically
    initVerificationTab();
  });

  btnTabSettings.addEventListener("click", () => {
    btnTabSettings.classList.add("active");
    btnTabPredictor.classList.remove("active");
    btnTabSquad.classList.remove("active");
    btnTabVerification.classList.remove("active");
    settingsView.classList.remove("hidden");
    predictorView.classList.add("hidden");
    squadAnalysisView.classList.add("hidden");
    document.getElementById("squad-analysis-placeholder").classList.add("hidden");
    verificationView.classList.add("hidden");

    updateSettingsPanel();
  });

  // Backtest filter buttons click event listeners
  const filterAll = document.getElementById("filter-all");
  const filterCorrect = document.getElementById("filter-correct");
  const filterIncorrect = document.getElementById("filter-incorrect");
  const filterDraws = document.getElementById("filter-draws");

  if (filterAll && filterCorrect && filterIncorrect && filterDraws) {
    const filters = [filterAll, filterCorrect, filterIncorrect, filterDraws];

    function applyFilter(activeBtn, type) {
      filters.forEach(btn => btn.classList.remove("active"));
      activeBtn.classList.add("active");

      const rows = document.querySelectorAll("#backtest-results-body tr");
      rows.forEach(row => {
        if (row.classList.contains("details-row")) {
          row.classList.add("hidden");
          return;
        }

        if (type === "all") {
          row.classList.remove("hidden");
        } else if (type === "draws") {
          if (row.dataset.actualOutcome === "DRAW") {
            row.classList.remove("hidden");
          } else {
            row.classList.add("hidden");
          }
        } else {
          if (row.dataset.correct === type) {
            row.classList.remove("hidden");
          } else {
            row.classList.add("hidden");
          }
        }
      });
    }

    filterAll.addEventListener("click", () => applyFilter(filterAll, "all"));
    filterCorrect.addEventListener("click", () => applyFilter(filterCorrect, "true"));
    filterIncorrect.addEventListener("click", () => applyFilter(filterIncorrect, "false"));
    filterDraws.addEventListener("click", () => applyFilter(filterDraws, "draws"));
  }

  const CAPTAINS_MAP = {
    FRA: 7, ARG: 10, BRA: 10, ENG: 9, ESP: 8,
    GER: 8, POR: 7, NED: 4, BEL: 10, CRO: 10,
    MEX: 3, USA: 10, CAN: 10, URU: 2, COL: 8,
    SEN: 5, MAR: 6, JPN: 10, KOR: 7, AUS: 10,
    SUI: 10, DEN: 10, SWE: 10, POL: 9, SRB: 10,
    TUR: 10, AUT: 10, ALG: 10, EGY: 10, NGR: 10,
    GHA: 10, CMR: 10, CIV: 10, SAU: 10, QAT: 10,
    IRN: 10, ECU: 10, VEN: 10, CHI: 10, PAR: 7,
    SCO: 6, HAI: 10, CUW: 10, NZL: 10, CPV: 10,
    IRQ: 10, NOR: 9, JOR: 10, COD: 10, UZB: 10,
    BIH: 10, SLO: 7, ROU: 10, GEO: 10, UKR: 10,
    RSA: 2, CZE: 10, CRI: 10, SLV: 10, PAN: 10
  };

  function isPlayerVerified(teamCode, playerName) {
    const internalTeam = TEAMS.find(t => t.id === teamCode);
    if (!internalTeam || !internalTeam.players) return false;

    const match = internalTeam.players.find(ip => {
      const ipName = ip.name.toLowerCase();
      const pName = playerName.toLowerCase();
      return ipName === pName || ipName.includes(pName) || pName.includes(ipName);
    });

    return !!(match && match.data_quality === 'FULL');
  }

  function getSortedStarters(squad) {
    const starters = squad.filter(p => p.isStarter !== undefined ? p.isStarter : p.starter);

    const gks = starters.filter(p => p.posGroup === 'GOALKEEPERS');
    const dfs = starters.filter(p => p.posGroup === 'DEFENDERS');
    const mfs = starters.filter(p => p.posGroup === 'MIDFIELDERS');
    const fws = starters.filter(p => p.posGroup === 'FORWARDS');

    gks.sort((a, b) => a.number - b.number);
    dfs.sort((a, b) => a.number - b.number);
    mfs.sort((a, b) => a.number - b.number);
    fws.sort((a, b) => a.number - b.number);

    return [...gks, ...dfs, ...mfs, ...fws];
  }

  async function renderSquadAnalysis() {
    const teamAId = squadTeamASelect.value;
    const teamBId = squadTeamBSelect.value;

    const btnTabSquad = document.getElementById("btn-tab-squad");
    const isSquadTabActive = btnTabSquad && btnTabSquad.classList.contains("active");

    if (!teamAId || !teamBId) {
      document.getElementById("squad-analysis-view").classList.add("hidden");
      if (isSquadTabActive) {
        document.getElementById("squad-analysis-placeholder").classList.remove("hidden");
      } else {
        document.getElementById("squad-analysis-placeholder").classList.add("hidden");
      }
      return;
    }

    if (isSquadTabActive) {
      document.getElementById("squad-analysis-placeholder").classList.add("hidden");
      document.getElementById("squad-analysis-view").classList.remove("hidden");
    } else {
      document.getElementById("squad-analysis-placeholder").classList.add("hidden");
      document.getElementById("squad-analysis-view").classList.add("hidden");
    }

    // Load squads if code changed
    if (lineupState.teamA.code !== teamAId) {
      const squadA = await getTeamSquad(teamAId);
      initializeLineupState(teamAId, squadA, 'teamA');
    }
    if (lineupState.teamB.code !== teamBId) {
      const squadB = await getTeamSquad(teamBId);
      initializeLineupState(teamBId, squadB, 'teamB');
    }

    // Get clean sheets
    const cleanSheetsA = await getTeamCleanSheets(teamAId);
    const cleanSheetsB = await getTeamCleanSheets(teamBId);

    // Get top scorers
    const topScorersList = await getTopScorers(15);

    const topScorerA = topScorersList.find(s => s.teamCode === teamAId) || null;
    const topScorerB = topScorersList.find(s => s.teamCode === teamBId) || null;

    // Render components
    renderGoldenBootBar(topScorersList, teamAId, teamBId);
    renderSingleTeamSquad(teamAId, lineupState.teamA.players, 'a');
    renderSingleTeamSquad(teamBId, lineupState.teamB.players, 'b');
    renderPitchSVG(lineupState.teamA.players, lineupState.teamB.players, teamAId, teamBId, topScorerA, topScorerB);
    await renderAwardsBar(teamAId, teamBId, topScorerA, topScorerB, cleanSheetsA, cleanSheetsB);

    // Show/hide modified banner
    const banner = document.getElementById("lineup-modified-banner");
    if (banner) {
      if (lineupState.modified) {
        banner.classList.remove("hidden");
      } else {
        banner.classList.add("hidden");
      }
    }

    // Update active formation button styling
    const formationSelector = document.getElementById("formation-selector");
    if (formationSelector) {
      const activeFormation = lineupState.teamA.formation || "4-3-3";
      formationSelector.querySelectorAll(".formation-btn").forEach(btn => {
        if (btn.dataset.formation === activeFormation) {
          btn.classList.add("active");
        } else {
          btn.classList.remove("active");
        }
      });
    }
  }


  function renderGoldenBootBar(scorers, teamACode, teamBCode) {
    const container = document.getElementById("golden-boot-chips-container");
    if (!container) return;
    container.innerHTML = "";

    if (scorers.length === 0) {
      container.innerHTML = `<div style="font-family: var(--font-data); font-size: 10px; color: #444; padding: 6px 0;">&gt; NO GOALS RECORDED YET IN TOURNAMENT</div>`;
      return;
    }

    const maxGoals = scorers[0]?.goals || 0;

    scorers.forEach((scorer, index) => {
      const chip = document.createElement("div");
      chip.className = "golden-boot-chip";
      chip.style.cssText = `
        border: 1px solid #1a1a1a;
        background: #070707;
        padding: 5px 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
        animation: fadeUp 0.3s ease forwards;
        opacity: 0;
        animation-delay: ${index * 0.06}s;
      `;

      const isLiveWire = scorer.goals === maxGoals && maxGoals > 0;
      const liveWireBadge = isLiveWire ? `
        <span style="background: #1a0808; color: #ef4444; border: 1px solid #ef444422; font-size: 8px; letter-spacing: 0.08em; padding: 1px 5px; text-transform: uppercase; font-family: var(--font-label);">LIVE WIRE</span>
      ` : "";

      chip.innerHTML = `
        <span style="color: #444; font-size: 9px; font-family: var(--font-label);">#${index + 1}</span>
        <span style="color: #e8e8e8; font-size: 10px; font-weight: 500;">${scorer.name}</span>
        <span style="color: #555; font-size: 9px; font-family: var(--font-label);">${scorer.teamCode}</span>
        <span style="color: #22c55e; font-size: 10px; font-weight: 600; font-family: var(--font-data);">${scorer.goals} G</span>
        ${liveWireBadge}
      `;
      container.appendChild(chip);
    });
  }

  function renderSingleTeamSquad(teamCode, squad, side) {
    const container = document.getElementById(`squad-team-${side}-panel`);
    if (!container) return;
    container.innerHTML = "";

    const team = TEAMS.find(t => t.id === teamCode) || {};
    const teamName = team.name || teamCode;
    const formation = side === 'a' ? lineupState.teamA.formation : lineupState.teamB.formation;

    const headerDiv = document.createElement("div");
    headerDiv.className = "squad-panel-header";
    headerDiv.style.cssText = "display: flex; flex-direction: column; gap: 2px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;";

    headerDiv.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-family: var(--font-display); font-size: 11px; font-weight: bold; color: var(--text-primary); text-transform: uppercase;">${team.flag || ''} ${teamName}</span>
        <span style="font-family: var(--font-label); font-size: 9px; color: #444;">${teamCode}</span>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
        <div style="display: flex; align-items: center; gap: 4px;">
          <span style="font-size: 8px; color: var(--text-secondary); font-family: var(--font-label); text-transform: uppercase;">◈ FORMATION:</span>
          <select class="terminal-select squad-formation-select" data-side="${side}" style="padding: 2px 4px; font-size: 9px; height: auto; font-family: var(--font-data); background: #000; border: 1px solid var(--border-color); color: var(--text-primary); cursor: pointer;">
            <option value="4-3-3" ${formation === '4-3-3' ? 'selected' : ''}>${formation === '4-3-3' ? '▣' : '○'} 4-3-3</option>
            <option value="4-2-3-1" ${formation === '4-2-3-1' ? 'selected' : ''}>${formation === '4-2-3-1' ? '▣' : '○'} 4-2-3-1</option>
            <option value="4-4-2" ${formation === '4-4-2' ? 'selected' : ''}>${formation === '4-4-2' ? '▣' : '○'} 4-4-2</option>
            <option value="3-5-2" ${formation === '3-5-2' ? 'selected' : ''}>${formation === '3-5-2' ? '▣' : '○'} 3-5-2</option>
            <option value="3-4-3" ${formation === '3-4-3' ? 'selected' : ''}>${formation === '3-4-3' ? '▣' : '○'} 3-4-3</option>
            <option value="5-3-2" ${formation === '5-3-2' ? 'selected' : ''}>${formation === '5-3-2' ? '▣' : '○'} 5-3-2</option>
            <option value="4-5-1" ${formation === '4-5-1' ? 'selected' : ''}>${formation === '4-5-1' ? '▣' : '○'} 4-5-1</option>
          </select>
        </div>
        <span style="font-size: 8px; color: #444; font-family: var(--font-label); text-transform: uppercase;">${team.confederation || ''}</span>
      </div>
    `;
    container.appendChild(headerDiv);

    // Add starting XI section header symbol (Requirement 2 & 3)
    const startingHeader = document.createElement("div");
    startingHeader.className = "tactical-divider";
    startingHeader.innerHTML = `${TACTICAL_ICONS.empty} STARTING XI`;
    container.appendChild(startingHeader);

    // Modified Section: 1. Independent formations, 2. Separate formation controls
    const selectEl = headerDiv.querySelector(".squad-formation-select");
    if (selectEl) {
      selectEl.addEventListener("change", (e) => {
        const selectedFormation = e.target.value;
        const teamKey = side === 'a' ? 'teamA' : 'teamB';
        adjustStartersForFormation(lineupState[teamKey], selectedFormation);
        lineupState.modified = true;
        renderSquadAnalysis();
      });
    }

    const posGroups = ["GOALKEEPERS", "DEFENDERS", "MIDFIELDERS", "FORWARDS"];
    const grouped = {
      GOALKEEPERS: [],
      DEFENDERS: [],
      MIDFIELDERS: [],
      FORWARDS: []
    };

    squad.forEach(p => {
      if (grouped[p.posGroup]) {
        grouped[p.posGroup].push(p);
      } else {
        grouped.FORWARDS.push(p);
      }
    });

    // Modified Section: 5. Reduce player list height (collapsible Bench details container)
    const benchDetails = document.createElement("details");
    benchDetails.style.cssText = "margin-top: 8px; width: 100%; border: 1px solid #111; background: #030303;";

    const benchSummary = document.createElement("summary");
    benchSummary.style.cssText = "font-family: var(--font-label); font-size: 8px; letter-spacing: 0.15em; color: #888; text-transform: uppercase; padding: 6px 8px; cursor: pointer; outline: none; list-style: none; user-select: none; border-bottom: 1px solid #111; display: flex; align-items: center; gap: 4px;";
    benchSummary.innerHTML = `${TACTICAL_ICONS.warning} RESERVE UNIT ▼`;

    const benchContainer = document.createElement("div");
    benchContainer.style.cssText = "display: flex; flex-direction: column; gap: 4px; padding: 4px 6px;";

    benchDetails.appendChild(benchSummary);
    benchDetails.appendChild(benchContainer);

    let hasBenchPlayers = false;

    function buildPlayerRow(player, idx) {
      const isCaptain = player.number === CAPTAINS_MAP[teamCode];
      const verified = isPlayerVerified(teamCode, player.name);

      const row = document.createElement("div");
      row.className = "squad-player-row";
      row.style.cssText = `
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 3px 4px;
        border-bottom: 1px solid #0a0a0a;
        cursor: pointer;
        transition: background 0.15s ease;
        animation: slideIn 0.2s ease forwards;
        opacity: 0;
        animation-delay: ${idx * 0.025}s;
      `;

      const isSelected = lineupState.selectedPlayer && lineupState.selectedPlayer.name === player.name && lineupState.selectedPlayer.teamSide === side;
      const isCandidate = lineupState.selectedPlayer && lineupState.selectedPlayer.teamSide === side && player.isStarter !== lineupState.selectedPlayer.isStarter && player.posGroup === lineupState.selectedPlayer.posGroup;

      row.dataset.playerName = player.name;
      row.dataset.teamSide = side;

      if (isSelected) {
        row.classList.add("selected");
        const teamColor = side === 'a' ? '#22c55e' : '#3b82f6';
        const bgColor = side === 'a' ? '#0a1a0a' : '#080d14';
        row.style.background = bgColor;
        row.style.borderLeft = `2px solid ${teamColor}`;
        row.style.color = teamColor;
      } else if (isCandidate) {
        row.classList.add("swap-candidate");
        row.style.borderLeft = "2px solid #f59e0b44";
        row.style.color = "#f59e0b";
      }

      // Modified Section: 7. Bench visibility
      if (!player.isStarter) {
        row.classList.add("bench-player");
      }

      row.onmouseover = () => {
        if (!row.classList.contains("selected") && !row.classList.contains("swap-candidate")) {
          row.style.background = "#0d0d0d";
        }
      };
      row.onmouseout = () => {
        if (!row.classList.contains("selected") && !row.classList.contains("swap-candidate")) {
          row.style.background = "transparent";
        }
      };

      row.addEventListener("click", (e) => {
        e.stopPropagation();

        if (isCandidate) {
          swapPlayers(lineupState.selectedPlayer.name, player.name, side);
          renderSquadAnalysis();
        } else if (isSelected) {
          lineupState.selectedPlayer = null;
          renderSquadAnalysis();
        } else {
          lineupState.selectedPlayer = {
            teamSide: side,
            name: player.name,
            number: player.number,
            pos: player.pos,
            posGroup: player.posGroup,
            isStarter: player.isStarter
          };
          renderSquadAnalysis();
        }
      });

      const captainBadge = isCaptain ? `
        <span style="color: #f59e0b; margin-left: 2px; display: inline-flex; align-items: center; justify-content: center;" title="Captain">${TACTICAL_ICONS.captain}</span>
      ` : "";

      // Modified Section: 10. Data Indicators (monochrome progress ticks instead of badge)
      const dataIndicator = verified ? `
        <span style="color: var(--accent-green); font-size: 8px; font-family: var(--font-data); margin-left: auto; letter-spacing: -1px;" title="Verified Data">|||||</span>
      ` : `
        <span style="color: #333; font-size: 8px; font-family: var(--font-data); margin-left: auto; letter-spacing: -1px;" title="Unverified Data">|||</span>
      `;

      // Modified Section: 7. Player Selection (small tactical marker beside player name)
      const selectedMarker = isSelected ? `
        <span style="color: ${side === 'a' ? '#22c55e' : '#3b82f6'}; display: inline-flex; align-items: center; justify-content: center;">${TACTICAL_ICONS.selected}</span>
      ` : (isCandidate ? `
        <span style="color: #f59e0b; display: inline-flex; align-items: center; justify-content: center;">${TACTICAL_ICONS.active}</span>
      ` : `
        <span style="color: #333; display: inline-flex; align-items: center; justify-content: center;">${TACTICAL_ICONS.empty}</span>
      `);

      // Modified Section: 7. Bench visibility (using var(--text-secondary) for bench player text)
      const nameColor = isSelected ? (side === 'a' ? '#22c55e' : '#3b82f6') : (isCandidate ? '#f59e0b' : (player.isStarter ? '#e8e8e8' : 'var(--text-secondary)'));
      const swapLabel = isCandidate ? `
        <span class="swap-label" style="font-size: 8px; color: #f59e0b; margin-left: auto; padding-left: 6px;">[SWAP]</span>
      ` : "";

      row.innerHTML = `
        ${selectedMarker}
        <span style="width: 14px; text-align: right; font-size: 9px; color: #888; font-family: var(--font-data); margin-right: 4px;">${player.number}</span>
        <span style="flex: 1; font-size: 10px; color: ${nameColor}; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${player.name}</span>
        <span style="font-size: 8px; color: #555; font-family: var(--font-data); margin-right: 4px;">${player.age}y</span>
        ${captainBadge}
        ${isCandidate ? swapLabel : dataIndicator}
      `;

      return row;
    }

    const categoryLabels = {
      GOALKEEPERS: `${TACTICAL_ICONS.empty} GOALKEEPERS`,
      DEFENDERS: `${TACTICAL_ICONS.warning} DEFENDERS`,
      MIDFIELDERS: `${TACTICAL_ICONS.intelligence} MIDFIELDERS`,
      FORWARDS: `${TACTICAL_ICONS.simulation} FORWARDS`
    };

    posGroups.forEach(groupKey => {
      const playersInGroup = grouped[groupKey];
      if (playersInGroup.length === 0) return;

      const startersInGroup = playersInGroup.filter(p => p.isStarter);
      const benchInGroup = playersInGroup.filter(p => !p.isStarter);

      if (startersInGroup.length > 0) {
        const groupHeader = document.createElement("div");
        groupHeader.className = "tactical-divider";
        groupHeader.innerHTML = categoryLabels[groupKey] || groupKey;
        container.appendChild(groupHeader);

        startersInGroup.forEach((player, idx) => {
          const row = buildPlayerRow(player, idx);
          container.appendChild(row);
        });
      }

      if (benchInGroup.length > 0) {
        hasBenchPlayers = true;
        benchInGroup.forEach((player, idx) => {
          const row = buildPlayerRow(player, idx);
          benchContainer.appendChild(row);
        });
      }
    });

    if (hasBenchPlayers) {
      container.appendChild(benchDetails);
    }
  }


  function getPitchShortName(fullName) {
    if (!fullName) return "";
    const name = fullName.trim();
    const parts = name.split(/\s+/);

    if (parts.length <= 1) {
      return name;
    }

    // Check for initials like "L. Messi"
    if (parts[0].length <= 2 && parts[0].includes('.')) {
      return parts.slice(1).join(' ');
    }

    // For names with 3 or more parts (e.g. Alexis Mac Allister, Kevin De Bruyne)
    if (parts.length >= 3) {
      const lastTwo = parts.slice(-2).join(' ');
      return lastTwo;
    }

    // For 2-part names (e.g. Kylian Mbappé, Lionel Messi)
    return parts[1];
  }

  function renderPitchSVG(squadA, squadB, teamACode, teamBCode, topScorerA, topScorerB) {
    const svgWrapper = document.getElementById("pitch-svg-wrapper");
    if (!svgWrapper) return;

    const formationA = lineupState.teamA.formation || "4-3-3";
    const formationB = lineupState.teamB.formation || "4-3-3";

    const startersA = getSortedStarters(squadA);
    const startersB = getSortedStarters(squadB);

    const coordsA = getStartersCoords(startersA, formationA, false);
    const coordsB = getStartersCoords(startersB, formationB, true);

    const labels = [];

    startersA.forEach((player) => {
      const coord = coordsA.get(player.name) || { x: 100, y: 147.5 };
      const isGK = player.posGroup === 'GOALKEEPERS';
      const isStar = topScorerA && player.name === topScorerA.name;
      const r = isStar ? 8 : 5.5;

      const shortName = getPitchShortName(player.name);

      labels.push({
        side: 'a',
        player,
        coord,
        r,
        text: shortName,
        isGK,
        isStar,
        x: coord.x,
        y: coord.y - (r + 3),
        width: Math.max(16, shortName.length * 2.8),
        height: 5
      });
    });

    startersB.forEach((player) => {
      const coord = coordsB.get(player.name) || { x: 100, y: 147.5 };
      const isGK = player.posGroup === 'GOALKEEPERS';
      const isStar = topScorerB && player.name === topScorerB.name;
      const r = isStar ? 8 : 5.5;

      const shortName = getPitchShortName(player.name);

      labels.push({
        side: 'b',
        player,
        coord,
        r,
        text: shortName,
        isGK,
        isStar,
        x: coord.x,
        y: coord.y - (r + 3),
        width: Math.max(16, shortName.length * 2.8),
        height: 5
      });
    });

    // Modified Section: 3. Fix player overlap (Collision handling pass)
    for (let pass = 0; pass < 8; pass++) {
      for (let i = 0; i < labels.length; i++) {
        for (let j = i + 1; j < labels.length; j++) {
          const l1 = labels[i];
          const l2 = labels[j];

          const dx = Math.abs(l1.x - l2.x);
          const dy = Math.abs(l1.y - l2.y);

          const minX = (l1.width + l2.width) / 2 + 1;
          const minY = 6;

          if (dx < minX && dy < minY) {
            const shiftY = minY - dy;
            if (l1.y <= l2.y) {
              l1.y -= shiftY / 2 + 1;
              l2.y += shiftY / 2 + 1;
            } else {
              l1.y += shiftY / 2 + 1;
              l2.y -= shiftY / 2 + 1;
            }

            if (dx < 4) {
              if (l1.x <= l2.x) {
                l1.x -= 2.5;
                l2.x += 2.5;
              } else {
                l1.x += 2.5;
                l2.x -= 2.5;
              }
            }
          }
        }
      }
    }

    // Modified Section: 9. Prevent clipping (Clamp label positions inside SVG viewport boundaries)
    labels.forEach(l => {
      const halfW = l.width / 2;
      if (l.x - halfW < 8) {
        l.x = 8 + halfW;
      }
      if (l.x + halfW > 192) {
        l.x = 192 - halfW;
      }
      if (l.y < 12) {
        l.y = 12;
      }
      if (l.y > 287) {
        l.y = 287;
      }
    });

    // Modified Section: 4. Dynamic pitch scaling, 6. Zoom support
    let svgHtml = `
      <svg viewBox="0 0 200 295" width="100%" style="display: block; width: 100%; height: auto; aspect-ratio: 200 / 295; font-family: var(--font-data);">
        <!-- Pitch Background -->
        <rect x="0" y="0" width="200" height="295" fill="#040404" />
        
        <!-- Boundary lines -->
        <rect x="8" y="8" width="184" height="279" fill="none" stroke="#111111" stroke-width="1.5" />
        
        <!-- Center line -->
        <line x1="8" y1="147.5" x2="192" y2="147.5" stroke="#111111" stroke-width="1" />
        
        <!-- Center Circle -->
        <circle cx="100" cy="147.5" r="28" fill="none" stroke="#111111" stroke-width="1" />
        <circle cx="100" cy="147.5" r="1.5" fill="#111111" />
        
        <!-- Top Goal/Penalty Area -->
        <rect x="40" y="8" width="120" height="46" fill="none" stroke="#111111" stroke-width="1" />
        <rect x="75" y="8" width="50" height="16" fill="none" stroke="#111111" stroke-width="1" />
        <circle cx="100" cy="38" r="1.5" fill="#111111" />
        <path d="M 77 54 A 28 28 0 0 0 123 54" fill="none" stroke="#111111" stroke-width="1" />
        
        <!-- Bottom Goal/Penalty Area -->
        <rect x="40" y="241" width="120" height="46" fill="none" stroke="#111111" stroke-width="1" />
        <rect x="75" y="271" width="50" height="16" fill="none" stroke="#111111" stroke-width="1" />
        <circle cx="100" cy="257" r="1.5" fill="#111111" />
        <path d="M 77 241 A 28 28 0 0 1 123 241" fill="none" stroke="#111111" stroke-width="1" />
    `;

    labels.forEach(l => {
      const pulseClass = l.isGK ? 'class="gk-pulse"' : '';

      let selectedVisuals = '';
      if (lineupState.selectedPlayer && lineupState.selectedPlayer.name === l.player.name && lineupState.selectedPlayer.teamSide === l.side) {
        const strokeColor = l.side === 'a' ? '#22c55e' : '#3b82f6';
        const rTicks = 12;
        selectedVisuals = `
          <circle cx="${l.coord.x}" cy="${l.coord.y}" r="22" fill="none" 
            stroke="${strokeColor}" stroke-width="0.8" 
            style="animation: pulseRing 3s cubic-bezier(0.215, 0.61, 0.355, 1) infinite; transform-origin: ${l.coord.x}px ${l.coord.y}px;" opacity="0.5"/>
          <circle cx="${l.coord.x}" cy="${l.coord.y}" r="16" fill="none" 
            stroke="${strokeColor}" stroke-width="0.8" stroke-dasharray="3 3" 
            style="animation: spin 6s linear infinite; transform-origin: ${l.coord.x}px ${l.coord.y}px;"/>
          <line x1="${l.coord.x - rTicks}" y1="${l.coord.y}" x2="${l.coord.x - rTicks + 2}" y2="${l.coord.y}" stroke="${strokeColor}" stroke-width="0.8" />
          <line x1="${l.coord.x + rTicks - 2}" y1="${l.coord.y}" x2="${l.coord.x + rTicks}" y2="${l.coord.y}" stroke="${strokeColor}" stroke-width="0.8" />
          <line x1="${l.coord.x}" y1="${l.coord.y - rTicks}" x2="${l.coord.x}" y2="${l.coord.y - rTicks + 2}" stroke="${strokeColor}" stroke-width="0.8" />
          <line x1="${l.coord.x}" y1="${l.coord.y + rTicks - 2}" x2="${l.coord.x}" y2="${l.coord.y + rTicks}" stroke="${strokeColor}" stroke-width="0.8" />
        `;
      }

      const strokeColor = l.side === 'a' ? '#22c55e' : '#3b82f6';
      const textColor = l.side === 'a' ? '#22c55e' : '#60a5fa';
      const bgColor = l.side === 'a' ? '#08130a' : '#080d14';

      svgHtml += `
        <g>
          ${selectedVisuals}
          <circle cx="${l.coord.x}" cy="${l.coord.y}" r="${l.r}" stroke="${strokeColor}" stroke-width="1.5" fill="${bgColor}" ${pulseClass} />
          <text x="${l.coord.x}" y="${l.coord.y + 3}" font-size="8px" fill="${textColor}" font-weight="bold" text-anchor="middle">${l.player.number}</text>
          <text x="${l.x}" y="${l.y}" font-size="6px" fill="${textColor}" fill-opacity="0.9" text-anchor="middle" font-weight="500">${l.text}</text>
        </g>
      `;
    });

    svgHtml += `</svg>`;
    svgWrapper.innerHTML = svgHtml;
  }


  async function renderAwardsBar(teamACode, teamBCode, topScorerA, topScorerB, cleanSheetsA, cleanSheetsB) {
    const container = document.getElementById("squad-awards-bar");
    if (!container) return;
    container.innerHTML = "";

    const squadA = await getTeamSquad(teamACode);
    const squadB = await getTeamSquad(teamBCode);

    const gkA = squadA.find(p => p.posGroup === "GOALKEEPERS") || { name: "N/A" };
    const gkB = squadB.find(p => p.posGroup === "GOALKEEPERS") || { name: "N/A" };

    const cells = [
      {
        badgeLabel: "LIVE WIRE",
        badgeType: "LIVE_WIRE",
        playerName: topScorerA ? topScorerA.name : "N/A",
        teamCode: teamACode,
        posGroup: "FORWARD",
        statValue: topScorerA ? `${topScorerA.goals} GOALS` : "0 GOALS"
      },
      {
        badgeLabel: "LIVE WIRE",
        badgeType: "LIVE_WIRE",
        playerName: topScorerB ? topScorerB.name : "N/A",
        teamCode: teamBCode,
        posGroup: "FORWARD",
        statValue: topScorerB ? `${topScorerB.goals} GOALS` : "0 GOALS"
      },
      {
        badgeLabel: "IRON HANDS",
        badgeType: "IRON_HANDS",
        playerName: gkA.name,
        teamCode: teamACode,
        posGroup: "GOALKEEPER",
        statValue: `${cleanSheetsA} CLEAN SHEETS`
      },
      {
        badgeLabel: "IRON HANDS",
        badgeType: "IRON_HANDS",
        playerName: gkB.name,
        teamCode: teamBCode,
        posGroup: "GOALKEEPER",
        statValue: `${cleanSheetsB} CLEAN SHEETS`
      }
    ];

    cells.forEach(cell => {
      const cellDiv = document.createElement("div");
      cellDiv.className = "award-cell";
      cellDiv.style.cssText = `
        padding: 14px 16px;
        border-right: 1px solid #0a0a0a;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
      `;

      const badgeBg = cell.badgeType === "LIVE_WIRE" ? "#0f0f0f" : "rgba(34, 197, 94, 0.05)";
      const badgeColor = cell.badgeType === "LIVE_WIRE" ? "#888" : "var(--accent-green)";
      const badgeBorder = cell.badgeType === "LIVE_WIRE" ? "1px solid #222" : "1px solid rgba(34, 197, 94, 0.15)";
      const statColor = cell.badgeType === "LIVE_WIRE" ? "#e8e8e8" : "var(--accent-green)";

      cellDiv.innerHTML = `
        <span style="
          display: inline-block;
          font-size: 7px;
          letter-spacing: 0.15em;
          padding: 2px 7px;
          margin-bottom: 8px;
          background: ${badgeBg};
          color: ${badgeColor};
          border: ${badgeBorder};
          font-family: var(--font-label);
          text-transform: uppercase;
        ">${cell.badgeLabel}</span>
        <span style="font-family: var(--font-display); font-size: 11px; color: #e8e8e8; font-weight: 500; margin-bottom: 2px; text-transform: uppercase; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%;">${cell.playerName}</span>
        <span style="font-family: var(--font-label); font-size: 9px; color: #666; text-transform: uppercase;">${cell.teamCode} · ${cell.posGroup}</span>
        <span style="font-family: var(--font-data); font-size: 13px; font-weight: 600; margin-top: auto; color: ${statColor}; text-transform: uppercase; padding-top: 6px;">${cell.statValue}</span>
      `;
      container.appendChild(cellDiv);
    });
  }

  let lastCompletedCount = 0;

  async function initVerificationTab() {
    const notesConsole = document.getElementById("backtest-engine-notes");
    notesConsole.innerHTML = '<div class="loading-box">[RUNNING LIVE BACKTEST ENGINE...]</div>';

    try {
      const { results, metrics } = await runLiveBacktest();

      // Store count of completed matches for auto-refresh checks
      lastCompletedCount = results.length;

      renderBacktestTable(results);
      renderMetricsSummary(metrics);
      renderEngineNotes(metrics, results);

      // Show timestamp
      document.getElementById('backtest-timestamp').textContent =
        'Last computed: ' + new Date().toLocaleTimeString() + ' · ' + results.length + ' matches analysed';
    } catch (err) {
      console.error(err);
      notesConsole.innerHTML = `<div class="console-line error-line">> ERROR RUNNING LIVE BACKTEST: ${err.message}</div>`;
    }
  }

  function renderBacktestTable(results) {
    const tableBody = document.getElementById("backtest-results-body");
    tableBody.innerHTML = "";

    results.forEach(match => {
      const row = document.createElement("tr");
      row.dataset.correct = match.outcomeCorrect.toString();
      row.dataset.actualOutcome = match.actualOutcome;
      row.style.cursor = "pointer";

      const teamAObj = TEAMS.find(t => t.id === match.homeTeam) || { flag: '', name: match.homeTeam };
      const teamBObj = TEAMS.find(t => t.id === match.awayTeam) || { flag: '', name: match.awayTeam };

      // Matchup Cell
      const matchupCell = document.createElement("td");
      matchupCell.textContent = `${teamAObj.flag} ${match.homeTeam} vs ${teamBObj.flag} ${match.awayTeam}`;
      row.appendChild(matchupCell);

      // Predicted WinA/Draw/WinB Pct Cell
      const predCell = document.createElement("td");
      predCell.textContent = `${match.winA_pct.toFixed(1)}% / ${match.draw_pct.toFixed(1)}% / ${match.winB_pct.toFixed(1)}%`;
      row.appendChild(predCell);

      // Predicted Scoreline Cell
      const predScoreCell = document.createElement("td");
      predScoreCell.textContent = match.mostLikelyScoreline;
      predScoreCell.style.color = "var(--text-muted)";
      row.appendChild(predScoreCell);

      // Actual Score Cell
      const actualCell = document.createElement("td");
      actualCell.textContent = match.actualScore;
      row.appendChild(actualCell);

      // Outcome Cell
      const outcomeCell = document.createElement("td");
      outcomeCell.style.textAlign = "center";

      let outcomeSymbol = "✗";
      if (match.outcomeCorrect) {
        outcomeSymbol = "✓";
        outcomeCell.style.color = "var(--accent-green)";
        outcomeCell.style.fontWeight = "bold";
      } else if (match.actualOutcome === "DRAW") {
        outcomeSymbol = "~";
        outcomeCell.style.color = "#ffb000";
        outcomeCell.style.fontWeight = "bold";
      } else {
        outcomeCell.style.color = "var(--accent-red)";
      }
      outcomeCell.textContent = outcomeSymbol;
      row.appendChild(outcomeCell);

      tableBody.appendChild(row);

      // Simple Expandable Row details
      const detailRow = document.createElement("tr");
      detailRow.className = "details-row hidden";
      detailRow.style.backgroundColor = "var(--bg-secondary)";

      const top5Html = match.top5.map((c, i) => `${i + 1}. ${c.scoreA}-${c.scoreB} (${(c.probability * 100).toFixed(1)}%)`).join(" | ");
      detailRow.innerHTML = `
        <td colspan="5" style="font-family: var(--font-data); font-size: 10px; padding: 10px; border-bottom: 1px solid var(--border-color);">
          <div style="display: flex; flex-direction: column; gap: 4px;">
            <div><strong>TOP 5 PROBABILITIES:</strong> ${top5Html}</div>
            <div><strong>ENGINE LAMBDAS:</strong> Home λ: ${match.lambda_A.toFixed(2)} | Away λ: ${match.lambda_B.toFixed(2)}</div>
            <div><strong>DATA SOURCE:</strong> ${match.hasLiveData ? "LIVE DATA STREAM INJECTED" : "HISTORICAL BASELINES ONLY"}</div>
          </div>
        </td>
      `;
      tableBody.appendChild(detailRow);

      row.addEventListener("click", () => {
        detailRow.classList.toggle("hidden");
      });
    });

    // Re-apply active filter to rows
    const activeFilterBtn = document.querySelector("#filter-all.active, #filter-correct.active, #filter-incorrect.active, #filter-draws.active");
    if (activeFilterBtn) {
      const typeMap = {
        'filter-all': 'all',
        'filter-correct': 'true',
        'filter-incorrect': 'false',
        'filter-draws': 'draws'
      };
      const filterType = typeMap[activeFilterBtn.id] || 'all';

      const rows = tableBody.querySelectorAll("tr");
      rows.forEach(row => {
        if (row.classList.contains("details-row")) {
          row.classList.add("hidden");
          return;
        }
        if (filterType === "all") {
          row.classList.remove("hidden");
        } else if (filterType === "draws") {
          if (row.dataset.actualOutcome === "DRAW") {
            row.classList.remove("hidden");
          } else {
            row.classList.add("hidden");
          }
        } else {
          if (row.dataset.correct === filterType) {
            row.classList.remove("hidden");
          } else {
            row.classList.add("hidden");
          }
        }
      });
    }
  }

  function renderMetricsSummary(metrics) {
    const metricsContainer = document.getElementById("metrics-summary-container");
    metricsContainer.innerHTML = "";

    const formatDiff = (diff) => (diff >= 0 ? `+${diff.toFixed(1)}%` : `${diff.toFixed(1)}%`);
    const verdictColor = metrics.verdict === 'STRONG SIGNAL' ? 'var(--accent-green)' : (metrics.verdict === 'MODERATE SIGNAL' ? 'var(--accent-blue)' : 'var(--accent-red)');

    metricsContainer.innerHTML = `
      <div class="metric-row-flat">
        <span class="flat-label">OUTCOME ACCURACY:</span>
        <span class="flat-value" style="font-weight: bold; ${metrics.overall.outcomeAccuracy >= 60 ? 'color: var(--accent-green);' : (metrics.overall.outcomeAccuracy < 50 ? 'color: var(--accent-red);' : '')}">${metrics.overall.outcomeAccuracy.toFixed(1)}% (${metrics.overall.outcomeCorrect}/${metrics.overall.totalMatches})</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">HOME WIN ACCURACY:</span>
        <span class="flat-value">${metrics.byOutcome.HOME.accuracy.toFixed(1)}%</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">DRAW ACCURACY:</span>
        <span class="flat-value">${metrics.byOutcome.DRAW.accuracy.toFixed(1)}%</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">AWAY WIN ACCURACY:</span>
        <span class="flat-value">${metrics.byOutcome.AWAY.accuracy.toFixed(1)}%</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">EXACT SCORE:</span>
        <span class="flat-value">${metrics.overall.exactScoreAccuracy.toFixed(1)}% (${metrics.overall.exactScoreCorrect}/${metrics.overall.totalMatches})</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">SCORE IN TOP 5:</span>
        <span class="flat-value">${metrics.overall.top5Accuracy.toFixed(1)}% (${metrics.overall.inTop5}/${metrics.overall.totalMatches})</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">BRIER SCORE:</span>
        <span class="flat-value">${metrics.brier.score.toFixed(3)} (${metrics.brier.interpretation})</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">vs RANDOM:</span>
        <span class="flat-value">${formatDiff(metrics.baselines.vsRandom)}</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">vs NAIVE:</span>
        <span class="flat-value">${formatDiff(metrics.baselines.vsFIFA)}</span>
      </div>
      <div class="metric-row-flat">
        <span class="flat-label">CALIBRATION:</span>
        <span class="flat-value">${metrics.calibration.trend}</span>
      </div>
      <div class="metric-row-flat" style="border-top: 1px solid var(--border-color); padding-top: 8px; margin-top: 4px;">
        <span class="flat-label" style="font-weight: bold;">VERDICT:</span>
        <span class="flat-value" style="font-weight: bold; color: ${verdictColor};">${metrics.verdict}</span>
      </div>
    `;
  }

  function renderEngineNotes(metrics, results) {
    const notesConsole = document.getElementById("backtest-engine-notes");
    notesConsole.innerHTML = "";

    const drawsMissed = results.filter(r => r.actualOutcome === 'DRAW' && !r.outcomeCorrect).length;

    let totalPredGoals = 0;
    let totalActualGoals = 0;
    results.forEach(r => {
      totalPredGoals += (r.lambda_A + r.lambda_B);
      totalActualGoals += (r.actualGoalsA + r.actualGoalsB);
    });
    const avgPredGoals = results.length > 0 ? (totalPredGoals / results.length).toFixed(2) : "0.00";
    const avgActualGoals = results.length > 0 ? (totalActualGoals / results.length).toFixed(2) : "0.00";

    const misses = results.filter(r => !r.outcomeCorrect);
    const missCounts = {};
    misses.forEach(r => {
      const key = `${r.actualOutcome} predicted wrong as ${r.predictedOutcome}`;
      missCounts[key] = (missCounts[key] || 0) + 1;
    });
    let mostCommonMiss = "NONE";
    let maxMissCount = 0;
    for (const [key, count] of Object.entries(missCounts)) {
      if (count > maxMissCount) {
        maxMissCount = count;
        mostCommonMiss = key;
      }
    }

    let strongestMatchup = "N/A";
    let strongestAcc = -1;
    let weakestMatchup = "N/A";
    let weakestAcc = 101;
    for (const [key, item] of Object.entries(metrics.byTierMatchup)) {
      const parts = key.split('v');
      const label = `Tier ${parts[0]} vs Tier ${parts[1]}`;
      if (item.accuracy > strongestAcc) {
        strongestAcc = item.accuracy;
        strongestMatchup = `${label} at ${item.accuracy.toFixed(1)}%`;
      }
      if (item.accuracy < weakestAcc) {
        weakestAcc = item.accuracy;
        weakestMatchup = `${label} at ${item.accuracy.toFixed(1)}%`;
      }
    }

    const now = new Date();
    const timestamp = now.toLocaleTimeString();

    const lines = [
      `LIVE BACKTEST COMPLETE [${timestamp}]`,
      `Matches analysed: ${results.length}`,
      `Draw accuracy issue: ${drawsMissed} draws missed`,
      `Goal delta: model predicts ${avgPredGoals} avg, actual avg is ${avgActualGoals}`,
      `Most common miss: ${mostCommonMiss.toUpperCase()}`,
      `Strongest matchup: ${strongestMatchup.toUpperCase()}`,
      `Weakest matchup: ${weakestMatchup.toUpperCase()}`,
      `--- TOP 3 LARGEST PREDICTION MISSES ---`
    ];

    const sortedMisses = [...results].sort((a, b) => b.error - a.error);
    const top3Misses = sortedMisses.slice(0, 3);
    top3Misses.forEach((match, idx) => {
      lines.push(`#${idx + 1} ${match.homeTeam} vs ${match.awayTeam} — ERROR GAP: ${match.error.toFixed(1)}%`);
      lines.push(`  ACTUAL: ${match.actualOutcome} (${match.actualScore}) | PREDICTED: ${match.predictedOutcome} (A:${match.winA_pct.toFixed(1)}% D:${match.draw_pct.toFixed(1)}% B:${match.winB_pct.toFixed(1)}%)`);
    });

    typewriterLines(notesConsole, lines, "> ");
  }

  function showRecomputeBanner() {
    if (document.getElementById("recompute-notification-banner")) return;

    const banner = document.createElement("div");
    banner.id = "recompute-notification-banner";
    banner.style.cssText = `
      background-color: var(--accent-blue);
      color: black;
      font-family: var(--font-data);
      font-size: 11px;
      font-weight: bold;
      text-align: center;
      padding: 8px;
      cursor: pointer;
      border: 1px solid var(--border-color);
      margin: 8px 12px 0 12px;
      animation: pulse 2s infinite;
    `;
    banner.innerHTML = `⚡ NEW MATCH DATA DETECTED — CLICK HERE TO [RECOMPUTE]`;

    const tabControlBar = document.querySelector(".tab-control-bar");
    if (tabControlBar) {
      tabControlBar.parentNode.insertBefore(banner, tabControlBar.nextSibling);
    } else {
      document.body.prepend(banner);
    }

    banner.addEventListener("click", () => {
      initVerificationTab();
      banner.remove();
    });
  }

  // Set refresh button listener
  const btnRefreshBacktest = document.getElementById("btn-refresh-backtest");
  if (btnRefreshBacktest) {
    btnRefreshBacktest.addEventListener("click", initVerificationTab);
  }

  // Silent check for new matches every 10 minutes
  setInterval(async () => {
    try {
      const cache = await getCache();
      const completed = cache.computed?.completedMatches || [];
      if (completed.length > lastCompletedCount) {
        showRecomputeBanner();
      }
    } catch (e) {
      console.warn("Failed to check cache refresh silently:", e);
    }
  }, 10 * 60 * 1000);

  // Pre-Match Flags Rendering in Match Prediction
  function renderPreMatchFlags() {
    const teamAId = teamASelect.value;
    const teamBId = teamBSelect.value;
    const container = document.getElementById("pre-match-flags-container");

    if (teamAId === teamBId) {
      container.innerHTML = "";
      container.classList.add("hidden");
      return;
    }

    const flagsA = runPreMatchFlags(teamAId);
    const flagsB = runPreMatchFlags(teamBId);

    const hasFlagsA = flagsA.critical.length > 0 || flagsA.warning.length > 0 || flagsA.info.length > 0;
    const hasFlagsB = flagsB.critical.length > 0 || flagsB.warning.length > 0 || flagsB.info.length > 0;

    if (!hasFlagsA && !hasFlagsB) {
      container.innerHTML = "";
      container.classList.add("hidden");
      return;
    }

    container.innerHTML = "";
    container.classList.remove("hidden");

    const box = document.createElement("div");
    box.className = "pre-match-flags-box";

    const renderTeamFlags = (teamId, flags) => {
      const block = document.createElement("div");
      block.className = "pre-match-flags-team-block";

      const team = TEAMS.find(t => t.id === teamId) || { name: teamId };

      // Determine worst flag severity
      let titleClass = "";
      let prefixSym = "ℹ INFO";
      if (flags.critical.length > 0) {
        titleClass = "critical";
        prefixSym = "🔴 CRITICAL";
      } else if (flags.warning.length > 0) {
        titleClass = "warning";
        prefixSym = "⚠ WARNING";
      }

      block.innerHTML = `
        <div class="pre-match-flags-title ${titleClass}">
          ${prefixSym} — ${team.name.toUpperCase()}
        </div>
        <ul class="pre-match-flags-list">
          ${flags.critical.map(f => `<li class="critical">${f}</li>`).join('')}
          ${flags.warning.map(f => `<li class="warning">${f}</li>`).join('')}
        </ul>
      `;

      if (flags.info.length > 0) {
        const infoHtml = `
          <details style="margin-top: 4px; cursor: pointer; color: var(--text-secondary);">
            <summary style="font-size: 10px; text-transform: uppercase;">Info Notes (${flags.info.length})</summary>
            <ul class="pre-match-flags-list" style="margin-top: 4px;">
              ${flags.info.map(f => `<li class="info" style="font-size: 10px;">${f}</li>`).join('')}
            </ul>
          </details>
        `;
        block.querySelector(".pre-match-flags-list").insertAdjacentHTML('afterend', infoHtml);
      }

      return block;
    };

    if (hasFlagsA) box.appendChild(renderTeamFlags(teamAId, flagsA));
    if (hasFlagsB) box.appendChild(renderTeamFlags(teamBId, flagsB));

    container.appendChild(box);
  }

  // Update Settings Panel and Data Inspector Table
  function updateSettingsPanel() {
    if (typeof localStorage === 'undefined') return;

    const meta = JSON.parse(localStorage.getItem('oracle26_meta') || 'null');
    if (meta) {
      document.getElementById("meta-version").textContent = meta.version;
      document.getElementById("meta-total-teams").textContent = meta.total_teams;
      document.getElementById("meta-total-players").textContent = meta.total_players;
      document.getElementById("meta-last-pull").textContent = meta.last_pull_attempt
        ? new Date(meta.last_pull_attempt).toLocaleTimeString()
        : "NEVER";
    }

    const tbody = document.getElementById("inspector-table-body");
    tbody.innerHTML = "";

    TEAMS.forEach(team => {
      const teamKey = `oracle26_team_${team.id}`;
      const injuryKey = `oracle26_injuries_${team.id}`;
      const cachedTeam = JSON.parse(localStorage.getItem(teamKey) || 'null');
      const cachedInjuries = JSON.parse(localStorage.getItem(injuryKey) || 'null');

      const flags = runPreMatchFlags(team.id);
      const criticalCount = flags.critical.length;
      const warningCount = flags.warning.length;

      let rowClass = "inspector-row-ok";
      if (criticalCount > 0) rowClass = "inspector-row-critical";
      else if (warningCount > 0) rowClass = "inspector-row-warning";

      let dataQualityLabel = "UNKNOWN";
      if (cachedTeam) {
        const starters = cachedTeam.squad.filter(p => p.is_starter);
        const fullCount = starters.filter(p => p.data_quality === 'FULL').length;
        const unknownCount = starters.filter(p => p.data_quality === 'UNKNOWN').length;
        const gk = starters.find(p => p.position === 'GK');
        const cbs = starters.filter(p => p.position === 'CB');
        const keyPositionsOk = [gk, ...cbs].every(p => p && p.data_quality !== 'UNKNOWN' && p.data_quality !== 'MINIMAL');
        const isDataComplete = starters.length > 0 && (fullCount / starters.length >= 0.8) && unknownCount <= 1 && keyPositionsOk;
        dataQualityLabel = isDataComplete ? "COMPLETE" : "CAUTIOUS";
      }

      let injuryAgeLabel = "NO DATA";
      if (cachedInjuries && cachedInjuries.updated_at) {
        const ageHrs = (Date.now() - new Date(cachedInjuries.updated_at).getTime()) / 3600000;
        injuryAgeLabel = `${Math.floor(ageHrs)} hrs`;
      }

      const flagsSummary = `${criticalCount} Crit, ${warningCount} Warn`;
      const lastUpdatedStr = cachedTeam && cachedTeam.updated_at
        ? new Date(cachedTeam.updated_at).toLocaleTimeString()
        : "NEVER";

      const tr = document.createElement("tr");
      tr.className = rowClass;
      tr.id = `inspector-row-${team.id}`;
      tr.innerHTML = `
        <td style="font-weight: bold;">${team.flag} ${team.name}</td>
        <td>${cachedTeam ? cachedTeam.squad.length : 0}</td>
        <td>${dataQualityLabel}</td>
        <td>${injuryAgeLabel}</td>
        <td>${flagsSummary}</td>
        <td>${lastUpdatedStr}</td>
      `;

      const detailsTr = document.createElement("tr");
      detailsTr.className = "details-row hidden";
      detailsTr.id = `inspector-details-${team.id}`;

      const allFlagsList = [
        ...flags.critical.map(f => `<span class="flag-item critical">[CRITICAL] ${f}</span>`),
        ...flags.warning.map(f => `<span class="flag-item warning">[WARNING] ${f}</span>`),
        ...flags.info.map(f => `<span class="flag-item info">[INFO] ${f}</span>`)
      ];

      const squadList = cachedTeam ? cachedTeam.squad : [];
      const playersHtml = squadList.map(p => {
        const badgeClass = `badge-${p.data_quality.toLowerCase()}`;
        return `
          <div class="inspector-player-card">
            <div>
              <div class="inspector-player-name">${p.name}</div>
              <div class="inspector-player-meta">${p.position} | Caps: ${p.caps}</div>
            </div>
            <div style="text-align: right;">
              <span class="${badgeClass}" style="font-size: 9px; padding: 2px 4px;">${p.data_quality}</span>
              <div class="inspector-player-meta" style="margin-top: 4px;">xG: ${(p.xG_approx !== undefined ? p.xG_approx : 0.00).toFixed(2)} (${p.xG_source || 'MOCK'})</div>
            </div>
          </div>
        `;
      }).join('');

      detailsTr.innerHTML = `
        <td colspan="6">
          <div class="inspector-details-container">
            <div>
              <h4 style="font-family: var(--font-display); font-size: 11px; margin-bottom: 6px; text-transform: uppercase; color: var(--accent-green);">Flag Reports</h4>
              <div class="inspector-flags-list" style="display: flex; flex-direction: column; gap: 4px;">
                ${allFlagsList.length > 0 ? allFlagsList.join('') : '<span style="color: var(--text-secondary); font-size: 11px;">NO FLAGS REPORTED</span>'}
              </div>
            </div>
            <div class="margin-top-sm">
              <h4 style="font-family: var(--font-display); font-size: 11px; margin-bottom: 6px; text-transform: uppercase; color: var(--accent-green);">Cached Squad (${squadList.length})</h4>
              <div class="inspector-players-grid">
                ${playersHtml.length > 0 ? playersHtml : '<div style="color: var(--text-secondary); font-size: 11px;">NO PLAYERS IN SQUAD</div>'}
              </div>
            </div>
          </div>
        </td>
      `;

      tbody.appendChild(tr);
      tbody.appendChild(detailsTr);

      tr.addEventListener("click", () => {
        detailsTr.classList.toggle("hidden");
      });
    });
  }

  // Setup Remote Control Synchronization Handlers
  // Setup Remote Control Synchronization Handlers
  const btnPullSquad = document.getElementById("btn-pull-squad");
  btnPullSquad.addEventListener("click", async () => {
    btnPullSquad.disabled = true;
    btnPullSquad.style.opacity = 0.5;

    const syncConsole = document.getElementById("sync-console");
    syncConsole.innerHTML = "> INITIATING SQUAD DATA SYNC VIA DELTA sync engine...\n";
    syncConsole.innerHTML += "> Connecting to backend synchronization server...\n";
    syncConsole.scrollTop = syncConsole.scrollHeight;

    try {
      const initRes = await fetch("http://localhost:3001/api/pull", { method: "POST" });
      if (!initRes.ok) {
        const errorData = await initRes.json().catch(() => ({}));
        throw new Error(errorData.error || `Server returned status: ${initRes.status}`);
      }

      syncConsole.innerHTML += "> Pull process started. Listening to log stream...\n";
      syncConsole.scrollTop = syncConsole.scrollHeight;

      const eventSource = new EventSource("http://localhost:3001/api/pull-stream");

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.log) {
            syncConsole.innerHTML += `${data.log}\n`;
            syncConsole.scrollTop = syncConsole.scrollHeight;

            if (data.log.includes("[SUCCESS]")) {
              const match = data.log.match(/\[SUCCESS\]\s+([A-Z]{3}):/);
              if (match) {
                const teamCode = match[1];
                fetch(`http://localhost:3001/cache/${teamCode}.json`)
                  .then(res => res.json())
                  .then(teamData => {
                    deltaUpdateTeam(teamCode, teamData.squad, {});
                    reloadTeams();
                  })
                  .catch(err => {
                    syncConsole.innerHTML += `[LOCAL ERROR] Failed to fetch cache for ${teamCode}: ${err.message}\n`;
                    syncConsole.scrollTop = syncConsole.scrollHeight;
                  });
              }
            }

            if (data.log.includes("PROCESS EXITED WITH CODE")) {
              eventSource.close();
              finalizeSync();
            }
          }
        } catch (e) {
          // JSON parse error
        }
      };

      eventSource.onerror = (error) => {
        // SSE closed
        eventSource.close();
        finalizeSync();
      };

    } catch (err) {
      syncConsole.innerHTML += `\n> ERROR: Cannot connect to synchronization server.\n> Please ensure that the Express backend is running (run "npm run server" in a separate terminal).\n> Details: ${err.message}\n`;
      syncConsole.scrollTop = syncConsole.scrollHeight;
      btnPullSquad.disabled = false;
      btnPullSquad.style.opacity = 1;
    }

    function finalizeSync() {
      const meta = JSON.parse(localStorage.getItem('oracle26_meta') || '{}');
      meta.last_pull_attempt = new Date().toISOString();
      localStorage.setItem('oracle26_meta', JSON.stringify(meta));

      syncConsole.innerHTML += "\n> SYNC PROCESS CONCLUDED.";
      syncConsole.scrollTop = syncConsole.scrollHeight;

      reloadTeams();
      updateDashboard();
      updateSettingsPanel();

      btnPullSquad.disabled = false;
      btnPullSquad.style.opacity = 1;
    }
  });

  const btnUpdateInjuries = document.getElementById("btn-update-injuries");
  btnUpdateInjuries.addEventListener("click", () => {
    btnUpdateInjuries.disabled = true;
    btnUpdateInjuries.style.opacity = 0.5;

    const syncConsole = document.getElementById("sync-console");
    syncConsole.innerHTML = "> INITIATING INJURY INDEX SYNC FOR SELECTED TEAMS...\n";

    // Get the two selected teams
    const teamA = document.getElementById("team-a-select").value;
    const teamB = document.getElementById("team-b-select").value;

    const teamsToUpdate = [teamA, teamB].filter(Boolean);
    if (teamsToUpdate.length === 0) {
      syncConsole.innerHTML += "> ERROR: No teams selected for injury sync.\n";
      btnUpdateInjuries.disabled = false;
      btnUpdateInjuries.style.opacity = 1;
      return;
    }

    let completed = 0;
    teamsToUpdate.forEach(async (teamId) => {
      syncConsole.innerHTML += `[${teamId}] Fetching live injury data...\n`;
      syncConsole.scrollTop = syncConsole.scrollHeight;

      try {
        const response = await fetch(`http://localhost:3001/api/injuries?team=${teamId}`);
        if (!response.ok) {
          throw new Error(`Server returned status: ${response.status}`);
        }
        const injuryData = await response.json();

        // Save to localStorage: oracle26_injuries_{teamId}
        const key = `oracle26_injuries_${teamId}`;
        localStorage.setItem(key, JSON.stringify(injuryData));

        syncConsole.innerHTML += `[${teamId}] Injury index synchronized. (Injured: ${injuryData.injured_players.length > 0 ? injuryData.injured_players.join(', ') : 'None'})\n`;
      } catch (err) {
        syncConsole.innerHTML += `[${teamId}] ERROR syncing injuries: ${err.message}\n`;
      } finally {
        syncConsole.scrollTop = syncConsole.scrollHeight;
        completed++;
        if (completed === teamsToUpdate.length) {
          syncConsole.innerHTML += "\n> INJURY SYNC COMPLETE.";
          syncConsole.scrollTop = syncConsole.scrollHeight;

          reloadTeams();
          updateDashboard();
          updateSettingsPanel();

          btnUpdateInjuries.disabled = false;
          btnUpdateInjuries.style.opacity = 1;
        }
      }
    });
  });

  async function syncLocalWithServerCache() {
    try {
      const response = await fetch("http://localhost:3001/api/cache-status");
      if (!response.ok) return;
      const data = await response.json();

      const promises = [];
      data.teams.forEach(team => {
        if (team.lastPulled) {
          const localKey = `oracle26_team_${team.code}`;
          const localData = JSON.parse(localStorage.getItem(localKey) || 'null');

          const needsSquadSync = !localData ||
            localData.squad.some(p => p.xG_source === 'MOCK') ||
            (localData.updated_at && new Date(localData.updated_at) < new Date(team.lastPulled));

          if (needsSquadSync) {
            promises.push(
              fetch(`http://localhost:3001/cache/${team.code}.json`)
                .then(r => r.json())
                .then(serverTeam => {
                  deltaUpdateTeam(team.code, serverTeam.squad, {});
                })
            );
          }
        }

        if (team.injuryAge) {
          const localInjuriesKey = `oracle26_injuries_${team.code}`;
          const localInjuries = JSON.parse(localStorage.getItem(localInjuriesKey) || 'null');

          const needsInjurySync = !localInjuries ||
            !localInjuries.updated_at ||
            (new Date(localInjuries.updated_at) < new Date(team.injuryAge));

          if (needsInjurySync) {
            promises.push(
              fetch(`http://localhost:3001/cache/${team.code}_injuries.json`)
                .then(r => r.json())
                .then(serverInjuries => {
                  localStorage.setItem(localInjuriesKey, JSON.stringify(serverInjuries));
                })
            );
          }
        }
      });

      if (promises.length > 0) {
        await Promise.all(promises);
        reloadTeams();
        updateDashboard();
        updateSettingsPanel();
      }
    } catch (err) {
      console.warn("Failed to sync local localStorage with server cache:", err);
    }
  }

  function populateSquadDropdowns() {
    if (!squadTeamASelect || !squadTeamBSelect) return;
    [squadTeamASelect, squadTeamBSelect].forEach(select => {
      select.innerHTML = "";

      for (let t = 1; t <= 4; t++) {
        const optgroup = document.createElement("optgroup");
        optgroup.label = TIERS[t].toUpperCase();

        const tierTeams = TEAMS.filter(team => team.tier === t);
        tierTeams.sort((a, b) => a.name.localeCompare(b.name));

        tierTeams.forEach(team => {
          const option = document.createElement("option");
          option.value = team.id;
          option.textContent = `${team.flag} ${team.name} [${team.id}]`;
          optgroup.appendChild(option);
        });

        select.appendChild(optgroup);
      }
    });

    squadTeamASelect.value = teamASelect.value || "FRA";
    squadTeamBSelect.value = teamBSelect.value || "ARG";
  }

  if (squadTeamASelect && squadTeamBSelect) {
    squadTeamASelect.addEventListener("change", () => {
      lineupState.selectedPlayer = null;
      renderSquadAnalysis();
    });
    squadTeamBSelect.addEventListener("change", () => {
      lineupState.selectedPlayer = null;
      renderSquadAnalysis();
    });
  }

  const btnResetLineup = document.getElementById("btn-reset-lineup");
  if (btnResetLineup) {
    btnResetLineup.addEventListener("click", () => {
      resetTeamLineup(lineupState.teamA);
      resetTeamLineup(lineupState.teamB);
      lineupState.modified = false;
      lineupState.selectedPlayer = null;
      renderSquadAnalysis();
    });
  }

  const formationSelector = document.getElementById("formation-selector");
  if (formationSelector) {
    formationSelector.addEventListener("click", (e) => {
      const btn = e.target.closest(".formation-btn");
      if (!btn) return;

      formationSelector.querySelectorAll(".formation-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const formation = btn.dataset.formation;

      adjustStartersForFormation(lineupState.teamA, formation);
      adjustStartersForFormation(lineupState.teamB, formation);
      lineupState.modified = true;
      lineupState.selectedPlayer = null;
      renderSquadAnalysis();
    });
  }

  document.addEventListener("click", (e) => {
    if (lineupState.selectedPlayer) {
      const isPanelClick = e.target.closest(".squad-side-panel");
      const isPitchClick = e.target.closest("#pitch-svg-wrapper");
      if (!isPanelClick && !isPitchClick) {
        lineupState.selectedPlayer = null;
        renderSquadAnalysis();
      }
    }
  });


  // System Info Modal Listeners
  const btnSystemInfo = document.getElementById('btn-system-info');
  const systemInfoModal = document.getElementById('system-info-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');

  if (btnSystemInfo && systemInfoModal && btnCloseModal) {
    btnSystemInfo.addEventListener('click', () => {
      systemInfoModal.style.display = 'block';
      document.body.style.overflow = 'hidden';
    });

    btnCloseModal.addEventListener('click', () => {
      systemInfoModal.style.display = 'none';
      document.body.style.overflow = '';
    });

    systemInfoModal.addEventListener('click', (e) => {
      if (e.target === systemInfoModal) {
        systemInfoModal.style.display = 'none';
        document.body.style.overflow = '';
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && systemInfoModal.style.display === 'block') {
        systemInfoModal.style.display = 'none';
        document.body.style.overflow = '';
      }
    });
  }

  // Initialize data on load
  populateDropdowns();
  populateSquadDropdowns();
  validateTeamSelection();
  updateResolvedFixture();
  renderPreMatchFlags();
  syncLocalWithServerCache();

  initScrapedData().then(() => {
    renderQuickFixtures();
    fetch('/data/scraped/match_events.json')
      .then(r => r.json())
      .then(d => { window._allMatchEvents = d; })
      .catch(() => { window._allMatchEvents = {}; });
  });

  function renderQuickFixtures() {
    const container = document.getElementById('quick-fixture-list');
    if (!container) return;

    const upcoming = getUpcomingFixtures().slice(0, 20);
    if (!upcoming.length) {
      container.innerHTML = '<div style="font-family:var(--font-data);font-size:9px;color:#333;padding:6px 0;">— No upcoming fixtures</div>';
      return;
    }

    upcoming.forEach(f => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.style.cssText = `
        display:flex; justify-content:space-between; align-items:center;
        width:100%; padding:6px 8px;
        background:transparent; border:1px solid #1a1a1a;
        font-family:var(--font-data); font-size:9px; color:#888;
        cursor:pointer; letter-spacing:0.06em;
        transition:border-color 0.1s,color 0.1s;
        text-align:left;
      `;
      const date = new Date(f.kickoff_utc).toLocaleDateString('en-GB',{month:'short',day:'numeric'});
      btn.innerHTML = `
        <span style="color:#c8c8c8;font-weight:600;letter-spacing:0.08em;">${f.home_team.slice(0,3).toUpperCase()} <span style="color:#555;font-weight:400;">vs</span> ${f.away_team.slice(0,3).toUpperCase()}</span>
        <span style="color:#555;font-size:8px;">${date} · ${f.stage}</span>
      `;
      btn.onmouseover = () => { btn.style.borderColor='#333'; btn.style.color='#c8c8c8'; };
      btn.onmouseout = () => { btn.style.borderColor='#1a1a1a'; btn.style.color='#888'; };

      btn.onclick = () => {
        // Find team codes from TEAMS array by name match
        const teamA = TEAMS.find(t => normalizeName(t.name) === normalizeName(f.home_team) || t.name === f.home_team);
        const teamB = TEAMS.find(t => normalizeName(t.name) === normalizeName(f.away_team) || t.name === f.away_team);
        if (!teamA || !teamB) return;

        document.getElementById('team-a-select').value = teamA.id;
        document.getElementById('team-b-select').value = teamB.id;

        // Trigger change events so existing JS picks up the selection
        document.getElementById('team-a-select').dispatchEvent(new Event('change'));
        document.getElementById('team-b-select').dispatchEvent(new Event('change'));

        // Highlight selected
        container.querySelectorAll('button').forEach(b => b.style.borderColor='#1a1a1a');
        btn.style.borderColor = '#333';
        btn.style.color = '#c8c8c8';
      };

      container.appendChild(btn);
    });
  }

  async function renderExpansionModules(teamACode, teamBCode) {
    const expansionContainer = document.getElementById('expansion-modules');
    if (expansionContainer) expansionContainer.classList.remove('hidden');

    // Wire sub-tab switching
    document.querySelectorAll('.exp-tab-btn').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.exp-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        ['events','conditions','goals'].forEach(p => {
          const el = document.getElementById('exp-pane-' + p);
          if (el) el.classList.toggle('hidden', p !== btn.dataset.pane);
        });
      };
    });

    // Resolve team names in case codes were passed
    const teamAName = TEAMS.find(t => t.id === teamACode)?.name || teamACode;
    const teamBName = TEAMS.find(t => t.id === teamBCode)?.name || teamBCode;

    // Find matched fixture from scraped data
    const allFixtures = [...(getCompletedFixtures()||[]), ...(getUpcomingFixtures()||[])];
    const fixture = allFixtures.find(f => {
      const fHome = f.home_team;
      const fAway = f.away_team;
      return (fHome === teamACode || fHome === teamAName || normalizeName(fHome) === teamACode || normalizeName(fHome) === teamAName) &&
             (fAway === teamBCode || fAway === teamBName || normalizeName(fAway) === teamBCode || normalizeName(fAway) === teamBName);
    }) || null;

    // EVENTS
    renderExpEvents(fixture);

    // CONDITIONS
    await renderExpConditions(fixture);

    // GOAL MAP
    renderExpGoalMap(fixture);
  }

  function renderExpEvents(fixture) {
    const container = document.getElementById('exp-timeline-container');
    const noEvents = document.getElementById('exp-no-events');
    if (!container) return;
    container.innerHTML = '';

    if (!fixture) { if (noEvents) noEvents.style.display='block'; return; }

    const allEvents = window._allMatchEvents || {};
    const homeCode = fixture.home_team.slice(0,3).toUpperCase();
    const awayCode = fixture.away_team.slice(0,3).toUpperCase();

    const events = Object.values(allEvents).find(e => {
      const h = (e.home||'').toUpperCase();
      const a = (e.away||'').toUpperCase();
      return (h === homeCode || h.includes(homeCode)) && 
             (a === awayCode || a.includes(awayCode));
    });

    if (!events || (!events.goals?.length && !events.yellow_cards?.length && !events.red_cards?.length)) {
      if (noEvents) {
        noEvents.textContent = '— No match event data for this fixture';
        noEvents.style.display = 'block';
      }
      return;
    }
    if (noEvents) noEvents.style.display = 'none';

    // Build unified event list
    const all = [
      ...(events.goals||[]).map(e=>({...e, kind:'goal'})),
      ...(events.yellow_cards||[]).map(e=>({...e, kind:'yellow'})),
      ...(events.red_cards||[]).map(e=>({...e, kind:'red'})),
      ...(events.subs||[]).map(e=>({...e, kind:'sub'}))
    ].sort((a,b) => parseInt(a.minute) - parseInt(b.minute));

    const icon = { goal:'⚽', yellow:'🟨', red:'🟥', sub:'↕' };

    all.forEach(e => {
      const isHome = e.team === events.home;
      const row = document.createElement('div');
      row.style.cssText = 'display:grid;grid-template-columns:1fr 52px 1fr;align-items:center;padding:4px 10px;border-bottom:1px solid #0d0d0d;font-family:var(--font-data);font-size:9px;';
      row.innerHTML = `
        <div style="text-align:right;color:${isHome?'#3b82f6':'transparent'}">${isHome ? icon[e.kind] + ' ' + (e.player_id||'') : ''}</div>
        <div style="text-align:center;font-size:8px;color:#333;border:1px solid #111;padding:2px 4px;">${e.minute||'—'}</div>
        <div style="text-align:left;color:${!isHome?'#888':'transparent'}">${!isHome ? icon[e.kind] + ' ' + (e.player_id||'') : ''}</div>
      `;
      container.appendChild(row);
    });
  }

  async function renderExpConditions(fixture) {
    const set = (id, val) => { const el = document.getElementById(id); if(el) el.textContent = val || '—'; };

    // Set venue from fixture first (always available)
    set('exp-cond-venue-val', fixture?.venue || '—');

    let hasWeather = false;

    // Try FIFA API for weather
    try {
      if (!window._fifaMatchMeta) {
        const r = await fetch('https://api.fifa.com/api/v3/calendar/matches?idCompetition=17&idSeason=285023&count=104&language=en-GB', {
          headers: { 'Accept': 'application/json' }
        });
        const d = await r.json();
        window._fifaMatchMeta = d.Results || [];
      }
      const home = fixture?.home_team;
      const away = fixture?.away_team;
      const fm = window._fifaMatchMeta.find(m =>
        m.Home?.TeamName?.[0]?.Description === home ||
        m.Away?.TeamName?.[0]?.Description === away
      );
      if (fm?.Weather) {
        const w = fm.Weather;
        set('exp-cond-temp-val', w.Temperature ? w.Temperature + '°C' : '—');
        set('exp-cond-humidity-val', w.Humidity ? w.Humidity + '%' : '—');
        set('exp-cond-wind-val', w.WindSpeed ? w.WindSpeed + ' km/h' : '—');
        set('exp-cond-type-val', w.TypeLocalized?.[0]?.Description || '—');
        if (w.Temperature || w.Humidity) {
          hasWeather = true;
        }
      }
      if (fm?.Stadium) {
        set('exp-cond-venue-val', fm.Stadium.Name?.[0]?.Description || fixture?.venue || '—');
      }
    } catch(e) {
      // fail silently — venue already set above
    }

    if (!hasWeather) {
      set('exp-cond-temp-val', 'N/A');
      set('exp-cond-humidity-val', 'N/A');
      set('exp-cond-wind-val', 'N/A');
      set('exp-cond-type-val', 'PRE-MATCH');
    }
  }

  function renderExpGoalMap(fixture) {
    const pitch = document.getElementById('exp-goal-pitch');
    const noGoals = document.getElementById('exp-no-goals');
    if (!pitch) return;

    // Clear old goals, leaving the middle line intact
    pitch.innerHTML = `<div style="position:absolute;left:50%;top:0;bottom:0;width:1px;background:#111;transform:translateX(-50%);"></div>`;

    if (!fixture) { if (noGoals) noGoals.style.display='block'; return; }

    const allEvents = window._allMatchEvents || {};
    const homeCode = fixture.home_team.slice(0,3).toUpperCase();
    const awayCode = fixture.away_team.slice(0,3).toUpperCase();

    const events = Object.values(allEvents).find(e => {
      const h = (e.home||'').toUpperCase();
      const a = (e.away||'').toUpperCase();
      return (h === homeCode || h.includes(homeCode)) && 
             (a === awayCode || a.includes(awayCode));
    });

    const goals = events?.goals?.filter(g => g.x != null && g.y != null) || [];

    if (!goals || !goals.length) { if (noGoals) noGoals.style.display='block'; return; }
    if (noGoals) noGoals.style.display = 'none';

    goals.forEach(g => {
      const dot = document.createElement('div');
      dot.style.cssText = `position:absolute;width:7px;height:7px;border-radius:50%;transform:translate(-50%,-50%);left:${g.x}%;top:${g.y}%;background:${g.team===events.home?'#3b82f6':'#ef4444'};opacity:0.85;`;
      pitch.appendChild(dot);
    });
  }
});
