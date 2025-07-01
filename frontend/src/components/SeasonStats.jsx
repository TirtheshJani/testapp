import { useEffect, useState } from 'react';

export default function SeasonStats({ athleteId }) {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    if (!athleteId) return;
    fetch(`/api/athletes/${athleteId}/stats/summary`)
      .then((res) => res.json())
      .then(setSummary)
      .catch((err) => console.error('Failed to load stat summary', err));
  }, [athleteId]);

  if (!summary) return null;

  const seasons = Object.keys(summary).sort();
  const statNames = new Set();
  seasons.forEach((season) => {
    const stats = summary[season] || {};
    Object.keys(stats).forEach((name) => statNames.add(name));
  });
  const columns = Array.from(statNames);

  const highs = {};
  columns.forEach((name) => {
    let max = -Infinity;
    seasons.forEach((season) => {
      const value = parseFloat(summary[season][name]);
      if (!isNaN(value) && value > max) {
        max = value;
      }
    });
    highs[name] = max;
  });

  return (
    <div className="season-stats">
      <h3>Season Totals</h3>
      <table className="stat-table">
        <thead>
          <tr>
            <th>Season</th>
            {columns.map((name) => (
              <th key={name}>{name}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {seasons.map((season) => (
            <tr key={season}>
              <td>{season}</td>
              {columns.map((name) => {
                const value = summary[season][name];
                const num = parseFloat(value);
                const isHigh = !isNaN(num) && num === highs[name];
                return (
                  <td key={name} className={isHigh ? 'career-high' : undefined}>
                    {value || '-'}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
