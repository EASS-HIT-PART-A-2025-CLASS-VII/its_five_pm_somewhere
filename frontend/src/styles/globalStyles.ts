import { Box } from '@mui/material';
import styled, { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  body {
    margin: 0;
    font-family: 'Roboto', sans-serif;
    background-color: #fff;
    color: #333;
  }

  * {
    box-sizing: border-box;
  }

  a {
    text-decoration: none;
  }

  .MuiTypography-root {
    font-family: 'Roboto', sans-serif;
  }
`;

export default GlobalStyles;

export const SquareImageBox = styled(Box)`
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 0 auto 24px;
  &:before {
    content: "";
    display: block;
    padding-top: 100%;
  }
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

export const DrinkImage = styled.img`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
`;
