import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { Button, TextField, Paper, Typography, Container, Box, Grid } from '@mui/material';


const WholesalerHomePage = () => {
    const [Trackinfo, setTrackinfo] = useState([]);
    
    const [Demandinfo, setDemandinfo] = useState([]);

    const [demandAmount_new, setDemandAmount_new] = useState("");
    const [demandAmount_update, setDemandAmount_update] = useState("");

    const [manufacturer_new, setmanufacturer_new] = useState("");   
    const [manufacturer_update, setmanufacturer_update] = useState("");
    const [manufacturer_checkingDemand, setmanufacturer_checkingDemand] = useState("");

    const [itemName_new, setitemName_new] = useState("");   
    const [itemName_update, setitemName_update] = useState("");
    const [itemName_checkingDemand, setitemName_checkingDemand] = useState("");

    const [itemName_tracking, setitemName_tracking] = useState("");
    const [destination, setDestination] = useState("");
    const [senddate, setSenddate] = useState("");
    const [source, setSource] = useState("");

    //=================control render=================
    const [showTrackInfo, setShowTrackInfo] = useState(false);
    const [showDemandHistory, setShowDemandHistory] = useState(false);
    
    //=================get trackinfo=================
    const fetchTrackinfo = () => {
      const token = localStorage.getItem('token');
      console.log("Sending :", token);
      const PORT_NUM = 8000;
      const tracking_name = {
        item_name:itemName_tracking,
        destination:destination,
        source:source,
        send_date:senddate,
      };

      console.log("sending track item with name: ",tracking_name)
  
      return fetch(`http://localhost:${PORT_NUM}/admin/wholesaler/tracking`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(tracking_name),
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
    
    const handleTrackNameSubmit = (e) => {
        e.preventDefault();
        fetchTrackinfo().then(data => {
            setTrackinfo(data);
            setShowTrackInfo(true);
            console.log("receving track: ",data)
        }).catch(error => {
            console.error("Error fetching track:", error);
        });
     };


    //=================get demand history=================
    const fetchDemand = () => {
      const token = localStorage.getItem('token');
      const PORT_NUM = 8000;
      const checkingDemand_name = {
        object_name:itemName_checkingDemand,
        manufacturer:manufacturer_checkingDemand,
      };

      console.log("sending",checkingDemand_name)
  
      return fetch(`http://localhost:${PORT_NUM}/admin/wholesaler/demand`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(checkingDemand_name),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            return response.json().then((errorData) => {
              throw new Error(`Error fetching demand: ${errorData.error}`);
            });
          }
        });
    };

    const handlefetchDemandSubmit = (e) => {
      e.preventDefault();
      fetchDemand().then(data => {
          setDemandinfo(data);
          setShowDemandHistory(true);
          console.log("get demand history :",data)
      }).catch(error => {
          console.error("Error fetching demand:", error);
      });
    };
    
    //=================post new demand=================
    const postDemand = (itemName_new,demandAmount_new,manufacturer_new) => {
      const token = localStorage.getItem('token');

      const PORT_NUM = 8000;
      const newDemand = {
        item_name:itemName_new,
        manufacturer:manufacturer_new,
        demand_amount: demandAmount_new,
      };

      console.log("sending new demand",newDemand)
  
      fetch(`http://localhost:${PORT_NUM}/admin/wholesaler/demand/new`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newDemand),
      })
        .then((response) => {
          if (response.ok) {
            console.log(response);
            return response.json();  
          } else {
            return response.json().then((errorData) => {
              throw new Error(`Error posting demand: ${errorData.error}`);
            });
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    };

    const handlenewDemandSubmit = (e) => {
      e.preventDefault();
      postDemand(itemName_new,demandAmount_new,manufacturer_new);
    };

    //=================update demand=================
    const updateDemand = (itemName_update,demandAmount_update) => {
      const token = localStorage.getItem('token');
      const PORT_NUM = 8000;
      const updateDemand = {
        item_name: itemName_update,
        manufacturer: manufacturer_update,
        demand_amount: demandAmount_update,
      };

      console.log("sending update demand",updateDemand)
  
      fetch(`http://localhost:${PORT_NUM}/admin/wholesaler/demand/update`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updateDemand),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            return response.json().then((errorData) => {
              throw new Error(`Error updating demand: ${errorData.error}`);
            });
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    };

    const handleupdateDemandSubmit = (e) => {
      e.preventDefault();
      updateDemand(itemName_update,demandAmount_update);
    };
    

    return (
      <Container maxWidth="md">
        <Navbar />
          <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
              {/* <Logout /> */}

              {/* Track item */}
              <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
                Track Item:
              </Typography>
              <Box component="form" onSubmit={handleTrackNameSubmit} noValidate sx={{ mt: 1 }}>
              <TextField
                        label="Track Name"
                        value={itemName_tracking}
                        onChange={(e) => setitemName_tracking(e.target.value)}
                        placeholder="Enter track name"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                    />
                    <TextField
                        label="Destination"
                        value={destination}
                        onChange={(e) => setDestination(e.target.value)}
                        placeholder="Enter Destination"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                    />
                    <TextField
                        label="Source"
                        value={source}
                        onChange={(e) => setSource(e.target.value)}
                        placeholder="Enter Source"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                    />
                    <TextField
                        label="Send Date"
                        value={senddate}
                        onChange={(e) => setSenddate(e.target.value)}
                        placeholder="Enter Send Date"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                    />
                  <Button type="submit" variant="contained" color="primary" fullWidth>
                      Track Item
                  </Button>
              </Box>

              <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
                Track Information:
              </Typography>
              {showTrackInfo && Trackinfo ? (
                  <Paper elevation={1} style={{ padding: '15px', marginTop: '10px' }}>
                      <Typography><strong>Departure:</strong> {Trackinfo.departure}</Typography>
                      <Typography><strong>Track Record:</strong> {Trackinfo.track_record}</Typography>
                      <Typography><strong>Destination:</strong> {Trackinfo.destination}</Typography>
                      <Typography><strong>Status:</strong> {Trackinfo.status}</Typography>
                  </Paper>
              ) : (
                  <Typography>No track information available.</Typography>
              )}
              <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
                Demand History:
              </Typography>
              
              {/* Check demand History */}
              <Box component="form" onSubmit={handlefetchDemandSubmit} noValidate sx={{ mt: 2 }}>
              <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Check Demand Item Name"
                        value={itemName_checkingDemand}
                        onChange={(e) => setitemName_checkingDemand(e.target.value)}
                        placeholder="Enter check demand Item Name"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Check Demand manufacturer"
                        value={manufacturer_checkingDemand}
                        onChange={(e) => setmanufacturer_checkingDemand(e.target.value)}
                        placeholder="Enter check demand manufacturer"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                      />
                    </Grid>
                  </Grid>
                <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
                  Fetch Demand History
                </Button>
              </Box>

              <Box mt={2}>
                <Typography variant="h6">Demand History:</Typography>
                {showDemandHistory && Demandinfo ? (
                  <Paper elevation={1} sx={{ padding: 2, mt: 1 }}>
                    <Typography><strong>Demand Record:</strong> {Demandinfo.demand_record}</Typography>
                  </Paper>
                ) : (
                  <Typography>No demand information available.</Typography>
                )}
              </Box>

              {/* Post new demand */}
              <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
                Post New Demand:
              </Typography>
              <Box component="form" onSubmit={handlenewDemandSubmit} noValidate sx={{ mt: 1 }}>
                <TextField
                        fullWidth
                        id="itemNameNew"
                        label="Item name"
                        value={itemName_new}
                        onChange={(e) => setitemName_new(e.target.value)}
                        placeholder="Enter Item ID"
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="manufacturer"
                        label="manufacturer"
                        value={manufacturer_new}
                        onChange={(e) => setmanufacturer_new(e.target.value)}
                        placeholder="Enter manufacturer"
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="demandAmountNew"
                        label="Demand Amount"
                        value={demandAmount_new}
                        onChange={(e) => setDemandAmount_new(e.target.value)}
                        placeholder="Enter Demand Amount"
                        margin="normal"
                    />
                <Button type="submit" variant="contained" color="primary" sx={{ mt: 3, mb: 2, width: '100%' }}>
                    Submit New Demand
                </Button>
            </Box>

            {/* Update demand */}
            <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
              Update Demand:
            </Typography>
            <Box component="form" onSubmit={handleupdateDemandSubmit} noValidate sx={{ mt: 1 }}>
                  <TextField
                      fullWidth
                      id="itemNameUpdate"
                      label="Item Name"
                      value={itemName_update}
                      onChange={(e) => setitemName_update(e.target.value)}
                      placeholder="Enter Item name to Update"
                      margin="normal"
                  />
                  <TextField
                      fullWidth
                      id="demandAmountUpdate"
                      label="New Demand Amount"
                      value={demandAmount_update}
                      onChange={(e) => setDemandAmount_update(e.target.value)}
                      placeholder="Enter New Demand Amount"
                      margin="normal"
                  />
                  <TextField
                      fullWidth
                      id="manufacturerUpdate"
                      label="New manufacturer"
                      value={manufacturer_update}
                      onChange={(e) => setmanufacturer_update(e.target.value)}
                      placeholder="Enter New manufacturer"
                      margin="normal"
                  />
                <Button type="submit" variant="contained" color="primary" sx={{ mt: 3, mb: 2, width: '100%' }}>
                    Update Demand
                </Button>
            </Box>
            
            <Box mt={4} mb={2}>
                <Link to="/wholesaler/inventory" style={{ textDecoration: 'none' }}>
                    <Button variant="outlined" color="secondary">
                        Go to Wholesaler Inventory
                    </Button>
                </Link>
            </Box>
          </Paper>
      </Container>
  );

};

export default WholesalerHomePage;
