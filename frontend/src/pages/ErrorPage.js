import React from "react";
import { Link } from 'react-router-dom';
import { Paper, Button, Typography, Container, Box} from '@mui/material';

const ErrorPage = () => {
    return(
        <Container maxWidth="md">
        <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
            <Typography variant="h4" gutterBottom>Wrong Route or Identidy!</Typography>
            <Box mt={4} mb={2}>
                <Link to="/login" style={{ textDecoration: 'none' }}>
                    <Button variant="outlined" color="secondary">
                        Go Back to Login Page
                    </Button>
                </Link>
            </Box>
            </Paper>
        </Container>       
    );
}

export default ErrorPage;