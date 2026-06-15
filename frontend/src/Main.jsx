import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './Global.css'
import App from './Routes/Index.jsx'
import Practice from './Routes/Practice.jsx'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.js';
 
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path='/practice' element={<Practice/>}/>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
