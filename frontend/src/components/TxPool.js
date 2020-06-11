import React, { useState, useEffect } from 'react'

import Transaction from './Transaction'
import MyNavbar from './Navbar'
import Footer from './Footer'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'


import { backend } from '../config'
import history from '../history'


const TxPool = () => {
    const [tx, settx] = useState([])
    const [showAlert, setshowAlert] = useState(false)


    const fetchTx = async () => {
        const response = await backend.get('/transactions')
        settx(response.data)
        console.log(response.data)
    }

    useEffect(() => {
        fetchTx()

        // check for new Tx every 10 seconds
        const iId = setInterval(fetchTx, 10000)

        // stop checking when component unmounts
        return () => clearInterval(iId)
    }, [])

    const mine = async () => {
        await backend.post('/blockchain/mine')
        
        setshowAlert(true)
        fetchTx()
    }

    const TxList = () => {
        if (tx.length !== 0) {
            return (
                <div>
                {
                    tx.map(t => (
                        <div key={t.id}>
                            <hr />
                            <Transaction transaction={t} />
                        </div>
                    ))
                }
            </div>
            )
        }
        return <div>No open Transactions.</div>
    }

    const AlertMsg = () => {
        if (showAlert) {
            return (
                <Alert variant="dark" onClose={() => {
                    setshowAlert(false)
                    history.push('/blockchain')
                }} dismissible>
                New Block mined!
                </Alert>
            )
        }
        return <div></div>

    }

    
    return (
        <div className="TransactionPool">
            <MyNavbar />
            <h3>Transaction Pool</h3>
            <AlertMsg />
            <TxList />
            <hr />
            <Button
                variant="outline-light"
                onClick={mine}
            >
                Mine a new Block
            </Button>
            <Footer />
        </div>
    )
}

export default TxPool