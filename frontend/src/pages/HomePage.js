import RoomItem from "../components/RoomItem";
import { Link } from "react-router-dom";
import { useState,useEffect,useContext } from "react";
import { useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

function Hompage(){


    let [rooms,setRooms] = useState([])
    let {authTokens} = useContext(AuthContext) 
    let [roomKey,setRoomKey] = useState(()=>
        localStorage.getItem('room_key') ? localStorage.getItem('room_key') : null
    )
    let navigate = useNavigate()

    let getOptions = {
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
        },
    }

    let getRooms = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/api/',getOptions)
        let data = await response.json()
        if (response.status === 200){
            setRooms(data)
        }
    }


    useEffect(()=>{
        if(roomKey){
            navigate(`/:${roomKey}`)
        }
              // eslint-disable-next-line react-hooks/exhaustive-deps
    },[])

    // use effect to render rooms. dependency to be number of rooms available
    useEffect(()=>{
        getRooms()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    },[rooms.length])

    return(
    <div>
        <h1>Welcome</h1>
        <Link to="/create">
        <button>Create Room</button>
        </Link>
        {rooms.map((room)=>(
                <RoomItem key={room.id_session} 
                room = {room}/>
            ))}

    </div>
    )
}

export default Hompage;