import { useEffect,useContext } from "react";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function SpotifyRedirect(){
    let {authTokens} = useContext(AuthContext)
    let navigate = useNavigate()
    let spotifyCallback = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/redirect/',{
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
            }       
        })
        let data = await response.json()
        if(response.ok){
            navigate('/')
        }
    }

    useEffect(()=>{

        spotifyCallback()

    },[])

}