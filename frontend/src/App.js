import{
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import './App.css';
import Hompage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Header from "./components/Header";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";

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
      </Routes>
      </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
