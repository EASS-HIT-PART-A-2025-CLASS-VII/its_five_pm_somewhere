import React from 'react';
import {
  Box,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Chip,
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import { DrinkRecipe } from '../client';

interface RecipePageProps {
  drink: DrinkRecipe;
  toggleFavoriteStatus: (drinkId: string) => void;
}

export const RecipePage: React.FC<RecipePageProps> = ({
  drink,
  toggleFavoriteStatus,
}) => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4" component="h1">
          {drink.name}
        </Typography>
        <IconButton onClick={() => toggleFavoriteStatus(drink.id!)}>
          {drink.isFavorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
        </IconButton>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Chip label={drink.type} color="primary" />
      </Box>

      <img
        src={drink.imageUrl ?? ""}
        alt={drink.name}
        style={{
          width: '100%',
          borderRadius: '12px',
          maxHeight: '300px',
          objectFit: 'cover',
          marginBottom: '16px',
        }}
      />

      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', sm: 'row' },
          gap: 2,
        }}
      >
        <Box sx={{ flex: { xs: 1, sm: '0 0 33%' }, maxWidth: { sm: '33%' } }}>
          <Typography variant="h6" gutterBottom>
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
          <Typography variant="h6" gutterBottom>
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
