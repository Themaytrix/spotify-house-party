import { useContext, useEffect, useState } from "react"
import { useParams,useNavigate } from "react-router-dom"
import AuthContext from "../context/AuthContext"

export default function ListeningPage(){
    let [activeRoom, setActiveRoom] = useState([])
    let [spotifyAuthenticated,setSpotifyAuthenticated] = useState(false)
    let {authTokens,user} = useContext(AuthContext)
    let {id} = useParams()
    let navigate = useNavigate()

    let getOptions = {
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
        },
    }

    let getRoomInfo = async ()=>{

        let response = await fetch(`http://127.0.0.1:8000/api/${id}/`,getOptions)

        let data = await response.json()
        if(response.ok){
            setActiveRoom(data)
            spotifyAuthenticate()
            if(!spotifyAuthenticated){
                // get auth url
                getAuthUrl()
            }

        }
    }

    let getAuthUrl = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/spotify/get-auth-url/',getOptions)
        
        let data = await response.json()
        if(response.ok){
            console.log(data)
            // Window.location.replace(url)
            
        }
    }

    let spotifyAuthenticate = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/spotify/is-authenticated/',getOptions)

        let data = await response.json()
        if(response.ok){
            setSpotifyAuthenticated(data.status)
        }
    }


    let leaveRoom = async (e)=>{
        e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/api/leave-room/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })

        let data = await response.json()
        if(response.ok){
            localStorage.removeItem('room_key')
            navigate('/')
        }
    }

    let endRoom = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/api/delete-room/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body:JSON.stringify({"id_session":id})
        })
        
        let data = await response.json()
        if(response.ok){
            localStorage.removeItem('room_key')
            navigate('/')
        }
    }


    useEffect(()=>{
        getRoomInfo()
        
    },[activeRoom.name])

    return(
        <div>
            <h3>{activeRoom.name}</h3>

            {activeRoom.host === user.user_id ? 
            <div>
                <button onClick={endRoom}>End Room</button>
            </div> : <div>
                <button onClick={leaveRoom}>Leave Room</button>
            </div>
            }
        </div>
    )
}