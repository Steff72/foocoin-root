import React, { useState, useEffect } from 'react'

import Block from './Block'
import { URL } from '../config'

const Blockchain = () => {
    const [blockchain, setblockchain] = useState([])

    useEffect(() => {
        fetch(`${URL}/blockchain`)
            .then(response => response.json())
            .then(json => setblockchain(json))
    }, [])

    return (
        <div className="Blockchain">
            <h3>FooChain</h3>
            <div>
                {blockchain.map((block, idx) => <Block key={idx} block={block} />)}
            </div>
        </div>
    )
}

export default Blockchain