import { NavLink } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <h1 className="logo">🍸 MixMaster</h1>
      <nav className="nav">
        <NavLink to="/" className="nav-link">Home</NavLink>
        <NavLink to="/add" className="nav-link">Add Drink</NavLink>
        <NavLink to="/profile" className="nav-link">Profile</NavLink>
      </nav>
    </header>
  );
};

export default Header;
