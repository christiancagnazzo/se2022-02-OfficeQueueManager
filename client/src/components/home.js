import { Button,ButtonGroup } from 'react-bootstrap';



import 'bootstrap-icons/font/bootstrap-icons.css';

function Home(props) {

    return (props.services.length!==0 ?
        <>
        <ButtonGroup >
            <Button type="button"  variant="primary" onClick={() => {clicking(0,props.updateQueue)}}>{ButtonSet(0,props)}</Button>
            <Button type="button"  variant="secondary" onClick={() => {clicking(1,props.updateQueue)}}>{ButtonSet(1,props)}</Button>
            <Button type="button"  variant="success" onClick={() => {clicking(2,props.updateQueue)}}>{ButtonSet(2,props)}</Button>
        </ButtonGroup>
        <ButtonGroup >
            <Button type="button"  variant="warning" onClick={() => {clicking(3,props.updateQueue)}}>{ButtonSet(3,props)}</Button>
            <Button type="button"  variant="danger" onClick={() => {clicking(4,props.updateQueue)}}>{ButtonSet(4,props)}</Button>
            <Button type="button"  variant="light" onClick={() => {clicking(5,props.updateQueue)}}>{ButtonSet(5,props)}</Button>
        </ButtonGroup>        
        </>:
        <h1 className="col-12 below-nav">Hey! non riceviamo alcuna risposta dal server! Prova a riaggiornare la pagina!</h1>
        
    );
}
function ButtonSet(n,props){
// PROPS HAVE SERVICES WITH REMAINING QUE FOR SERVICE
/*
let x = props.services[n]
let y =props.queue[n]
return (<>
    <div>{x}</div>
    <div>queue: {y}</div>
    </>)
*/
    return (<>
    <div>servizio</div>
    <div>coda</div>
    </>)
}

function clicking(n,updateQueue){
    updateQueue(n)
}

export default Home;