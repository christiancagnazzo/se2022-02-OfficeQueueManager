import './App.css';
import './custom.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import API from './API';
import Home from './components/home';
import Officer from './components/officer';
import { Alert, Container, Row } from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { LoginForm } from './components/login';
import MyNavbar2 from './components/navbarlogin';
import Manager from './components/manager.js';

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
  const [flag,setFlag]=useState(false)
  const [message, setMessage] = useState('');
  const [services,setServices]=useState([1]);
  const [dirty,setDirty]=useState(true);
  const [gettedTicket,setGettedTicket]=useState('-');
  const [minWait,setMinWait]=useState('-');
  const [ticket,setTicket]=useState('-');
  const [info,setInfo]=useState(null)
  
  const navigate = useNavigate();
  /*useEffect(()=> {
    const checkAuth = async() => {
      if (dirty && loggedIn)  
        try {
          const user = await API.getUserInfo();
          setLoggedIn(true);
          setUser(user.num);
          setFlag(user.flag)
          setDirty(false)
        } catch(err) {
          handleError(err);
        }
    };
      checkAuth();
}, [dirty,loggedIn,user]);*/

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
    setFlag(false)
    setDirty(true);
    navigate('/');
  }

  
  const login = ()=>{navigate("/login")}
  const doLogin = (credentials) => {
    API.login(credentials)
      .then( user => {
        setLoggedIn(true);
        setUser(user.num);
        setFlag(user.flag);
        setDirty(true);
        setMessage('');
        navigate('/officer');
      })
      .catch(err => {
        setMessage(err);
      }
        )
  }

  const updateQueue= async (service)=>{
    try {
      let res = await API.postQueue(service);
      setDirty(true);
      setGettedTicket(res['Ticket'])
      setMinWait(res['Time'])
    } catch(err) {
        handleError(err)
    }
  }

  const nextClient= async(counter)=>{
    await API.nextClient(counter)
    .then((c)=>{setTicket(c['next_client'])}).catch(err => setTicket(err))
  }
  const update=async()=>{
    await API.update().then((c)=>{setInfo(c)}).catch(err=>handleError(err))
  }

  return (
    <>
    {/*<MyNavbar2 loggedIn={loggedIn} logout={doLogout} login={login}/>*/}
    <Container fluid>
       <Row className="vheight-100">
            <Routes> 
              {/* 
               <Route path='/' element={(loggedIn ? <Navigate to='/officer' /> : <Home services={services} updateQueue={updateQueue} gettedTicket={gettedTicket} minWait={minWait} loggedIn={loggedIn}  ></Home>)}></Route>
               <Route path='/login'  element={loggedIn ? <Navigate to='/officer' /> : <LoginForm login={doLogin} loginError={message} setLoginError={setMessage} /> }/>
               <Route path='/officer'  element={(loggedIn && !flag) ? <Officer next={nextClient} client={ticket}/> : <Navigate to='/manager' />}/>
               <Route path='/manager'  element={true ? <Manager update={update} info={info}/> : <Navigate to='/' />}/>
               <Route />
               */}
               <Route path='/' element={<Home services={services} updateQueue={updateQueue} gettedTicket={gettedTicket} minWait={minWait} loggedIn={loggedIn}  ></Home>}></Route>
               <Route path='/officer/:id'  element={<Officer next={nextClient} client={ticket}/>}/>
               <Route path='/manager'  element={<Manager setInfo={setInfo} update={update} info={info}/>}/>
               <Route />
            </Routes>
       </Row>
    </Container>
    </>
    );
  
}

export default App;
