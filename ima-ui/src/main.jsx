import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { registerContinuity } from './services/deviceContinuity';

registerContinuity();

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
