import { BrowserRouter, Routes, Route } from "react-router-dom";
import ResponsiveAppBar from "./components/navbar/App-bar";
import StickyFooter from "./components/footer/Footer";
import Home from "./components/pages/home/Home";
import Chronologie from "./components/pages/chronologie/Chronologie";
import Participants from "./components/pages/participants/Participants";
import Participant from "./components/pages/participants/Participant";
import Analyse from "./components/pages/analyse/Analyse";
import Votes from "./components/pages/votes/Votes";
import './App.css';

function App() {
  return (
    <div className="App">
			<BrowserRouter>
				<ResponsiveAppBar/>
				<Routes>
					<Route path="/" element={<Home/>}/>
					<Route path="/Chronologie" element={<Chronologie/>}/>
					<Route path="/Participants" element={<Participants/>}/>
					<Route path="/Participant:name" element={<Participant/>}/>
					<Route path="/Votes" element={<Votes/>}/>
					<Route path="/Analyse" element={<Analyse/>}/>
				</Routes>
				<StickyFooter/>
			</BrowserRouter>
		</div>
  );
}

export default App;
