import React from 'react';
import ReactDOM from 'react-dom';
import './i18n';
import { App } from './App.js';
import * as serviceWorker from './serviceWorker';

const appVersion = process.env.APP_VERSION

ReactDOM.render(<App version={appVersion}/>, document.getElementById('root'));

serviceWorker.unregister();
