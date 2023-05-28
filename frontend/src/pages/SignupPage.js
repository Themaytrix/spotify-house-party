import { useContext } from "react"
import AuthContext from "../context/AuthContext"

export default function SignupPage(){
    let {signupUser} = useContext(AuthContext)
    return(
        <div>
            <form onSubmit={signupUser}>
            <input type="text" name="username" placeholder="Enter Username" />
            <input type="password" name="password" placeholder="Enter Password" />
            <input type="email" name ="email" placeholder="Enter email" />
            <input type="submit"  />
            </form>
        </div>
    )
}