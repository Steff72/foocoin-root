import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

import FormGroup from 'react-bootstrap/FormGroup'
import FormControl from 'react-bootstrap/FormControl'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'

import { backend } from '../config'
import history from '../history'

const SendTx = () => {
    const [amount, setamount] = useState(0)
    const [recipient, setrecipient] = useState('')
    const [showAlert, setshowAlert] = useState(false)
    const [knownAddresses, setknownAddresses] = useState([])

    useEffect(() => {
        backend.get('/known-addresses')
            .then(response => setknownAddresses(response.data))
    }, [])

    const handleRecipient = event => setrecipient(event.target.value)
    const handleAmount = event => setamount(Number(event.target.value))

    const submitTx = async () => {
        const response = await backend.post('/wallet/transact', { recipient, amount })
        console.log(response.data)
        setshowAlert(true)
    }

    const AlertMsg = () => {
        if (showAlert) {
            return (
                <Alert variant="danger" onClose={() => {
                    setshowAlert(false)
                    history.push('/transactions')
                }} dismissible>
                Transaction sent!
                </Alert>
            )
        }
        return <div></div>

    }

    const KnownAddresses = () => {
        if (knownAddresses.length !== 0) {
            return (
                <div>
                {
                    knownAddresses.map((kA, i) => (
                        <span key={kA}><u>{kA}</u>{i !== knownAddresses.length - 1 ? ', ' : ''}</span>
                    ))
                }
            </div>
            )
        }

        return <div>None so far...</div>
    }


    return (
        <div className="ConductTransaction">
            <Link to="/">Home</Link>
            <hr />
            <h3>Make a Transaction</h3>
            <AlertMsg />
            <FormGroup>
                <FormControl 
                    input="text"
                    placeholder="Recipient"
                    value={recipient}
                    onChange={handleRecipient}
                />
            </FormGroup>
            <FormGroup>
                <FormControl 
                    input="number"
                    placeholder="Amount"
                    value={amount}
                    onChange={handleAmount}
                />
            </FormGroup>
            <div>
                <Button
                    variant="danger"
                    onClick={submitTx}
                >Submit</Button>
            </div>
            <br />
            <h4>Known Addresses</h4>
            <KnownAddresses />
        </div>
    )
}

export default SendTx