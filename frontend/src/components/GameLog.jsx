import { useEffect, useState } from 'react';

export default function GameLog({ athleteId }) {
  const [games, setGames] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [season, setSeason] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const perPage = 5;

  // Load available seasons from stat summary
  useEffect(() => {
    if (!athleteId) return;
    fetch(`/api/athletes/${athleteId}/stats/summary`)
      .then((res) => res.json())
      .then((data) => {
        const keys = Object.keys(data || {}).filter((s) => s !== 'career').sort();
        setSeasons(keys);
        if (!season && keys.length) {
          setSeason(keys[keys.length - 1]);
        }
      })
      .catch((err) => console.error('Failed to load seasons', err));
  }, [athleteId]);

  // Load games when season or page changes
  useEffect(() => {
    if (!athleteId) return;
    const params = new URLSearchParams();
    if (season) params.append('season', season);
    params.append('page', page);
    params.append('per_page', perPage);
    fetch(`/api/athletes/${athleteId}/game-log?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setGames(data);
          setTotal(data.length);
        } else {
          setGames(data.items || []);
          setTotal(data.total || 0);
        }
      })
      .catch((err) => console.error('Failed to load game log', err));
  }, [athleteId, season, page]);

  const lastPage = Math.max(1, Math.ceil(total / perPage));

  return (
    <div className="game-log">
      <h3>Game Log{season ? ` (${season})` : ''}</h3>
      {seasons.length > 0 && (
        <select
          value={season}
          onChange={(e) => {
            setSeason(e.target.value);
            setPage(1);
          }}
        >
          {seasons.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      )}
      <table className="stat-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Opponent</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {games.map((g) => (
            <tr key={g.game_id}>
              <td>{g.date}</td>
              <td>{g.opponent_name}</td>
              <td>
                {g.home_team_score} - {g.visitor_team_score}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {lastPage > 1 && (
        <div className="pagination">
          <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}>
            Prev
          </button>
          <span>
            {page} / {lastPage}
          </span>
          <button onClick={() => setPage((p) => Math.min(lastPage, p + 1))} disabled={page === lastPage}>
            Next
          </button>
        </div>
      )}
    </div>
  );
}
