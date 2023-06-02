import Room from "../components/Room";
import { Link } from "react-router-dom";
function Hompage(){
    return(
    <div>
        <h1>Welcome</h1>
        <Link to="/create">
        <button>Create Room</button>
        </Link>
        <Room/>

    </div>
    )
}

export default Hompage;