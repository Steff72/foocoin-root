import React, { useState, useEffect } from 'react';

import Blockchain from './Blockchain'

import logo from '../assets/logo.png'
import { URL } from '../config'


const App = () => {
  const [walletInfo, setwalletInfo] = useState({})

  useEffect( () => {
    fetch(`${URL}/wallet/info`)
      .then(response => response.json())
      .then(json => setwalletInfo(json))

    return () => {
      // cleanup
    }
  }, [])

  const { address, balance } = walletInfo
  
  return (
    <div className="App">
      <img className='logo' src={logo} alt="logo" />
      <h3>FooCoin</h3>
      <br />
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance} FOC</div>
      </div>
      <br />
      <Blockchain />
    </div>
  );
}

export default App;
