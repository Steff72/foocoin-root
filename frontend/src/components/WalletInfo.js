import React, { useState, useEffect } from 'react'

import logo from '../assets/logo.png'
import { backend } from '../config'


const WalletInfo = () => {
  const [walletInfo, setwalletInfo] = useState({})

  useEffect( () => {
    backend.get('/wallet/info')
      .then(response => setwalletInfo(response.data))

  }, [])

  const { address, balance } = walletInfo
  
  return (
    <div className="Walletinfo">
        <img className='logo' src={logo} alt="logo" />
        <h3>FooCoin</h3>
        <hr />
            <div>My Address: {address}</div>
            <div>My Balance: {balance} FOC</div>
    </div>
  );
}

export default WalletInfo