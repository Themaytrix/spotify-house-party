import { Navigate } from "react-router-dom";

export default function PrivateRoute({user,children}){
    user = true
    if(!user){
    return(
        <Navigate to="/login" replace/>
    )
    }
    return children;
}