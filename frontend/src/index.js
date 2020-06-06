import React from 'react'
import ReactDOM from 'react-dom'
import { Router, Switch, Route } from 'react-router-dom'

import './index.css';
import history from './history'

import App from './components/App'
import Blockchain from './components/Blockchain'
import SendTx from './components/SendTx'
import TxPool from './components/TxPool'


ReactDOM.render(
    <Router history={history}>
      <Switch>
        <Route path='/' exact component={App} />
        <Route path='/blockchain' component={Blockchain} />
        <Route path='/send-tx' component={SendTx} />
        <Route path='/transactions' component={TxPool} />
      </Switch>
    </Router>,
  document.getElementById('root')
);