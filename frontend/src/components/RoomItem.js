import { useContext } from "react"
import AuthContext from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function RoomItem(props){
    let {authTokens} =useContext(AuthContext)
    let navigate = useNavigate()
    let joinRoom = async ()=>{
        let response = await fetch('',{
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body:JSON.stringify({'id_session': props.room.id_session})
        })

        let data = await response.json()
        if(response.ok){
            navigate("/")
        }
    }
    return(
        <div>
        
            <h4>{props.room.name}</h4>
            <button key={props.room.id_session} onClick={joinRoom}>Join Room</button>
        
        </div>
    )
}