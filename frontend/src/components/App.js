import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

import MyNavbar from './Navbar'

import logo from '../assets/logo.png'
import { backend } from '../config'


const App = () => {
  const [walletInfo, setwalletInfo] = useState({})

  useEffect( () => {
    backend.get('/wallet/info')
      .then(response => setwalletInfo(response.data))

    return () => {
      // cleanup
    }
  }, [])

  const { address, balance } = walletInfo
  
  return (
    <div className="App">
    <MyNavbar />
      <img className='logo' src={logo} alt="logo" />
      <h3>FooCoin</h3>
      <hr />
      <Link to="/blockchain">Explore the Blockchain</Link>
      <Link to="/send-tx">Make a Transaction</Link>
      <Link to="/transactions">Transaction Pool</Link>
      <hr />
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance} FOC</div>
      </div>
    </div>
  );
}

export default App;
