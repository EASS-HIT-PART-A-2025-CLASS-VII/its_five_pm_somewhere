import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDrinkContext } from '../contexts/DrinkContext';
import {
  Box,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import { DrinkRecipe } from '../client';
import { getPexelsImageUrl } from '../utils/imageService';
import styled from 'styled-components';
import { MAX_WIDTH_PAGE } from '../constants';

const LOADING_TIMEOUT_MS = 3000;

const SquareImageBox = styled(Box)`
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

const DrinkImage = styled.img`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
`;

export const Recipe = () => {
  const { id } = useParams<{ id: string }>();
  const { getDrinkById, toggleFavoriteStatus } = useDrinkContext();
  const [drink, setDrink] = useState<DrinkRecipe | null | undefined>(undefined);
  const [timedOut, setTimedOut] = useState(false);

  useEffect(() => {
    if (id) {
      const foundDrink = getDrinkById(id);
      if (foundDrink) {
        setDrink(foundDrink);
      } else {
        const timer = setTimeout(() => setTimedOut(true), LOADING_TIMEOUT_MS);
        return () => clearTimeout(timer);
      }
    }
  }, [id, getDrinkById]);

  if (drink === undefined) {
    if (timedOut) {
      return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="calc(100vh - 64px)">
          <Typography variant="h6" color="textSecondary">
            We can’t find this drink… perhaps it’s still being shaken up?
          </Typography>
        </Box>
      );
    }
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="calc(100vh - 64px)">
        <CircularProgress />
      </Box>
    );
  }

  if (drink === null) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="calc(100vh - 64px)">
        <Typography variant="h6" color="textSecondary">
          Your drink has not been found.
        </Typography>
      </Box>
    );
  }

  return (
    <Box maxWidth={MAX_WIDTH_PAGE + "px"} margin="auto" p={3} pt={10}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h3" component="h1" fontWeight={600}>
          {drink.name}
        </Typography>
        <IconButton onClick={() => toggleFavoriteStatus(drink.id!)}>
          {drink.isFavorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
        </IconButton>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Chip label={drink.type} color="primary" />
      </Box>

      <SquareImageBox>
        <DrinkImage
          src={getPexelsImageUrl(drink.imageId)}
          alt={drink.name}
        />
      </SquareImageBox>

      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', sm: 'row' },
          gap: 3,
        }}
      >
        <Box sx={{ flex: { xs: 1, sm: '0 0 33%' }, maxWidth: { sm: '33%' } }}>
          <Typography variant="h5" gutterBottom>
            Ingredients
          </Typography>
          <List dense>
            {drink.ingredients.map((ing, i) => (
              <ListItem key={i} sx={{ wordBreak: 'break-word' }}>
                <ListItemText
                  primary={`${ing.name} — ${ing.unit === 'top_up' ? 'top up to taste' : `${ing.amount} ${ing.unit}`}`}
                />
              </ListItem>
            ))}
          </List>
        </Box>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5" gutterBottom>
            Instructions
          </Typography>
          <List>
            {drink.instructions.map((step, i) => (
              <ListItem key={i} sx={{ wordBreak: 'break-word' }}>
                <ListItemText primary={`${i + 1}. ${step}`} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Box>
    </Box>
  );
};

export default Recipe;
