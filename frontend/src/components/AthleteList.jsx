import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function AthleteList() {
  const [athletes, setAthletes] = useState([]);

  useEffect(() => {
    fetch('/api/athletes')
      .then((res) => res.json())
      .then((data) => setAthletes(data.items || []))
      .catch((err) => console.error('Failed to fetch athletes', err));
  }, []);

  return (
    <div>
      <h1>Athletes</h1>
      <ul>
        {athletes.map((a) => (
          <li key={a.athlete_id}>
            <Link to={`/athletes/${a.athlete_id}`}>{a.user.full_name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
