import { Form, Button, Alert, Container, Row, Col } from 'react-bootstrap';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginForm(props) {
  const [username, setUsername] = useState('1@polito.it');
  const [password, setPassword] = useState('password');
  const [errorMessage, setErrorMessage] = useState('') ;
  const navigate = useNavigate();
  

  function validateEmail(input){      
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailPattern.test(input); 
  } 
 

  const handleSubmit = (event) => {
      event.preventDefault();
      setErrorMessage('');
      const credentials = { username, password };
          
      if(username.trim().length === 0 || password.trim().length === 0)
          setErrorMessage('Compilare tutti i campi correttamente. ')
      else if(!validateEmail(username))
      {
        setErrorMessage('Formato email non valido')
      }
      else {
        props.login(credentials);
      }
  };

  return (
      <Container className="below-nav">
          <Row className='justify-content-center '>
              <Col>
                  <h2 className='text-center'>Login</h2>
                  <Form>
                      {errorMessage ? <Alert variant='danger' onClose={() => setErrorMessage('')} dismissible >{errorMessage}</Alert> : false}
                      {props.loginError ? <Alert variant='danger' onClose={() => props.setLoginError('')} dismissible >{props.loginError}</Alert> : false}
                      <Form.Group controlId='username'>
                          <Form.Label>Email</Form.Label>
                          <Form.Control type='email' value={username} onChange={ev => setUsername(ev.target.value)} />
                      </Form.Group>
                      <Form.Group controlId='password'>
                          <Form.Label>Password</Form.Label>
                          <Form.Control type='password' value={password} onChange={ev => setPassword(ev.target.value)} />
                      </Form.Group>
                      <div align ="center"> <Button className="mt-3" type="submit" variant="dark" onClick={handleSubmit}>Login</Button></div>
                      <div align ="center"><Button className="mt-3" variant="dark" onClick={() => navigate(`/`)}>Go back</Button></div>
                  </Form>
              </Col>
          </Row>
      </Container>
    )
}



export { LoginForm };