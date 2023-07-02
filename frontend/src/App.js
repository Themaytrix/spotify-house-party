import{
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import './App.css';
import Hompage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Header from "./components/Header";
import SignupPage from "./pages/SignupPage";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
import CreateRoom from "./pages/CreateRoom";
import ListeningPage from "./pages/ListeningPage";
import SpotifyRedirect from "./pages/SpotifyRedirect";

function App() {
  let user
  return (
    <Router>
      <AuthProvider>
      <div className="App">
        <Header/>
      <Routes>
        <Route path="/" element={
          <PrivateRoute user={user}>
            <Hompage/>
          </PrivateRoute>} />
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/register" element={<SignupPage/>}/>
        <Route path="/create" element={<CreateRoom/>}/>
        <Route path="/callback" element={<SpotifyRedirect/>}/>
        <Route path="/:id" element={<ListeningPage/>}/>
        

      </Routes>
      </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
