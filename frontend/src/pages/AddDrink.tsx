import { FormEvent, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardMedia,
  CircularProgress,
  Container,
  Divider,
  FormControl,
  FormLabel,
  IconButton,
  MenuItem,
  Select,
  Snackbar,
  Stack,
  Switch,
  TextField,
  Typography,
  useMediaQuery,
  useTheme
} from '@mui/material';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import styled from 'styled-components';
import { DrinkRecipe, DrinkType, Ingredient, Unit } from '../client';
import { useDrinkContext } from '../contexts/DrinkContext';
import ImageSelectModal from '../components/ImageSelectModal';
import { Lightbox } from '../components/Lightbox';
import { useNavigate } from 'react-router-dom';
import { MAX_WIDTH_PAGE } from '../constants';
import { getPexelsImageUrl } from '../utils/imageService';

const AddDrinkContainer = styled(Box)`
  padding: 2rem 1rem;
  min-height: calc(100vh - 64px);
  background: linear-gradient(45deg, #543bff 0%, #5e6eff 99%, #008fff 100%);
  max-width: ${MAX_WIDTH_PAGE}px;
`;

const FormCard = styled(Card)`
  padding: 2rem;
  margin: 0 auto;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

const IngredientStack = styled(Stack)`
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const getUnitLabel = (unit: Unit) => (unit === Unit.TOP_UP ? 'top up' : unit);

const AddDrink = () => {
  const { addDrink, loading, error, clearError, fetchImages } = useDrinkContext();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [ingredients, setIngredients] = useState<Ingredient[]>([{ name: '', amount: 1, unit: Unit.PIECE }]);
  const [instructions, setInstructions] = useState<string[]>(['']);
  const [alcoholContent, setAlcoholContent] = useState(false);
  const [drinkType, setDrinkType] = useState<DrinkType>(DrinkType.COCKTAIL);
  const [isFavorite, setIsFavorite] = useState(false);
  const [imageId, setImageId] = useState<number | null>(null);
  const [imageModalOpen, setImageModalOpen] = useState(false);

  const [ingredientErrors, setIngredientErrors] = useState<{ name: boolean; amount: boolean }[]>([{ name: false, amount: false }]);
  const [formError, setFormError] = useState<string | null>(null);

  const validateIngredient = (ingredient: Ingredient) => ({
    name: ingredient.name.trim().length < 2,
    amount: ingredient.unit === Unit.TOP_UP ? false : ingredient.amount <= 0
  });

  const handleAddIngredient = () => {
    setIngredients([...ingredients, { name: '', amount: 1, unit: Unit.PIECE }]);
    setIngredientErrors([...ingredientErrors, { name: false, amount: false }]);
  };

  const handleRemoveIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
    setIngredientErrors(ingredientErrors.filter((_, i) => i !== index));
  };

  const handleIngredientChange = (index: number, field: keyof Ingredient, value: string | number | Unit) => {
    const newIngredients = [...ingredients];
    if (field === 'unit') {
      newIngredients[index].unit = value as Unit;
      if (value === Unit.TOP_UP) {
        newIngredients[index].amount = 1;
      }
    } else if (field === 'amount') {
      newIngredients[index].amount = typeof value === 'number' ? value : parseFloat(value as string) || 1;
    } else if (field === 'name') {
      newIngredients[index].name = value as string;
    }
    setIngredients(newIngredients);

    const errors = validateIngredient(newIngredients[index]);
    const newErrors = [...ingredientErrors];
    newErrors[index] = errors;
    setIngredientErrors(newErrors);
  };

  const handleAddInstruction = () => {
    setInstructions([...instructions, '']);
  };

  const handleRemoveInstruction = (index: number) => {
    setInstructions(instructions.filter((_, i) => i !== index));
  };

  const handleInstructionChange = (index: number, value: string) => {
    const newInstructions = [...instructions];
    newInstructions[index] = value;
    setInstructions(newInstructions);
  };

  const isFormValid = () => {
    let valid = true;
    const errors = ingredients.map(validateIngredient);
    setIngredientErrors(errors);
    for (const err of errors) {
      if (err.name || err.amount) valid = false;
    }
    if (!name.trim()) valid = false;
    if (!instructions[0].trim()) valid = false;
    return valid;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setFormError(null);
    if (!isFormValid()) {
      setFormError('Please fix ingredient errors and fill all required fields.');
      return;
    }
    const drink: DrinkRecipe = {
      name,
      ingredients: ingredients.filter(i => i.name.trim().length >= 2),
      instructions: instructions.filter(i => i.trim() !== ''),
      alcoholContent,
      type: drinkType,
      imageId: imageId,
      isFavorite
    };
    const newDrink = await addDrink(drink);
    navigate(`/recipe/${newDrink.id}`)
  };

  return (
    <AddDrinkContainer>
      <Container maxWidth="md">
        <FormCard>
          <Typography variant="h4" gutterBottom>
            Add New Drink
          </Typography>
          <form onSubmit={handleSubmit} noValidate>
            <Stack gap={2}>
              <TextField
                label="Drink Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                fullWidth
                error={!name.trim()}
                helperText={!name.trim() ? 'Required' : ''}
              />
              <Divider />
              <Typography variant="h6">Ingredients</Typography>
              <IngredientStack>
                {ingredients.map((ingredient, index) => (
                  <Stack key={index} direction={isMobile ? 'column' : 'row'} gap={1}>
                    <TextField
                      label="Ingredient"
                      value={ingredient.name}
                      onChange={(e) => handleIngredientChange(index, 'name', e.target.value)}
                      required
                      sx={{ flex: 2 }}
                      error={ingredientErrors[index]?.name}
                      helperText={ingredientErrors[index]?.name ? 'At least 2 characters' : ''}
                    />
                    <TextField
                      label="Amount"
                      type="number"
                      value={ingredient.amount}
                      onChange={(e) => handleIngredientChange(index, 'amount', parseFloat(e.target.value) || 1)}
                      required
                      sx={{ flex: 1 }}
                      disabled={ingredient.unit === Unit.TOP_UP}
                      error={ingredientErrors[index]?.amount}
                      helperText={ingredient.unit === Unit.TOP_UP ? '' : ingredientErrors[index]?.amount ? 'Must be > 0' : ''}
                      inputProps={{ min: 1 }}
                    />
                    <TextField
                      select
                      label="Unit"
                      value={ingredient.unit}
                      onChange={(e) => handleIngredientChange(index, 'unit', e.target.value as Unit)}
                      sx={{ flex: 1 }}
                    >
                      {Object.values(Unit).map((unit) => (
                        <MenuItem key={unit} value={unit}>
                          {getUnitLabel(unit)}
                        </MenuItem>
                      ))}
                    </TextField>
                    {ingredients.length > 1 && (
                      isMobile ? (
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => handleRemoveIngredient(index)}
                          sx={{ mt: 1, width: '100%' }}
                        >
                          Remove
                        </Button>
                      ) : (
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => handleRemoveIngredient(index)}
                          sx={{ height: 56, minWidth: 100 }}
                        >
                          Remove
                        </Button>
                      )
                    )}
                  </Stack>
                ))}
                <Button variant="outlined" onClick={handleAddIngredient}>
                  Add Ingredient
                </Button>
              </IngredientStack>
              <Divider />
              <Typography variant="h6">Instructions</Typography>
              <IngredientStack>
                {instructions.map((instruction, index) => (
                  <Stack
                    key={index}
                    direction={isMobile ? 'column' : 'row'}
                    gap={1}
                    alignItems={isMobile ? 'stretch' : 'center'}
                  >
                    <TextField
                      label={`Step ${index + 1}`}
                      value={instruction}
                      onChange={(e) => handleInstructionChange(index, e.target.value)}
                      required={index === 0}
                      fullWidth
                      multiline
                      error={index === 0 && !instruction.trim()}
                      helperText={index === 0 && !instruction.trim() ? 'Required' : ''}
                      sx={{ flex: 1 }}
                    />
                    {instructions.length > 1 && (
                      isMobile ? (
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => handleRemoveInstruction(index)}
                          sx={{ mt: 1, width: '100%' }}
                        >
                          Remove
                        </Button>
                      ) : (
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => handleRemoveInstruction(index)}
                          sx={{ height: 56, minWidth: 100 }}
                        >
                          Remove
                        </Button>
                      )
                    )}
                  </Stack>
                ))}
                <Button variant="outlined" onClick={handleAddInstruction}>
                  Add Step
                </Button>
              </IngredientStack>

              <Divider />
              <FormControl component="fieldset" sx={{ flexDirection: 'row', alignItems: 'center', gap: 2 }}>
                <FormLabel component="legend" sx={{ mr: 2 }}>
                  Alcohol Content
                </FormLabel>
                <Stack direction="row" alignItems="center" gap={1}>
                  <Typography>Non-Alcoholic</Typography>
                  <Switch
                    checked={alcoholContent}
                    onChange={(e) => setAlcoholContent(e.target.checked)}
                    color="secondary"
                    inputProps={{ 'aria-label': 'Alcoholic Switch' }}
                  />
                  <Typography>Alcoholic</Typography>
                </Stack>
              </FormControl>
              <FormControl fullWidth>
                <FormLabel sx={{ mb: 1 }}>Drink Type</FormLabel>
                <Select
                  value={drinkType}
                  onChange={(e) => setDrinkType(e.target.value as DrinkType)}
                  variant="outlined"
                  sx={{
                    background: '#fff',
                    borderRadius: 2,
                    fontWeight: 500,
                  }}
                >
                  {Object.values(DrinkType).map((type) => (
                    <MenuItem key={type} value={type}>
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <Divider />
              <Stack direction="row" alignItems="center" gap={1}>
                <Typography>Favorite</Typography>
                <IconButton onClick={() => setIsFavorite(!isFavorite)}>
                  {isFavorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
                </IconButton>
              </Stack>
              <Divider />
              <Typography variant="h6">Drink Image</Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Stack direction="row" gap={1}>
                  <Button variant="outlined" onClick={() => setImageModalOpen(true)}>
                    Choose Image
                  </Button>
                  {imageId && (
                    <Button
                      variant="text"
                      color="error"
                      onClick={() => setImageId(null)}
                    >
                      Remove Image
                    </Button>
                  )}
                </Stack>
                {imageId ? (
                  <CardMedia
                    component="img"
                    image={getPexelsImageUrl(imageId)}
                    alt="Selected drink"
                    sx={{ height: 200, objectFit: 'cover', borderRadius: 2, maxWidth: 400 }}
                  />
                ) : (
                  <Typography color="text.secondary">No image selected</Typography>
                )}
              </Box>
              {formError && (
                <Typography color="error" sx={{ mt: 1 }}>
                  {formError}
                </Typography>
              )}
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                disabled={loading}
                sx={{ mt: 3 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Save Recipe'}
              </Button>
            </Stack>
          </form>
        </FormCard>
      </Container>
      {imageModalOpen && (
        <Lightbox onClose={() => setImageModalOpen(false)}>
          <ImageSelectModal
            onClose={() => setImageModalOpen(false)}
            onSelect={setImageId}
            fetchImages={fetchImages}
          />
        </Lightbox>
      )}
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={clearError}
        message={error}
        action={
          <Button color="inherit" size="small" onClick={clearError}>
            Close
          </Button>
        }
      />
    </AddDrinkContainer>
  );
};

export default AddDrink;
