import {
  Box,
  Typography,
  TextField,
  Button,
  ToggleButton,
  ToggleButtonGroup,
  ListItem,
  ListItemAvatar,
  Avatar,
  ListItemText,
  Chip,
  Stack,
  IconButton,
  Tooltip
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ShuffleIcon from '@mui/icons-material/Shuffle';
import SearchIcon from '@mui/icons-material/Search';
import { useDrinkContext } from '../contexts/DrinkContext';
import { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { MAX_WIDTH_PAGE } from '../constants';
import { getPexelsImageUrl } from '../utils/imageService';
import IngredientSelectModal from '../components/IngredientSelectModal';
import { Lightbox } from '../components/Lightbox';


const DrinkCard = styled(ListItem)`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 12px;
  min-width: 180px;
  max-width: 220px;
  height: 240px;
  box-sizing: border-box;
  &:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }
  @media (max-width: 600px) {
    flex-direction: row;
    width: 100%;
    height: auto;
    min-width: auto;
    max-width: none;
    margin-bottom: 8px;
  }
`;

const Home = () => {
  const navigate = useNavigate();
  const { drinks, ingredientsToChoose, fetchRandomDrink, toggleFavoriteStatus, generateDrink } = useDrinkContext();
  const [search, setSearch] = useState('');
  const [alcoholFilter, setAlcoholFilter] = useState<'all' | 'alcoholic' | 'non-alcoholic'>('all');
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [ingredientModalOpen, setIngredientModalOpen] = useState(false);
  const types = Array.from(new Set(drinks.map(d => d.type)));


  const handleAlcoholFilter = (_: any, newValue: any) => {
    if (newValue) setAlcoholFilter(newValue);
  };

  const handleTypeClick = (type: string) => {
    setSelectedTypes(prev =>
      prev.includes(type)
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  const handleGetRandomDrink = async () => {
    const randomDrink = await fetchRandomDrink();
    navigate(`/recipe/${randomDrink.id}`);
  };

  const filteredDrinks = drinks.filter(drink => {
    const matchesSearch = drink.name.toLowerCase().includes(search.toLowerCase());
    const matchesAlcohol =
      alcoholFilter === 'all' ||
      (alcoholFilter === 'alcoholic' && drink.alcoholContent) ||
      (alcoholFilter === 'non-alcoholic' && !drink.alcoholContent);
    const matchesTypes = selectedTypes.length === 0 || selectedTypes.includes(drink.type);
    return matchesSearch && matchesAlcohol && matchesTypes;
  });

  return (
    <>
      <Box p={3} maxWidth={MAX_WIDTH_PAGE + "px"} margin="auto">
        <Typography variant="h4" fontWeight={600} gutterBottom>
          Discover Drinks 🍹
        </Typography>

        <Stack direction="row" spacing={2} mb={2}>
          <TextField
            fullWidth
            placeholder="Explore drinks by name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{ endAdornment: <SearchIcon color="action" /> }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={() => setIngredientModalOpen(true)}
          >
            What can I make?
          </Button>
          <Tooltip title="Get a random drink recipe">
            <IconButton color="secondary" onClick={handleGetRandomDrink} >
              <ShuffleIcon />
            </IconButton>
          </Tooltip>
        </Stack>

        <Box mb={2}>
          <ToggleButtonGroup
            value={alcoholFilter}
            exclusive
            onChange={handleAlcoholFilter}
            size="small"
          >
            <ToggleButton value="all">All</ToggleButton>
            <ToggleButton value="alcoholic">Alcoholic</ToggleButton>
            <ToggleButton value="non-alcoholic">Non-Alcoholic</ToggleButton>
          </ToggleButtonGroup>
        </Box>

        <Stack direction="row" spacing={1} flexWrap="wrap" mb={2}>
          {types.map((type) => (
            <Chip
              key={type}
              label={type}
              variant={selectedTypes.includes(type) ? "filled" : "outlined"}
              color={selectedTypes.includes(type) ? "primary" : "default"}
              onClick={() => handleTypeClick(type)}
              sx={{ cursor: 'pointer' }}
            />
          ))}
        </Stack>


        {ingredientModalOpen && (
          <Lightbox onClose={() => setIngredientModalOpen(false)}>
            <IngredientSelectModal
              onClose={() => setIngredientModalOpen(false)}
              generateDrink={generateDrink}
              navigate={navigate}
              ingredientsToChoose={ingredientsToChoose}
            />
          </Lightbox>
        )}

        <Box display="flex" flexWrap="wrap" gap={2} justifyContent="center">
          {filteredDrinks.map((drink) => (
            <DrinkCard
              key={drink.id}
              onClick={() => navigate(`/recipe/${drink.id}`)}
            >
              <ListItemAvatar>
                <Avatar
                  variant="rounded"
                  src={getPexelsImageUrl(drink.imageId)}
                  sx={{ width: 80, height: 80, mb: 1 }}
                />
              </ListItemAvatar>
              <ListItemText
                primary={drink.name}
                secondary={`${drink.type} • ${drink.alcoholContent ? 'Alcoholic' : 'Non-Alcoholic'}`}
                sx={{ textAlign: 'center' }}
              />
              <IconButton
                onClick={(e) => {
                  e.stopPropagation();
                  toggleFavoriteStatus(drink.id!);
                }}
              >
                {drink.isFavorite ? (
                  <FavoriteIcon color="error" />
                ) : (
                  <FavoriteBorderIcon />
                )}
              </IconButton>
            </DrinkCard>
          ))}
        </Box>

      </Box>

      <Fab
        color="primary"
        sx={{
          position: 'fixed',
          bottom: 32,
          right: 32,
          backgroundColor: '#6a7df8',
          '&:hover': { backgroundColor: '#3f54df' }
        }}
        onClick={() => navigate('/add')}
      >
        <AddIcon />
      </Fab>
    </>
  );
};

export default Home;
