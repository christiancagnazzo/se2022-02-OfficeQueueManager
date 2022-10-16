import './App.css';
import './custom.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import API from './API';
import Home from './components/home';
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
  const [services,setServices]=useState([]);
  const [dirty,setDirty]=useState(true)
  
  const navigate = useNavigate();
  useEffect(()=> {
    const checkAuth = async() => {
      if (dirty && loggedIn)  
        try {
          const user = await API.getUserInfo();
          setLoggedIn(true);
          setUser(user);
          setDirty(false)
        } catch(err) {
          handleError(err);
        }
    };
      checkAuth();
}, [dirty,loggedIn,user]);

useEffect(()=> {
  const getInfos = async() => {
    if (dirty)  
      try {
        const services = await API.getAllInfos();
        setServices(services)
        setDirty(false)
      } catch(err) {
        handleError(err);
      }
  };
  getInfos();
}, [dirty]);

function handleError(err){
  console.log(err);
}


  const doLogout = async () => {
    await API.logout();
    setLoggedIn(false);
    setUser({});
    setDirty(true);
    navigate('/');
  }

  
  const login = ()=>{navigate("/login")}
  const doLogin = (credentials) => {
    API.login(credentials)
      .then( user => {
        setLoggedIn(true);
        setUser(user);
        setDirty(true);
        setMessage('');
        navigate('/officer');
      })
      .catch(err => {
        setMessage(err);
      }
        )
  }

  const updateQueue= async (n)=>{
    await API.postQueue().catch(err => handleError(err)) 
    setDirty(true)
  }


  return (
    <>
    <MyNavbar2 loggedIn={loggedIn} logout={doLogout} login={login}/>
    <Container fluid>
       <Row className="vheight-100">
            <Routes> 
               <Route path='/' element={(loggedIn ? <Navigate to='/officer' /> : <Home services={services} updateQueue={updateQueue} /*cc={cc} setCc = {setCc} piano={piano} setPiano={setPiano} updateUser={updateUser} */loggedIn={loggedIn}  ></Home>)}></Route>
               <Route path='/login'  element={loggedIn ? <Navigate to='/officer' /> : <LoginForm login={doLogin} loginError={message} setLoginError={setMessage} /> }/>
               <Route path='/officer'  element={loggedIn ? <Navigate to='/officer' /> : <Navigate to='/' />}/>
            </Routes>
       </Row>
    </Container>
    </>
    );
  
}

export default App;
