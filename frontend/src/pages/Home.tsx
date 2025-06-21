import {
  Box,
  Typography,
  TextField,
  Button,
  ToggleButton,
  ToggleButtonGroup,
  List,
  ListItem,
  ListItemAvatar,
  Avatar,
  ListItemText,
  Chip,
  Stack,
  IconButton
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ShuffleIcon from '@mui/icons-material/Shuffle';
import SearchIcon from '@mui/icons-material/Search';
import { useDrinkContext } from '../contexts/DrinkContext';
import { useState } from 'react';
import styled from 'styled-components';
import { Lightbox } from '../components/Lightbox';
import { RecipePage } from '../components/RecipePage';


// Placeholder for the modal component that will show when "What Can I Make" is clicked.
const ModalPlaceholder = styled(Box)`
  padding: 20px;
  background-color: #f1f1f1;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;


const Home = () => {
  const { drinks, fetchRandomDrink, toggleFavoriteStatus } = useDrinkContext();
  const [search, setSearch] = useState('');
  const [alcoholFilter, setAlcoholFilter] = useState<'all' | 'alcoholic' | 'non-alcoholic'>('all');
  const [showModal, setShowModal] = useState(false);
  const [selectedDrinkId, setSelectedDrinkId] = useState<string | null>(null);
  const selectedDrink = drinks.find(drink => drink.id === selectedDrinkId) ?? null;

  const handleOpenModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  console.log('drinks', drinks)
  const types = Array.from(new Set(drinks.map(d => d.type)));

  const handleAlcoholFilter = (_: any, newValue: any) => {
    if (newValue) setAlcoholFilter(newValue);
  };

  const filteredDrinks = drinks.filter(drink => {
    const matchesSearch = drink.name.toLowerCase().includes(search.toLowerCase());
    const matchesAlcohol =
      alcoholFilter === 'all' ||
      (alcoholFilter === 'alcoholic' && drink.alcoholContent) ||
      (alcoholFilter === 'non-alcoholic' && !drink.alcoholContent);
    return matchesSearch && matchesAlcohol;
  });

  return (
    <Box p={3} maxWidth="800px" margin="auto">
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
        <Button variant="contained" color="primary" onClick={handleOpenModal}>
          What can I make?
        </Button>
        <IconButton color="secondary" onClick={fetchRandomDrink}>
          <ShuffleIcon />
        </IconButton>
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
          <Chip key={type} label={type} variant="outlined" />
        ))}
      </Stack>

      {/* Placeholder for Modal */}
      {showModal && (
        <ModalPlaceholder>
          <Typography variant="h6">Select Ingredients to Create a Drink</Typography>
          {/* Placeholder for ingredient selection UI */}
          <Typography>Ingredients Selection UI will go here...</Typography>
          <Button variant="contained" color="secondary" onClick={handleCloseModal}>
            Close
          </Button>
        </ModalPlaceholder>
      )}

      <List>
        {filteredDrinks.map((drink) => (
          <ListItem
            key={drink.id}
            sx={{ borderBottom: '1px solid #eee', cursor: 'pointer' }}
            onClick={() => setSelectedDrinkId(drink.id!)}
          >
            <ListItemAvatar>
              <Avatar variant="rounded" src={drink.imageUrl ?? ""} />
            </ListItemAvatar>
            <ListItemText
              primary={drink.name}
              secondary={`${drink.type} • ${drink.alcoholContent ? 'Alcoholic' : 'Non-Alcoholic'}`}
            />
            <IconButton
              edge="end"
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
          </ListItem>
        ))}
      </List>

      {selectedDrink && (
        <Lightbox onClose={() => setSelectedDrinkId(null)}>
          <RecipePage
            drink={selectedDrink}
            toggleFavoriteStatus={toggleFavoriteStatus}
          />
        </Lightbox>
      )}

    </Box>
  );
};

export default Home;
