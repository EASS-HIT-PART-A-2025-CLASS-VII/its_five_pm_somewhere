import { useState, useEffect, FC } from 'react';
import {
    Box,
    Button,
    CardActionArea,
    CardMedia,
    Paper,
    Stack,
    TextField,
    Typography,
    Snackbar,
    CircularProgress,
    Alert,
} from '@mui/material';
import styled from 'styled-components';
import { IMAGES_PER_PAGE } from '../constants';
import { getPexelsImageUrl } from '../utils/imageService';

const MAX_PAGE = 4;
const DEBOUNCE_TIMEOUT = 500;

interface ImageSelectModalProps {
    onClose: () => void;
    onSelect: (src: number) => void;
    fetchImages: (query: string, page: number) => Promise<number[] | undefined>;
    maxPerRow?: number;
}

const ImageFlexContainer = styled(Box)`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
`;

const ImageCard = styled(Box) <{ $maxPerRow: number }>`
  flex: 1 1 calc(100% / ${(props) => props.$maxPerRow} - 1rem);
  min-width: calc(100% / ${(props) => props.$maxPerRow} - 1rem);
  max-width: calc(100% / ${(props) => props.$maxPerRow} - 1rem);
  @media (max-width: 600px) {
    flex: 1 1 calc(100% / 2 - 1rem);
    min-width: calc(100% / 2 - 1rem);
    max-width: calc(100% / 2 - 1rem);
  }
`;

const ImageSelectModal: FC<ImageSelectModalProps> = ({
    onClose,
    onSelect,
    fetchImages,
    maxPerRow = IMAGES_PER_PAGE,
}) => {
    const [query, setQuery] = useState('');
    const [imagesIds, setImagesIds] = useState<number[]>([]);
    const [page, setPage] = useState(1);
    const [selectedImgId, setSelectedImgId] = useState<number | null>(null);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setPage(1);
    }, [query]);

    useEffect(() => {
        if (query.trim() === '') {
            setImagesIds([]);
            return;
        }
        const handler = setTimeout(async () => {
            setLoading(true);
            setError(null);
            try {
                const results = await fetchImages(query, page);
                setImagesIds(results || []);
            } catch (err) {
                setError('Looks like our image mixer is out of juice. Try searching again!');
                setImagesIds([]);
            } finally {
                setLoading(false);
            }
        }, DEBOUNCE_TIMEOUT);

        return () => clearTimeout(handler);
    }, [query, page, fetchImages]);

    const handleConfirm = () => {
        if (selectedImgId) {
            onSelect(selectedImgId);
            onClose();
        } else {
            setSnackbarOpen(true);
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
                <Typography variant="h5">Select an Image</Typography>
                <TextField
                    fullWidth
                    label="Search for images"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g. cocktail, smoothie"
                />
                {loading && (
                    <Box display="flex" justifyContent="center" py={2}>
                        <CircularProgress />
                    </Box>
                )}
                {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        {error}
                    </Alert>
                )}
                {!loading && !error && (
                    <ImageFlexContainer>
                        {imagesIds.slice(0, maxPerRow).map((imgId) => (
                            <ImageCard key={imgId} $maxPerRow={maxPerRow}>
                                <CardActionArea
                                    onClick={() => setSelectedImgId(imgId)}
                                    sx={{
                                        border: selectedImgId === imgId ? '2px solid #1976d2' : '2px solid transparent',
                                        borderRadius: 1,
                                        boxShadow: selectedImgId === imgId ? '0 0 8px rgba(25, 118, 210, 0.6)' : 'none',
                                    }}
                                >
                                    <CardMedia
                                        component="img"
                                        image={getPexelsImageUrl(imgId)}
                                        alt={`Drink image: ${query}`}
                                        sx={{ height: 140, objectFit: 'cover', borderRadius: 1 }}
                                    />
                                </CardActionArea>
                            </ImageCard>
                        ))}
                    </ImageFlexContainer>
                )}
                <Box
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                    mt={2}
                >
                    <Button
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        disabled={page <= 1}
                        sx={{ flex: 1, maxWidth: 100 }}
                    >
                        Previous
                    </Button>
                    <Typography variant="body1" sx={{ mx: 2 }}>
                        Page {page} of {MAX_PAGE}
                    </Typography>
                    <Button
                        onClick={() => setPage(p => p + 1)}
                        disabled={page >= MAX_PAGE}
                        sx={{ flex: 1, maxWidth: 100 }}
                    >
                        Next
                    </Button>
                </Box>

                <Button onClick={handleConfirm} variant="outlined" fullWidth>
                    Confirm Selection
                </Button>
            </Stack>
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={3000}
                onClose={() => setSnackbarOpen(false)}
                message="Please select an image before confirming."
            />
        </Paper>
    );
};

export default ImageSelectModal;
