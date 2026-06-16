// app.js - Controller for ORACLE-26 UI and Event Handling
import { TEAMS, reloadTeams } from './data/index.js';
import { runPrediction } from './engine.js';
import { runBacktest, computeMetrics, diagnoseWeaknesses } from './verification.js';
import { runPreMatchFlags } from './engine/preMatchFlags.js';
import { deltaUpdateTeam } from './data/deltaSync.js';



document.addEventListener("DOMContentLoaded", () => {
  const teamASelect = document.getElementById("team-a-select");
  const teamBSelect = document.getElementById("team-b-select");
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
  function renderFormSquares(team, container) {
    container.innerHTML = "";
    team.last_6.forEach(result => {
      const tile = document.createElement("div");
      tile.className = `form-tile ${result}`;
      tile.textContent = result;
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

  teamASelect.addEventListener("change", () => {
    if (validateTeamSelection()) {
      renderSquadAnalysis();
      renderPreMatchFlags();
    }
  });
  teamBSelect.addEventListener("change", () => {
    if (validateTeamSelection()) {
      renderSquadAnalysis();
      renderPreMatchFlags();
    }
  });

  // Update Prediction Dashboard
  function updateDashboard() {
    const teamAId = teamASelect.value;
    const teamBId = teamBSelect.value;
    
    if (teamAId === teamBId) return;

    const teamA = TEAMS.find(t => t.id === teamAId);
    const teamB = TEAMS.find(t => t.id === teamBId);

    const options = {
      staleData: staleToggle.checked,
      injureKeyA: injuryAToggle.checked,
      injureKeyB: injuryBToggle.checked,
      stage: stageSelect.value
    };

    // Calculate prediction metrics
    const results = runPrediction(teamA, teamB, options);

    // 1. PROBABILITY BAR TEXT & LABELS
    probTeamAName.textContent = teamA.name.toUpperCase();
    probTeamBName.textContent = teamB.name.toUpperCase();
    
    probTeamAVal.textContent = `${results.winA_pct.toFixed(1)}%`;
    probDrawVal.textContent = `${results.draw_pct.toFixed(1)}%`;
    probTeamBVal.textContent = `${results.winB_pct.toFixed(1)}%`;

    // 3-Segment width transition (Discrete animation from center)
    // To animate from center on load, reset segment widths to 0, then expand.
    // However, since it is a fast interface, standard transitions do this beautifully.
    setTimeout(() => {
      probSegmentA.style.width = `${results.winA_pct}%`;
      probSegmentDraw.style.width = `${results.draw_pct}%`;
      probSegmentB.style.width = `${results.winB_pct}%`;
    }, 50);

    // 2. EXPECTED GOALS & SCORELINE CARDS
    cardXgALabel.textContent = `XG ${teamA.id}`;
    cardXgAVal.textContent = results.lambda_A.toFixed(1);
    
    cardXgBLabel.textContent = `XG ${teamB.id}`;
    cardXgBVal.textContent = results.lambda_B.toFixed(1);
    
    cardScorelineVal.textContent = results.mostLikelyScoreline;

    // 4. RECENT FORM SQUARES
    formTeamAHeader.textContent = teamA.name.toUpperCase();
    formTeamBHeader.textContent = teamB.name.toUpperCase();
    renderFormSquares(teamA, formTeamASquares);
    renderFormSquares(teamB, formTeamBSquares);

    // 5. HEAD TO HEAD BLOCK
    h2hMainRecord.textContent = results.h2hText;
    h2hMatchNote.textContent = results.h2hNote || "No notable notes in archive.";

    // 3. TOP 5 SCORELINES BAR CHART
    matrixListRows.innerHTML = "";
    const maxProb = results.top5[0].probability; // highest probability
    
    results.top5.forEach(row => {
      const percentageText = `${(row.probability * 100).toFixed(1)}%`;
      // Fill width proportional to probability relative to highest probability (highest = 100% width)
      const fillPercentage = maxProb > 0 ? (row.probability / maxProb) * 100 : 0;
      
      const matrixRow = document.createElement("div");
      matrixRow.className = "matrix-row";
      
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
    setTimeout(() => {
      confidenceMeterFill.style.width = `${results.confidence}%`;
    }, 50);

    // 8. LAYER BREAKDOWN
    layerStaticVal.textContent = `P = ${results.P_static_A.toFixed(1)}`;
    layerFormVal.textContent = `P = ${results.P_dynamic_A.toFixed(1)}`;
    layerFinalVal.textContent = `${results.winA_pct.toFixed(1)}%`;

    // 6. PREDICTION DRIVERS (ENGINE NOTES CONSOLE LOGS)
    engineNotesConsole.innerHTML = "";
    
    // Log static timestamp
    const now = new Date();
    const timestamp = now.toISOString().replace("T", " ").substring(0, 19);
    
    const lines = [
      `SYS LOG: PREDICTION ENGINE COMPILATION COMPLETE [${timestamp}]`,
      `STAGE SELECTED: ${options.stage.toUpperCase()}`,
      `STATIC BASE: P_static_A = ${results.P_static_A.toFixed(3)} | P_static_B = ${results.P_static_B.toFixed(3)}`,
      `DYNAMIC MOD: P_dynamic_A = ${results.P_dynamic_A.toFixed(3)} | P_dynamic_B = ${results.P_dynamic_B.toFixed(3)}`,
      `--- MODEL INSIGHTS OUTPUT ---`
    ];

    // Add calculations details
    results.drivers.forEach(driver => {
      lines.push(`> ${driver.toUpperCase()}`);
    });

    if (options.staleData) {
      lines.push(`WARNING: CONFIDENCE DEDUCTION APPLIED [STALE DATA DETECTED]`);
    }

    lines.forEach((lineText, idx) => {
      const line = document.createElement("div");
      line.className = "console-line";
      
      if (lineText.startsWith("WARNING:")) {
        line.classList.add("warning-line");
      } else if (lineText.startsWith("SYS LOG:") || lineText.startsWith("STAGE") || lineText.startsWith("STATIC") || lineText.startsWith("DYNAMIC")) {
        line.classList.add("muted-line");
      }
      
      line.textContent = lineText;
      engineNotesConsole.appendChild(line);
    });

    // Scroll console to bottom
    engineNotesConsole.scrollTop = engineNotesConsole.scrollHeight;

    // Update Squad Analysis
    renderSquadAnalysis();
    renderPreMatchFlags();
  }

  // Trigger Predict click handler
  predictBtn.addEventListener("click", () => {
    if (!validateTeamSelection()) return;

    // Show computing loading screen
    loadingState.classList.remove("hidden");

    // Hide calculations, wait 200ms, then render results
    setTimeout(() => {
      loadingState.classList.add("hidden");
      updateDashboard();
    }, 200);
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
    settingsView.classList.add("hidden");
    
    // Execute backtest and display results
    executeAndRenderBacktest();
  });

  btnTabSettings.addEventListener("click", () => {
    btnTabSettings.classList.add("active");
    btnTabPredictor.classList.remove("active");
    btnTabSquad.classList.remove("active");
    btnTabVerification.classList.remove("active");
    settingsView.classList.remove("hidden");
    predictorView.classList.add("hidden");
    squadAnalysisView.classList.add("hidden");
    verificationView.classList.add("hidden");
    
    updateSettingsPanel();
  });

  function renderSquadAnalysis() {
    const teamAId = teamASelect.value;
    const teamBId = teamBSelect.value;
    if (teamAId === teamBId) return;

    const teamA = TEAMS.find(t => t.id === teamAId);
    const teamB = TEAMS.find(t => t.id === teamBId);

    if (teamA) renderSingleTeamSquad(teamA, 'a');
    if (teamB) renderSingleTeamSquad(teamB, 'b');
  }

  function renderSingleTeamSquad(team, suffix) {
    const players = team.players || [];
    
    // 1. Position-based starters and keyPositionsOk
    const starters = players.filter(p => p.is_starter);
    const fullCount = starters.filter(p => p.data_quality === 'FULL').length;
    const unknownCount = starters.filter(p => p.data_quality === 'UNKNOWN').length;
    const gk = starters.find(p => p.position === 'GK');
    const cbs = starters.filter(p => p.position === 'CB');
    
    const keyPositionsOk = [gk, ...cbs].every(p => 
      p && p.data_quality !== 'UNKNOWN' && p.data_quality !== 'MINIMAL'
    );
    
    const isDataComplete = starters.length > 0 && 
                           (fullCount / starters.length >= 0.8) && 
                           unknownCount <= 1 && 
                           keyPositionsOk;

    // Mode Banner & Mode styling
    const modeBannerEl = document.getElementById(`squad-team-${suffix}-mode-banner`);
    if (isDataComplete) {
      modeBannerEl.className = "mode-status-banner banner-complete";
      modeBannerEl.textContent = "DATA-COMPLETE";
    } else {
      modeBannerEl.className = "mode-status-banner banner-cautious";
      modeBannerEl.textContent = "CAUTIOUS MODE";
    }

    // Calculate top 5 players by mean_xG_per90 descending
    const sortedPlayers = [...players].sort((a, b) => b.mean_xG_per90 - a.mean_xG_per90);
    const top5 = sortedPlayers.slice(0, 5);

    // Helper to format xG value depending on Cautious mode
    const formatXG = (val) => {
      if (!isDataComplete) {
        const low = Math.max(0, val - 0.3).toFixed(2);
        const high = (val + 0.3).toFixed(2);
        return `${low} - ${high}`;
      }
      return val.toFixed(2);
    };

    // Render Panel 1: Attacking Threat player list
    const playerListEl = document.getElementById(`squad-team-${suffix}-players`);
    playerListEl.innerHTML = "";
    
    top5.forEach(player => {
      const row = document.createElement("div");
      row.className = "player-row";
      
      // Check for X-Factor
      let xFactorBadge = "";
      if (player.xG_intl_per90 === 0 || player.best_match_source === "UNAVAILABLE") {
        xFactorBadge = `<span class="badge-awaiting" style="color: var(--text-secondary); border: 1px dashed var(--text-secondary); font-size: 8px; padding: 1px 4px; margin-left: 6px; font-weight: bold; text-transform: uppercase;">X-FACTOR EVAL: AWAITING INTL DATA</span>`;
      } else {
        const TUS = (player.xG_club_per90 * player.league_difficulty_coeff) > 0 
          ? (player.xG_intl_per90 / (player.xG_club_per90 * player.league_difficulty_coeff)) 
          : 0;
        const TUS_weighted = TUS * Math.log((player.caps || 0) + 1);
        const Ceiling = player.mean_xG_per90 > 0 
          ? ((player.xG_best_single_match - player.mean_xG_per90) / player.mean_xG_per90) 
          : 0;
          
        const hasXFactor = TUS_weighted > 1.8 && Ceiling > 1.0 
                           && player.data_quality !== 'UNKNOWN' && player.data_quality !== 'MINIMAL';

        if (hasXFactor) {
          xFactorBadge = `<span class="badge-xfactor">X-FACTOR</span>`;
        }
      }
      const qualityClass = `badge-${player.data_quality.toLowerCase()}`;
      
      row.innerHTML = `
        <div class="player-info">
          <span class="player-name">${player.name}</span>
          <span class="player-pos-badge">${player.position}</span>
          ${xFactorBadge}
        </div>
        <div class="player-badges">
          <span class="player-xg-val" style="margin-right: 8px;">${formatXG(player.mean_xG_per90)}</span>
          <span class="${qualityClass}">${player.data_quality}</span>
        </div>
      `;
      playerListEl.appendChild(row);
    });

    // Calculate sum of starter contributions (Expected Goals This Match)
    const startersSumXG = starters.reduce((sum, p) => sum + p.mean_xG_per90, 0);
    const totalXGEl = document.getElementById(`squad-team-${suffix}-total-xg`);
    totalXGEl.textContent = formatXG(startersSumXG);

    // Panel 2: Squad Confidence progress bar
    const completenessPct = starters.length > 0 ? (fullCount / starters.length) * 100 : 0;
    document.getElementById(`squad-team-${suffix}-full-pct`).textContent = `${completenessPct.toFixed(0)}%`;
    
    const barEl = document.getElementById(`squad-team-${suffix}-full-bar`);
    barEl.style.width = `${completenessPct}%`;
    barEl.className = "confidence-meter-fill " + (isDataComplete ? "HIGH" : "LOW");

    // Panel 3: Star Dependency & Depth
    // Starters sorted by mean_xG_per90 descending
    const sortedStarters = [...starters].sort((a, b) => b.mean_xG_per90 - a.mean_xG_per90);
    const player_1 = sortedStarters[0] || { mean_xG_per90: 0 };
    const player_1_xg = player_1.mean_xG_per90;
    
    // Depth score calculation
    const players_2_to_5 = sortedStarters.slice(1, 5);
    let depthScore = 0;
    if (players_2_to_5.length > 0 && player_1_xg > 0) {
      const mean_players_2_to_5_xg = players_2_to_5.reduce((sum, p) => sum + p.mean_xG_per90, 0) / players_2_to_5.length;
      depthScore = mean_players_2_to_5_xg / player_1_xg;
    }

    // SRI (Star Reliance Index) percentage
    // SRI = (top starter xG / sum of all starters xG) * 100
    const sriPct = startersSumXG > 0 ? (player_1_xg / startersSumXG) * 100 : 0;

    // Team xG with top player removed (conservative subtraction only)
    const xgRemoved = startersSumXG - player_1_xg;

    // Display Star Dependency values
    document.getElementById(`squad-team-${suffix}-xg-inc`).textContent = formatXG(startersSumXG);
    document.getElementById(`squad-team-${suffix}-xg-exc`).textContent = formatXG(xgRemoved);
    document.getElementById(`squad-team-${suffix}-sri-val`).textContent = `${sriPct.toFixed(1)}%`;
    document.getElementById(`squad-team-${suffix}-depth-val`).textContent = depthScore.toFixed(2);

    // SRI Classification Banner & text explanation
    let classification = "DISTRIBUTED";
    let explanation = "";
    let sriBannerClass = "sri-classification-banner banner-distributed";

    if (sriPct < 35) {
      classification = "DISTRIBUTED";
      explanation = `${team.name} exhibits a distributed attacking structure, reducing tactical reliance on any single individual.`;
      sriBannerClass = "sri-classification-banner banner-distributed";
    } else if (sriPct >= 35 && sriPct <= 60) {
      classification = "DEPENDENT";
      explanation = `${team.name}'s offense is dependent on ${player_1.name || 'their top forward'}, presenting a clear focal point for opposition scouts.`;
      sriBannerClass = "sri-classification-banner banner-dependent";
    } else {
      classification = "FRAGILE";
      explanation = `${team.name}'s system is fragile. Neutralizing ${player_1.name || 'their star player'} will likely collapse their entire offensive production.`;
      sriBannerClass = "sri-classification-banner banner-fragile";
    }

    const sriBannerEl = document.getElementById(`squad-team-${suffix}-sri-banner`);
    sriBannerEl.className = sriBannerClass;
    sriBannerEl.textContent = classification;

    document.getElementById(`squad-team-${suffix}-explanation`).textContent = explanation;

    // Title and Flag metadata headers
    document.getElementById(`squad-team-${suffix}-title`).textContent = `${team.name.toUpperCase()} SQUAD ANALYSIS`;
    document.getElementById(`squad-team-${suffix}-flag`).textContent = `${team.flag} ${team.id}`;
  }

  function executeAndRenderBacktest() {
    const backtestResults = runBacktest();
    const metrics = computeMetrics(backtestResults);

    // 1. Render Results Table
    const tableBody = document.getElementById("backtest-results-body");
    tableBody.innerHTML = "";
    backtestResults.forEach(match => {
      const row = document.createElement("tr");
      
      const matchupCell = document.createElement("td");
      matchupCell.textContent = `${match.teamA} vs ${match.teamB}`;
      row.appendChild(matchupCell);

      const predCell = document.createElement("td");
      predCell.textContent = `${match.predictedWinA.toFixed(1)}% / ${match.predictedDraw.toFixed(1)}% / ${match.predictedWinB.toFixed(1)}%`;
      row.appendChild(predCell);

      const actualCell = document.createElement("td");
      actualCell.textContent = `${match.actualGoalsA}-${match.actualGoalsB}`;
      row.appendChild(actualCell);

      const outcomeCell = document.createElement("td");
      outcomeCell.style.textAlign = "center";
      if (match.correct) {
        outcomeCell.textContent = "✓";
        outcomeCell.className = "correct-cell";
      } else {
        outcomeCell.textContent = "✗";
        outcomeCell.className = "incorrect-cell";
      }
      row.appendChild(outcomeCell);

      tableBody.appendChild(row);
    });

    // 2. Render Metrics Summary
    const metricsContainer = document.getElementById("metrics-summary-container");
    metricsContainer.innerHTML = "";

    // Outcome Accuracy block
    const accuracyRow = document.createElement("div");
    accuracyRow.className = "metric-row-flat";
    
    const accuracyLabel = document.createElement("span");
    accuracyLabel.className = "flat-label";
    accuracyLabel.textContent = "OUTCOME ACCURACY:";
    accuracyRow.appendChild(accuracyLabel);

    const accuracyVal = document.createElement("span");
    accuracyVal.className = "flat-value";
    accuracyVal.textContent = `${metrics.outcomeAccuracy.toFixed(1)}%`;
    if (metrics.outcomeAccuracy > 60) {
      accuracyVal.classList.add("accuracy-green");
    } else if (metrics.outcomeAccuracy < 50) {
      accuracyVal.classList.add("accuracy-red");
    }
    accuracyRow.appendChild(accuracyVal);
    metricsContainer.appendChild(accuracyRow);

    // Avg Confidence block
    const confidenceRow = document.createElement("div");
    confidenceRow.className = "metric-row-flat";
    
    const confidenceLabel = document.createElement("span");
    confidenceLabel.className = "flat-label";
    confidenceLabel.textContent = "AVG CONFIDENCE:";
    confidenceRow.appendChild(confidenceLabel);

    const confidenceVal = document.createElement("span");
    confidenceVal.className = "flat-value";
    confidenceVal.textContent = metrics.avgConfidence.toFixed(1);
    confidenceRow.appendChild(confidenceVal);
    metricsContainer.appendChild(confidenceRow);

    // Upsets Missed block
    const upsetsRow = document.createElement("div");
    upsetsRow.className = "metric-row-flat flex-column";
    upsetsRow.style.alignItems = "stretch";
    
    const upsetsLabel = document.createElement("span");
    upsetsLabel.className = "flat-label";
    upsetsLabel.textContent = "UPSETS MISSED:";
    upsetsRow.appendChild(upsetsLabel);

    const upsetsConsole = document.createElement("div");
    upsetsConsole.className = "upset-list-console";

    if (metrics.upsets.length === 0) {
      upsetsConsole.textContent = "NONE";
    } else {
      metrics.upsets.forEach(match => {
        const upsetLine = document.createElement("div");
        upsetLine.className = "upset-item-line";
        
        const actualWinnerProb =
          match.actualOutcome === 'A' ? match.predictedWinA :
          match.actualOutcome === 'B' ? match.predictedWinB :
          match.predictedDraw;
        
        upsetLine.textContent = `> ${match.teamA} vs ${match.teamB} — predicted ${match.predictedOutcome}, actual ${match.actualOutcome} (prob: ${actualWinnerProb.toFixed(1)}%)`;
        upsetsConsole.appendChild(upsetLine);
      });
    }
    upsetsRow.appendChild(upsetsConsole);
    metricsContainer.appendChild(upsetsRow);

    // Goal Prediction Delta block
    const goalDeltaRow = document.createElement("div");
    goalDeltaRow.className = "metric-row-flat";
    
    const goalDeltaLabel = document.createElement("span");
    goalDeltaLabel.className = "flat-label";
    goalDeltaLabel.textContent = "GOAL PREDICTION DELTA:";
    goalDeltaRow.appendChild(goalDeltaLabel);

    const goalDeltaVal = document.createElement("span");
    goalDeltaVal.className = "flat-value";
    goalDeltaVal.textContent = `ΔA=${metrics.avgGoalDeltaA.toFixed(1)}  ΔB=${metrics.avgGoalDeltaB.toFixed(1)}`;
    goalDeltaRow.appendChild(goalDeltaVal);
    metricsContainer.appendChild(goalDeltaRow);

    // 3. Render Engine Notes - Backtesting (Top 3 Misses & Weaknesses)
    const notesConsole = document.getElementById("backtest-engine-notes");
    notesConsole.innerHTML = "";

    const misses = backtestResults.map(match => {
      const actualOutcomeProb =
        match.actualOutcome === 'A' ? match.predictedWinA :
        match.actualOutcome === 'B' ? match.predictedWinB :
        match.predictedDraw;
      
      const gap = 100 - actualOutcomeProb;
      return { ...match, gap };
    });

    misses.sort((a, b) => b.gap - a.gap);
    const top3Misses = misses.slice(0, 3);

    const now = new Date();
    const timestamp = now.toISOString().replace("T", " ").substring(0, 19);

    const logHeader = document.createElement("div");
    logHeader.className = "console-line muted-line";
    logHeader.textContent = `SYS LOG: BACKTEST ENGINE ANALYSIS COMPLETE [${timestamp}]`;
    notesConsole.appendChild(logHeader);

    // Call diagnoseWeaknesses and print them
    const diagnosisHeader = document.createElement("div");
    diagnosisHeader.className = "console-line muted-line";
    diagnosisHeader.style.marginTop = "8px";
    diagnosisHeader.textContent = "--- SYSTEM DIAGNOSTIC REPORT ---";
    notesConsole.appendChild(diagnosisHeader);

    const weaknesses = diagnoseWeaknesses(backtestResults);
    weaknesses.forEach(weakness => {
      const weaknessLine = document.createElement("div");
      weaknessLine.className = "console-line";
      weaknessLine.textContent = `> ${weakness}`;
      notesConsole.appendChild(weaknessLine);
    });

    const subHeader = document.createElement("div");
    subHeader.className = "console-line muted-line";
    subHeader.style.marginTop = "12px";
    subHeader.textContent = "--- TOP 3 LARGEST PREDICTION MISSES ---";
    notesConsole.appendChild(subHeader);

    top3Misses.forEach((match, idx) => {
      const rankLine = document.createElement("div");
      rankLine.className = "console-line warning-line";
      rankLine.style.marginTop = "8px";
      rankLine.textContent = `> #${idx + 1} ${match.teamA} vs ${match.teamB} — ERROR GAP: ${match.gap.toFixed(1)}%`;
      notesConsole.appendChild(rankLine);

      const detailLine = document.createElement("div");
      detailLine.className = "console-line";
      detailLine.textContent = `  ACTUAL: ${match.actualOutcome} (${match.actualGoalsA}-${match.actualGoalsB}) | PREDICTED: ${match.predictedOutcome} (A:${match.predictedWinA.toFixed(1)}% D:${match.predictedDraw.toFixed(1)}% B:${match.predictedWinB.toFixed(1)}%)`;
      notesConsole.appendChild(detailLine);
    });
  }

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

  // Initialize data on load
  populateDropdowns();
  validateTeamSelection();
  updateDashboard();
  renderPreMatchFlags();
  syncLocalWithServerCache();
});
