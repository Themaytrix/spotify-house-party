import { Link } from "react-router-dom";

export default function Header(){
    return(
        <div>
            <Link to="/">Home</Link> 
            <span> | </span>
            <Link to="/login">Login</Link> 
        </div>
    )
}