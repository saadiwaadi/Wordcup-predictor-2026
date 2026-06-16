// h2h.js - Head-to-head records
const rawH2H = {
  "FRA-ARG": { wins: 2, draws: 1, losses: 2, note: "2022 WC Final — ARG won pens" },
  "FRA-ENG": { wins: 3, draws: 1, losses: 1, note: "France dominant recently" },
  "BRA-ARG": { wins: 2, draws: 2, losses: 1, note: "Classic rivalry" },
  "ESP-ENG": { wins: 3, draws: 0, losses: 2, note: "Spain edges recent form" },
  "GER-ENG": { wins: 2, draws: 1, losses: 2, note: "England beat GER EURO 2021" },
  "MAR-FRA": { wins: 1, draws: 1, losses: 3, note: "Morocco beat France 2022 WC Semi" },
  "ARG-ESP": { wins: 2, draws: 2, losses: 1, note: "Argentina won 2023 Finalissima" },
  "JPN-GER": { wins: 1, draws: 0, losses: 2, note: "Japan shocked Germany 2022 WC" },
  "USA-ENG": { wins: 0, draws: 2, losses: 2, note: "Drew 0-0 in 2022 WC group" },
  "POR-FRA": { wins: 1, draws: 2, losses: 2, note: "France beat Portugal EURO 2016" },
  "BEL-FRA": { wins: 1, draws: 1, losses: 3, note: "France beat Belgium 2018 WC Semi" },
  "NED-ARG": { wins: 1, draws: 2, losses: 2, note: "ARG beat NED on pens 2022 WC" }
};

const H2H = {};

Object.entries(rawH2H).forEach(([key, data]) => {
  const [teamA, teamB] = key.split("-");
  
  if (!H2H[teamA]) H2H[teamA] = {};
  if (!H2H[teamB]) H2H[teamB] = {};
  
  H2H[teamA][teamB] = {
    wins: data.wins,
    draws: data.draws,
    losses: data.losses,
    note: data.note
  };
  
  H2H[teamB][teamA] = {
    wins: data.losses,
    draws: data.draws,
    losses: data.wins,
    note: data.note
  };
});

export { H2H };
