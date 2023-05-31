// import { useContext } from "react";
// import AuthContext from "../context/AuthContext";
import { Link } from "react-router-dom";
function Hompage(){
    
    return(
    <div>
        <h1>Welcome</h1>
        <Link to="/create">
        <button>Create Room</button>
        </Link>

        <span> | </span>

        <button>Join Room</button>

    </div>
    )
}

export default Hompage;