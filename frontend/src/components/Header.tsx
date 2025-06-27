import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography } from '@mui/material';
import styled from 'styled-components';

export const APP_BAR_HEIGHT = 64;

const StyledAppBar = styled(AppBar)`
  background-color: #3f51b5;
  height: ${APP_BAR_HEIGHT}px;
  position: sticky;
  top: 0;
  z-index: 100;
`;

const Logo = styled(Typography)`
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
`;


const Header = () => {
  const navigate = useNavigate();

  return (
    <StyledAppBar>
      <Toolbar sx={{ gap: '20px' }}>
        <Logo
          variant="h6"
          onClick={() => navigate('/')}
          sx={{ cursor: 'pointer' }}
        >
          🍸 MixMaster
        </Logo>
      </Toolbar>
    </StyledAppBar>
  );
};

export default Header;
