import { useContext } from "react"
import AuthContext from "../context/AuthContext"
import { Link } from "react-router-dom"

export default function LoginPage(){
    let {loginUser} = useContext(AuthContext)
    return(
    <div>
        <form onSubmit={loginUser} >
            <input type="email" name="email" placeholder="Enter email" />
            <input type="password" name="password" placeholder="Enter Password" />
            <input type="submit" />
        </form>
        <br />
        <Link to="/register">SignUp</Link>

    </div>
    )
}