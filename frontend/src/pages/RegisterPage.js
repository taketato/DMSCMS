import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Container, Typography, TextField, Button, FormControl, InputLabel, Select, MenuItem, Box } from "@mui/material";

const RegisterPage = () => {
  const [identity, setIdentity] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const [errormessage, setErrormessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const body = {
      email,
      password,
      identity,
      name,
    };
    console.log("Sending :", body);

    const PORT_NUM = '8000';
    fetch(`http://127.0.0.1:${PORT_NUM}/admin/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      //mode: 'no-cors',
      body: JSON.stringify(body),
    })//api call to register
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
            return response.json().then(json => {
              throw new Error(json.message || 'Registration failed');
          });
        }
      })
      .then((data) => {
        localStorage.setItem('token', data.token);
        console.log('token: ',localStorage.getItem('token'));
        navigate(`/login`);
      })
      .catch(error => {
        console.error('Error during registration:', error);
        setErrormessage(error.message); 
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">
          Register
        </Typography>

        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
          {errormessage && (
            <Box sx={{ mt: 2, color: 'red' }}>
              <Typography variant="body2">
                {errormessage}
              </Typography>
            </Box>
          )}
          <TextField
            margin="normal"
            fullWidth
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter username"
            variant="outlined"
          />
          <FormControl fullWidth margin="normal">
            <InputLabel id="identity-label">Identity</InputLabel>
            <Select
              value={identity}
              label="Identity"
              onChange={(e) => setIdentity(e.target.value)}
            >
              <MenuItem value="hospital">Hospital</MenuItem>
              <MenuItem value="wholesaler">Wholesaler</MenuItem>
              <MenuItem value="manufacturer">Manufacturer</MenuItem>
              {/* <MenuItem value="governmentAgent">Government Agent</MenuItem> */}
            </Select>
          </FormControl>
          <TextField
            margin="normal"
            fullWidth
            label="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter Email Address"
            variant="outlined"
          />
          <TextField
            margin="normal"
            fullWidth
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter Password"
            variant="outlined"
            type="password"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Register
          </Button>
          <Box textAlign="center">
            <Link to="/login" style={{ textDecoration: 'none', color: 'inherit' }}>
              {"Already have an account? Login"}
            </Link>
          </Box>
          <Box textAlign="center">
            <Link to="/patient/homepage" style={{ textDecoration: 'none', color: 'inherit' }}>
              {"Are you a patient? Tracking"}
            </Link>
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default RegisterPage;


// return (
//   <div>
//     <h2>Register</h2>
//     <form onSubmit={handleSubmit}>
//       <div>
//         <label htmlFor="Name">Name: </label>
//         <input
//           type="text"
//           placeholder="Name"
//           value={name}
//           onChange={(e) => setName(e.target.value)}
//         />
//       </div>
//       <div>
//         <label htmlFor="Identity">Identity: </label>
//         <select
//           value={identity}
//           onChange={(e) => setIdentity(e.target.value)}
//         >
//           <option value="" disabled>Select your identity</option>
//           <option value="producer">Producer</option>
//           <option value="wholesaler">Wholesaler</option>
//           <option value="hospital">Hospital</option>
//           <option value="governmentAgent">Government Agent</option>
//         </select>
//       </div>
//       <div>
//         <label htmlFor="Email">Email: </label>
//         <input
//           type="text"
//           placeholder="Email"
//           value={email}
//           onChange={(e) => setEmail(e.target.value)}
//         />
//       </div>
//       <div>
//         <label htmlFor="password">Password: </label>
//         <input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//         />
//       </div>
//       <button type="submit">Register</button>
//       <div>
//         Already have an account? <Link to="/login">Login</Link>
//       </div>
//     </form>
//   </div>
// );