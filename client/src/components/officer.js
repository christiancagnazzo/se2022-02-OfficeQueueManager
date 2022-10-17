import { Button} from 'react-bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';

function Officer(props) {

    return (
            <Button type="button"  onClick={() => {clicking(props.next)}}>{ButtonSet(props.client)}</Button>        
    );
}
function ButtonSet(n){
    return (<>
    <div>You are serving: {n}</div>
    <div>Call next client</div>
    </>)
}

function clicking(next){
    next();
}

export default Officer;