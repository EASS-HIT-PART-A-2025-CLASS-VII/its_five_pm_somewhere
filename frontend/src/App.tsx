import { DrinkProvider } from './contexts/DrinkContext';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import Home from './pages/Home';
import Profile from './pages/Profile';
import AddDrink from './pages/AddDrink';
import Recipe from './pages/Recipe';
import NotFound from './pages/NotFound';

const App: React.FC = () => {
  return (
    <DrinkProvider>
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/add" element={<AddDrink />} />
          <Route path="/recipe/:id" element={<Recipe />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </DrinkProvider>
  );
};

export default App;
