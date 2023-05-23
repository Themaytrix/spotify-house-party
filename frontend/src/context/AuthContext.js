import { useState,useEffect,createContext } from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

// creating context for auth
const AuthContext = createContext()

export default AuthContext;


export const AuthProvider = ({children}) => {
    // setting user states
    let [user,setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null)
    // setting auth tokens
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    let navigate = useNavigate()

    let [loading,setLoading] = useState(true)

    // fetching user data from dj backend
    let loginUser = async (e) =>{
        e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/accounts/api/token/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'username':e.target.username.value, 'password':e.target.password.value})
        })

        let data = await response.json()
        if(response.status === 200){
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens',JSON.stringify(data))
            navigate("/")
        }

        console.log('data:', data)
        console.log(user)
    }

    // logout
    let logoutUser = () =>{
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
        navigate('/login')

    }

    // updateToken

    let updateToken = async () =>{
        let response = await fetch('http://127.0.0.1:8000/accounts/api/token/refresh',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'refresh':authTokens.refresh})
        })
        let data = await response.json()
        if(response.status === 200){
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens',JSON.stringify(data))
        }else{
            logoutUser()
        }
    }


    // setting contextdata
    let contextData = {
        user:user,
        loginUser:loginUser,
        logoutUser:logoutUser,
    }

    useEffect(()=>{
        let interval = setInterval(()=>{
            if(authTokens){
                updateToken()
            }
        },2000)
        return ()=> clearInterval(interval)
    },[authTokens,loading])

    return(
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
} 