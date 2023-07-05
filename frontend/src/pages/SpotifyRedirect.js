import { useEffect,useContext,useState } from "react";
import AuthContext from "../context/AuthContext";
import { useNavigate} from "react-router-dom";

export default function SpotifyRedirect(){
    let {authTokens} = useContext(AuthContext)

    const urlCode = new URLSearchParams(window.location.search)

    let code = urlCode.get('code')
    console.log(code)
    let id_session = localStorage.getItem('room_key')

    let navigate = useNavigate()
    let spotifyCallback = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/spotify/redirect/',{
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body: JSON.stringify({"code": code, "id_session": id_session})
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