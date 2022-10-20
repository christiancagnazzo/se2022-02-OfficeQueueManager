import { Button} from 'react-bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';
import  {useParams, useLocation} from  'react-router-dom';


function Officer(props) {
    const {id} = useParams()
    console.log(id)
    return (
            <Button type="button"  onClick={() => {clicking(props.next, id)}}>{ButtonSet(props.client, id)}</Button>        
    );
}
function ButtonSet(n, counter_id){
    return (<>
    <div>Counter: {counter_id} </div>
    <div>You are serving: {n}</div>
    <div>Click to call next client</div>
    </>)
}

function clicking(next,id){
    next(id);
}

export default Officer;