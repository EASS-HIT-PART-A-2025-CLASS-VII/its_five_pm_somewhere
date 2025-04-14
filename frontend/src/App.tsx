import { DrinkProvider } from './contexts/DrinkContext';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header'
import Home from './pages/Home';
import Profile from './pages/Profile';
import AddDrink from './pages/AddDrink';
import Recipe from './pages/Recipe';
import NotFound from './pages/NotFound';
import GlobalError from './components/GlobalError';
import { Container } from '@mui/material';
import styled from 'styled-components';
import GlobalStyles from './styles/globalStyles';

// Styled components for layout
const Layout = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

const MainContent = styled.main`
  flex-grow: 1;
  padding: 20px;
  background-color: #fff;
`;

const App: React.FC = () => {
  return (
    <>
      <GlobalStyles />
      <DrinkProvider>
        <Router>
          <Layout>
            <Header />
            <GlobalError />
            <MainContent>
              <Container maxWidth="lg">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/add" element={<AddDrink />} />
                  <Route path="/recipe/:id" element={<Recipe />} />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Container>
            </MainContent>
          </Layout>
        </Router>
      </DrinkProvider>
    </>
  );
};

export default App;
