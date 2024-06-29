import React, { useState , useEffect } from 'react';
import Logout from '../components/Logout';
import { Link } from 'react-router-dom';
import { Button, TextField, Paper, Typography, Container, Box, Grid } from '@mui/material';
import Navbar from '../components/Navbar';


const ManufacturerItemPage = () => {

    const [Name, setName] = useState("");
    const [Type, setType] = useState("");
    const [Allitems, setAllitems] = useState([]);


    const newItem = (Name,Type) => {
      const token = localStorage.getItem('token');

      const PORT_NUM = 8000;
      const newItem = {
        name: Name,
        type:Type,
      };
  
      fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/item/new`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newItem),
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

    const handlenewItemSubmit = (e) => {
      e.preventDefault();
      newItem(Name,Type);
    };

    const fetchallItems = async () => {
      const token = localStorage.getItem('token');
      const PORT_NUM = 8000;

      try {
        const response = await fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/items`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`Error fetching items: ${errorData.error}`);
        }

        return await response.json();
      } catch (error) {
        console.error('Error:', error);
        throw error; 
      }
    };


    useEffect(() => {
      fetchallItems()
      .then(data => {
          const itemList = data.item_list.split(', ');
          setAllitems(itemList);
        })
    }, []);

    const handlefetchallItemsSubmit = (e) => {
      e.preventDefault();
      console.log("here2")
      fetchallItems().then(data => {
        console.log("data",data)
        setAllitems(data);
        console.log("get all items :",data)
      }).catch(error => {
          console.error("Error fetching items:", error);
      });
    };


    return(
      <Container maxWidth="md">
        <Navbar />
        <Paper elevation={3} style={{ padding: '20px', marginTop: '30px' }}>
          {/* <Logout /> */}
          {/* <Typography variant="h4" gutterBottom>Manufacturer Item Page</Typography> */}
          <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
            Submit New Items:
          </Typography>

          <Box component="form" onSubmit={handlenewItemSubmit} noValidate sx={{ mt: 1 }}>
              <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                    fullWidth
                    id="Name"
                    label="Item Name"
                    value={Name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter Item Name"
                    margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                    fullWidth
                    id="Type"
                    label="Item Type"
                    value={Type}
                    onChange={(e) => setType(e.target.value)}
                    placeholder="Enter Item Type"
                    margin="normal"
                />
              </Grid>
            </Grid>
            <Button type="submit" variant="contained" color="primary" sx={{ mt: 3, mb: 2, width: '100%' }}>
                Submit New Item
            </Button>

            <Box mt={2}>
                {/* <Typography variant="h6">All items:</Typography> */}
                {Allitems ? (
                    <Typography><strong>Submitted items:</strong> {Allitems.item_list}</Typography>
                ) : (
                  <Typography>No Submitted Items.</Typography>
                )}
            </Box>

            <Button onClick={handlefetchallItemsSubmit} variant="contained" color="secondary">
              Update Item List
            </Button>

            <Box mt={4} mb={2}>
                <Link to="/manufacturer/homepage" style={{ textDecoration: 'none' }}>
                    <Button variant="outlined" color="secondary">
                        Go to Manufacturer homepage
                    </Button>
                </Link>
                <Link to="/manufacturer/inventory" style={{ textDecoration: 'none' }}>
                    <Button variant="outlined" color="secondary">
                        Go to Manufacturer inventory
                    </Button>
                </Link>
            </Box>

          </Box>
        </Paper>
      </Container>
);


};

export default ManufacturerItemPage;





// const [items, setItems] = useState([]);

// const fetchAllItems = async () => {
//   const token = localStorage.getItem('token');
//   const PORT_NUM = 8000;

//   try {
//     const response = await fetch(`http://localhost:${PORT_NUM}/admin/manufacturer/items`, {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         Authorization: `Bearer ${token}`,
//       },
//     });

//     if (!response.ok) {
//       const errorData = await response.json();
//       throw new Error(`Error fetching items: ${errorData.error}`);
//     }

//     return await response.json();
//   } catch (error) {
//     console.error('Error:', error);
//     throw error; // Re-throw the error if you want to handle it outside of this function
//   }
// };

// // Usage

// useEffect(() => {
//   fetchAllItems()
//     .then(data => {
//       // Split the item_list string into an array
//       const itemList = data.item_list.split(', ');
//       setItems(itemList);
//     })
//     .catch(error => {
//       setError(error.message);
//     });
// }, []);

// return (
//   <div>
//     <h1>Items</h1>
//     <ul>
//       {items.map((item, index) => (
//         <li key={index}>{item}</li> // Use index as key in absence of unique ids
//       ))}
//     </ul>
//   </div>
// );