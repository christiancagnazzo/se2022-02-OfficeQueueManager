import { Col, ListGroup, Button } from 'react-bootstrap';
import { useState, useEffect } from 'react'


import 'bootstrap-icons/font/bootstrap-icons.css';

function Home(props) {
console.log(props.services.length)
    return (props.services.length!==0 ?
        <>
        
            <Col md={12} className="col-12 below-nav"> 
                <ImgSet services={props.services}></ImgSet>
            </Col>
            <Col md={12} >
            ciao2    
            </Col>
        </>:
        <h1 className="col-12 below-nav">Hey! non riceviamo alcuna risposta dal server! Prova a riaggiornare la pagina!</h1>
        
    );
}
function ImgSet(props){

}

export default Home;