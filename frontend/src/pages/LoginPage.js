import React, { useState } from "react";
import { useNavigate, Link} from "react-router-dom";
import { Container, Typography, TextField, Button, FormControl, InputLabel, Select, MenuItem, Box } from "@mui/material";

// require('react-dom');
// window.React2 = require('react');
// console.log(window.React1 === window.React2);
const LoginPage = () => {
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

    const PORT_NUM = '8000';
    console.log('sending: ',body);
    fetch(`http://127.0.0.1:${PORT_NUM}/admin/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    }) //api call to login
      .then((response) => {
        console.log('response: ',response);
        if (response.ok) {
          return response.json();
        } else {
            return response.json().then(json => {
              throw new Error(json.message || 'Login failed');
          });
        }
      })
      .then((data) => {
        localStorage.setItem('token', data.token);
        console.log('token: ',localStorage.getItem('token'));
        navigate(`/${identity}/homepage`);//redirect to identity homapage
      })
      .catch((error) => {
        console.error('Error during login:', error);
        setErrormessage(error.message); 
      });
  };
  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">
          Login
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          {errormessage && (
              <Box sx={{ mt: 2, color: 'red' }}>
                <Typography variant="body2">
                  {errormessage}
                </Typography>
              </Box>
          )}
          <TextField
            margin="normal"
            variant="outlined"
            fullWidth
            label="Name"
            placeholder="Enter username"
            value={name}
            onChange={(e) => setName(e.target.value)}
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
            variant="outlined"
            placeholder="Enter email"
          />
          <TextField
            margin="normal"
            fullWidth
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            variant="outlined"
            placeholder="Enter password"
            type="password"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Login
          </Button>
          <Box textAlign="center">
            <Link to="/register" style={{ textDecoration: 'none' }}>
              {"Don't have an account? Register"}
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

export default LoginPage;


// return (
//   <div>
//     <h2>Login</h2>
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
//       <button type="submit">Login</button>
//       <div>
//         Don&apos;t have an account? <Link to="/register">Register</Link>
//       </div>
//     </form>
//   </div>
// );