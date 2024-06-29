import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Typography, Card, CardActionArea, CardContent, Container, Grid } from '@mui/material';

const MainPage = () => {
  return (
    <Container maxWidth="sm" style={{ textAlign: 'center', paddingTop: '50px' }}>
      <Typography variant="h4" gutterBottom>
        Decentralized Medical Supply Chain Management System
      </Typography>
      <Typography variant="h5" gutterBottom>
        DMSCMS
      </Typography>
      <Grid container spacing={2} mt={4}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardActionArea component={RouterLink} to="/patient/homepage">
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  Patient
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Track your order directly if you are a patient
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardActionArea component={RouterLink} to="/login">
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  Login
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Access your account if you are not a patient
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardActionArea component={RouterLink} to="/register">
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  Register
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Create a new account if you are not a patient
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default MainPage;
