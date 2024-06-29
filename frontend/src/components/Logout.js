import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';
const Logout = () => {
    const navigate = useNavigate();

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

    return (
        <Button variant="outlined" color="primary" onClick={handleLogout}>Logout</Button>
    );
};

export default Logout;
