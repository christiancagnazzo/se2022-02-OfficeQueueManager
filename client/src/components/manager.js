import {Col, Button,Row} from 'react-bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '../custom.css';

function Manager(props) {
    return (<>
        <Col className="col-12 below-nav">
            <Row>Daily:{''}</Row>
            <Row>Service1:{''}</Row>
            <Row>Service2:{''}</Row>
            <Row>Service3{''}</Row>
            <Row>Service4:{''}</Row>
            <Row>Service5:{''}</Row>
            <Row>Service6:{''}</Row>
        </Col>
        <Col className="col-12 below-nav">
            <Row>Weekly:{''}</Row>
            <Row>Service1:{''}</Row>
            <Row>Service2:{''}</Row>
            <Row>Service3{''}</Row>
            <Row>Service4:{''}</Row>
            <Row>Service5:{''}</Row>
            <Row>Service6:{''}</Row>
        </Col>    
        <Col className="col-12 below-nav">
            <Row>Monthly:{''}</Row>
            <Row>Service1:{''}</Row>
            <Row>Service2:{''}</Row>
            <Row>Service3{''}</Row>
            <Row>Service4:{''}</Row>
            <Row>Service5:{''}</Row>
            <Row>Service6:{''}</Row>
            <Button type="button"  onClick={() => {clicking(props.update)}}>Update dates</Button>        
        </Col>
    </>
    );
}


function clicking(update){
    update();
}

export default Manager;