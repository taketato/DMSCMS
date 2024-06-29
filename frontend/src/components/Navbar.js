import React, { useState, useEffect } from 'react';
import { useNavigate , useLocation } from 'react-router-dom';
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { jwtDecode } from 'jwt-decode'; 
import { Link } from 'react-router-dom';

const Navbar = () => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [username, setUsername] = useState('');
    const [useridentity, setUseridentity] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
        try {
            const decoded = jwtDecode(token);
            setUsername(decoded.username);
            setUseridentity(decoded.sub);
        } catch (error) {
            console.error('Token decoding failed:', error);
        }
        }
    }, []); 

    const handleMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        console.log("Sending :", token);

        const PORT_NUM = '8000';
        fetch(`http://127.0.0.1:${PORT_NUM}/admin/auth/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
        })
        .then((response) => {
            console.log("response: ", response);
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Invalid --token');
            }
        })
        .then(() => {
            console.log('token removed: ', token);
            localStorage.removeItem('token'); 
            navigate('/login');
        })
        .catch(error => {
            console.error('Error during logout:', error);
        });
    };
    const location = useLocation();

    const pageNames = {
        '/hospital/homepage': 'Hospital Homepage',
        '/hospital/inventory': 'Hospital Inventory',
        '/wholesaler/homepage': 'Wholesaler Homepage',
        '/wholesaler/inventory': 'Wholesaler Inventory',
        '/manufacturer/homepage': 'Manufacturer Homepage',
        '/manufacturer/inventory': 'Manufacturer Inventory',
        '/manufacturer/items': 'Manufacturer Items',
    };

    const currentPageName = pageNames[location.pathname] 

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    {currentPageName}  - Logged in as {username}   
                </Typography>
                <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    onClick={handleMenu}
                    sx={{ mr: 2 }}
                >
                <MenuIcon />
                </IconButton>
                <Menu
                    anchorEl={anchorEl}
                    anchorOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                    }}
                    keepMounted
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                    }}
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                >
                {
                    useridentity === 'hospital' && (
                    <MenuItem component={Link} to="/hospital/homepage">
                        Hospital Homepage
                    </MenuItem>
                    )
                }
                {
                    useridentity === 'hospital' && (
                    <MenuItem component={Link} to="/hospital/inventory">
                        Hospital Inventory
                    </MenuItem>
                    )
                }
                {
                    useridentity === 'wholesaler' && (
                    <MenuItem component={Link} to="/wholesaler/homepage">
                        Wholesaler Homepage
                    </MenuItem>
                    )
                }
                {
                    useridentity === 'wholesaler' && (
                    <MenuItem component={Link} to="/wholesaler/inventory">
                        Wholesaler Inventory
                    </MenuItem>
                    )
                }
                {
                    useridentity === 'manufacturer' && (
                    <MenuItem component={Link} to="/manufacturer/homepage">
                        Manufacturer Homepage
                    </MenuItem>
                    )
                }
                {
                    useridentity === 'manufacturer' && (
                    <MenuItem component={Link} to="/manufacturer/inventory">
                        Manufacturer Inventory
                    </MenuItem>
                    )
                }
                {
                    useridentity === 'manufacturer' && (
                    <MenuItem component={Link} to="/manufacturer/items">
                        Manufacturer Items
                    </MenuItem>
                    )
                }
                {
                    <MenuItem component={Link} to="/">
                        Frontpage
                    </MenuItem>           
                }
                {
                    <MenuItem component={Link} to="/patient/homepage">
                        Patient
                    </MenuItem>           
                }
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
        </Toolbar>
        </AppBar>
    );
};

export default Navbar;

