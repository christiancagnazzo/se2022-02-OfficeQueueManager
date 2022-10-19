import {Col, Button,Row} from 'react-bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '../custom.css';
import API from '../API';
import { useEffect, useState } from 'react';

function Manager(props) {
    useEffect(()=> {
        const info = async() => {
            await API.update().then((c)=>{props.setInfo(c)}).catch(err=>console.log(err))
        }
        
        info();
      }, []);

    return (
        !props.info ? null :
        <>
        <Col className="col-12 below-nav">
            <Row>Daily</Row>
            <Row>Shipping: {props.info['daily']['Shipping'] }</Row>
            <Row>Account Management: {props.info['daily']['Account Management']}</Row>
            <Row>Credit Card: {props.info['daily']['Credit Card']}</Row>
            <Row>Pension: {props.info['daily']['Pension']}</Row>
        </Col>
        <Col className="col-12 below-nav">
            <Row>Weekly</Row>
            <Row>Shipping: {props.info['weekly']['Shipping'] }</Row>
            <Row>Account Management: {props.info['weekly']['Account Management']}</Row>
            <Row>Credit Card: {props.info['weekly']['Credit Card']}</Row>
            <Row>Pension: {props.info['weekly']['Pension']}</Row>
        </Col>  
        <Col className="col-12 below-nav">
            <Row>Monthly</Row>
            <Row>Shipping: {props.info['monthly']['Shipping'] }</Row>
            <Row>Account Management: {props.info['monthly']['Account Management']}</Row>
            <Row>Credit Card: {props.info['monthly']['Credit Card']}</Row>
            <Row>Pension: {props.info['monthly']['Pension']}</Row>
        </Col> 
        <Button type="button"  onClick={() => {clicking(props.update)}}>Update dates</Button>        
        
    </>
    );
}


function clicking(update){
    update();
}

export default Manager;