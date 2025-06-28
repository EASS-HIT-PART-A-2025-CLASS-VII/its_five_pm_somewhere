import { Alert, Snackbar } from '@mui/material';
import { useEffect, useState } from 'react';
import { useDrinkContext } from '../contexts/DrinkContext'

const GlobalError = () => {
  const { error, clearError } = useDrinkContext();
  const [open, setOpen] = useState<boolean>(false);

  useEffect(() => {
    if (error) {
      setOpen(true);
    }
  }, [error]);

  const handleClose = () => {
    setOpen(false);
    clearError();
  };

  if (!error) return null;

  return (
    <Snackbar open={open} autoHideDuration={4000} onClose={handleClose} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
      <Alert severity="error" onClose={handleClose} sx={{ width: '100%' }}>
        {error}
      </Alert>
    </Snackbar>
  );
};

export default GlobalError;
