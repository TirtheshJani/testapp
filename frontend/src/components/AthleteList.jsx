import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function AthleteList() {
  const [athletes, setAthletes] = useState([]);
  const [q, setQ] = useState('');
  const [sport, setSport] = useState('');
  const [minAge, setMinAge] = useState('');
  const [maxAge, setMaxAge] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAthletes = () => {
    setLoading(true);
    setError(null);

    const params = new URLSearchParams();
    if (q) params.append('q', q);
    if (sport) params.append('sport', sport);
    if (minAge) params.append('min_age', minAge);
    if (maxAge) params.append('max_age', maxAge);

    fetch(`/api/athletes/search?${params.toString()}`)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then((data) => setAthletes(data.results || []))
      .catch((err) => {
        console.error('Failed to fetch athletes', err);
        setError('Failed to fetch athletes');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAthletes();
  }, []);

  return (
    <div>
      <h1>Athletes</h1>
      <div>
        <input
          type="text"
          placeholder="Search..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <input
          type="text"
          placeholder="Sport"
          value={sport}
          onChange={(e) => setSport(e.target.value)}
        />
        <input
          type="number"
          placeholder="Min Age"
          value={minAge}
          onChange={(e) => setMinAge(e.target.value)}
        />
        <input
          type="number"
          placeholder="Max Age"
          value={maxAge}
          onChange={(e) => setMaxAge(e.target.value)}
        />
        <button onClick={fetchAthletes}>Search</button>
      </div>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <ul>
          {athletes.map((a) => (
            <li key={a.athlete_id}>
              <Link to={`/athletes/${a.athlete_id}`}>{a.user.full_name}</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
