import React from 'react';
import ReactDOM from 'react-dom';
import './i18n';
import App from './App';
import * as serviceWorker from './serviceWorker';

const appVersion = window._env_.APP_VERSION

ReactDOM.render(<App version={appVersion}/>, document.getElementById('root'));

serviceWorker.unregister();
