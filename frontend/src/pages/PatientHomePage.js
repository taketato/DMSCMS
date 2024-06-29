import React, { useState } from 'react';
//import Logout from './components/Logout';
//import { Link } from 'react-router-dom';
import { Button, TextField, Paper, Typography, Container, Box, Grid } from '@mui/material';
import { Link } from 'react-router-dom';
const PatientHomePage = () => {
    const [Trackinfo, setTrackinfo] = useState([]);
    const [ItemName, setItemName] = useState("");
    const [ItemProductiondate, setItemProductiondate] = useState("");
    const [ItemBatchno, setItemBatchno] = useState("");

    const [showTrackInfo, setshowTrackInfo] = useState(false);

    const fetchTrackinfo = () => {
      const PORT_NUM = 8000;
      const tracking_info= {
        item_name:ItemName,
        production_date:ItemProductiondate,
        batch_no:ItemBatchno
      };
  
      console.log("Sending :", tracking_info);
  
      return fetch(`http://localhost:${PORT_NUM}/patient/tracking`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tracking_info),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            return response.json().then((errorData) => {
              throw new Error(`Error fetching track: ${errorData.error}`);
            });
          }
        });
    };
    
    const handleTrackInfoSubmit = (e) => {
        e.preventDefault();
        fetchTrackinfo().then(data => {
            console.log("rec:",data);
            setTrackinfo(data);
            setshowTrackInfo(true);
        }).catch(error => {
            console.error("Error fetching track:", error);
        });
     };
         
     
    return (
      <Container maxWidth="md">
          <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
              <Typography variant="h4" gutterBottom>Patient Home Page</Typography>

              {/* Track item */}
              <Box component="form" onSubmit={handleTrackInfoSubmit} noValidate sx={{ mt: 1 }}>
                  <TextField
                      label="Track item Name"
                      value={ItemName}
                      onChange={(e) => setItemName(e.target.value)}
                      placeholder="Enter item name"
                      fullWidth
                      margin="normal"
                      variant="outlined"
                  />
                <TextField
                      label="Track item production date"
                      value={ItemProductiondate}
                      onChange={(e) => setItemProductiondate(e.target.value)}
                      placeholder="Enter item production date"
                      fullWidth
                      margin="normal"
                      variant="outlined"
                  />
                <TextField
                      label="Track item batch number"
                      value={ItemBatchno}
                      onChange={(e) => setItemBatchno(e.target.value)}
                      placeholder="Enter item batch number"
                      fullWidth
                      margin="normal"
                      variant="outlined"
                  />
                  <Button type="submit" variant="contained" color="primary" fullWidth>
                      Track Items
                  </Button>
              </Box>

              <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
                Track Information:
              </Typography>
              {showTrackInfo && Trackinfo ? (
                  <Paper elevation={1} style={{ padding: '15px', marginTop: '10px' }}>
                      <Typography><strong>manufacturer:</strong> {Trackinfo.manufacturer}</Typography>
                      <Typography><strong>departure_date_manufacturer:</strong> {Trackinfo.departure_date_manufacturer}</Typography>
                      <Typography><strong>arrival_date_wholesaler:</strong> {Trackinfo.arrival_date_wholesaler}</Typography>
                      <Typography><strong>wholesaler:</strong> {Trackinfo.wholesaler}</Typography>
                      <Typography><strong>departure_date_wholesaler:</strong> {Trackinfo.departure_date_wholesaler}</Typography>
                      <Typography><strong>arrival_date_hospital:</strong> {Trackinfo.arrival_date_hospital}</Typography>
                      <Typography><strong>hospital:</strong> {Trackinfo.hospital}</Typography>
                  </Paper>
              ) : (
                  <Typography>No track information available.</Typography>
              )}

              <Box mt={4} mb={2}>
                  <Link to="/" style={{ textDecoration: 'none' }}>
                      <Button variant="outlined" color="secondary">
                          Go to Front Page
                      </Button>
                  </Link>
              </Box>
          </Paper>
      </Container>
  );

};
     
export default PatientHomePage;
     




