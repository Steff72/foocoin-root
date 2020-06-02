import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'

import Transaction from './Transaction'


const TxDisplay = ({ block }) => {
    const [dispaly, setdispaly] = useState(false)
    const { data } = block

    const toggle = () => setdispaly(!dispaly)

    if (dispaly) {
        return (
            <div>{
                data.map((tx, idx) => (
                    <div key={idx}>
                        <hr />
                        <Transaction transaction={tx} />
                    </div>
                ))}
                <br />
                <Button variant="danger" size="sm" onClick={toggle}>Hide Tx</Button>
            </div>
        )
    }

    return (
        <div>
            <br />
            <Button variant="danger" size="sm" onClick={toggle}>Show Tx</Button>
        </div>
    )
}


const Block = ({ block }) => {
    const { timestamp, prev_hash, hash, difficulty, nonce } = block

    const timestampDisplay = new Date(timestamp / 1000000).toLocaleString()
    const prev_hashDisplay = `${prev_hash.substring(0, 10)}...`
    const hashDisplay = `${hash.substring(0, 10)}...`

    return (
        <div className="Block">
            <div>Timestamp: {timestampDisplay}</div>
            <div>Prev Hash: {prev_hashDisplay}</div>
            <div>Hash: {hashDisplay}</div>
            <div>Difficulty: {difficulty}</div>
            <div>Nonce: {nonce}</div>
            <TxDisplay block={block} />
        </div>
    )
}

export default Block