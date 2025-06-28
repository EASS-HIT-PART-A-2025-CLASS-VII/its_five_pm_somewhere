import { useState, FC } from 'react';
import {
    Box,
    Button,
    CardActionArea,
    Paper,
    Stack,
    TextField,
    Typography,
    Snackbar,
    CircularProgress,
    Alert,
    Chip,
} from '@mui/material';
import styled from 'styled-components';
import { getPexelsImageUrl } from '../utils/imageService';
import { ChooseIngredient, DrinkRecipe } from '../client';
import { DrinkImage, SquareImageBox } from '../styles/globalStyles';

interface IngredientSelectModalProps {
    onClose: () => void;
    generateDrink: (ingredients: string[]) => Promise<DrinkRecipe>;
    navigate: (path: string) => void;
    ingredientsToChoose: ChooseIngredient[];
}

const MAX_PER_ROW = 4;

const IngredientFlexContainer = styled(Box)`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
`;

const IngredientCard = styled(CardActionArea) <{ $isSelected: boolean }>`
  flex: 1 1 calc(100% / ${MAX_PER_ROW} - 1rem);
  min-width: calc(100% / ${MAX_PER_ROW} - 1rem);
  max-width: calc(100% / ${MAX_PER_ROW} - 1rem);
  border: ${props => props.$isSelected ? '2px solid #1976d2' : '2px solid transparent'};
  border-radius: 8px;
  box-shadow: ${props => props.$isSelected ? '0 0 8px rgba(25, 118, 210, 0.6)' : 'none'};
  transition: all 0.2s;
  @media (max-width: 600px) {
    flex: 1 1 calc(100% / 2 - 1rem);
    min-width: calc(100% / 2 - 1rem);
    max-width: calc(100% / 2 - 1rem);
  }
`;

const IngredientSelectModal: FC<IngredientSelectModalProps> = ({
    onClose,
    generateDrink,
    navigate,
    ingredientsToChoose
}) => {
    const [query, setQuery] = useState('');
    const [selected, setSelected] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    const filteredIngredients = ingredientsToChoose.filter(ingredient =>
        ingredient.name.toLowerCase().includes(query.toLowerCase())
    );

    const toggleIngredient = (name: string) => {
        setSelected(prev =>
            prev.includes(name)
                ? prev.filter(i => i !== name)
                : [...prev, name]
        );
    };

    const handleCreateDrink = async () => {
        if (selected.length < 3) {
            setSnackbarOpen(true);
            return;
        }
        setLoading(true);
        try {
            const newDrink = await generateDrink(selected);
            navigate(`/recipe/${newDrink.id}`);
            onClose();
        } catch (err) {
            setError('Failed to generate a drink. Please try again!');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Paper
            sx={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: { xs: '90%', sm: '80%', md: '60%' },
                maxWidth: 800,
                p: 4,
                borderRadius: 4,
                outline: 'none',
            }}
            elevation={24}
        >
            <Stack gap={2}>
                <Typography variant="h5">Choose Your Ingredients</Typography>
                <TextField
                    fullWidth
                    label="Search for ingredients"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g. lemon, mint, gin"
                />
                {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        {error}
                    </Alert>
                )}
                <IngredientFlexContainer>
                    {filteredIngredients.map((ingredient) => (
                        <IngredientCard
                            key={ingredient.name}
                            $isSelected={selected.includes(ingredient.name)}
                            onClick={() => toggleIngredient(ingredient.name)}
                        >
                            <SquareImageBox>
                                <DrinkImage
                                    src={getPexelsImageUrl(ingredient.imageId)}
                                    alt={ingredient.name}
                                />
                            </SquareImageBox>
                            <Box p={1}>
                                <Typography variant="body2" textAlign="center">
                                    {ingredient.name}
                                </Typography>
                            </Box>
                        </IngredientCard>
                    ))}
                </IngredientFlexContainer>
                {filteredIngredients.length === 0 && (
                    <Typography variant="body1" textAlign="center" py={2}>
                        No ingredients match your search
                    </Typography>
                )}
                <Stack direction="row" spacing={1} flexWrap="wrap" mt={1}>
                    {selected.map(name => (
                        <Chip key={name} label={name} onDelete={() => toggleIngredient(name)} />
                    ))}
                </Stack>
                <Button
                    onClick={handleCreateDrink}
                    variant="contained"
                    color="primary"
                    fullWidth
                    disabled={loading}
                    endIcon={loading ? <CircularProgress size={20} /> : null}
                >
                    {loading ? 'Creating...' : 'Create Drink'}
                </Button>
            </Stack>
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={3000}
                onClose={() => setSnackbarOpen(false)}
                message="Please select at least two ingredients."
            />
        </Paper>
    );
};

export default IngredientSelectModal;
