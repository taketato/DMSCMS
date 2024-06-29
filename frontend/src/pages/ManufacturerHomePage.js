import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, TextField, Paper, Typography, Container, Box, Grid } from '@mui/material';
import Navbar from '../components/Navbar';


const ManufacturerHomePage = () => {
    const [Trackinfo, setTrackinfo] = useState([]);
    const [itemName_tracking, setitemName_tracking] = useState("");
    const [destination, setDestination] = useState("");
    const [senddate, setSenddate] = useState("");
    const [source, setSource] = useState("");

    //=================control render=================
    const [showTrackInfo, setShowTrackInfo] = useState(false);
    
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

      console.log("sending track item with name: ",itemName_tracking)
  
      return fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/tracking`, {
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


    return (
      <Container maxWidth="md">
        <Navbar />
          <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
              {/* <Typography variant="h4" gutterBottom>Manufacturer Home Page</Typography> */}
              {/* <Logout /> */}

              {/* Track item */}
              <Box component="form" onSubmit={handleTrackNameSubmit} noValidate sx={{ mt: 1 }}>
              <TextField
                        label="Track item name"
                        value={itemName_tracking}
                        onChange={(e) => setitemName_tracking(e.target.value)}
                        placeholder="Enter track item name"
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
                      Track item
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
              
            
            <Box mt={4} mb={2}>
                <Link to="/manufacturer/inventory" style={{ textDecoration: 'none' }}>
                    <Button variant="outlined" color="secondary">
                        Go to Manufacturer inventory
                    </Button>
                </Link>
                <Link to="/manufacturer/items" style={{ textDecoration: 'none' }}>
                    <Button variant="outlined" color="secondary">
                        Go to Manufacturer items
                    </Button>
                </Link>
            </Box>

          </Paper>
      </Container>
  );

};

export default ManufacturerHomePage;

    // return (
    //     <div>
    //       <h2>ManufacturerHomePage</h2>
    //         <Logout />
    //         <form onSubmit={handleTrackNameSubmit}>
    //             <input
    //                 type="text"
    //                 value={itemName_tracking}
    //                 onChange={(e) => setitemName_tracking(e.target.value)}
    //                 placeholder="Enter track Name"
    //             />
    //             <button type="submit">Fetch Track Info</button>
    //         </form>
    //         <div>
    //             <h3>Track Information:</h3>
    //             {showTrackInfo && Trackinfo ? (
    //                 <div>
    //                     <p><strong>Departure:</strong> {Trackinfo.departure}</p>
    //                     <p><strong>Track Record:</strong> {Trackinfo.track_record}</p>
    //                     <p><strong>Destination:</strong> {Trackinfo.destination}</p>
    //                     <p><strong>Status:</strong> {Trackinfo.status}</p>
    //                 </div>
    //             ) : (
    //                 <p>No track information available.</p>
    //             )}
    //         </div>

    //         <form onSubmit={handlefetchDemandSubmit}>
    //             <input
    //                 type="text"
    //                 value={itemName_checkingDemand}
    //                 onChange={(e) => setitemName_checkingDemand(e.target.value)}
    //                 placeholder="Enter check demand Name"
    //             />
    //             <button type="submit">Fetch Demand History</button>
    //         </form>

    //         <div>
    //             <h3>Demand History:</h3>
    //             {showDemandHistory && Demandinfo ? (
    //                 <div>
    //                     <p><strong>Demand record:</strong> {Demandinfo.demand_record}</p>
    //                 </div>
    //             ) : (
    //                 <p>No demand information available.</p>
    //             )}
    //         </div>

    //         <form onSubmit={handlenewDemandSubmit}>
    //             <input
    //                 type="text"
    //                 value={demandAmount_new}
    //                 onChange={(e) => setDemandAmount_new(e.target.value)}
    //                 placeholder="Enter demand amount"
    //             />
    //             <input
    //                 type="text"
    //                 value={itemId_new}
    //                 onChange={(e) => setitemId_new(e.target.value)}
    //                 placeholder="Enter demand item id"
    //             />
    //             <button type="submit">Post New Demand</button>
    //         </form>

    //         <form onSubmit={handleupdateDemandSubmit}>
    //             <input
    //                 type="text"
    //                 value={demandAmount_update}
    //                 onChange={(e) => setDemandAmount_update(e.target.value)}
    //                 placeholder="Enter demand amount"
    //             />
    //             <input
    //                 type="text"
    //                 value={itemId_update}
    //                 onChange={(e) => setitemId_update(e.target.value)}
    //                 placeholder="Enter demand item id"
    //             />
    //             <button type="submit">Update Demand</button>
    //         </form>
    //         <div>
    //           Access Inventory Management: <Link to="/Manufacturer/inventory">Go to Manufacturer inventory</Link>
    //         </div>
    //     </div>
    // );