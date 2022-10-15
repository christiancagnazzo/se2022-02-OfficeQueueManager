import './App.css';
import './custom.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import API from './API';
import { Container, Row } from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { LoginForm } from './components/login';
import MyNavbar2 from './components/navbarlogin';

function App(){
  return (
    <Router>
      <App2/>
    </Router>
  )
}

function App2() {
  const [loggedIn,setLoggedIn]=useState(false);
  const [user, setUser] = useState({});
  const [message, setMessage] = useState('');
  
  const navigate = useNavigate();

  const doLogout = async () => {
    await API.logout();
    setLoggedIn(false);
    setUser({});
    /*
    setFirsttime(true);
    setDirty(true);
    i'll see after if ill need it
    */
    navigate('/');
  }

  // used to login
  const login = ()=>{navigate("/login")}
  const doLogin = (credentials) => {
    API.login(credentials)
      .then( user => {
        setLoggedIn(true);
        setUser(user);
        //setFirsttime(true);
        setMessage('');
        navigate('/officer');
      })
      .catch(err => {
        setMessage(err);
      }
        )
  }

  return (
    <>
    <MyNavbar2 loggedIn={loggedIn} logout={doLogout} login={login}/>
    <Container fluid>
       <Row className="vheight-100">
            <Routes> 
               <Route path='/' /*element={(<Home cc={cc} setCc = {setCc} piano={piano} setPiano={setPiano} updateUser={updateUser} loggedIn={loggedIn} deleteUser={deleteUser} */></Route>
               <Route path='/login'  element={loggedIn ? <Navigate to='/officer' /> : <LoginForm login={doLogin} loginError={message} setLoginError={setMessage} /> }/>
               <Route path='/officer'  element={loggedIn ? <Navigate to='/officer' /> : <Navigate to='/' />}/>
            </Routes>
       </Row>
    </Container>
    </>
    );
  
}

export default App;
