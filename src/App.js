import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import AllStudentsList from "./pages/AllStudentsList";
import Login from "./pages/Login";
import Registration from "./pages/Registration";
import StudentDetails from "./pages/StudentDetails";
import StudentVerification from "./pages/StudentVerification";

function App() {
  return (
    // <div>
    //   <Login />
    // </div>
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/registration" element={<Registration />} />
          <Route path="/student_list" element={<AllStudentsList />} />
          <Route path="/student_detail/:id" element={<StudentDetails />} />
          <Route path="/verify_student/:id" element={<StudentVerification />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
