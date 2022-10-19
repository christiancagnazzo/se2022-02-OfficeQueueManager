import { Button} from 'react-bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';

const HARD_CODED_COUNTER = 1 // only for the demo

function Officer(props) {

    return (
            <Button type="button"  onClick={() => {clicking(props.next)}}>{ButtonSet(props.client)}</Button>        
    );
}
function ButtonSet(n){
    return (<>
    <div>Counter: {HARD_CODED_COUNTER}</div>
    <div>You are serving: {n}</div>
    <div>Click to call next client</div>
    </>)
}

function clicking(next){
    next(HARD_CODED_COUNTER);
}

export default Officer;