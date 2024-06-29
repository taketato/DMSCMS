import React, { useState } from 'react';
import Logout from '../components/Logout';
import { Link } from 'react-router-dom';
import { Button, TextField, Container, Typography, Box, Paper} from '@mui/material';
import Navbar from '../components/Navbar';
//import Container from '@mui/material/Container';

const ManufacturerInvPage = () => {
    const [Invinfo, setInvinfo] = useState([]);
    const [Itemname_check, setItemname_check] = useState('');
    const [Itemname_receive, setItemname_receive] = useState('');
    const [Itemquantity_receive, setItemquantity_receive] = useState('');
    const [Itembatchno_receive, setItembatchno_receive] = useState('');
    const [Itemproductiondate_receive, setItemproductiondate_receive] = useState('');
    const [Itemname_send, setItemname_send] = useState('');
    const [Itemquantity_send, setItemquantity_send] = useState('');
    const [Itembatchno_send, setItembatchno_send] = useState('');
    const [Itemproductiondate_send, setItemproductiondate_send] = useState('');
    const [Itemdestination_send, setItemdestination_send] = useState('');

    const [showInvinfo, setshowinvInfo] = useState(false);
    //=================check Inventory information=================

    const fetchInvinfo = () => {
        const token = localStorage.getItem('token');
        const PORT_NUM = 8000;
        const item_Name = {
            item_name:Itemname_check,
        };
    
        return fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/inventory`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(item_Name),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            } else {
              return response.json().then((errorData) => {
                throw new Error(`Error fetching Inventory information: ${errorData.error}`);
              });
            }
          });
      };

    const handlefetchInvinfoSubmit = (e) => {
        e.preventDefault();
        fetchInvinfo().then(data => {
            setInvinfo(data);
            setshowinvInfo(true)
        }).catch(error => {
            console.error("Error fetching inventory:", error);
        });
    };

    //=================update Inventory information when receive=================

    const updateInvinfo_receive = () => {
        const token = localStorage.getItem('token');
        const PORT_NUM = 8000;
        const item_info_receive = {
            item_name:Itemname_receive,
            item_quantity:parseInt(Itemquantity_receive,10),
            item_batch_no:parseInt(Itembatchno_receive,10),
            item_production_date:parseInt(Itemproductiondate_receive,10),
        };

        console.log("sending",item_info_receive)


    
        return fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/set_inventory`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(item_info_receive),
        })
            .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then((errorData) => {
                throw new Error(`Error updating Inventory information: ${errorData.error}`);
                });
            }
            });
        };

    const handleupdateInvinfo_receiveSubmit = (e) => {
        e.preventDefault();
        updateInvinfo_receive().then(data => {
            setInvinfo(data);
            setshowinvInfo(true)
        }).catch(error => {
            console.error("Error updating inventory:", error);
        });
    };

    //=================update Inventory information when send=================

    const updateInvinfo_send = () => {
        const token = localStorage.getItem('token');
        const PORT_NUM = 8000;
        const item_info_send = {
            item_name:Itemname_send,
            item_quantity:parseInt(Itemquantity_send,10),
            item_batch_no:parseInt(Itembatchno_send,10),
            item_production_date:parseInt(Itemproductiondate_send,10),
            destination:Itemdestination_send,
        };

        console.log("sending",item_info_send)
    
        return fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/set_outbound`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(item_info_send),
        })
            .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then((errorData) => {
                throw new Error(`Error updating Inventory information: ${errorData.error}`);
                });
            }
            });
        };

    const handleupdateInvinfo_sendSubmit = (e) => {
        e.preventDefault();
        updateInvinfo_send().then(data => {
            console.log("data",data)
            setInvinfo(data);
            setshowinvInfo(true)
        }).catch(error => {
            console.error("Error updating inventory:", error);
        });
    };



    return (
        <Container maxWidth="md">
            <Navbar />
            <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
                {/* <Typography variant="h4" gutterBottom>
                    Manufacturer Inventory Page
                </Typography> */}
                {/* <Logout /> */}

                {/* Fetch Inventory Info */}
                <Box component="form" onSubmit={handlefetchInvinfoSubmit} sx={{ mt: 1 }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Check inventory item name"
                        placeholder="Enter item name"
                        value={Itemname_check}
                        onChange={(e) => setItemname_check(e.target.value)}
                        margin="normal"
                    />
                    <Button type="submit" fullWidth variant="contained" color="primary">
                        Check Inventory
                    </Button>
                </Box>

                {/* Update Inventory Info on Receive */}
                <Box component="form" onSubmit={handleupdateInvinfo_receiveSubmit} sx={{ mt: 1 }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Received item name"
                        placeholder="Enter item name"
                        value={Itemname_receive}
                        onChange={(e) => setItemname_receive(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Received item quantity"
                        placeholder="Enter item quantity"
                        value={Itemquantity_receive}
                        onChange={(e) => setItemquantity_receive(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Received item batch number"
                        placeholder="Enter item batch number"
                        value={Itembatchno_receive}
                        onChange={(e) => setItembatchno_receive(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Received item production date"
                        placeholder="Enter item production date"
                        value={Itemproductiondate_receive}
                        onChange={(e) => setItemproductiondate_receive(e.target.value)}
                        margin="normal"
                    />
                    <Button type="submit" fullWidth variant="contained" color="secondary" sx={{ mt: 2 }}>
                        Set Inventory on Receive
                    </Button>
                </Box>
               
                {/* Update Inventory Info on Send */}
                <Box component="form" onSubmit={handleupdateInvinfo_sendSubmit} sx={{ mt: 1 }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Sent item name"
                        placeholder="Enter item name"
                        value={Itemname_send}
                        onChange={(e) => setItemname_send(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Sent item quantity"
                        placeholder="Enter item quantity"
                        value={Itemquantity_send}
                        onChange={(e) => setItemquantity_send(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Sent item batch number"
                        placeholder="Enter item batch number"
                        value={Itembatchno_send}
                        onChange={(e) => setItembatchno_send(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Sent item production date"
                        placeholder="Enter item production date"
                        value={Itemproductiondate_send}
                        onChange={(e) => setItemproductiondate_send(e.target.value)}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Sent item destination"
                        placeholder="Enter item destination "
                        value={Itemdestination_send}
                        onChange={(e) => setItemdestination_send(e.target.value)}
                        margin="normal"
                    />
                    <Button type="submit" fullWidth variant="contained" color="secondary" sx={{ mt: 2 }}>
                        Set Inventory on Send
                    </Button>
                </Box>


                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                        Inventory Information:
                </Typography>
                {showInvinfo && Invinfo ? (
                    <Box>
                        <Typography><strong>Item name:</strong> {Invinfo.item_name}</Typography>
                        <Typography><strong>Item quantity:</strong> {Invinfo.item_quantity}</Typography>
                    </Box>
                ) : (
                    <Typography>No inventory information available.</Typography>
                )}

                {/* Link to Homepage */}
                <Box mt={4} mb={2}>
                  <Link to="/manufacturer/homepage" style={{ textDecoration: 'none' }}>
                      <Button variant="outlined" color="secondary">
                        Go to Manufacturer homepage
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


export default ManufacturerInvPage;
