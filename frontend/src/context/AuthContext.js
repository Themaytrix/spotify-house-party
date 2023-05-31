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
    let [room,setRoom] = useState(null)

    // fetching user data from dj backend
    let loginUser = async (e) =>{
        e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/users/api/token/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'email':e.target.email.value, 'password':e.target.password.value})
        })

        let data = await response.json()
        if(response.status === 200){
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens',JSON.stringify(data))
            navigate("/")
        }


    }

    // signup
    let signupUser = async (e) =>{
        e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/users/',{
            method: 'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'username':e.target.username.value, 'password':e.target.password.value, 'email':e.target.email.value})
        })
        if(response.status === 201){
            navigate('/login')
        }
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
        let response = await fetch('http://127.0.0.1:8000/users/api/token/refresh/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'refresh':authTokens?.refresh})
        })
        let data = await response.json()
        if(response.status === 200){
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens',JSON.stringify(data))
        }else{
            logoutUser()
        }

        if(loading){
            setLoading(false)
        }
    }

    //creating room
    let createRoom = async (e)=>{
        e.preventDefault()

        let response = await fetch('http://127.0.0.1:8000/api/create/',{
            method: "POST",
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer' + String(authTokens.access)
            },
            body: JSON.stringify({'name':e.target.name.value, 'votes-to-skip': e.target.votes_to_skip.value})
        })

        let data = await response.json()
        if(response.status === 200){
            setRoom(data)
            navigate("/")
        }

    }


    // setting contextdata
    let contextData = {
        user:user,
        room:room,
        loginUser:loginUser,
        logoutUser:logoutUser,
        signupUser:signupUser,
        createRoom:createRoom,

    }

    useEffect(()=>{

        if(loading){
            updateToken()
        }

        let refresTime = 1000 * 60 * 4
        let interval = setInterval(()=>{
            if(authTokens){
                updateToken()
            }
        },refresTime)
        return ()=> clearInterval(interval)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    },[authTokens,loading])

    return(
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )
} 