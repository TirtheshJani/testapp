import { Routes, Route, Link } from 'react-router-dom';
import AthleteList from './components/AthleteList';
import AthleteProfile from './views/AthleteProfile';

export default function App() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
      </nav>
      <Routes>
        <Route path="/" element={<AthleteList />} />
        <Route path="/athletes/:id" element={<AthleteProfile />} />
      </Routes>
    </div>
  );
}
