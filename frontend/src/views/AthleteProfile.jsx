import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function AthleteProfile() {
  const { id } = useParams();
  const [athlete, setAthlete] = useState(null);

  useEffect(() => {
    fetch(`/api/athletes/${id}`)
      .then((res) => res.json())
      .then((data) => setAthlete(data))
      .catch((err) => console.error('Failed to fetch athlete', err));
  }, [id]);

  if (!athlete) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-container container">
      <h2>{athlete.user.full_name}</h2>
      <p>{athlete.bio}</p>
      <p>Date of Birth: {athlete.date_of_birth}</p>
    </div>
  );
}
