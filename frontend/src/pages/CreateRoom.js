import { useContext } from "react"
import AuthContext from "../context/AuthContext"

export default function CreateRoom(){
let {createRoom} = useContext(AuthContext)

    return(
        <div>
            <form onSubmit={createRoom}>
                <input type="text" name="room-name" placeholder="Room name"  />
                <input type="number" name="votes_to_skip" />
                <input type="submit" value="Create Room"/>
            </form>
        </div>
    )
}