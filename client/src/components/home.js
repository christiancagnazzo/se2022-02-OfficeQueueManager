import { Alert, Button,ButtonGroup } from 'react-bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';

const colors = ["primary", "danger", "success", "warning", "light", "secondary" ]

function Home(props) {
    return (
        <>
            <Alert className='center'>
                <div> Your ticket is: {props.gettedTicket}</div>
                <div>Minimum waiting time: {props.minWait}</div>
            </Alert>
            {
                props.services.map( (s,i)=> {
                    return (
                        <Button className="marg" type="button"  variant={colors[i%6]} onClick={() => {clicking(s.name,props.updateQueue)}}>
                            <ButtonSet service={s}></ButtonSet>
                        </Button>
                    )
                })
            }
        </>
    );
}


function ButtonSet(props){
    return (<>
        <div>{props.service.tag}</div>
        <div>{props.service.name}</div>
        <div>People waiting: {props.service.last - props.service.actual}</div>
    </>)
}

function clicking(service, updateQueue){
    updateQueue(service)
}

export default Home;