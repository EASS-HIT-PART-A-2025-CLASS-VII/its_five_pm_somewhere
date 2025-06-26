import { createGlobalStyle } from 'styled-components';

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
