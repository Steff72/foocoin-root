import React from 'react'

const Transaction = ({ transaction }) => {
    const { input, output } = transaction
    const sender = input.address
    const recipients = Object.keys(output)

    return (
        <div className="Transaction">
            <div>From: {sender}</div>
            {
                recipients.map((recipient, idx) => <div key={idx}>To: {recipient} | Amount: {output[recipient]}</div>)
            }
        </div>
    )
}

export default Transaction