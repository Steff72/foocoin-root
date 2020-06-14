import React, { useState, useEffect } from 'react'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faWallet} from '@fortawesome/free-solid-svg-icons'

import logo from '../assets/logo.png'
import { backend } from '../config'


const WalletInfo = () => {
  const [walletInfo, setwalletInfo] = useState({})

  const fetchWalletInfo = async () => {
    const response = await backend.get('/wallet/info')
    setwalletInfo(response.data)
  }

  useEffect( () => {
    fetchWalletInfo()

    // check Info every 5 seconds
    const iId = setInterval(fetchWalletInfo, 5000)

    // cleanup 
    return () => clearInterval(iId)
  }, [])

  const { address, balance } = walletInfo
  
  return (
    <div className="Walletinfo">
        <img className='logo' src={logo} alt="logo" />
        <hr />
        <h3>My Wallet  <FontAwesomeIcon icon={faWallet} /></h3>
        <div>Address: {address}</div>
        <div>Balance: {balance} FOC</div>
    </div>
  );
}

export default WalletInfo