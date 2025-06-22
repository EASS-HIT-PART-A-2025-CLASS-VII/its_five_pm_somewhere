import React from 'react';
import { NavLink } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import styled from 'styled-components';

export const APP_BAR_HEIGHT = 64;

const StyledAppBar = styled(AppBar)`
  background-color: #3f51b5;
  height: ${APP_BAR_HEIGHT}px;
`;

const Logo = styled(Typography)`
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
`;

const StyledNav = styled(Box)`
  display: flex;
  gap: 20px;
`;

const StyledNavLink = styled(NavLink)`
  color: white;
  text-decoration: none;
  font-size: 1rem;

  /* Active Link Style */
  &.active {
    border-bottom: 2px solid white;
  }

  &:hover {
    opacity: 0.8;
  }
`;

const Header: React.FC = () => {
  return (
    <StyledAppBar position="sticky">
      <Toolbar sx={{ gap: '20px' }}>
        <Logo variant="h6">🍸 MixMaster</Logo>
        <StyledNav>
          {['/', '/add', '/profile'].map((path, index) => (
            <StyledNavLink
              key={index}
              to={path}
              className={({ isActive }: { isActive: boolean }) => (isActive ? 'active' : '')}
            >
              {path === '/' ? 'Home' : path === '/add' ? 'Add Drink' : 'Profile'}
            </StyledNavLink>
          ))}
        </StyledNav>
      </Toolbar>
    </StyledAppBar>
  );
};

export default Header;
