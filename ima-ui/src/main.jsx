import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { registerContinuity } from './services/deviceContinuity';
import { scheduleDeviceHealth } from './services/deviceHealth';

registerContinuity();
scheduleDeviceHealth();

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
