import { useState, useEffect, FC, useCallback } from 'react';
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
} from '@mui/material';
import styled from 'styled-components';
import { IMAGES_PER_PAGE } from '../constants';

const MAX_PAGE = 4;
const DEBOUNCE_TIMEOUT = 500;

interface ImageSelectModalProps {
    onClose: () => void;
    onSelect: (src: string) => void;
    fetchImages: (query: string, page: number) => Promise<string[] | undefined>;
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
    const [images, setImages] = useState<string[]>([]);
    const [page, setPage] = useState(1);
    const [selectedImg, setSelectedImg] = useState<string | null>(null);
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    // Debounced search effect
    useEffect(() => {
        if (query.trim() === '') {
            setImages([]);
            return;
        }
        const handler = setTimeout(() => {
            fetchImages(query, page)
                .then(results => setImages(results || []))
                .catch(console.error);
        }, DEBOUNCE_TIMEOUT);

        return () => clearTimeout(handler);
    }, [query, page, fetchImages]);

    const handleConfirm = () => {
        if (selectedImg) {
            onSelect(selectedImg);
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
                <ImageFlexContainer>
                    {images.slice(0, maxPerRow).map((img) => (
                        <ImageCard key={img} $maxPerRow={maxPerRow}>
                            <CardActionArea
                                onClick={() => setSelectedImg(img)}
                                sx={{
                                    border: selectedImg === img ? '2px solid #1976d2' : '2px solid transparent',
                                    borderRadius: 1,
                                    boxShadow: selectedImg === img ? '0 0 8px rgba(25, 118, 210, 0.6)' : 'none',
                                }}
                            >
                                <CardMedia
                                    component="img"
                                    image={img}
                                    alt={`Drink image: ${query}`}
                                    sx={{ height: 140, objectFit: 'cover', borderRadius: 1 }}
                                />
                            </CardActionArea>
                        </ImageCard>
                    ))}
                </ImageFlexContainer>

                <Stack direction="row" justifyContent="space-between" mt={2}>
                    <Button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page <= 1}>
                        Previous
                    </Button>
                    <Button onClick={() => setPage(p => p + 1)} disabled={page >= MAX_PAGE}>
                        Next
                    </Button>
                </Stack>
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
