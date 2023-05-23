import { Link } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";


export default function Header(){
    let {user,logoutUser} = useContext(AuthContext)
    return(
        <div>
            <Link to="/">Home</Link> 
            <span> | </span>
            { user ? <Link onClick={logoutUser} to="/login">Logout</Link> : <Link to="/login">Login</Link> }
           

            {user && <p>{user.username}</p>}
        </div>
    )
}